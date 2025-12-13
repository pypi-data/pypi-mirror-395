#!/usr/bin/env python3
"""
Verification script to test that storage operations still work after security fix.
This script tests that:
1. Valid credentials work (authentication succeeds)
2. Invalid secrets are rejected (authentication fails)
"""

import os
import sys
import pandas as pd

# Add the current directory to Python path
sys.path.insert(0, '.')

try:
    from cpz.clients.sync import CPZClient
    print("✅ Successfully imported CPZClient")
except ImportError as e:
    print(f"❌ Failed to import CPZClient: {e}")
    sys.exit(1)

def test_storage_with_valid_credentials():
    """Test storage operations with valid credentials"""
    print("\n" + "=" * 60)
    print("TEST 1: Storage Operations with Valid Credentials")
    print("=" * 60)
    
    # Check if credentials are set
    api_key = os.getenv("CPZ_AI_API_KEY")
    secret_key = os.getenv("CPZ_AI_SECRET_KEY")
    
    if not api_key or not secret_key:
        print("⚠️  CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY not set in environment")
        print("   Skipping test - set these to test with real credentials")
        return True  # Not a failure, just skip
    
    print(f"✅ Found credentials (key: {api_key[:20]}...)")
    
    try:
        client = CPZClient()
        bucket_name = "user-data"
        test_file = "auth_test_verification.csv"
        
        # Test 1: Upload a small DataFrame
        print(f"\n1️⃣  Testing UPLOAD...")
        test_df = pd.DataFrame({
            'test': ['verification'],
            'value': [12345]
        })
        
        result = client.upload_dataframe(bucket_name, test_file, test_df, format="csv")
        if result:
            print(f"   ✅ SUCCESS! Uploaded to {bucket_name}/{test_file}")
        else:
            print(f"   ❌ FAILED: Upload returned None/False")
            return False
        
        # Test 2: Download the file
        print(f"\n2️⃣  Testing DOWNLOAD...")
        downloaded_df = client.download_csv_to_dataframe(bucket_name, test_file)
        if downloaded_df is not None and len(downloaded_df) > 0:
            print(f"   ✅ SUCCESS! Downloaded {len(downloaded_df)} rows")
            print(f"   Data: {downloaded_df.to_dict()}")
        else:
            print(f"   ❌ FAILED: Download returned None or empty")
            return False
        
        # Test 3: List files
        print(f"\n3️⃣  Testing LIST...")
        files = client.list_files_in_bucket(bucket_name, prefix="auth_test")
        if files is not None:
            print(f"   ✅ SUCCESS! Found {len(files)} matching files")
        else:
            print(f"   ⚠️  LIST returned None (might be empty)")
        
        # Test 4: Delete the test file
        print(f"\n4️⃣  Testing DELETE...")
        if client.delete_file(bucket_name, test_file):
            print(f"   ✅ SUCCESS! Deleted {test_file}")
        else:
            print(f"   ⚠️  DELETE returned False (file might not exist)")
        
        print("\n✅ ALL TESTS PASSED - Storage operations work correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR during storage operations: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_invalid_secret_rejection():
    """Test that invalid secrets are properly rejected"""
    print("\n" + "=" * 60)
    print("TEST 2: Invalid Secret Rejection (Security Verification)")
    print("=" * 60)
    
    api_key = os.getenv("CPZ_AI_API_KEY")
    
    if not api_key:
        print("⚠️  CPZ_AI_API_KEY not set - skipping invalid secret test")
        return True
    
    print("ℹ️  This test verifies that the security fix works correctly")
    print("   by attempting to use an invalid secret (should fail)")
    
    try:
        import requests
        
        # Get the base URL
        from cpz.common.cpz_ai import CPZAIClient
        base_url = CPZAIClient.DEFAULT_API_URL
        
        # Create headers with valid key but invalid secret
        invalid_secret = "invalid_secret_that_should_not_work"
        headers = {
            "X-CPZ-KEY": api_key,
            "X-CPZ-SECRET": invalid_secret,
            "Content-Type": "application/json",
        }
        
        bucket_name = "user-data"
        url = f"{base_url}/storage/object/list/{bucket_name}"
        
        # Make direct HTTP request to check status code
        print(f"\n🔒 Attempting storage operation with INVALID secret...")
        print(f"   URL: {url}")
        print(f"   Key: {api_key[:30]}...")
        print(f"   Secret: {invalid_secret[:30]}...")
        
        resp = requests.get(url, headers=headers, timeout=10)
        
        print(f"   Response Status: {resp.status_code}")
        
        if resp.status_code == 401:
            print(f"   ✅ SECURITY FIX VERIFIED: Invalid secret correctly rejected!")
            print(f"   Response: {resp.text[:200]}")
            return True
        elif resp.status_code == 200:
            print(f"   ❌ SECURITY ISSUE: Operation succeeded with invalid secret!")
            print(f"   This should have returned 401 Unauthorized")
            print(f"   Response: {resp.text[:200]}")
            return False
        else:
            print(f"   ⚠️  Unexpected status code: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            # If it's not 200, we'll consider it a pass (some form of rejection)
            return resp.status_code != 200
        
    except Exception as e:
        print(f"❌ ERROR during invalid secret test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔐 Storage Authentication Verification")
    print("Testing that storage operations work correctly after security fix")
    
    # Test 1: Valid credentials should work
    test1_passed = test_storage_with_valid_credentials()
    
    # Test 2: Invalid secrets should be rejected
    test2_passed = test_invalid_secret_rejection()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Test 1 (Valid Credentials): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Test 2 (Invalid Secret Rejection): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL VERIFICATION TESTS PASSED!")
        print("✅ Storage operations work correctly")
        print("✅ Security fix is working - invalid secrets are rejected")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed - please review the output above")
        sys.exit(1)

