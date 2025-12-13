#!/usr/bin/env python3
"""
Test order execution using CPZ AI SDK.

Requires environment variables:
  - CPZ_AI_API_KEY
  - CPZ_AI_SECRET_KEY
  - CPZ_STRATEGY_ID (optional but recommended)

Optional:
  - CPZ_BROKER (default: "alpaca")
  - CPZ_ENV (default: "paper" - set to "live" explicitly if needed)
  - CPZ_ACCOUNT_ID (optional, read from environment)

⚠️  WARNING: This script defaults to PAPER trading for safety.
    To use live trading, explicitly set CPZ_ENV="live" in your environment.
"""

import os
import sys
from cpz.clients.sync import CPZClient

# Load credentials from environment
api_key = os.getenv("CPZ_AI_API_KEY")
secret_key = os.getenv("CPZ_AI_SECRET_KEY")
strategy_id = os.getenv("CPZ_STRATEGY_ID")

if not api_key or not secret_key:
    print("❌ ERROR: CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment")
    print("   Example: export CPZ_AI_API_KEY='cpz_key_...'")
    print("   Example: export CPZ_AI_SECRET_KEY='cpz_secret_...'")
    sys.exit(1)

if not strategy_id:
    print("⚠️  WARNING: CPZ_STRATEGY_ID not set in environment")
    print("   Example: export CPZ_STRATEGY_ID='...'")

# Disable fill polling
os.environ["CPZ_ENABLE_FILL_POLLING"] = "false"

SYMBOL = "AAPL"  # Use a cheaper symbol for testing
qty = 1
broker = os.getenv("CPZ_BROKER", "alpaca")
environment = os.getenv("CPZ_ENV", "paper")  # Default to paper trading for safety
account_id = os.getenv("CPZ_ACCOUNT_ID")  # Read from environment, optional

print("=" * 60)
print("ORDER EXECUTION TEST")
print("=" * 60)
print(f"Symbol: {SYMBOL}")
print(f"Quantity: {qty}")
print(f"Broker: {broker}")
print(f"Environment: {environment}")
if environment == "live":
    print("⚠️  WARNING: LIVE TRADING MODE - Real money at risk!")
print(f"Strategy ID: {strategy_id}")
print(f"Account ID: {account_id}")
print("=" * 60)

try:
    client = CPZClient()
    print("✅ Client initialized")
    
    # Configure broker
    client.execution.use_broker(broker, environment=environment, account_id=account_id)
    print(f"✅ Broker configured: {broker} ({environment})")
    
    # Check account balance first
    account = client.execution.get_account()
    print(f"\nAccount Info:")
    print(f"  Buying Power: ${account.buying_power:,.2f}")
    print(f"  Equity: ${account.equity:,.2f}")
    print(f"  Cash: ${account.cash:,.2f}")
    
    # Test placing a market buy order
    print(f"\nPlacing MARKET BUY order for {qty} {SYMBOL}...")
    order = client.execution.order(
        symbol=SYMBOL,
        qty=qty,
        side="buy",
        order_type="market",
        time_in_force="DAY",
        strategy_id=strategy_id,
    )
    
    print("\n✅ Order placed successfully!")
    print("Order details:")
    print(order.model_dump_json(indent=2))
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    # Don't print full traceback for cleaner output
    if "buying_power" in str(e):
        print("\n💡 Tip: This is a broker-side error (insufficient funds), not an SDK issue.")
        print("   The SDK is working correctly - try paper trading or a cheaper symbol.")
    sys.exit(1)
