#!/usr/bin/env python3
"""
Test the exact pattern from the user's notebook to verify it works
"""

import os
import sys

try:
    from cpz.clients.sync import CPZClient
    import cpz
    print("✅ Successfully imported CPZClient and cpz")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)


def test_notebook_pattern():
    """Test the exact pattern from the notebook"""
    print("\n" + "=" * 60)
    print("Testing Notebook Pattern")
    print("=" * 60)
    
    # Pattern from notebook:
    # import os
    # from cpz.clients.sync import CPZClient
    # os.environ["CPZ_AI_API_KEY"] = "..."
    # os.environ["CPZ_AI_SECRET_KEY"] = "..."
    # client = CPZClient()
    # downloaded_df = client.download_csv_to_dataframe("data-bucket", "GDP_2025-11-25.csv")
    
    print("\n1. Testing CPZ SDK Version check...")
    try:
        version = cpz.__version__
        print(f"   ✅ CPZ SDK Version: {version}")
    except AttributeError:
        print("   ⚠️  __version__ not found, but that's OK")
    
    print("\n2. Testing CPZClient instantiation...")
    try:
        client = CPZClient()
        print("   ✅ CPZClient() instantiated successfully")
    except Exception as e:
        print(f"   ❌ Failed to instantiate CPZClient: {e}")
        return False
    
    print("\n3. Testing download_csv_to_dataframe method exists...")
    if not hasattr(client, 'download_csv_to_dataframe'):
        print("   ❌ download_csv_to_dataframe method not found!")
        return False
    print("   ✅ download_csv_to_dataframe method exists")
    
    print("\n4. Testing download_csv_to_dataframe is callable...")
    try:
        # This will fail because file doesn't exist, but shouldn't raise AttributeError
        result = client.download_csv_to_dataframe("data-bucket", "GDP_2025-11-25.csv")
        print(f"   ✅ Method callable (returned: {result})")
    except AttributeError as e:
        print(f"   ❌ AttributeError raised - BUG NOT FIXED: {e}")
        return False
    except Exception as e:
        # Any other exception means the method exists and was called
        print(f"   ✅ Method exists and was called (got expected error: {type(e).__name__})")
        print(f"      Error message: {str(e)[:100]}...")
    
    print("\n5. Testing other file operation methods...")
    methods_to_test = [
        'upload_dataframe',
        'download_json_to_dataframe',
        'download_parquet_to_dataframe',
        'list_files_in_bucket',
        'delete_file',
    ]
    
    for method_name in methods_to_test:
        if hasattr(client, method_name):
            print(f"   ✅ {method_name} exists")
        else:
            print(f"   ❌ {method_name} NOT FOUND")
            return False
    
    print("\n" + "=" * 60)
    print("✅ ALL CHECKS PASSED!")
    print("=" * 60)
    print("\nThe exact pattern from your notebook should now work:")
    print("""
    from cpz.clients.sync import CPZClient
    
    client = CPZClient()
    downloaded_df = client.download_csv_to_dataframe("data-bucket", "GDP_2025-11-25.csv")
    """)
    print("\nNote: The method will return None if the file doesn't exist,")
    print("but it will NOT raise AttributeError anymore!")
    
    return True


if __name__ == "__main__":
    success = test_notebook_pattern()
    sys.exit(0 if success else 1)






