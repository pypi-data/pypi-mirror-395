#!/usr/bin/env python3
"""
Comprehensive Storage Functionality Test
Tests all storage operations through the SDK
"""

import os
import sys
import pandas as pd
from cpz.clients.sync import CPZClient

# Load credentials from environment
api_key = os.getenv("CPZ_AI_API_KEY")
secret_key = os.getenv("CPZ_AI_SECRET_KEY")

if not api_key or not secret_key:
    print("❌ ERROR: CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment")
    print("   Example: export CPZ_AI_API_KEY='cpz_key_...'")
    print("   Example: export CPZ_AI_SECRET_KEY='cpz_secret_...'")
    sys.exit(1)

print("🧪 Comprehensive Storage Functionality Test")
print("=" * 60)

client = CPZClient()
bucket_name = "user-data"
test_file = "test_storage.csv"

# Test 1: Download existing file
print(f"\n1️⃣  Testing DOWNLOAD CSV...")
print(f"   Bucket: {bucket_name}, File: GDP_2025-11-25.csv")
try:
    df = client.download_csv_to_dataframe(bucket_name, "GDP_2025-11-25.csv")
    if df is not None:
        print(f"   ✅ SUCCESS! Downloaded {len(df)} rows")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Shape: {df.shape}")
    else:
        print(f"   ❌ FAILED: Returned None")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 2: Create and upload test DataFrame
print(f"\n2️⃣  Testing UPLOAD DataFrame as CSV...")
try:
    test_df = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'MSFT'],
        'price': [150.25, 2750.80, 310.45],
        'volume': [1000000, 500000, 800000]
    })
    result = client.upload_dataframe(bucket_name, test_file, test_df, format="csv")
    if result:
        print(f"   ✅ SUCCESS! Uploaded to {bucket_name}/{test_file}")
    else:
        print(f"   ❌ FAILED: Upload returned None/False")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 3: Download the file we just uploaded
print(f"\n3️⃣  Testing DOWNLOAD uploaded file...")
try:
    downloaded_df = client.download_csv_to_dataframe(bucket_name, test_file)
    if downloaded_df is not None:
        print(f"   ✅ SUCCESS! Downloaded {len(downloaded_df)} rows")
        print(f"   Data matches: {test_df.equals(downloaded_df)}")
    else:
        print(f"   ❌ FAILED: Returned None")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 4: List files in bucket
print(f"\n4️⃣  Testing LIST files...")
try:
    files = client.list_files_in_bucket(bucket_name)
    if files:
        print(f"   ✅ SUCCESS! Found {len(files)} files")
        for f in files[:5]:  # Show first 5
            name = f.get('name', 'Unknown')
            print(f"      - {name}")
    else:
        print(f"   ⚠️  No files found (might be empty or error)")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 5: Upload JSON
print(f"\n5️⃣  Testing UPLOAD DataFrame as JSON...")
try:
    json_file = "test_storage.json"
    result = client.upload_dataframe(bucket_name, json_file, test_df, format="json")
    if result:
        print(f"   ✅ SUCCESS! Uploaded JSON")
    else:
        print(f"   ❌ FAILED")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 6: Download JSON
print(f"\n6️⃣  Testing DOWNLOAD JSON...")
try:
    json_df = client.download_json_to_dataframe(bucket_name, json_file)
    if json_df is not None:
        print(f"   ✅ SUCCESS! Downloaded JSON DataFrame")
    else:
        print(f"   ❌ FAILED")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 7: Delete file
print(f"\n7️⃣  Testing DELETE file...")
try:
    result = client.delete_file(bucket_name, test_file)
    if result:
        print(f"   ✅ SUCCESS! Deleted {test_file}")
    else:
        print(f"   ❌ FAILED: Delete returned None/False")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 8: Verify deletion
print(f"\n8️⃣  Testing LIST after deletion...")
try:
    files_after = client.list_files_in_bucket(bucket_name)
    test_file_exists = any(f.get('name') == test_file for f in files_after) if files_after else False
    if not test_file_exists:
        print(f"   ✅ SUCCESS! File {test_file} no longer in list")
    else:
        print(f"   ⚠️  File still exists in list")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "=" * 60)
print("🎯 Test Summary:")
print("   Check results above to see which operations work")
print("=" * 60)

