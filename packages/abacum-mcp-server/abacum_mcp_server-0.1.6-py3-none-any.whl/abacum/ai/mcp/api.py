"""
Abacum API Client
Handles OAuth2 authentication and data fetching.
"""

import httpx
import os
import sys
import hashlib
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Abacum API Configuration
ABACUM_API_BASE = "https://api.abacum.io"
ABACUM_TOKEN_URL = f"{ABACUM_API_BASE}/server-authentication/oauth2/token/"

# Token cache (to avoid requesting a new token for every call)
_token_cache = {
    "access_token": None,
    "expires_at": None
}

# DataFrame cache with TTL (5 minutes default)
# Format: {cache_key: {"dataframe": df, "metadata": dict, "expires_at": datetime}}
_dataframe_cache = {}
CACHE_TTL_SECONDS = 300  # 5 minutes
MAX_CACHE_SIZE = 10


class ApiError(Exception):
    """Custom exception for API-related errors."""

    def __init__(self, message, status_code=None, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details

    def to_dict(self):
        return {
            "error": str(self),
            "status_code": self.status_code,
            "details": self.details
        }


def get_api_credentials() -> (str, str):
    """
    Get Abacum API credentials from environment variables.

    Reads from the variable names specified in the CLIENTS.md setup.
    """
    client_id = os.getenv("ABACUM_API_CLIENT_ID")
    client_secret = os.getenv("ABACUM_API_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ApiError(
            "Abacum API credentials not found. "
            "Please set ABACUM_API_CLIENT_ID and ABACUM_API_CLIENT_SECRET environment variables."
        )
    return client_id, client_secret


async def get_abacum_access_token() -> str:
    """
    Get or refresh the Abacum API access token using OAuth2 client credentials flow.
    Tokens are cached and automatically refreshed when expired.
    """
    # Check if we have a valid cached token
    if _token_cache["access_token"] and _token_cache["expires_at"]:
        if datetime.now() < _token_cache["expires_at"]:
            return _token_cache["access_token"]

    # Get credentials
    client_id, client_secret = get_api_credentials()

    # Request a new token
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                ABACUM_TOKEN_URL,
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": "client_credentials"
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )

            response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx

            token_data = response.json()
            access_token = token_data.get("access_token")

            # Tokens expire in 1 week, cache with a 5-min buffer
            expires_in = token_data.get("expires_in", 604800)  # Default 7 days
            expires_at = datetime.now() + timedelta(seconds=expires_in - 300)

            # Cache the token
            _token_cache["access_token"] = access_token
            _token_cache["expires_at"] = expires_at

            return access_token

        except httpx.HTTPStatusError as e:
            raise ApiError(
                f"Failed to get access token: {e.response.status_code}",
                status_code=e.response.status_code,
                details=e.response.text
            )
        except Exception as e:
            raise ApiError(f"Failed to get access token: {str(e)}")


async def _make_api_request(url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    """Helper function to make authenticated GET requests."""
    access_token = await get_abacum_access_token()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                params=params,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                }
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ApiError("Authentication failed. Please check your Abacum API credentials.", 401)
            if e.response.status_code == 403:
                raise ApiError("Access forbidden. You may not have permission.", 403)
            if e.response.status_code == 404:
                raise ApiError("Resource not found.", 404)
            raise ApiError(
                f"API request failed with status {e.response.status_code}",
                status_code=e.response.status_code,
                details=e.response.text
            )
        except Exception as e:
            raise ApiError(f"API request failed: {str(e)}")


def _generate_cache_key(model_id: str, endpoint: str, scenario_id: Optional[str] = None,
                       start_date: Optional[str] = None, end_date: Optional[str] = None,
                       variable_ids: Optional[list[str]] = None) -> str:
    """Generate a unique cache key for the request parameters."""
    key_parts = [model_id, endpoint]
    if scenario_id:
        key_parts.append(scenario_id)
    if start_date:
        key_parts.append(start_date)
    if end_date:
        key_parts.append(end_date)
    if variable_ids:
        key_parts.append(",".join(sorted(variable_ids)))

    key_string = "|".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def _get_from_cache(cache_key: str) -> Optional[Dict[str, Any]]:
    """Get cached DataFrame if it exists and hasn't expired."""
    if cache_key not in _dataframe_cache:
        return None

    cache_entry = _dataframe_cache[cache_key]
    if datetime.now() >= cache_entry["expires_at"]:
        # Expired, remove from cache
        del _dataframe_cache[cache_key]
        return None

    sys.stderr.write(f"Cache hit for key: {cache_key}\n")
    return cache_entry


