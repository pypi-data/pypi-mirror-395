#!/usr/bin/env python3

"""
Time-based strategy using CPZ AI SDK for order placement (paper by default).

Requires environment variables:
  - CPZ_AI_API_KEY
  - CPZ_AI_SECRET_KEY
  - CPZ_STRATEGY_ID

Optional:
  - CPZ_BROKER (default: "alpaca")
  - CPZ_ENV (default: "paper")
  - CPZ_ACCOUNT_ID (if you want to target a specific broker account)
"""

import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from cpz.clients.sync import CPZClient

# --- Configuration (from environment variables) ---
# Set these environment variables before running:
#   export CPZ_AI_API_KEY="your_api_key"
#   export CPZ_AI_SECRET_KEY="your_secret_key"
#   export CPZ_STRATEGY_ID="your_strategy_id"
# Optional:
#   export CPZ_BROKER="alpaca"  # default: "alpaca"
#   export CPZ_ENV="paper"  # or "live", default: "paper"
#   export CPZ_ACCOUNT_ID="your_account_id"
#   export CPZ_ENABLE_FILL_POLLING="false"
#   export CPZ_POLL_TOTAL_SECONDS="5"

# --- Validation ---
if not os.getenv("CPZ_AI_API_KEY") or not os.getenv("CPZ_AI_SECRET_KEY"):
    print("CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment", file=sys.stderr)
    sys.exit(2)

strategy_id = os.getenv("CPZ_STRATEGY_ID")
if not strategy_id:
    print("CPZ_STRATEGY_ID must be set in environment", file=sys.stderr)
    sys.exit(2)

SYMBOL = "GPRO"
qty = 1
broker = os.getenv("CPZ_BROKER", "alpaca")
environment = os.getenv("CPZ_ENV", "paper")  # choose "paper" or "live"
account_id = os.getenv("CPZ_ACCOUNT_ID")  # optional, can be None

# Safety check: warn if live trading is detected
if environment == "live":
    print("⚠️  WARNING: LIVE TRADING MODE - Real money at risk!", file=sys.stderr)

TZ_ET = ZoneInfo("US/Eastern")
client = CPZClient()

# If account_id is provided, env is not used by the router for credential resolution
if account_id:
    client.execution.use_broker(broker, environment=environment, account_id=account_id)
else:
    client.execution.use_broker(broker, environment=environment)


def place(side: str):
    order = client.execution.order(
        symbol=SYMBOL,
        qty=qty,
        side=side,
        order_type="market",
        time_in_force="DAY",
        strategy_id=strategy_id,
    )
    print(order.model_dump_json())


def main():
    now_et = datetime.now(TZ_ET)
    ten_am = now_et.replace(hour=10, minute=0, second=0, microsecond=0).time()
    if now_et.time() < ten_am:
        print(f"[{now_et}] Before 10:00 AM ET -> BUY {qty} {SYMBOL}")
        place("buy")
    elif now_et.time() > ten_am:
        print(f"[{now_et}] After 10:00 AM ET -> SELL {qty} {SYMBOL}")
        place("sell")
    else:
        print(f"[{now_et}] Exactly 10:00 AM ET -> no action")


if __name__ == "__main__":
    main()




