"""
Validation utilities for configuration and input
"""

import re
import sys
from dataclasses import dataclass
from typing import Any, Generic, List, Optional, TypeVar
from urllib.parse import urlparse

from pydantic import BaseModel, ValidationError as PydanticValidationError

from testdino_cli.types import ConfigurationError, ValidationError

T = TypeVar("T")


@dataclass
class ValidationResult(Generic[T]):
    """Validation result type"""

    success: bool
    data: Optional[T] = None
    errors: Optional[List[str]] = None


class ValidationUtils:
    """Configuration validation utilities"""

    @staticmethod
    def validate_schema(
        schema: type[BaseModel], data: Any, context: str
    ) -> ValidationResult[Any]:
        """Validate data against a Pydantic schema with user-friendly error messages"""
        try:
            validated = schema.model_validate(data)
            return ValidationResult(success=True, data=validated)
        except PydanticValidationError as error:
            errors = []
            for err in error.errors():
                path = ".".join(str(p) for p in err["loc"]) if err["loc"] else "root"
                errors.append(f"{path}: {err['msg']}")
            return ValidationResult(success=False, errors=errors)
        except Exception as error:
            return ValidationResult(
                success=False,
                errors=[f"Unexpected validation error in {context}: {str(error)}"],
            )

    @staticmethod
    def validate_or_throw(schema: type[BaseModel], data: Any, context: str) -> Any:
        """Validate and throw appropriate error with context"""
        result = ValidationUtils.validate_schema(schema, data, context)

        if not result.success:
            raise ValidationError(
                f"Validation failed for {context}: {', '.join(result.errors or [])}"
            )

        return result.data

    @staticmethod
    def validate_api_token(token: str) -> None:
        """Validate API token format with detailed feedback"""
        if not token:
            raise ValidationError("API token is required")

        if len(token) < 10:
            raise ValidationError("API token is too short")

        token_pattern = re.compile(r"^trx_(development|staging|production)_[a-f0-9]{64}$")
        if not token_pattern.match(token):
            parts = token.split("_")

            if len(parts) != 3:
                raise ValidationError(
                    "API token must have 3 parts separated by underscores: trx_{environment}_{key}"
                )

            prefix = parts[0]
            environment = parts[1]
            key = parts[2]

            if prefix != "trx":
                raise ValidationError(
                    f'API token must start with "trx", found "{prefix}"'
                )

            if environment not in ["development", "staging", "production"]:
                raise ValidationError(
                    f'Invalid environment "{environment}". Must be: development, staging, or production'
                )

            if not re.match(r"^[a-f0-9]{64}$", key):
                raise ValidationError(
                    "API token key must be 64 lowercase hexadecimal characters"
                )

    @staticmethod
    def validate_url(url: str, context: str) -> None:
        """Validate URL format with helpful feedback"""
        if not url:
            raise ValidationError(f"{context} URL is required")

        try:
            parsed = urlparse(url)

            if parsed.scheme not in ["http", "https"]:
                raise ValidationError(
                    f"{context} URL must use HTTP or HTTPS protocol, found: {parsed.scheme}"
                )

            if not parsed.hostname:
                raise ValidationError(f"{context} URL must have a valid hostname")

        except ValidationError:
            raise
        except Exception:
            raise ValidationError(f"Invalid {context} URL format: {url}")

    @staticmethod
    def validate_file_path(path: str, context: str) -> None:
        """Validate file path exists and is accessible"""
        if not path:
            raise ValidationError(f"{context} path is required")

        if ".." in path:
            raise ValidationError(
                f"{context} path cannot contain parent directory references (..)"
            )

        if path.startswith("/") and not sys.platform.startswith("win"):
            print(f"⚠️  Using absolute path for {context}: {path}")

    @staticmethod
    def validate_python_version(required_version: str = "3.9.0") -> None:
        """Validate Python version meets minimum requirement.

        Args:
            required_version: Minimum required Python version (default: 3.9.0)

        Raises:
            ConfigurationError: If current Python version is below required version
        """
        current_version = (
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
        current = ValidationUtils._parse_version(current_version)
        required = ValidationUtils._parse_version(required_version)

        if ValidationUtils._compare_versions(current, required) < 0:
            raise ConfigurationError(
                f"Python {required_version} or higher is required. "
                f"Current version: {current_version}"
            )

    @staticmethod
    def _parse_version(version: str) -> tuple[int, int, int]:
        """Parse semantic version string"""
        parts = [int(p) for p in version.split(".")]
        return (parts[0] if len(parts) > 0 else 0, parts[1] if len(parts) > 1 else 0, parts[2] if len(parts) > 2 else 0)

    @staticmethod
    def _compare_versions(
        a: tuple[int, int, int], b: tuple[int, int, int]
    ) -> int:
        """
        Compare two semantic versions
        Returns: -1 if a < b, 0 if a == b, 1 if a > b
        """
        for i in range(3):
            if a[i] < b[i]:
                return -1
            if a[i] > b[i]:
                return 1
        return 0

    @staticmethod
    def validate_env_var_name(name: str) -> None:
        """Validate environment variable name"""
        if not name:
            raise ValidationError("Environment variable name is required")

        if not re.match(r"^[A-Z][A-Z0-9_]*$", name):
            raise ValidationError(
                f'Environment variable name "{name}" must be uppercase letters, numbers, and underscores only'
            )

    @staticmethod
    def validate_file_size(size: int, max_size: int, filename: str) -> None:
        """Sanitize and validate file size"""
        if size < 0:
            raise ValidationError(f"Invalid file size for {filename}: {size}")

        if size > max_size:
            size_mb = round(size / 1024 / 1024)
            max_size_mb = round(max_size / 1024 / 1024)

            raise ValidationError(
                f"File {filename} is too large: {size_mb}MB (max: {max_size_mb}MB)"
            )

    @staticmethod
    def validate_timeout(timeout: int) -> None:
        """Validate timeout value"""
        if timeout <= 0:
            raise ValidationError("Timeout must be greater than 0")

        if timeout > 300000:  # 5 minutes
            print(f"⚠️  Large timeout value: {timeout}ms ({timeout / 1000}s)")

    @staticmethod
    def validate_retry_count(retries: int) -> None:
        """Validate retry count"""
        if retries < 0:
            raise ValidationError("Retry count cannot be negative")

        if retries > 10:
            print(f"⚠️  High retry count: {retries} (this may cause long delays)")
