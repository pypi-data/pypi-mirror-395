#!/usr/bin/env python3
"""Test script to verify credential validation works correctly."""

import os
import sys

# Clear any existing credentials
for key in ["CPZ_AI_API_KEY", "CPZ_AI_SECRET_KEY"]:
    if key in os.environ:
        del os.environ[key]

from cpz.clients.sync import CPZClient
from cpz.common.cpz_ai import CPZAIClient


def test_missing_credentials():
    """Test that missing credentials raise ValueError immediately."""
    print("Test 1: Missing credentials should raise ValueError...")
    try:
        client = CPZClient()
        print("  ❌ FAILED: Should have raised ValueError for missing credentials")
        return False
    except ValueError as e:
        if "missing" in str(e).lower() or "invalid" in str(e).lower():
            print(f"  ✅ PASSED: Correctly raised ValueError: {e}")
            return True
        else:
            print(f"  ❌ FAILED: Wrong error message: {e}")
            return False
    except Exception as e:
        print(f"  ❌ FAILED: Wrong exception type: {type(e).__name__}: {e}")
        return False


def test_invalid_credentials():
    """Test that invalid credentials raise ValueError immediately."""
    print("\nTest 2: Invalid credentials should raise ValueError...")
    os.environ["CPZ_AI_API_KEY"] = "invalid_key"
    os.environ["CPZ_AI_SECRET_KEY"] = "invalid_secret"
    try:
        client = CPZClient()
        print("  ❌ FAILED: Should have raised ValueError for invalid credentials")
        return False
    except ValueError as e:
        if "invalid" in str(e).lower() or "format" in str(e).lower():
            print(f"  ✅ PASSED: Correctly raised ValueError: {e}")
            return True
        else:
            print(f"  ❌ FAILED: Wrong error message: {e}")
            return False
    except Exception as e:
        print(f"  ❌ FAILED: Wrong exception type: {type(e).__name__}: {e}")
        return False
    finally:
        # Clean up
        del os.environ["CPZ_AI_API_KEY"]
        del os.environ["CPZ_AI_SECRET_KEY"]


def test_cpz_client_direct():
    """Test CPZAIClient directly with invalid credentials."""
    print("\nTest 3: CPZAIClient.from_env() should validate credentials...")
    os.environ["CPZ_AI_API_KEY"] = "invalid_key"
    os.environ["CPZ_AI_SECRET_KEY"] = "invalid_secret"
    try:
        client = CPZAIClient.from_env()
        print("  ❌ FAILED: Should have raised ValueError for invalid credentials")
        return False
    except ValueError as e:
        if "invalid" in str(e).lower() or "format" in str(e).lower():
            print(f"  ✅ PASSED: Correctly raised ValueError: {e}")
            return True
        else:
            print(f"  ❌ FAILED: Wrong error message: {e}")
            return False
    except Exception as e:
        print(f"  ❌ FAILED: Wrong exception type: {type(e).__name__}: {e}")
        return False
    finally:
        # Clean up
        del os.environ["CPZ_AI_API_KEY"]
        del os.environ["CPZ_AI_SECRET_KEY"]


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Credential Validation")
    print("=" * 60)
    
    results = []
    results.append(test_missing_credentials())
    results.append(test_invalid_credentials())
    results.append(test_cpz_client_direct())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Credential validation is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
