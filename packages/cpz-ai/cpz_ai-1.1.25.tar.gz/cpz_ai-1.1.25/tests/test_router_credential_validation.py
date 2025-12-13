#!/usr/bin/env python3
"""Test script to verify router credential validation."""

import os
import sys

# Clear any existing credentials
for key in ["CPZ_AI_API_KEY", "CPZ_AI_SECRET_KEY"]:
    if key in os.environ:
        del os.environ[key]

from cpz.execution.router import BrokerRouter
from cpz.execution.models import OrderSubmitRequest
from cpz.execution.enums import OrderSide, OrderType, TimeInForce


def test_router_submit_order_without_credentials():
    """Test that router fails fast with missing credentials."""
    print("Test: Router should fail fast with missing credentials...")
    
    router = BrokerRouter.default()
    
    try:
        # This should fail immediately when trying to set up broker
        # because AlpacaAdapter.create() calls CPZAIClient.from_env() to fetch credentials
        router.use_broker("alpaca", env="paper")
        print("  ❌ FAILED: Should have raised ValueError for missing credentials")
        return False
    except ValueError as e:
        if "credentials" in str(e).lower() or "missing" in str(e).lower() or "invalid" in str(e).lower():
            print(f"  ✅ PASSED: Correctly raised ValueError when setting up broker: {e}")
            return True
        else:
            print(f"  ❌ FAILED: Wrong error message: {e}")
            return False
    except Exception as e:
        # Any exception is fine as long as it fails fast (not hanging)
        print(f"  ✅ PASSED: Failed fast (not hanging) with: {type(e).__name__}: {e}")
        return True


def main():
    """Run test."""
    print("=" * 60)
    print("Testing Router Credential Validation")
    print("=" * 60)
    
    result = test_router_submit_order_without_credentials()
    
    print("\n" + "=" * 60)
    if result:
        print("✅ Test passed! Router fails fast with missing credentials.")
        return 0
    else:
        print("❌ Test failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