def _add_to_cache(cache_key: str, dataframe: pd.DataFrame, metadata: dict):
    """Add DataFrame to cache with TTL, managing cache size."""
    global _dataframe_cache

    # If cache is full, remove oldest entry
    if len(_dataframe_cache) >= MAX_CACHE_SIZE:
        oldest_key = min(_dataframe_cache.keys(),
                        key=lambda k: _dataframe_cache[k]["expires_at"])
        del _dataframe_cache[oldest_key]
        sys.stderr.write(f"Cache full, removed oldest entry: {oldest_key}\n")

    _dataframe_cache[cache_key] = {
        "dataframe": dataframe,
        "metadata": metadata,
        "expires_at": datetime.now() + timedelta(seconds=CACHE_TTL_SECONDS)
    }
    sys.stderr.write(f"Cached data for key: {cache_key}\n")


async def _fetch_and_parse_csv(url: str) -> pd.DataFrame:
    """Fetch CSV data from S3 URL and parse into DataFrame."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()

            # Parse CSV into DataFrame
            df = pd.read_csv(StringIO(response.text))
            sys.stderr.write(f"Fetched and parsed DataFrame with shape: {df.shape}\n")
            return df

        except httpx.HTTPStatusError as e:
            raise ApiError(
                f"Failed to fetch CSV data: {e.response.status_code}",
                status_code=e.response.status_code,
                details=e.response.text
            )
        except Exception as e:
            raise ApiError(f"Failed to parse CSV data: {str(e)}")


async def list_models() -> dict:
    """Fetches all models from Abacum API."""
    data = await _make_api_request(f"{ABACUM_API_BASE}/public-api/models")
    return {
        "success": True,
        "models": data.get("data", []),
        "count": len(data.get("data", [])),
        "timestamp": datetime.now().isoformat()
    }


async def list_scenarios() -> dict:
    """Fetches all scenarios from Abacum API."""
    data = await _make_api_request(f"{ABACUM_API_BASE}/public-api/scenarios")
    return {
        "success": True,
        "scenarios": data.get("data", []),
        "count": len(data.get("data", [])),
        "timestamp": datetime.now().isoformat()
    }


async def _get_model_data(
        endpoint: str,
        model_id: str,
        scenario_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        variable_ids: Optional[list[str]] = None
) -> dict:
    """Generic function to fetch model data (actuals, scenario, rolling) with caching."""

    if (start_date and not end_date) or (end_date and not start_date):
        raise ApiError("Both start_date and end_date must be provided together")

    # Generate cache key
    cache_key = _generate_cache_key(model_id, endpoint, scenario_id, start_date, end_date, variable_ids)

    # Check cache first
    cached_data = _get_from_cache(cache_key)
    if cached_data:
        return {
            "success": True,
            "model_id": model_id,
            "scenario_id": scenario_id,
            "metadata": cached_data["metadata"],
            "data": cached_data["dataframe"].to_dict(orient='split'),
            "timestamp": datetime.now().isoformat(),
            "cached": True
        }

    # Build URL
    if scenario_id:
        url = f"{ABACUM_API_BASE}/public-api/models/{model_id}/{endpoint}/{scenario_id}"
    else:
        url = f"{ABACUM_API_BASE}/public-api/models/{model_id}/{endpoint}"

    params = {}
    if start_date and end_date:
        params["start_date"] = start_date
        params["end_date"] = end_date
    if variable_ids:
        params["variable_ids"] = ",".join(variable_ids)

    # Fetch API response (contains S3 URL and metadata)
    api_response = await _make_api_request(url, params=params)

    # Extract S3 URL and metadata
    s3_url = api_response.get("data")
    metadata = api_response.get("metadata")

    if not s3_url:
        raise ApiError("No data URL returned from API")

    # Fetch and parse CSV data into DataFrame
    df = await _fetch_and_parse_csv(s3_url)

    # Cache the parsed DataFrame
    _add_to_cache(cache_key, df, metadata)

    return {
        "success": True,
        "model_id": model_id,
        "scenario_id": scenario_id,
        "metadata": metadata,
        "data": df.to_dict(orient='split'),
        "timestamp": datetime.now().isoformat(),
        "cached": False
    }


async def get_model_actuals(
        model_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        variable_ids: Optional[list[str]] = None
) -> dict:
    return await _get_model_data(
        "actuals_data", model_id,
        start_date=start_date, end_date=end_date, variable_ids=variable_ids
    )


async def get_scenario_data(
        model_id: str,
        scenario_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        variable_ids: Optional[list[str]] = None
) -> dict:
    return await _get_model_data(
        "scenario_data", model_id, scenario_id,
        start_date=start_date, end_date=end_date, variable_ids=variable_ids
    )


async def get_rolling_data(
        model_id: str,
        scenario_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        variable_ids: Optional[list[str]] = None
) -> dict:
    return await _get_model_data(
        "rolling_data", model_id, scenario_id,
        start_date=start_date, end_date=end_date, variable_ids=variable_ids
    )

async def list_variables(model_id: Optional[str]) -> dict:
    url = f"{ABACUM_API_BASE}/public-api/variables"
    params = {"model_id": model_id} if model_id else None

    data = await _make_api_request(url, params=params)

    return {
        "success": True,
        "variables": data.get("data", []),
        "count": len(data.get("data", [])),
        "timestamp": datetime.now().isoformat()
    }