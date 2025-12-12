"""Cache API client extension for TestDino API"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import httpx

from testdino_cli.config.index import Config
from testdino_cli.types import AuthenticationError, NetworkError
from testdino_cli.utils.retry import RetryOptions, with_retry
from testdino_cli.version import VERSION


@dataclass
class CacheSubmissionResponse:
    """Cache submission response from TestDino API"""

    success: bool
    cache_id: str
    message: Optional[str] = None


@dataclass
class CacheRetrievalOptions:
    """Cache retrieval options"""

    cache_id: str
    shard_index: Optional[int] = None
    for_all_shards: bool = False


@dataclass
class CachePayload:
    """Cache payload structure matching new API specification"""

    cache_id: str
    pipeline_id: str
    commit: str
    branch: str
    repository: str
    ci: Dict[str, str]
    is_sharded: bool
    shard_index: Optional[int]
    shard_total: Optional[int]
    failures: List[Dict[str, str]]
    summary: Dict[str, int]
    timestamp: str


class CacheApiClient:
    """Cache API client for submitting test metadata to TestDino"""

    def __init__(self, config: Config):
        self.base_url = str(config.api_url)
        self.api_key = config.token

    async def submit_cache_data(
        self, payload: Union[CachePayload, Dict[str, Any]]
    ) -> CacheSubmissionResponse:
        """Submit cache data to TestDino API with retry logic"""
        return await with_retry(
            lambda: self._submit_cache_data_attempt(payload),
            RetryOptions(max_attempts=3, base_delay=1000, max_delay=5000),
        )

    async def _submit_cache_data_attempt(
        self, payload: Any
    ) -> CacheSubmissionResponse:
        """Single attempt to submit cache data"""
        url = f"{self.base_url}/api/cache"

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                # Handle both dict and CachePayload object
                if isinstance(payload, dict):
                    payload_dict = {
                        "cacheId": payload.get("cacheId"),
                        "pipelineId": payload.get("pipelineId"),
                        "commit": payload.get("commit"),
                        "branch": payload.get("branch"),
                        "repository": payload.get("repository"),
                        "ci": payload.get("ci"),
                        "isSharded": payload.get("isSharded"),
                        "shardIndex": payload.get("shardIndex"),
                        "shardTotal": payload.get("shardTotal"),
                        "failures": payload.get("failures"),
                        "summary": payload.get("summary"),
                        "timestamp": payload.get("timestamp"),
                    }
                else:
                    payload_dict = {
                        "cacheId": payload.cache_id,
                        "pipelineId": payload.pipeline_id,
                        "commit": payload.commit,
                        "branch": payload.branch,
                        "repository": payload.repository,
                        "ci": payload.ci,
                        "isSharded": payload.is_sharded,
                        "shardIndex": payload.shard_index,
                        "shardTotal": payload.shard_total,
                        "failures": payload.failures,
                        "summary": payload.summary,
                        "timestamp": payload.timestamp,
                    }

                response = await client.post(
                    url, headers=self._get_headers(), json=payload_dict
                )

                if not response.is_success:
                    await self._handle_http_error(response)

                data = response.json()
                return self._parse_response(data)

            except (AuthenticationError, NetworkError):
                raise
            except Exception as error:
                raise NetworkError(f"Failed to submit cache data: {str(error)}")

    def _get_headers(self) -> Dict[str, str]:
        """Headers for API requests"""
        return {
            "Content-Type": "application/json",
            "User-Agent": f"testdino-cache/{VERSION}",
            "X-API-Key": self.api_key,
        }

    async def _handle_http_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses"""
        try:
            error_body = response.text
        except Exception:
            error_body = "Unable to read error response"

        status = response.status_code

        if status == 401:
            raise AuthenticationError("Invalid API key for cache submission")
        elif status == 403:
            raise AuthenticationError(
                "API key does not have permission to submit cache data"
            )
        elif status == 400:
            raise NetworkError(f"Bad cache data format: {error_body}")
        elif status == 404:
            raise NetworkError(
                "Cache endpoint not found - feature may not be available yet"
            )
        elif status == 409:
            # Conflict - cache data already exists (not an error, don't retry)
            conflict_error = NetworkError("Cache data already exists for this shard")
            conflict_error.retryable = False  # type: ignore
            raise conflict_error
        elif status == 413:
            raise NetworkError(
                "Cache payload too large - consider reducing failure data"
            )
        elif status == 429:
            raise NetworkError("Rate limit exceeded for cache submissions")
        elif status in (500, 502, 503, 504):
            raise NetworkError(
                f"Server error submitting cache data ({status}) - will retry"
            )
        else:
            raise NetworkError(
                f"Cache submission failed: HTTP {status} - {error_body}"
            )

    def _parse_response(self, data: Any) -> CacheSubmissionResponse:
        """Parse and validate API response"""
        if not data or not isinstance(data, dict):
            raise NetworkError("Invalid cache submission response format")

        # Handle response with nested data structure
        if "success" in data and "data" in data and isinstance(data["data"], dict):
            response_data = data["data"]
            return CacheSubmissionResponse(
                success=bool(data["success"]),
                cache_id=str(response_data.get("cacheId", "unknown")),
                message=str(data["message"]) if "message" in data else None,
            )

        # Handle flat response format
        if "success" in data and "cacheId" in data:
            return CacheSubmissionResponse(
                success=bool(data["success"]),
                cache_id=str(data.get("cacheId", "unknown")),
                message=str(data["message"]) if "message" in data else None,
            )

        # Fallback: assume success if we got a response
        return CacheSubmissionResponse(
            success=True,
            cache_id=str(data.get("cacheId", "unknown")),
            message=str(data["message"]) if "message" in data else None,
        )

    async def test_cache_endpoint(self) -> bool:
        """Test if cache API endpoint is available (health check)"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.request(
                    "OPTIONS",
                    f"{self.base_url}/api/v1/cache",
                    headers={"User-Agent": f"testdino-cache/{VERSION}"},
                )

                # Even 404 means the server is responding
                return response.status_code < 500
        except Exception:
            return False

    async def get_cache_data(
        self, cache_id: str, options: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """Get cache data for specific cache ID (simplified for last-failed command)"""
        try:
            from urllib.parse import urlencode

            url = f"{self.base_url}/api/cache/{cache_id}"

            # Add query parameters if provided
            if options:
                query_params = urlencode(
                    {k: v for k, v in options.items() if v is not None}
                )
                if query_params:
                    url = f"{url}?{query_params}"

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self._get_headers())

                if not response.is_success:
                    # Return None for 404 or other errors
                    return None

                data = response.json()

                # Extract the data we need for last-failed command
                if data and data.get("data") and data["data"].get("cache"):
                    return {
                        "cacheId": data["data"].get("cacheId", cache_id),
                        "failures": data["data"]["cache"].get("failures", []),
                        "branch": data["data"]["cache"].get("branch", "unknown"),
                        "repository": data["data"]["cache"].get("repository", "unknown"),
                    }

                return None
        except Exception:
            # Network error - return None to allow fallback
            return None

    async def get_latest_cache_data(
        self, branch: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get latest cache data (with optional branch filter)"""
        try:
            from urllib.parse import urlencode

            url = f"{self.base_url}/api/cache/latest"

            if branch:
                url = f"{url}?{urlencode({'branch': branch})}"

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self._get_headers())

                if not response.is_success:
                    return None

                data = response.json()

                # Extract the data we need for last-failed command
                if data and data.get("data") and data["data"].get("cache"):
                    return {
                        "cacheId": data["data"].get("cacheId", "unknown"),
                        "failures": data["data"]["cache"].get("failures", []),
                        "branch": data["data"]["cache"].get("branch", "unknown"),
                        "repository": data["data"]["cache"].get("repository", "unknown"),
                    }

                return None
        except Exception:
            return None
