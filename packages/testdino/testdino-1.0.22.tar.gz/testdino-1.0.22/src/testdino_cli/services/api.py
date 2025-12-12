"""API client for communicating with the TestDino API"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

from testdino_cli.config.index import Config
from testdino_cli.types import AuthenticationError, NetworkError
from testdino_cli.version import VERSION

# Upload endpoint relative to base API URL
UPLOAD_ENDPOINT = "/api/reports/playwright"


@dataclass
class ReportUploadResponse:
    """Response payload from the TestDino API when uploading a report"""

    test_run_id: str
    organization_id: Optional[str] = None
    project_id: Optional[str] = None
    view_url: Optional[str] = None
    status: Optional[str] = None
    extra: Dict[str, Any] = None  # type: ignore

    def __post_init__(self) -> None:
        if self.extra is None:
            self.extra = {}


class ApiClient:
    """Client for communicating with the TestDino API"""

    def __init__(self, config: Config):
        self.base_url = str(config.api_url)
        self.api_key = config.token

    def _get_headers(self) -> Dict[str, str]:
        """Headers to include on every API request"""
        return {
            "Content-Type": "application/json",
            "User-Agent": f"testdino/{VERSION}",
            "X-API-Key": self.api_key,
        }

    async def upload_report(self, payload: Any) -> ReportUploadResponse:
        """Upload a JSON payload to the TestDino API with enhanced error handling"""
        url = f"{self.base_url}{UPLOAD_ENDPOINT}"

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(
                    url, headers=self._get_headers(), json=payload
                )
            except httpx.RequestError as error:
                raise NetworkError(
                    f"Failed to connect to TestDino API: {str(error)}"
                )

            # Handle HTTP error responses
            if not response.is_success:
                await self._handle_http_error(response)

            # Parse JSON response
            try:
                json_data = response.json()
            except Exception as error:
                raise NetworkError(f"Invalid JSON response from API: {str(error)}")

            # Extract response data
            return self._parse_upload_response(json_data)

    async def _handle_http_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses with detailed error messages"""
        try:
            error_body = response.text
        except Exception:
            error_body = "Unable to read error response"

        status = response.status_code

        if status == 401:
            raise AuthenticationError("Invalid API key or unauthorized access")
        elif status == 403:
            raise AuthenticationError(
                "API key does not have permission to upload reports"
            )
        elif status == 400:
            raise NetworkError(f"Bad request - Invalid data format: {error_body}")
        elif status == 413:
            raise NetworkError(
                "Report payload too large - consider uploading without HTML/traces"
            )
        elif status == 429:
            raise NetworkError("Rate limit exceeded - please wait before retrying")
        elif status in (500, 502, 503, 504):
            raise NetworkError(
                f"TestDino API server error ({status}) - please try again later"
            )
        else:
            raise NetworkError(f"HTTP {status}: {error_body or response.reason_phrase}")

    def _parse_upload_response(self, json_data: Any) -> ReportUploadResponse:
        """Parse and validate the upload response"""
        if not json_data or not isinstance(json_data, dict):
            raise NetworkError("Invalid response format - expected JSON object")

        # Handle different response structures
        response_data: Dict[str, Any] = {}

        # Check for direct response
        if "testRunId" in json_data:
            response_data = json_data
        # Check for wrapped response
        elif (
            "data" in json_data
            and isinstance(json_data["data"], dict)
            and "testRunId" in json_data["data"]
        ):
            response_data = json_data["data"]
        # Check for success wrapper
        elif (
            "success" in json_data
            and "result" in json_data
            and isinstance(json_data["result"], dict)
            and "testRunId" in json_data["result"]
        ):
            response_data = json_data["result"]
        else:
            raise NetworkError(f"Unexpected API response structure: {json_data}")

        # Validate required fields
        if not response_data.get("testRunId") or not isinstance(
            response_data["testRunId"], str
        ):
            raise NetworkError("API response missing required testRunId field")

        # Build response object
        extra_fields = {
            k: v
            for k, v in response_data.items()
            if k not in ["testRunId", "organizationId", "projectId", "viewUrl", "status"]
        }

        return ReportUploadResponse(
            test_run_id=response_data["testRunId"],
            organization_id=response_data.get("organizationId"),
            project_id=response_data.get("projectId"),
            view_url=response_data.get("viewUrl"),
            status=response_data.get("status"),
            extra=extra_fields,
        )

    async def health_check(self) -> bool:
        """Health check endpoint to verify API connectivity"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/health",
                    headers={"User-Agent": f"testdino/{VERSION}"},
                )
                return response.is_success
        except Exception:
            return False
