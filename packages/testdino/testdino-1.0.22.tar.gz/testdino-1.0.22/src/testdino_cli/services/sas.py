"""Service to request and manage Azure SAS tokens from TestDino API"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import httpx

from testdino_cli.config.index import Config
from testdino_cli.types import AuthenticationError, NetworkError
from testdino_cli.version import VERSION

# Endpoint for SAS token
SAS_ENDPOINT = "/api/storage/token"


@dataclass
class UploadInstructions:
    """Upload instructions from SAS response"""

    base_url: str
    path_prefix: str
    allowed_file_types: List[str]
    max_file_size: int
    example_upload: Dict[str, Any]


@dataclass
class SasTokenResponse:
    """Response structure for SAS token request"""

    token_id: str
    sas_token: str
    container_url: str
    blob_path: str
    unique_id: str
    expires_at: str
    max_size: int
    permissions: List[str]
    upload_instructions: UploadInstructions


class SasTokenService:
    """Service to request and manage Azure SAS tokens from TestDino API"""

    def __init__(self, config: Config):
        self.base_url = str(config.api_url)
        self.api_key = config.token

    def _get_headers(self) -> Dict[str, str]:
        """Headers to include on every SAS token request"""
        return {
            "Content-Type": "application/json",
            "User-Agent": f"testdino/{VERSION}",
            "X-API-Key": self.api_key,
        }

    async def request_sas_token(self) -> SasTokenResponse:
        """Request a SAS token from TestDino API using POST method"""
        url = f"{self.base_url}{SAS_ENDPOINT}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    url, headers=self._get_headers(), json={}
                )
            except httpx.RequestError as error:
                raise NetworkError(f"Network error requesting SAS token: {str(error)}")

            # Handle HTTP error responses
            if not response.is_success:
                await self._handle_sas_error(response)

            # Parse JSON response
            try:
                data = response.json()
            except Exception as error:
                raise NetworkError(f"Failed to parse SAS token response: {str(error)}")

            # Validate and extract SAS token data
            return self._validate_sas_response(data)

    async def _handle_sas_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses with detailed error messages"""
        try:
            error_body = response.text
        except Exception:
            error_body = "Unable to read error response"

        status = response.status_code

        if status == 401:
            raise AuthenticationError("Invalid API key for SAS token request")
        elif status == 403:
            raise AuthenticationError(
                "API key does not have permission to request SAS tokens"
            )
        elif status == 400:
            raise NetworkError(f"Bad SAS token request: {error_body}")
        elif status == 404:
            raise NetworkError(
                f"SAS token endpoint not found ({status}): {error_body}"
            )
        elif status == 429:
            raise NetworkError("Rate limit exceeded for SAS token requests")
        elif status in (500, 502, 503, 504):
            raise NetworkError(
                f"Server error requesting SAS token ({status}) - please try again later"
            )
        else:
            raise NetworkError(
                f"SAS token request failed: HTTP {status} - {error_body}"
            )

    def _validate_sas_response(self, data: Any) -> SasTokenResponse:
        """Validate and parse the SAS token response"""
        if not data or not isinstance(data, dict):
            raise NetworkError(
                "Invalid SAS token response format - expected JSON object"
            )

        # Check for success wrapper format
        if data.get("success") is not True or not isinstance(data.get("data"), dict):
            message = data.get("message", "Unknown error")
            raise NetworkError(f"SAS token request failed: {message}")

        sas_data = data["data"]

        # Validate required fields
        required_fields = [
            "tokenId",
            "sasToken",
            "containerUrl",
            "blobPath",
            "uniqueId",
            "expiresAt",
            "uploadInstructions",
        ]
        missing_fields = [f for f in required_fields if f not in sas_data]

        if missing_fields:
            raise NetworkError(
                f"SAS token response missing required fields: {', '.join(missing_fields)}"
            )

        # Validate field types
        if not isinstance(sas_data["tokenId"], str):
            raise NetworkError("SAS token response: tokenId must be a string")

        if not isinstance(sas_data["sasToken"], str):
            raise NetworkError("SAS token response: sasToken must be a string")

        if not isinstance(sas_data["containerUrl"], str):
            raise NetworkError("SAS token response: containerUrl must be a string")

        if not isinstance(sas_data["expiresAt"], str):
            raise NetworkError("SAS token response: expiresAt must be a string")

        # Validate container URL format
        try:
            from urllib.parse import urlparse

            result = urlparse(sas_data["containerUrl"])
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL")
        except Exception:
            raise NetworkError(
                f"Invalid containerUrl format: {sas_data['containerUrl']}"
            )

        # Validate upload instructions
        if not isinstance(sas_data.get("uploadInstructions"), dict):
            raise NetworkError(
                "SAS token response: uploadInstructions must be an object"
            )

        instructions = sas_data["uploadInstructions"]
        if not instructions.get("baseUrl") or not instructions.get("pathPrefix"):
            raise NetworkError(
                "SAS token response: uploadInstructions missing baseUrl or pathPrefix"
            )

        # Prepare example upload
        example_upload = {"method": "PUT", "url": "", "headers": {}}
        if isinstance(instructions.get("exampleUpload"), dict):
            eu = instructions["exampleUpload"]
            if isinstance(eu.get("method"), str):
                example_upload["method"] = eu["method"]
            if isinstance(eu.get("url"), str):
                example_upload["url"] = eu["url"]
            if isinstance(eu.get("headers"), dict):
                example_upload["headers"] = eu["headers"]

        # Build response
        return SasTokenResponse(
            token_id=sas_data["tokenId"],
            sas_token=sas_data["sasToken"],
            container_url=sas_data["containerUrl"],
            blob_path=sas_data["blobPath"],
            unique_id=sas_data["uniqueId"],
            expires_at=sas_data["expiresAt"],
            max_size=sas_data.get("maxSize", 2147483648),  # 2GB default
            permissions=sas_data.get("permissions", []),
            upload_instructions=UploadInstructions(
                base_url=instructions["baseUrl"],
                path_prefix=instructions["pathPrefix"],
                allowed_file_types=instructions.get("allowedFileTypes", []),
                max_file_size=instructions.get("maxFileSize", sas_data.get("maxSize", 2147483648)),
                example_upload=example_upload,
            ),
        )

    def is_token_expired(self, sas_response: SasTokenResponse) -> bool:
        """Check if SAS token is expired"""
        try:
            expiration_date = datetime.fromisoformat(
                sas_response.expires_at.replace("Z", "+00:00")
            )
            now = datetime.now(expiration_date.tzinfo)

            # Add small buffer (5 minutes) to account for clock skew
            buffer_seconds = 5 * 60
            from datetime import timedelta

            return (expiration_date - timedelta(seconds=buffer_seconds)) <= now
        except Exception:
            # If we can't parse the date, assume it's expired for safety
            return True

    def get_time_until_expiry(self, sas_response: SasTokenResponse) -> int:
        """Get time until SAS token expires (in minutes)"""
        try:
            expiration_date = datetime.fromisoformat(
                sas_response.expires_at.replace("Z", "+00:00")
            )
            now = datetime.now(expiration_date.tzinfo)
            diff = expiration_date - now
            return int(diff.total_seconds() / 60)  # Convert to minutes
        except Exception:
            return 0
