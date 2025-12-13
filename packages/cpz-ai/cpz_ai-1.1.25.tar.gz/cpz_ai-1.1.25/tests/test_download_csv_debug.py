import os
import sys
import requests
from cpz.clients.sync import CPZClient

# --- Load credentials from environment ---
api_key = os.getenv("CPZ_AI_API_KEY")
secret_key = os.getenv("CPZ_AI_SECRET_KEY")

if not api_key or not secret_key:
    print("❌ ERROR: CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment")
    print("   Example: export CPZ_AI_API_KEY='cpz_key_...'")
    print("   Example: export CPZ_AI_SECRET_KEY='cpz_secret_...'")
    sys.exit(1)

client = CPZClient()

# Check what URL is being used
print(f"CPZ API URL: {client._cpz_client.url}")
print(f"API Key: {client._cpz_client.api_key[:20]}...")
print(f"Secret Key: {client._cpz_client.secret_key[:20]}...")

# Try the download
print("\nAttempting to download CSV file...")
print(f"Endpoint will be: {client._cpz_client.url}/storage/object/data-bucket/GDP_2025-11-25.csv")

downloaded_df = client.download_csv_to_dataframe("data-bucket", "GDP_2025-11-25.csv")

if downloaded_df is not None:
    print("✅ Success! Downloaded DataFrame:")
    print(downloaded_df.head())
    print(f"\nShape: {downloaded_df.shape}")
else:
    print("❌ Failed to download - returned None")
    print("\nThe error indicates the backend edge function is failing with BOOT_ERROR.")
    print("This means the backend needs to either:")
    print("1. Deploy a working storage edge function, or")
    print("2. Configure the API gateway to route storage requests directly without edge functions")



