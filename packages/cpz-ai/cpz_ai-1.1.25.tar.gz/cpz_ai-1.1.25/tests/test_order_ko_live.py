#!/usr/bin/env python3

# Place a single KO market buy order using CPZ AI keys from environment.



import os
import sys

from cpz.clients.sync import CPZClient


# --- Direct argument values / configuration ---

qty = 1  # order quantity

# Strategy and CPZ credentials must come from the real environment.
# Example (paper):
#   CPZ_AI_API_KEY=... CPZ_AI_SECRET_KEY=... CPZ_STRATEGY_ID=... \
#       python -m pytest tests/test_order_ko_live.py -s
cpz_api_key = os.getenv("CPZ_AI_API_KEY")
cpz_secret_key = os.getenv("CPZ_AI_SECRET_KEY")
strategy_id = os.getenv("CPZ_STRATEGY_ID")

env = "paper"         # choose "paper" or "live"

broker = "alpaca"     # choose broker name

# --- Validation ---

if not cpz_api_key or not cpz_secret_key:
    print(
        "CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment",
        file=sys.stderr,
    )
    sys.exit(2)

if not strategy_id:
    print("--strategy-id (or CPZ_STRATEGY_ID) is required", file=sys.stderr)
    sys.exit(2)


# --- Execute order ---

print("Creating CPZClient...", file=sys.stderr)
client = CPZClient()
print("CPZClient created successfully", file=sys.stderr)

print(f"Setting up broker: {broker}, env: {env}, account_id: 902221772", file=sys.stderr)
print("About to call use_broker...", file=sys.stderr)
import time
start = time.time()
try:
    client.execution.use_broker(broker, environment=env, account_id="902221772")
    elapsed = time.time() - start
    print(f"Broker setup complete (took {elapsed:.2f}s)", file=sys.stderr)
except Exception as e:
    elapsed = time.time() - start
    print(f"Broker setup FAILED after {elapsed:.2f}s: {e}", file=sys.stderr)
    raise

print("Placing order...", file=sys.stderr)
order = client.execution.order(
    symbol="KO",
    qty=qty,
    side="buy",
    order_type="market",
    time_in_force="DAY",
    strategy_id=strategy_id,
)
print("Order placed successfully", file=sys.stderr)

print(order.model_dump_json())
