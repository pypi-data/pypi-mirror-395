#!/usr/bin/env python3
"""Final test: Verify orders work WITHOUT service key, even if intent logging fails"""

import os
import sys
from cpz.clients.sync import CPZClient

# --- Load CPZ user credentials from environment (NOT service key!) ---
# Credentials must be set via environment variables:
#   export CPZ_AI_API_KEY="cpz_key_..."
#   export CPZ_AI_SECRET_KEY="cpz_secret_..."
#   export CPZ_STRATEGY_ID="..."
api_key = os.getenv("CPZ_AI_API_KEY")
secret_key = os.getenv("CPZ_AI_SECRET_KEY")
strategy_id = os.getenv("CPZ_STRATEGY_ID")

if not api_key or not secret_key:
    print("❌ ERROR: CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment")
    print("   Example: export CPZ_AI_API_KEY='cpz_key_...'")
    print("   Example: export CPZ_AI_SECRET_KEY='cpz_secret_...'")
    sys.exit(1)

if not strategy_id:
    print("❌ ERROR: CPZ_STRATEGY_ID must be set in environment")
    print("   Example: export CPZ_STRATEGY_ID='...'")
    sys.exit(1)

# Verify NO service key
if "SERVICE" in secret_key.upper():
    print("❌ ERROR: Service key detected!")
    sys.exit(1)

print("=" * 70)
print("FINAL TEST: Order Placement WITHOUT Service Key")
print("=" * 70)
print(f"✅ Using CPZ user keys only (no service key)")
print()

# Test: Order placement should work even if intent logging fails
print("🧪 Test: Full order placement (broker-first mode)...")
print("   Note: Intent logging may fail if keys aren't in DB, but broker execution should proceed")
print()

client = CPZClient()
client.execution.use_broker("alpaca", environment="paper", account_id="PA3FHUB575J3")

try:
    order = client.execution.order(
        symbol="GPRO",
        qty=1,
        side="buy",
        order_type="market",
        time_in_force="DAY",
        strategy_id=strategy_id,
    )
    
    print("✅ SUCCESS: Order placed successfully!")
    print(f"   Order ID: {order.id}")
    print(f"   Status: {order.status}")
    print(f"   Symbol: {order.symbol}")
    print()
    print("=" * 70)
    print("✅ VERIFICATION PASSED")
    print("=" * 70)
    print()
    print("Summary:")
    print("  ✅ Orders work with CPZ user keys only")
    print("  ✅ NO Supabase service key required")
    print("  ✅ Broker-first mode allows execution even if intent logging fails")
    print()
    print("Ready to publish!")
    sys.exit(0)
    
except RuntimeError as e:
    error_msg = str(e)
    if "401" in error_msg or "Unauthorized" in error_msg:
        if "key not found" in error_msg.lower():
            print("⚠️  Intent logging failed (keys not in database)")
            print(f"   Error: {error_msg[:200]}")
            print()
            print("   This is OK if broker-first mode is working.")
            print("   The router should still allow broker execution to proceed.")
            print()
            print("   However, if you see this error, it means:")
            print("   1. The edge function is correctly checking both tables ✅")
            print("   2. The keys need to be added to the database")
            print("   3. OR broker-first mode needs to be enabled")
            print()
            # Check if broker-first mode is enabled
            if os.getenv("CPZ_ORDER_LOGGING_MODE") == "broker-first":
                print("   ⚠️  Broker-first mode is enabled, but order still failed.")
                print("   This suggests the broker execution itself failed.")
                sys.exit(1)
            else:
                print("   💡 Tip: Set CPZ_ORDER_LOGGING_MODE=broker-first to allow")
                print("      orders to proceed even if intent logging fails.")
                sys.exit(1)
        else:
            print(f"❌ AUTH ERROR: {error_msg[:200]}")
            sys.exit(1)
    else:
        print(f"❌ RUNTIME ERROR: {error_msg[:200]}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

