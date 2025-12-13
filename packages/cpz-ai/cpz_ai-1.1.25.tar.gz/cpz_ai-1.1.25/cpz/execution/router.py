from __future__ import annotations

import os
from typing import AsyncIterator, Callable, Dict, Iterable, Optional
import time

from ..common.errors import BrokerNotRegistered
from ..common.logging import get_logger
from .interfaces import BrokerAdapter
from .models import Account, Order, OrderReplaceRequest, OrderSubmitRequest, Position, Quote

BROKER_ALPACA = "alpaca"


class BrokerRouter:
    _registry: Dict[str, Callable[..., BrokerAdapter]] = {}

    def __init__(self) -> None:
        self._active: Optional[BrokerAdapter] = None
        self._active_name: Optional[str] = None
        self._active_kwargs: Dict[str, object] = {}
        # Optional CPZ platform client for order logging/credentials
        self._cpz_client: object | None = None

    @classmethod
    def register(cls, name: str, factory: Callable[..., BrokerAdapter]) -> None:
        cls._registry[name] = factory

    def list_brokers(self) -> list[str]:
        return list(self._registry.keys())

    @classmethod
    def default(cls) -> "BrokerRouter":
        if BROKER_ALPACA not in cls._registry:
            try:
                from .alpaca.adapter import AlpacaAdapter

                cls.register(BROKER_ALPACA, AlpacaAdapter.create)
            except Exception:
                pass
        return cls()

    def with_cpz_client(self, cpz_client: object) -> "BrokerRouter":
        """Inject a CPZ platform client instance for use in order logging.

        If not provided, the router will fall back to CPZAIClient.from_env().
        """
        self._cpz_client = cpz_client
        return self

    def use_broker(self, name: str, **kwargs: object) -> None:
        if name not in self._registry:
            raise BrokerNotRegistered(name)
        # Normalize kwargs for adapter factories
        if "environment" in kwargs and "env" not in kwargs:
            # Accept both styles; adapters typically expect "env"
            k = dict(kwargs)
            k["env"] = k.pop("environment")
            kwargs = k  # type: ignore[assignment]
        factory = self._registry[name]
        self._active = factory(**kwargs)
        self._active_name = name
        self._active_kwargs = dict(kwargs)

    def active_selection(self) -> Optional[tuple[str, Dict[str, object]]]:
        """Return the currently selected broker name and kwargs, or None if none selected."""
        if self._active_name is None:
            return None
        return self._active_name, dict(self._active_kwargs)

    def _require_active(self) -> BrokerAdapter:
        if self._active is None:
            if len(self._registry) == 1:
                _name, factory = next(iter(self._registry.items()))
                self._active = factory()
                # Keep metadata consistent for downstream logging
                self._active_name = _name
                self._active_kwargs = {}
                return self._active
            if os.getenv("ALPACA_API_KEY_ID"):
                self.use_broker(BROKER_ALPACA, env=os.getenv("ALPACA_ENV", "paper"))
            else:
                raise BrokerNotRegistered("<none>")
        assert self._active is not None
        return self._active

    def get_account(self) -> Account:
        return self._require_active().get_account()

    def get_positions(self) -> list[Position]:
        return self._require_active().get_positions()

    def submit_order(self, req: OrderSubmitRequest) -> Order:
        from ..common.cpz_ai import CPZAIClient

        broker_name = self._active_name or BROKER_ALPACA
        env = str(self._active_kwargs.get("env") or "") or "paper"
        account_id = str(self._active_kwargs.get("account_id") or "")

        # 1) Create order intent (best-effort). Do not block execution if gateway is warming up.
        # Validate credentials before attempting to create order intent
        sb = None
        intent = None
        try:
            # This will raise ValueError if credentials are missing/invalid
            sb = CPZAIClient.from_env()
            # CRITICAL: account_id must always be provided (never None or empty)
            # If not provided, get it from broker adapter
            # account_id should be the broker's account number (e.g., "PA3FHUB575J3" for Alpaca)
            if not account_id:
                try:
                    account = self._require_active().get_account()
                    # Use account.id which should be account_number from Alpaca (e.g., "PA3FHUB575J3")
                    account_id = getattr(account, "id", None) or getattr(account, "account_id", None) or ""
                except Exception:
                    account_id = ""
            
            intent = sb.create_order_intent(
                symbol=req.symbol,
                side=req.side.value,
                qty=req.qty,
                type=req.type.value,
                time_in_force=req.time_in_force.value,
                broker=broker_name,
                env=env,
                strategy_id=getattr(req, "strategy_id", ""),
                status="pending",
                account_id=account_id,  # CRITICAL: Must always be set (never None)
            )
        except ValueError as ve:
            # Re-raise credential validation errors immediately - these are critical
            raise ValueError(f"CPZ API credentials validation failed: {ve}") from ve
        except Exception as exc:
            # For other exceptions (network errors, gateway warmup, etc.), log but don't block order execution
            # The order can still be submitted to the broker even if intent creation fails
            logger = get_logger()
            logger.warning(
                "failed_to_create_order_intent_non_blocking",
                error=str(exc),
                message="Order will still be submitted to broker",
            )
            intent = None

        # 2) Send to broker
        order = self._require_active().submit_order(req)

        # 3) CRITICAL: Update order record with broker order_id immediately
        # The order_id MUST match Alpaca's order_id for tracking
        # This is essential for order tracking and analytics
        try:
            if sb is None:
                # CPZ client not available (e.g., network error during initialization)
                # Order was successfully placed with broker, but cannot be recorded
                logger = get_logger()
                logger.warning(
                    "cpz_client_unavailable_cannot_record_order",
                    broker_order_id=order.id,
                    message="Order placed with broker but CPZ client unavailable - order_id not recorded in database",
                )
            elif intent and isinstance(intent, dict) and intent.get("id"):
                # Update existing intent record with broker order_id and details
                # This MUST succeed - order_id is critical for tracking
                update_success = sb.update_order_record(
                    id=str(intent.get("id")),
                    order_id=order.id,  # CRITICAL: Alpaca's order_id for tracking
                    status=getattr(order, "status", None),
                    filled_qty=getattr(order, "filled_qty", None),
                    average_fill_price=getattr(order, "average_fill_price", None),
                    submitted_at=(
                        getattr(order, "submitted_at", None).isoformat()
                        if getattr(order, "submitted_at", None)
                        else None
                    ),
                    filled_at=(
                        getattr(order, "filled_at", None).isoformat()
                        if getattr(order, "filled_at", None)
                        else None
                    ),
                )
                if not update_success:
                    # Update failed - CRITICAL: order_id must be set for tracking
                    # Try record_order as fallback to ensure order_id is recorded
                    logger = get_logger()
                    logger.warning(
                        "failed_to_update_order_record_fallback",
                        broker_order_id=order.id,
                        intent_id=intent.get("id"),
                        message="PATCH update failed, trying record_order fallback to ensure order_id is set",
                    )
                    try:
                        # Fallback: record_order will create/update with order_id
                        # Use "pending" status if status is invalid - database constraint requires valid status
                        order_status = getattr(order, "status", None) or "pending"
                        # Normalize status to valid values (pending, filled, canceled, etc.)
                        if order_status.lower() not in ["pending", "filled", "canceled", "partially_filled", "accepted"]:
                            order_status = "pending"
                        recorded = sb.record_order(
                            order_id=order.id,  # CRITICAL: Alpaca's order_id
                            symbol=req.symbol,
                            side=req.side.value,
                            qty=req.qty,
                            type=req.type.value,
                            time_in_force=req.time_in_force.value,
                            broker=broker_name,
                            env=env,
                            strategy_id=getattr(req, "strategy_id", ""),
                            status=order_status,
                            filled_at=(
                                getattr(order, "filled_at", None).isoformat()
                                if getattr(order, "filled_at", None)
                                else None
                            ),
                            account_id=account_id,  # CRITICAL: Must always be set
                        )
                        if recorded:
                            intent = recorded  # Use updated record for polling
                    except Exception as fallback_exc:
                        logger.error(
                            "failed_to_record_order_fallback",
                            error=str(fallback_exc),
                            broker_order_id=order.id,
                            message="CRITICAL: order_id not recorded in database - tracking will fail",
                        )
            elif sb is not None:
                # Initial insert failed - create complete record NOW with broker order_id
                # This ensures we ALWAYS have order_id recorded for tracking
                # Use "pending" status if status is invalid - database constraint requires valid status
                order_status = getattr(order, "status", None) or "pending"
                # Normalize status to valid values (pending, filled, canceled, etc.)
                if order_status.lower() not in ["pending", "filled", "canceled", "partially_filled", "accepted"]:
                    order_status = "pending"
                recorded = sb.record_order(
                    order_id=order.id,  # CRITICAL: Alpaca's order_id for tracking
                    symbol=req.symbol,
                    side=req.side.value,
                    qty=req.qty,
                    type=req.type.value,
                    time_in_force=req.time_in_force.value,
                    broker=broker_name,
                    env=env,
                    strategy_id=getattr(req, "strategy_id", ""),
                    status=order_status,
                    filled_at=(
                        getattr(order, "filled_at", None).isoformat()
                        if getattr(order, "filled_at", None)
                        else None
                    ),
                    account_id=account_id,  # CRITICAL: Must always be set
                )
                if recorded:
                    intent = recorded  # Use this for polling updates
                else:
                    # CRITICAL: order_id was not recorded
                    logger = get_logger()
                    logger.error(
                        "failed_to_record_order_id",
                        broker_order_id=order.id,
                        message="CRITICAL: order_id not recorded in database - tracking will fail",
                    )
        except Exception as exc:
            # Log but don't fail - order was successfully placed with broker
            # But this is CRITICAL for tracking
            logger = get_logger()
            logger.error(
                "failed_to_record_order",
                error=str(exc),
                broker_order_id=order.id,
                message="CRITICAL: Order placed with broker but order_id not recorded in database - tracking will fail",
            )

        # 4) Optional polling to sync fills until terminal or timeout
        # This ensures order status and fills are kept in sync with broker
        try:
            poll_total = int(os.getenv("CPZ_POLL_TOTAL_SECONDS", "60"))
            poll_interval = float(os.getenv("CPZ_POLL_INTERVAL_SECONDS", "2"))
            enable_poll = os.getenv("CPZ_ENABLE_FILL_POLLING", "true").lower() != "false"
            if enable_poll and poll_total > 0:
                deadline = time.time() + poll_total
                while time.time() < deadline:
                    cur = self._require_active().get_order(order.id)
                    if sb is not None and intent and isinstance(intent, dict) and intent.get("id"):
                        # Update order record with latest status and fills
                        # CRITICAL: order_id must always match broker's order_id
                        sb.update_order_record(
                            id=str(intent.get("id")),
                            order_id=cur.id,  # Always keep order_id in sync with broker
                            status=getattr(cur, "status", None),
                            filled_qty=getattr(cur, "filled_qty", None),
                            average_fill_price=getattr(cur, "average_fill_price", None),
                            submitted_at=(
                                getattr(cur, "submitted_at", None).isoformat()
                                if getattr(cur, "submitted_at", None)
                                else None
                            ),
                            filled_at=(
                                getattr(cur, "filled_at", None).isoformat()
                                if getattr(cur, "filled_at", None)
                                else None
                            ),
                        )
                    # Check if order reached terminal state
                    if str(getattr(cur, "status", "")).lower() in {
                        "filled",
                        "canceled",
                        "partially_filled",
                    }:
                        order = cur
                        break
                    time.sleep(poll_interval)
        except Exception:
            pass

        return order

    def get_order(self, order_id: str) -> Order:
        return self._require_active().get_order(order_id)

    def cancel_order(self, order_id: str) -> Order:
        return self._require_active().cancel_order(order_id)

    def replace_order(self, order_id: str, req: OrderReplaceRequest) -> Order:
        return self._require_active().replace_order(order_id, req)

    def stream_quotes(self, symbols: Iterable[str]) -> AsyncIterator[Quote]:
        active = self._require_active()
        return active.stream_quotes(symbols)

    # --- Data passthroughs ---
    def get_quotes(self, symbols: list[str]) -> list[Quote]:
        return self._require_active().get_quotes(symbols)

    def get_historical_data(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 100,
        start: Optional[object] = None,
        end: Optional[object] = None,
    ) -> list[object]:
        # Types align with BrokerAdapter; keep signature flexible for call sites
        return self._require_active().get_historical_data(symbol, timeframe, limit, start, end)
