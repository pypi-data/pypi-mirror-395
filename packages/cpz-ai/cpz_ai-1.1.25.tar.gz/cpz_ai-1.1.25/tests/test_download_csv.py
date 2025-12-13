import os
import sys
from cpz.clients.sync import CPZClient

# --- CPZ context (user key is fine; service-role not required with broker-first) ---

# --- Load credentials from environment ---
api_key = os.getenv("CPZ_AI_API_KEY")
secret_key = os.getenv("CPZ_AI_SECRET_KEY")

if not api_key or not secret_key:
    print("❌ ERROR: CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment")
    print("   Example: export CPZ_AI_API_KEY='cpz_key_...'")
    print("   Example: export CPZ_AI_SECRET_KEY='cpz_secret_...'")
    sys.exit(1)

client = CPZClient()

# If account_id is provided, env is not used by the router for credential resolution

# Download CSV and load to DataFrame

print("Attempting to download CSV file...")
downloaded_df = client.download_csv_to_dataframe("user-data", "GDP_2025-11-25.csv")

if downloaded_df is not None:
    print("✅ Success! Downloaded DataFrame:")
    print(downloaded_df)
    print(f"\nShape: {downloaded_df.shape}")
    print(f"Columns: {list(downloaded_df.columns)}")
else:
    print("❌ Failed to download - returned None")

