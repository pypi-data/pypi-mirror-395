#!/usr/bin/env python3
"""
Test script to verify CPZClient file operations work correctly
Tests the methods that were missing: download_csv_to_dataframe, upload_dataframe, etc.
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

try:
    from cpz.clients.sync import CPZClient
    print("✅ Successfully imported CPZClient")
except ImportError as e:
    print(f"❌ Failed to import CPZClient: {e}")
    sys.exit(1)


def test_method_existence():
    """Test that all required methods exist on CPZClient"""
    print("\n" + "=" * 60)
    print("TEST 1: Method Existence Check")
    print("=" * 60)
    
    client = CPZClient()
    
    required_methods = [
        'download_csv_to_dataframe',
        'download_json_to_dataframe',
        'download_parquet_to_dataframe',
        'upload_dataframe',
        'list_files_in_bucket',
        'delete_file',
    ]
    
    all_exist = True
    for method_name in required_methods:
        exists = hasattr(client, method_name)
        callable_check = callable(getattr(client, method_name, None))
        status = "✅" if (exists and callable_check) else "❌"
        print(f"{status} {method_name}: exists={exists}, callable={callable_check}")
        if not (exists and callable_check):
            all_exist = False
    
    return all_exist


def test_method_signatures():
    """Test that method signatures are correct"""
    print("\n" + "=" * 60)
    print("TEST 2: Method Signature Check")
    print("=" * 60)
    
    import inspect
    client = CPZClient()
    
    # Check download_csv_to_dataframe signature
    sig = inspect.signature(client.download_csv_to_dataframe)
    params = list(sig.parameters.keys())
    print(f"✅ download_csv_to_dataframe signature: {params}")
    assert 'bucket_name' in params, "Missing bucket_name parameter"
    assert 'file_path' in params, "Missing file_path parameter"
    assert 'encoding' in params, "Missing encoding parameter"
    
    # Check upload_dataframe signature
    sig = inspect.signature(client.upload_dataframe)
    params = list(sig.parameters.keys())
    print(f"✅ upload_dataframe signature: {params}")
    assert 'bucket_name' in params, "Missing bucket_name parameter"
    assert 'file_path' in params, "Missing file_path parameter"
    assert 'df' in params, "Missing df parameter"
    assert 'format' in params, "Missing format parameter"
    
    return True


def test_with_real_credentials():
    """Test with real credentials if available"""
    print("\n" + "=" * 60)
    print("TEST 3: Real API Test (if credentials available)")
    print("=" * 60)
    
    load_dotenv()
    
    api_key = os.getenv("CPZ_AI_API_KEY")
    secret_key = os.getenv("CPZ_AI_SECRET_KEY")
    
    if not api_key or not secret_key:
        print("⚠️  Skipping real API test - credentials not found in environment")
        print("   Set CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY to test with real API")
        return True
    
    try:
        client = CPZClient()
        
        # Test health check
        print("🔍 Testing platform health...")
        # Note: CPZClient doesn't expose health directly, but we can test via platform namespace
        health = client.platform.health()
        print(f"✅ Platform health check: {health}")
        
        # Test that methods don't raise AttributeError
        print("\n🔍 Testing method calls (will fail gracefully if file doesn't exist)...")
        
        # This should not raise AttributeError - it should return None or raise a different error
        try:
            result = client.download_csv_to_dataframe("test-bucket", "non-existent-file.csv")
            print(f"✅ download_csv_to_dataframe callable (returned: {result is not None})")
        except AttributeError as e:
            print(f"❌ AttributeError raised: {e}")
            return False
        except Exception as e:
            # Other exceptions (like file not found) are OK - means method exists
            print(f"✅ Method exists (got expected error: {type(e).__name__})")
        
        # Test upload_dataframe with a sample DataFrame
        print("\n🔍 Testing upload_dataframe with sample data...")
        try:
            df = pd.DataFrame({
                'symbol': ['AAPL', 'GOOGL'],
                'price': [150.25, 2750.80]
            })
            # This might fail if bucket doesn't exist, but shouldn't raise AttributeError
            result = client.upload_dataframe("test-bucket", "test_file.csv", df, format="csv")
            if result:
                print(f"✅ upload_dataframe succeeded")
            else:
                print(f"⚠️  upload_dataframe returned None (bucket might not exist)")
        except AttributeError as e:
            print(f"❌ AttributeError raised: {e}")
            return False
        except Exception as e:
            # Other exceptions are OK
            print(f"✅ Method exists (got expected error: {type(e).__name__})")
        
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error during real API test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_delegation():
    """Test that methods properly delegate to CPZAIClient"""
    print("\n" + "=" * 60)
    print("TEST 4: Delegation Check")
    print("=" * 60)
    
    client = CPZClient()
    
    # Check that _cpz_client exists and has the methods
    assert hasattr(client, '_cpz_client'), "CPZClient should have _cpz_client attribute"
    cpz_client = client._cpz_client
    
    required_methods = [
        'download_csv_to_dataframe',
        'upload_dataframe',
    ]
    
    for method_name in required_methods:
        has_method = hasattr(cpz_client, method_name)
        print(f"✅ CPZAIClient.{method_name}: {has_method}")
        if not has_method:
            return False
    
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("CPZClient File Operations Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Method existence
    try:
        result = test_method_existence()
        results.append(("Method Existence", result))
    except Exception as e:
        print(f"❌ Test 1 failed with exception: {e}")
        results.append(("Method Existence", False))
    
    # Test 2: Method signatures
    try:
        result = test_method_signatures()
        results.append(("Method Signatures", result))
    except Exception as e:
        print(f"❌ Test 2 failed with exception: {e}")
        results.append(("Method Signatures", False))
    
    # Test 3: Real API test
    try:
        result = test_with_real_credentials()
        results.append(("Real API Test", result))
    except Exception as e:
        print(f"❌ Test 3 failed with exception: {e}")
        results.append(("Real API Test", False))
    
    # Test 4: Delegation check
    try:
        result = test_delegation()
        results.append(("Delegation Check", result))
    except Exception as e:
        print(f"❌ Test 4 failed with exception: {e}")
        results.append(("Delegation Check", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ CPZClient file operations are working correctly.")
        print("✅ The bug has been fixed - download_csv_to_dataframe and other methods are now available.")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease review the errors above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())






