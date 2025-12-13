import os
import sys
from cpz.clients.sync import CPZClient

# Load credentials from environment
api_key = os.getenv("CPZ_AI_API_KEY")
secret_key = os.getenv("CPZ_AI_SECRET_KEY")

if not api_key or not secret_key:
    print("❌ ERROR: CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment")
    print("   Example: export CPZ_AI_API_KEY='cpz_key_...'")
    print("   Example: export CPZ_AI_SECRET_KEY='cpz_secret_...'")
    sys.exit(1)

client = CPZClient()

# Download CSV and load to DataFrame
print("Testing storage download...")
df = client.download_csv_to_dataframe("user-data", "1764787508368-ts6ko79dwe8.csv")

if df is not None:
    print(f"✅ SUCCESS! Got DataFrame with {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst few rows:")
    print(df.head())
else:
    print("❌ Failed - got None")
