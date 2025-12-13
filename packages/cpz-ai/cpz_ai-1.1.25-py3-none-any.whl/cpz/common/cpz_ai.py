from __future__ import annotations

import io
import os
from typing import Any, Mapping, Optional, List, Dict
from urllib.parse import urlparse

import requests

from .auth import validate_cpz_credentials
from .logging import get_logger


class CPZAIClient:
    """Client for accessing CPZ AI database (strategies and files)"""

    # Default platform REST URL (not configurable via env for end-users)
    # All requests go through api-ai.cpz-lab.com proxy - no direct Supabase access
    DEFAULT_API_URL = "https://api-ai.cpz-lab.com/cpz"

    def __init__(
        self, url: str, api_key: str, secret_key: str, user_id: str = None, is_admin: bool = False
    ) -> None:
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.secret_key = secret_key
        self.user_id = user_id
        self.is_admin = is_admin
        self.logger = get_logger()
        # Validate credential format (skip for admin clients which may use JWT tokens)
        if not is_admin:
            is_valid, error_msg = validate_cpz_credentials(api_key, secret_key)
            if not is_valid:
                raise ValueError(error_msg or "Invalid CPZ API credentials format")

    @staticmethod
    def from_env(environ: Optional[Mapping[str, str]] = None) -> "CPZAIClient":
        env = environ or os.environ
        
        # Validate environment variable names and provide clear error messages
        errors = []
        warnings = []
        
        # Check for missing required variables
        api_key = env.get("CPZ_AI_API_KEY", "")
        # Support multiple names for backward compatibility, but prefer CPZ_AI_API_SECRET_KEY for consistency
        secret_key_preferred = env.get("CPZ_AI_API_SECRET_KEY", "")  # Preferred: consistent with CPZ_AI_API_KEY
        secret_key_alt1 = env.get("CPZ_AI_SECRET_KEY", "")  # Alternative 1
        secret_key_alt2 = env.get("CPZ_AI_API_SECRET", "")  # Alternative 2 (deprecated)
        
        if not api_key:
            errors.append("Missing required environment variable: CPZ_AI_API_KEY")
        
        # Determine which secret key is being used
        secret_key = secret_key_preferred or secret_key_alt1 or secret_key_alt2
        
        if not secret_key:
            errors.append("Missing required environment variable: CPZ_AI_API_SECRET_KEY")
        else:
            # Warn about deprecated/alternative names
            if secret_key_alt1 and not secret_key_preferred:
                warnings.append(
                    "Using alternative variable name: CPZ_AI_SECRET_KEY\n"
                    "For consistency with CPZ_AI_API_KEY, please use: CPZ_AI_API_SECRET_KEY"
                )
            elif secret_key_alt2 and not secret_key_preferred:
                warnings.append(
                    "Using deprecated variable name: CPZ_AI_API_SECRET\n"
                    "For consistency with CPZ_AI_API_KEY, please use: CPZ_AI_API_SECRET_KEY"
                )
        
        # Raise error if any validation failures
        if errors:
            error_msg = "CPZ AI environment variable configuration error:\n\n"
            error_msg += "\n".join(f"  • {e}" for e in errors)
            error_msg += "\n\nRequired variables:\n"
            error_msg += "  - CPZ_AI_API_KEY\n"
            error_msg += "  - CPZ_AI_API_SECRET_KEY (for consistency with CPZ_AI_API_KEY)\n"
            error_msg += "  - CPZ_AI_STRATEGY_ID (required for placing orders)\n"
            error_msg += "\nAlternative names (backward compatible):\n"
            error_msg += "  - CPZ_AI_SECRET_KEY (also accepted)\n"
            error_msg += "  - CPZ_AI_API_SECRET (deprecated, will be removed in future)\n"
            error_msg += "  - CPZ_STRATEGY_ID (also accepted, but CPZ_AI_STRATEGY_ID preferred)\n"
            error_msg += "\nOptional variables:\n"
            error_msg += "  - CPZ_AI_BASE_URL\n"
            error_msg += "  - CPZ_AI_USER_ID\n"
            raise ValueError(error_msg)
        
        # Log warnings if any
        if warnings:
            logger = get_logger()
            for warning in warnings:
                logger.warning("cpz_env_var_deprecation", message=warning)
        
        # Validate credential format before creating client
        # Skip validation for admin clients (they may use JWT tokens)
        is_admin = env.get("CPZ_AI_IS_ADMIN", "false").lower() == "true"
        if not is_admin:
            is_valid, error_msg = validate_cpz_credentials(api_key, secret_key)
            if not is_valid:
                raise ValueError(error_msg or "Invalid CPZ API credentials format")
        
        # Allow overriding the API base for local development
        # Examples:
        #   CPZ_AI_BASE_URL="http://127.0.0.1:54321/functions/v1"
        #   CPZ_AI_BASE_URL="https://api-ai.cpz-lab.com/cpz"  (default)
        url = (env.get("CPZ_AI_BASE_URL") or CPZAIClient.DEFAULT_API_URL).rstrip("/")
        # secret_key already determined above (preferred: CPZ_AI_API_SECRET_KEY, fallback to alternatives)
        user_id = env.get("CPZ_AI_USER_ID", "")
        return CPZAIClient(
            url=url, api_key=api_key, secret_key=secret_key, user_id=user_id, is_admin=is_admin
        )

    @staticmethod
    def from_keys(
        api_key: str, secret_key: str, user_id: Optional[str] = None, is_admin: bool = False
    ) -> "CPZAIClient":
        """Create client from keys only, using built-in default URL."""
        # Validation happens in __init__, but we can validate here too for early feedback
        # Skip validation for admin clients (they may use JWT tokens)
        if not is_admin:
            is_valid, error_msg = validate_cpz_credentials(api_key, secret_key)
            if not is_valid:
                raise ValueError(error_msg or "Invalid CPZ API credentials format")
        return CPZAIClient(
            url=CPZAIClient.DEFAULT_API_URL,
            api_key=api_key,
            secret_key=secret_key,
            user_id=user_id or "",
            is_admin=is_admin,
        )

    def _headers(self) -> dict[str, str]:
        # Support both gateway styles: custom header keys and PostgREST defaults
        # Match PyPI version that was working before - simple and robust
        headers = {
            "X-CPZ-KEY": self.api_key,
            "X-CPZ-SECRET": self.secret_key,
            # Default PostgREST schema headers (safe no-ops for non-PostgREST endpoints)
            "Accept-Profile": "public",
            "Content-Profile": "public",
            "Content-Type": "application/json",
        }
        # For admin/service keys: use JWT token in Authorization header
        if self.is_admin and self.secret_key.startswith("eyJ"):  # JWT tokens start with "eyJ"
            headers["Authorization"] = f"Bearer {self.secret_key}"
            headers["apikey"] = self.secret_key
        else:
            # For user keys: add placeholder Authorization header
            # The gateway/edge function needs this to accept the request, but will use X-CPZ headers for actual auth
            # This matches the pattern used in storage endpoint routing
            headers["Authorization"] = "Bearer cpz-auth-placeholder"
        return headers


    def health(self) -> bool:
        """Check if the CPZ AI Platform is accessible"""
        try:
            # Try PostgREST style first
            resp = requests.get(f"{self.url}/", headers=self._headers(), timeout=10)
            return resp.status_code < 500
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_platform_health_error", error=str(exc))
            return False

    def get_strategies(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get user's strategies from strategies table"""
        try:
            params = {"limit": limit, "offset": offset}

            # Filter by user_id unless admin
            if not self.is_admin and self.user_id:
                params["user_id"] = f"eq.{self.user_id}"

            resp = requests.get(
                f"{self.url}/strategies", headers=self._headers(), params=params, timeout=10
            )
            if resp.status_code == 200:
                return resp.json()
            else:
                self.logger.error(
                    "cpz_ai_get_strategies_error", status=resp.status_code, response=resp.text
                )
                return []
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_get_strategies_exception", error=str(exc))
            return []

    def get_strategy(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific strategy by ID"""
        try:
            resp = requests.get(
                f"{self.url}/strategies",
                headers=self._headers(),
                params={"id": f"eq.{strategy_id}"},
                timeout=10,
            )
            if resp.status_code == 200:
                strategies = resp.json()
                return strategies[0] if strategies else None
            else:
                self.logger.error(
                    "cpz_ai_get_strategy_error", status=resp.status_code, response=resp.text
                )
                return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_get_strategy_exception", error=str(exc))
            return None

    def get_orders(self, limit: int = 100, offset: int = 0, strategy_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get user's orders from orders table
        
        Args:
            limit: Maximum number of orders to return (default: 100)
            offset: Number of orders to skip (default: 0)
            strategy_id: Optional strategy ID to filter by
        
        Returns:
            List of order dictionaries
        """
        try:
            params = {"limit": limit, "offset": offset, "order": "created_at.desc", "select": "*"}

            # Filter by user_id unless admin
            if not self.is_admin and self.user_id:
                params["user_id"] = f"eq.{self.user_id}"
            
            # Filter by strategy_id if provided
            if strategy_id:
                params["strategy_id"] = f"eq.{strategy_id}"

            headers = self._headers()
            
            # Query orders table via gateway at api-ai.cpz-lab.com
            # All requests go through the proxy - no direct Supabase access
            resp = requests.get(
                f"{self.url}/orders", headers=headers, params=params, timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                # Handle both list and single object responses
                # Edge function returns {"ok": true} for GET, so check if it's a list
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "ok" in data:
                    # Edge function GET endpoint - return empty (orders are in database, not via edge function GET)
                    return []
                elif isinstance(data, dict):
                    return [data]
                else:
                    return []
            else:
                self.logger.error(
                    "cpz_ai_get_orders_error", status=resp.status_code, response=resp.text[:200]
                )
                return []
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_get_orders_exception", error=str(exc))
            return []

    def create_strategy(self, strategy_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new strategy"""
        try:
            # Automatically set user_id unless admin
            if not self.is_admin and self.user_id:
                strategy_data["user_id"] = self.user_id

            resp = requests.post(
                f"{self.url}/strategies", headers=self._headers(), json=strategy_data, timeout=10
            )
            if resp.status_code == 201:
                return resp.json()[0] if resp.json() else None
            else:
                self.logger.error(
                    "cpz_ai_create_strategy_error", status=resp.status_code, response=resp.text
                )
                return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_create_strategy_exception", error=str(exc))
            return None

    def update_strategy(
        self, strategy_id: str, strategy_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an existing strategy"""
        try:
            resp = requests.patch(
                f"{self.url}/strategies",
                headers=self._headers(),
                params={"id": f"eq.{strategy_id}"},
                json=strategy_data,
                timeout=10,
            )
            if resp.status_code == 200:
                return resp.json()[0] if resp.json() else None
            else:
                self.logger.error(
                    "cpz_ai_update_strategy_error", status=resp.status_code, response=resp.text
                )
                return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_update_strategy_exception", error=str(exc))
            return None

    def delete_strategy(self, strategy_id: str) -> None:
        """Delete a strategy"""
        try:
            resp = requests.delete(
                f"{self.url}/strategies",
                headers=self._headers(),
                params={"id": f"eq.{strategy_id}"},
                timeout=10,
            )
            return resp.status_code == 200
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_delete_strategy_error", error=str(exc))
            return False

    def _get_storage_base_url(self) -> str:
        """Get the base URL for storage operations - routes through API gateway"""
        # Storage operations go through the same API gateway as other endpoints
        # The gateway will route /storage/* requests to the appropriate backend
        return self.url

    def get_files(self, bucket_name: str = "default") -> List[Dict[str, Any]]:
        """Get files from a storage bucket"""
        try:
            # For user-specific access, keep bucket name as-is, prefix path with user_id
            # Bucket structure: user-data/{user_id}/files...
            if not self.is_admin and self.user_id:
                # Keep bucket name as-is (e.g., "user-data")
                # Path will be prefixed with user_id by the edge function
                pass

            storage_base = self._get_storage_base_url()
            resp = requests.get(
                f"{storage_base}/storage/object/list/{bucket_name}", headers=self._headers(), timeout=10
            )
            if resp.status_code == 200:
                files = resp.json()

                # Filter files by user_id unless admin
                if not self.is_admin and self.user_id and files:
                    # Filter files that belong to this user
                    user_files = []
                    for file in files:
                        # Check if file path contains user_id or if metadata indicates ownership
                        if (
                            self.user_id in file.get("name", "")
                            or file.get("metadata", {}).get("user_id") == self.user_id
                        ):
                            user_files.append(file)
                    return user_files

                return files
            else:
                self.logger.error(
                    "cpz_ai_get_files_error", status=resp.status_code, response=resp.text
                )
                return []
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_get_files_exception", error=str(exc))
            return []

    def get_file(self, bucket_name: str, file_path: str) -> Optional[Dict[str, Any]]:
        """Get file metadata from storage"""
        try:
            storage_base = self._get_storage_base_url()
            resp = requests.get(
                f"{storage_base}/storage/object/info/{bucket_name}/{file_path}",
                headers=self._headers(),
                timeout=10,
            )
            if resp.status_code == 200:
                return resp.json()
            else:
                self.logger.error(
                    "cpz_ai_get_file_error", status=resp.status_code, response=resp.text
                )
                return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_get_file_exception", error=str(exc))
            return None

    def upload_file(
        self,
        bucket_name: str,
        file_path: str,
        file_content: bytes,
        content_type: str = "application/octet-stream",
    ) -> Optional[Dict[str, Any]]:
        """Upload a file to storage"""
        try:
            # For user-specific access, keep bucket name as-is, prefix path with user_id
            if not self.is_admin and self.user_id:
                # Keep bucket name as-is (e.g., "user-data")
                # Prefix path with user_id folder for isolation
                if not file_path.startswith(f"{self.user_id}/"):
                    file_path = f"{self.user_id}/{file_path}"

            headers = self._headers()
            headers["Content-Type"] = content_type

            storage_base = self._get_storage_base_url()
            resp = requests.post(
                f"{storage_base}/storage/object/{bucket_name}/{file_path}",
                headers=headers,
                data=file_content,
                timeout=30,
            )
            if resp.status_code == 200:
                return resp.json()
            else:
                self.logger.error(
                    "cpz_ai_upload_file_error", status=resp.status_code, response=resp.text
                )
                return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_upload_file_exception", error=str(exc))
            return None

    def upload_csv_file(
        self, bucket_name: str, file_path: str, csv_content: str, encoding: str = "utf-8"
    ) -> Optional[Dict[str, Any]]:
        """Upload a CSV file to storage"""
        try:
            csv_bytes = csv_content.encode(encoding)
            return self.upload_file(bucket_name, file_path, csv_bytes, "text/csv")
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_upload_csv_exception", error=str(exc))
            return None

    def upload_dataframe(
        self, bucket_name: str, file_path: str, df: Any, format: str = "csv", **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Upload a pandas DataFrame to storage"""
        try:
            if format.lower() == "csv":
                csv_content = df.to_csv(index=False, **kwargs)
                return self.upload_csv_file(bucket_name, file_path, csv_content)
            elif format.lower() == "json":
                json_content = df.to_json(orient="records", **kwargs)
                json_bytes = json_content.encode("utf-8")
                return self.upload_file(bucket_name, file_path, json_bytes, "application/json")
            elif format.lower() == "parquet":
                # Convert DataFrame to parquet bytes
                buffer = io.BytesIO()
                df.to_parquet(buffer, index=False, **kwargs)
                buffer.seek(0)
                return self.upload_file(
                    bucket_name, file_path, buffer.getvalue(), "application/octet-stream"
                )
            else:
                raise ValueError(f"Unsupported format: {format}. Use 'csv', 'json', or 'parquet'")
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_upload_dataframe_exception", error=str(exc))
            return None

    def download_file(self, bucket_name: str, file_path: str) -> Optional[bytes]:
        """Download a file from storage"""
        try:
            # For user-specific access, use user-specific bucket
            if not self.is_admin and self.user_id:
                user_bucket = f"{bucket_name}-{self.user_id}"
                bucket_name = user_bucket

                # Add user_id to file path if not already present
                if not file_path.startswith(f"{self.user_id}/"):
                    file_path = f"{self.user_id}/{file_path}"

            storage_base = self._get_storage_base_url()
            resp = requests.get(
                f"{storage_base}/storage/object/{bucket_name}/{file_path}",
                headers=self._headers(),
                timeout=30,
            )
            if resp.status_code == 200:
                return resp.content
            else:
                self.logger.error(
                    "cpz_ai_download_file_error", status=resp.status_code, response=resp.text
                )
                return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_download_file_exception", error=str(exc))
            return None

    def download_csv_to_dataframe(
        self, bucket_name: str, file_path: str, encoding: str = "utf-8", **kwargs
    ) -> Optional[Any]:
        """Download a CSV file and load it into a pandas DataFrame"""
        try:
            import pandas as pd

            file_content = self.download_file(bucket_name, file_path)
            if file_content:
                csv_content = file_content.decode(encoding)
                return pd.read_csv(io.StringIO(csv_content), **kwargs)
            return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_download_csv_exception", error=str(exc))
            return None

    def download_json_to_dataframe(
        self, bucket_name: str, file_path: str, **kwargs
    ) -> Optional[Any]:
        """Download a JSON file and load it into a pandas DataFrame"""
        try:
            import pandas as pd

            file_content = self.download_file(bucket_name, file_path)
            if file_content:
                json_content = file_content.decode("utf-8")
                return pd.read_json(json_content, **kwargs)
            return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_download_json_exception", error=str(exc))
            return None

    def download_parquet_to_dataframe(
        self, bucket_name: str, file_path: str, **kwargs
    ) -> Optional[Any]:
        """Download a Parquet file and load it into a pandas DataFrame"""
        try:
            import pandas as pd

            file_content = self.download_file(bucket_name, file_path)
            if file_content:
                buffer = io.BytesIO(file_content)
                return pd.read_parquet(buffer, **kwargs)
            return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_download_parquet_exception", error=str(exc))
            return None

    def list_files_in_bucket(
        self, bucket_name: str, prefix: str = "", limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List files in a storage bucket with optional prefix filtering"""
        try:
            # For user-specific access, keep bucket name as-is, prefix path with user_id
            if not self.is_admin and self.user_id:
                # Keep bucket name as-is (e.g., "user-data")
                # Prefix with user_id folder for isolation
                if prefix and not prefix.startswith(f"{self.user_id}/"):
                    prefix = f"{self.user_id}/{prefix}"
                elif not prefix:
                    prefix = f"{self.user_id}/"

            params = {"limit": limit}
            if prefix:
                params["prefix"] = prefix

            storage_base = self._get_storage_base_url()
            resp = requests.get(
                f"{storage_base}/storage/object/list/{bucket_name}",
                headers=self._headers(),
                params=params,
                timeout=10,
            )
            if resp.status_code == 200:
                files = resp.json()

                # Filter files by user_id unless admin
                if not self.is_admin and self.user_id and files:
                    # Filter files that belong to this user
                    user_files = []
                    for file in files:
                        # Check if file path contains user_id or if metadata indicates ownership
                        if (
                            self.user_id in file.get("name", "")
                            or file.get("metadata", {}).get("user_id") == self.user_id
                        ):
                            user_files.append(file)
                    return user_files

                return files
            else:
                self.logger.error(
                    "cpz_ai_list_files_error", status=resp.status_code, response=resp.text
                )
                return []
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_list_files_exception", error=str(exc))
            return []

    def create_bucket(self, bucket_name: str, public: bool = False) -> bool:
        """Create a new storage bucket"""
        try:
            # Keep bucket name as-is - users share the same bucket (e.g., "user-data")
            # User isolation is handled by folder structure ({user_id}/files...)
            if not self.is_admin and self.user_id:
                # Keep bucket name as-is
                pass

            bucket_data = {"name": bucket_name, "public": public}

            storage_base = self._get_storage_base_url()
            resp = requests.post(
                f"{storage_base}/storage/bucket", headers=self._headers(), json=bucket_data, timeout=10
            )
            return resp.status_code == 200
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_create_bucket_exception", error=str(exc))
            return False

    def delete_file(self, bucket_name: str, file_path: str) -> bool:
        """Delete a file from storage"""
        try:
            # For user-specific access, use user-specific bucket
            if not self.is_admin and self.user_id:
                user_bucket = f"{bucket_name}-{self.user_id}"
                bucket_name = user_bucket

                # Add user_id to file path if not already present
                if not file_path.startswith(f"{self.user_id}/"):
                    file_path = f"{self.user_id}/{file_path}"

            storage_base = self._get_storage_base_url()
            resp = requests.delete(
                f"{storage_base}/storage/object/{bucket_name}/{file_path}",
                headers=self._headers(),
                timeout=10,
            )
            return resp.status_code == 200
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_delete_file_error", error=str(exc))
            return False

    def list_tables(self) -> list[str]:
        """List available tables in the CPZ AI Platform"""
        # Prefer consolidated /metadata endpoint with flexible shapes
        try:
            meta = requests.get(f"{self.url}/metadata", headers=self._headers(), timeout=10)
            if meta.status_code == 200:
                data = meta.json()
                tables: list[str] = []
                if isinstance(data, dict):
                    # Common shapes we support:
                    # 1) { "orders": {"columns": [...]}, "strategies": {...}, ... }
                    # 2) { "tables": ["orders", "strategies", ...] }
                    # 3) { "tables": [{"name": "orders"}, {"name": "strategies"}] }
                    # 4) { "columns": { "orders": [...], "strategies": [...] } }
                    if any(isinstance(v, dict) and "columns" in v for v in data.values()):
                        tables = [
                            str(k)
                            for k, v in data.items()
                            if isinstance(v, dict) and ("columns" in v or "fields" in v)
                        ]
                    elif "tables" in data:
                        t = data.get("tables")
                        if isinstance(t, list):
                            if t and isinstance(t[0], str):
                                tables = [str(x) for x in t]
                            elif t and isinstance(t[0], dict):
                                tables = [
                                    str(x.get("name") or x.get("table") or x.get("id"))
                                    for x in t
                                    if (x.get("name") or x.get("table") or x.get("id"))
                                ]
                    elif "columns" in data and isinstance(data["columns"], dict):
                        tables = [str(k) for k in data["columns"].keys()]
                    else:
                        # As a last resort, if dict looks like {"columns": ..., "user_id": ...}, ignore and try fallback
                        tables = []
                if tables:
                    return sorted({t for t in tables if t})
        except Exception as exc:  # noqa: BLE001
            self.logger.warning("cpz_ai_metadata_error", error=str(exc))
        # Fallback to PostgREST discovery
        try:
            resp = requests.get(f"{self.url}/", headers=self._headers(), timeout=10)
            if resp.status_code == 200 and isinstance(resp.json(), dict):
                # PostgREST root returns an object whose keys are allowed tables/views
                allowed = resp.json()
                return sorted([str(k) for k in allowed.keys()])
        except Exception as exc:  # noqa: BLE001
            self.logger.warning("cpz_ai_list_tables_error", error=str(exc))
        return []

    def list_trading_credentials(self) -> list[Dict[str, Any]]:
        """Return all trading credentials rows accessible to this key.
        
        Uses the fast /trading_credentials_private endpoint with a short timeout
        to avoid hanging while still enabling enrichment logic in create_order_intent().
        """
        try:
            headers = self._headers()
            # Use the same fast endpoint as get_broker_credentials() to avoid hanging
            resp = requests.get(
                f"{self.url}/trading_credentials_private",
                headers=headers,
                timeout=(0.5, 0.5)  # 500ms max - fail fast
            )
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    return data
            return []
        except Exception:  # noqa: BLE001
            # Fail fast - return empty list immediately, don't hang
            return []

    # --- Orders ---
    def record_order(
        self,
        *,
        order_id: str,
        symbol: str,
        side: str,
        qty: float,
        type: str,
        time_in_force: str,
        broker: str,
        env: str,
        strategy_id: Optional[str] = None,
        status: Optional[str] = None,
        filled_at: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Persist an execution record into CPZ orders table.

        Writes to consolidated gateway first (POST /orders) and falls back to
        PostgREST path if needed.
        """
        # Discover actual columns to avoid schema mismatches (e.g., quantity vs qty)
        columns: set[str] = set()
        try:
            meta = requests.get(f"{self.url}/metadata", headers=self._headers(), timeout=8)
            if meta.ok and isinstance(meta.json(), dict):
                orders_meta = meta.json().get("orders") or {}
                cols = orders_meta.get("columns") or []
                if isinstance(cols, list):
                    columns = {str(c) for c in cols}
        except Exception:
            pass

        def include(name: str) -> bool:
            return not columns or name in columns

        payload: Dict[str, Any] = {}
        if order_id and include("order_id"):
            payload["order_id"] = order_id
        if include("symbol"):
            payload["symbol"] = symbol
        if include("side"):
            payload["side"] = side
        # quantity column variations
        if "quantity" in columns:
            payload["quantity"] = qty
        elif include("qty"):
            payload["qty"] = qty
        # order type variations
        if "order_type" in columns:
            payload["order_type"] = type
        elif include("type"):
            payload["type"] = type
        if include("time_in_force"):
            payload["time_in_force"] = time_in_force
        if include("broker"):
            payload["broker"] = broker
        # Do not persist env; account_id/broker is sufficient for routing
        if strategy_id and include("strategy_id"):
            payload["strategy_id"] = strategy_id
        if status and include("status"):
            payload["status"] = status
        if filled_at and include("filled_at"):
            payload["filled_at"] = filled_at
        # CRITICAL: account_id must always be set (never NULL or empty)
        if account_id and include("account_id"):
            payload["account_id"] = account_id
        elif include("account_id"):
            # If account_id column exists but not provided, set empty string (edge function will resolve)
            payload["account_id"] = ""

        headers = self._headers()
        # Route through CPZ API gateway at api-ai.cpz-lab.com
        orders_url = f"{self.url}/orders"
        
        try:
            resp = requests.post(orders_url, headers=headers, json=payload, timeout=10)
            if 200 <= resp.status_code < 300:
                try:
                    data = resp.json()
                    return data
                except Exception:
                    return {"id": "unknown"}  # Success but no JSON response
            else:
                self.logger.warning(
                    "cpz_ai_record_order_error", 
                    status=resp.status_code, 
                    response=resp.text[:200]
                )
        except Exception as exc:  # noqa: BLE001
            self.logger.warning("cpz_ai_record_order_error", error=str(exc))
        
        return None

    # Intent-first logging. Create a row before broker handoff; returns created row (must include id)
    def create_order_intent(
        self,
        *,
        symbol: str,
        side: str,
        qty: float,
        type: str,
        time_in_force: str,
        broker: str,
        env: str,
        strategy_id: str,
        status: str = "pending",
        account_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        # Discover columns
        columns: set[str] = set()
        try:
            meta = requests.get(f"{self.url}/metadata", headers=self._headers(), timeout=8)
            if meta.ok and isinstance(meta.json(), dict):
                orders_meta = meta.json().get("orders") or {}
                cols = orders_meta.get("columns") or []
                if isinstance(cols, list):
                    columns = {str(c) for c in cols}
        except Exception:
            pass

        def include(name: str) -> bool:
            return not columns or name in columns

        payload: Dict[str, Any] = {}
        if include("symbol"):
            payload["symbol"] = symbol
        if include("side"):
            payload["side"] = side
        if "quantity" in columns:
            payload["quantity"] = qty
        elif include("qty"):
            payload["qty"] = qty
        if "order_type" in columns:
            payload["order_type"] = type
        elif include("type"):
            payload["type"] = type
        if include("time_in_force"):
            payload["time_in_force"] = time_in_force
        if include("broker"):
            payload["broker"] = broker
        # Do not persist env into orders
        if include("strategy_id"):
            payload["strategy_id"] = strategy_id
        if include("status"):
            payload["status"] = status
        # CRITICAL: account_id must always be set (never NULL or empty)
        if account_id and include("account_id"):
            payload["account_id"] = account_id
        elif include("account_id"):
            # If account_id column exists but not provided, set empty string (edge function will resolve)
            payload["account_id"] = ""

        # Enrich from trading credentials: user_id/account_id/broker if present
        try:
            rows = self.list_trading_credentials()
            broker_l = (broker or "").lower()
            env_l = (env or "").lower()
            acct_l = (account_id or "").strip()
            match = None
            for r in rows:
                if str(r.get("broker", "")).lower() != broker_l:
                    continue
                env_val = str(r.get("env") or r.get("environment") or r.get("mode") or "").lower()
                is_paper = (
                    r.get("is_paper")
                    or r.get("paper")
                    or r.get("sandbox")
                    or r.get("is_sandbox")
                    or r.get("paper_trading")
                )
                r_acct = str(r.get("account_id") or r.get("account") or "")
                if acct_l:
                    # Require matching account_id; env optional
                    if r_acct == acct_l and (
                        not env_l or env_val == env_l or (env_l == "paper" and bool(is_paper))
                    ):
                        match = r
                        break
                    else:
                        continue
                # No account filter; match by env if provided
                if env_l and (env_val == env_l or (env_l == "paper" and bool(is_paper))):
                    match = r
                    break
                if not env_l:
                    match = r
                    break
            if match:
                uid = match.get("user_id") or match.get("owner_id")
                aid = match.get("account_id") or match.get("account")
                mbroker = match.get("broker") or match.get("provider") or match.get("platform")
                if uid and include("user_id"):
                    payload["user_id"] = uid
                # Prefer user_id; do not require owner_id. If only owner_id exists and table expects it, include it.
                if uid and include("owner_id") and "user_id" not in columns:
                    payload["owner_id"] = uid
                if aid and include("account_id"):
                    payload["account_id"] = aid
                if mbroker and include("broker"):
                    payload["broker"] = mbroker
        except Exception:
            pass

        headers = self._headers()
        # Route through CPZ API gateway at api-ai.cpz-lab.com
        # The gateway will handle routing to the appropriate backend
        orders_url = f"{self.url}/orders"

        # Gateway endpoint
        try:
            r = requests.post(orders_url, headers=headers, json=payload, timeout=10)
            if 200 <= r.status_code < 300:
                try:
                    data = r.json()
                    # Accept dict or list-of-dicts
                    if isinstance(data, dict) and data.get("id"):
                        return data
                    if isinstance(data, list) and data:
                        first = data[0]
                        if isinstance(first, dict) and first.get("id"):
                            return first
                    # Some gateways return empty body or no id; try to find the row we just inserted
                    # Build a filter using fields most likely present
                    # Note: Platform functions endpoint doesn't support GET queries, so skip this for functions endpoint
                    if "/functions/v1/orders" not in orders_url:
                        params: Dict[str, str] = {
                            "select": "*",
                            "order": "created_at.desc",
                            "limit": "1",
                        }
                        for key in (
                            "user_id",
                            "account_id",
                            "broker",
                            "strategy_id",
                            "symbol",
                            "status",
                        ):
                            if key in payload and payload[key] is not None:
                                params[key] = f"eq.{payload[key]}"
                        rr = requests.get(
                            f"{self.url}/orders", headers=headers, params=params, timeout=8
                        )
                        if rr.ok:
                            found = rr.json()
                            if isinstance(found, list) and found:
                                row = found[0]
                                if isinstance(row, dict):
                                    return row
                        # Relax filters (drop broker/account_id) and retry
                        relaxed = {
                            k: v for k, v in params.items() if k not in ("broker", "account_id")
                        }
                        rr2 = requests.get(
                            f"{self.url}/orders", headers=headers, params=relaxed, timeout=8
                        )
                        if rr2.ok:
                            found = rr2.json()
                            if isinstance(found, list) and found:
                                row = found[0]
                                if isinstance(row, dict):
                                    return row
                except Exception:
                    return None
            else:
                # Extract error message from response
                error_msg = r.text
                try:
                    import json

                    error_body = json.loads(r.text)
                    if isinstance(error_body, dict) and "error" in error_body:
                        error_msg = error_body["error"]
                except Exception:
                    pass
                # Don't raise for 400 errors - these are often backend configuration issues
                # (e.g., "Invalid table" means the orders table might not be set up)
                # The order will still be submitted to the broker, which is the important part
                if r.status_code == 400 and "Invalid table" in error_msg:
                    # This is a backend configuration issue, not a critical error
                    # Log it but don't raise - order will still go to broker
                    self.logger.warning(
                        "cpz_orders_table_not_configured",
                        message="Orders table not configured in CPZ AI platform. Order will still be submitted to broker.",
                        error=error_msg
                    )
                    return None
                raise RuntimeError(f"orders insert failed ({r.status_code}): {error_msg}")
        except RuntimeError:
            # Re-raise RuntimeErrors as-is (they already have good error messages)
            raise
        except Exception as gw_exc:  # noqa: BLE001
            # All requests go through api-ai.cpz-lab.com proxy - no direct Supabase access
            raise RuntimeError(f"Failed to create order intent via gateway: {str(gw_exc)}")

    def update_order_record(
        self,
        *,
        id: str,
        order_id: Optional[str] = None,
        status: Optional[str] = None,
        filled_qty: Optional[float] = None,
        average_fill_price: Optional[float] = None,
        submitted_at: Optional[str] = None,
        filled_at: Optional[str] = None,
    ) -> bool:
        headers = self._headers()
        body: Dict[str, Any] = {}
        if order_id is not None:
            body["order_id"] = order_id
        if status is not None:
            body["status"] = status
        if filled_qty is not None:
            # Use filled_quantity (correct column name)
            body["filled_quantity"] = filled_qty
        if average_fill_price is not None:
            body["average_fill_price"] = average_fill_price
        if submitted_at is not None:
            body["submitted_at"] = submitted_at
        if filled_at is not None:
            body["filled_at"] = filled_at
        if not body:
            return True
        ok = False
        # Gateway attempt
        # All requests go through api-ai.cpz-lab.com proxy - no direct Supabase access
        # Try PATCH first (will work once Vercel is deployed)
        try:
            r = requests.patch(
                f"{self.url}/orders",
                headers=headers,
                params={"id": f"eq.{id}"},
                json=body,
                timeout=10,
            )
            if r.status_code in (200, 204):
                return True
            elif r.status_code == 405:
                # PATCH not supported yet - use POST upsert workaround
                # Include the record ID in the body so edge function can update
                upsert_body = body.copy()
                upsert_body["_update_id"] = id
                upsert_body["_upsert"] = True
                r2 = requests.post(
                    f"{self.url}/orders",
                    headers=headers,
                    json=upsert_body,
                    timeout=10,
                )
                if r2.status_code in (200, 201, 204):
                    return True
                else:
                    self.logger.warning(
                        "cpz_ai_update_order_record_post_fallback_error",
                        status=r2.status_code,
                        response=r2.text[:200],
                        order_id=id
                    )
            else:
                # Log error for debugging
                self.logger.warning(
                    "cpz_ai_update_order_record_error",
                    status=r.status_code,
                    response=r.text[:200],
                    order_id=id
                )
        except Exception as exc:
            self.logger.warning("cpz_ai_update_order_record_exception", error=str(exc), order_id=id)
        
        # Final fallback: Try POST upsert directly
        try:
            upsert_body = body.copy()
            upsert_body["_update_id"] = id
            upsert_body["_upsert"] = True
            r = requests.post(
                f"{self.url}/orders",
                headers=headers,
                json=upsert_body,
                timeout=10,
            )
            if r.status_code in (200, 201, 204):
                return True
        except Exception:
            pass
        
        return False

    def echo(self) -> dict[str, Any]:
        """Test connection to CPZ AI Platform"""
        try:
            resp = requests.get(f"{self.url}/", headers=self._headers(), timeout=10)
            return {"status": resp.status_code, "ok": resp.ok}
        except Exception as exc:  # noqa: BLE001
            return {"status": 0, "ok": False, "error": str(exc)}

    # --- Trading & Credentials ---
    def get_broker_credentials(
        self, broker: str = "alpaca", env: Optional[str] = None, account_id: Optional[str] = None
    ) -> Optional[Dict[str, str]]:
        """Fetch broker trading credentials from CPZ AI using the service key.

        Tries a few common table/field shapes to maximize compatibility without
        hard-coding a single schema. Returns a dict with keys
        {"api_key_id", "api_secret_key", "env"} if found, else None.
        """
        try:
            # Normalize inputs
            broker = (broker or "").strip().lower()
            env_norm = (env or "").strip().lower() or None
            account_norm = (account_id or "").strip()

            # Fetch all credentials and filter client-side (more reliable than query params)
            headers = self._headers()
            try:
                # Fetch all trading credentials with fast timeout
                resp = requests.get(
                    f"{self.url}/trading_credentials_private",
                    headers=headers,
                    timeout=(0.5, 0.5)  # 500ms max - fail fast
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list) and data:
                        # Filter client-side for matching broker/env/account
                        for row in data:
                            # Check broker match
                            row_broker = str(
                                row.get("broker") or row.get("broker_name") or row.get("provider") or ""
                            ).lower()
                            if broker not in row_broker and row_broker not in broker:
                                continue
                            
                            # Check account_id match if provided
                            if account_norm:
                                row_account = str(row.get("account_id") or row.get("account") or "")
                                if row_account != account_norm:
                                    continue
                            
                            # Check env match if provided
                            if env_norm:
                                row_env = str(row.get("env") or row.get("environment") or row.get("mode") or "").lower()
                                is_paper = bool(
                                    row.get("is_paper") or row.get("paper") or row.get("sandbox") or row.get("paper_trading")
                                )
                                env_match = (
                                    row_env == env_norm or 
                                    (env_norm == "paper" and is_paper) or
                                    (env_norm == "live" and not is_paper and row_env == "live")
                                )
                                if not env_match:
                                    continue
                            
                            # Extract credentials - handle multiple field name variations
                            api_key_id = str(
                                row.get("api_key_id") or 
                                row.get("api_key") or 
                                row.get("key_id") or 
                                row.get("key") or 
                                ""
                            )
                            api_secret_key = str(
                                row.get("api_secret_key") or 
                                row.get("api_secret") or 
                                row.get("secret_key") or 
                                row.get("secret") or 
                                ""
                            )
                            if api_key_id and api_secret_key:
                                # Determine env from row
                                row_env = str(
                                    row.get("env") or 
                                    row.get("environment") or 
                                    row.get("mode") or 
                                    ""
                                ).lower()
                                is_paper = bool(
                                    row.get("is_paper") or 
                                    row.get("paper") or 
                                    row.get("sandbox") or 
                                    row.get("paper_trading")
                                )
                                resolved_env = row_env or (env_norm or ("paper" if is_paper else "live"))
                                
                                return {
                                    "api_key_id": api_key_id,
                                    "api_secret_key": api_secret_key,
                                    "env": resolved_env,
                                }
            except Exception:  # noqa: BLE001
                # Fail fast - return None immediately, don't try slow fallbacks
                return None
            
            # No credentials found - return None immediately
            return None
        except Exception as exc:  # noqa: BLE001
            self.logger.error("cpz_ai_get_broker_credentials_error", error=str(exc))
            return None


# Legacy alias for backward compatibility (will be removed in future versions)
# Use CPZAIClient instead
