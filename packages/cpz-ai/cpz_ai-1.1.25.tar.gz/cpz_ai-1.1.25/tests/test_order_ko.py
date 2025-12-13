#!/usr/bin/env python3

# Place a single KO market buy order using CPZ AI keys from environment.

import os
import sys
from cpz.clients.sync import CPZClient

# --- Configuration (from environment variables) ---
# Set these environment variables before running:
#   export CPZ_AI_API_KEY="your_api_key"
#   export CPZ_AI_SECRET_KEY="your_secret_key"
#   export CPZ_STRATEGY_ID="your_strategy_id"
# Optional:
#   export CPZ_ORDER_LOGGING_MODE="broker-first"  # or "disabled"
#   export CPZ_ENABLE_FILL_POLLING="false"
#   export CPZ_ACCOUNT_ID="your_account_id"

# --- Direct argument values ---
qty = 1
strategy_id = os.getenv("CPZ_STRATEGY_ID")
broker = "alpaca"     # choose broker name
account_id = os.getenv("CPZ_ACCOUNT_ID")  # optional, can be None

# --- Validation ---
if not os.getenv("CPZ_AI_API_KEY") or not os.getenv("CPZ_AI_SECRET_KEY"):
    print("CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment", file=sys.stderr)
    sys.exit(2)

if not strategy_id:
    print("CPZ_STRATEGY_ID must be set in environment", file=sys.stderr)
    sys.exit(2)

# --- Execute order ---
client = CPZClient()
if account_id:
    client.execution.use_broker(broker, account_id=account_id)
else:
    client.execution.use_broker(broker)

order = client.execution.order(
    symbol="GPRO",
    qty=qty,
    side="buy",
    order_type="market",
    time_in_force="DAY",
    strategy_id=strategy_id,
)

print(order.model_dump_json())




