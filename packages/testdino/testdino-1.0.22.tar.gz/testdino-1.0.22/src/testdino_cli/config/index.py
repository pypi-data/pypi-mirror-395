"""
Configuration management with environment detection and validation
"""

import os
from typing import Any, Callable, Dict, Optional, TypeVar

from dotenv import load_dotenv
from pydantic import ValidationError as PydanticValidationError

from testdino_cli.types import (
    CLIOptions,
    Config,
    ConfigurationError,
    ValidationError,
    string_to_boolean,
)
from testdino_cli.utils.env import CIProvider, EnvironmentType, EnvironmentUtils
from testdino_cli.utils.validation import ValidationUtils

# Load environment variables
load_dotenv()

T = TypeVar("T")


class DefaultConfig:
    """Default configuration values"""

    # API URLs by environment
    API_URLS = {
        EnvironmentType.PRODUCTION: "https://api.testdino.com",
        EnvironmentType.STAGING: "https://staging-api.testdino.com",
        EnvironmentType.DEVELOPMENT: "http://localhost:3000",
        EnvironmentType.TEST: "http://localhost:3000",
    }

    # Default options
    UPLOAD_IMAGES = False
    UPLOAD_VIDEOS = False
    UPLOAD_HTML = False
    UPLOAD_TRACES = False
    UPLOAD_FILES = False
    UPLOAD_FULL_JSON = False
    VERBOSE = False

    # Performance settings
    TIMEOUT_MS = 60000  # 60 seconds
    RETRY_COUNT = 3
    MAX_FILE_SIZE_MB = 100
    BATCH_SIZE = 5
    MAX_CONCURRENT_UPLOADS = 10
    UPLOAD_TIMEOUT = 60000


class EnvironmentDetectorClass:
    """Environment detection utilities"""

    def get_environment_type(self) -> EnvironmentType:
        """Determine current environment type"""
        return EnvironmentUtils.detect_environment_type()

    def is_development(self) -> bool:
        """Determine if we're in development mode"""
        return EnvironmentUtils.is_development()

    def is_production(self) -> bool:
        """Determine if we're in production mode"""
        return EnvironmentUtils.is_production()

    def is_test(self) -> bool:
        """Determine if we're in test mode"""
        return EnvironmentUtils.is_test()

    def is_ci(self) -> bool:
        """Check if running in CI environment"""
        return EnvironmentUtils.is_ci()

    def get_ci_provider(self) -> CIProvider:
        """Get CI provider information"""
        return EnvironmentUtils.detect_ci_provider()

    def get_api_url(self) -> str:
        """Get the appropriate API URL based on environment"""
        env_type = self.get_environment_type()

        # Check for explicit override (always allow override)
        override = EnvironmentUtils.get_string_env("TESTDINO_API_URL")
        if override:
            return override

        # Use environment-specific default
        return DefaultConfig.API_URLS[env_type]

    def get_environment_info(self) -> Dict[str, Any]:
        """Get environment summary for debugging"""
        return {
            **EnvironmentUtils.get_environment_summary(),
            "apiUrl": self.get_api_url(),
            "isCI": self.is_ci(),
            "ciProvider": self.get_ci_provider().value,
        }


class ConfigLoader:
    """Enhanced configuration loader and validator"""

    def _validate_token(self, token: str) -> None:
        """Validate API token format and environment compatibility"""
        ValidationUtils.validate_api_token(token)

        # Extract environment from token
        token_env = token.split("_")[1]
        EnvironmentDetector.get_environment_type()

        # Warn about environment mismatches in development
        if EnvironmentDetector.is_development() and token_env != "development":
            print(
                f"⚠️  Using {token_env} token in development environment. "
                "Consider using a development token for local testing."
            )

    def _resolve_config_value(
        self,
        cli_value: Optional[T],
        env_key: str,
        default_value: T,
        converter: Optional[Callable[[str], T]] = None,
    ) -> T:
        """Resolve configuration values with proper precedence"""
        # CLI option has highest precedence
        if cli_value is not None:
            return cli_value

        # Environment variable is second
        env_value = EnvironmentUtils.get_string_env(env_key)
        if env_value is not None:
            if converter:
                return converter(env_value)
            # For boolean values
            if isinstance(default_value, bool):
                return string_to_boolean(env_value)  # type: ignore
            return env_value  # type: ignore

        # Default value is last
        return default_value

    def create_cache_config(self, token: Optional[str] = None) -> Config:
        """Create configuration specifically for cache command.

        Matches TypeScript CommandManager.createConfigForCache() pattern.
        """
        # Resolve token from CLI option or environment variable
        resolved_token = token or os.environ.get("TESTDINO_TOKEN", "")

        if not resolved_token:
            raise ValidationError(
                "API token is required. Provide via --token flag or TESTDINO_TOKEN environment variable."
            )

        # Create minimal config for cache command
        return Config(
            api_url=os.environ.get("TESTDINO_API_URL", "https://api.testdino.com"),
            token=resolved_token,
            upload_images=False,
            upload_videos=False,
            upload_html=False,
            upload_traces=False,
            upload_files=False,
            upload_full_json=False,
            verbose=False,
            batch_size=5,
            max_concurrent_uploads=10,
            upload_timeout=60000,
            retry_attempts=3,
        )

    def create_config(self, options: CLIOptions) -> Config:
        """Create configuration from CLI options with environment fallbacks"""
        # Token resolution: CLI > ENV > error
        token = self._resolve_config_value(options.token, "TESTDINO_TOKEN", "")

        if not token:
            raise ConfigurationError(
                "API token is required. Provide via --token flag or TESTDINO_TOKEN environment variable."
            )

        # Validate token format
        self._validate_token(token)

        # Build configuration with only CLI options (no environment variable fallbacks)
        config_data = {
            "api_url": EnvironmentDetector.get_api_url(),
            "token": token,
            "upload_images": options.upload_images or DefaultConfig.UPLOAD_IMAGES,
            "upload_videos": options.upload_videos or DefaultConfig.UPLOAD_VIDEOS,
            "upload_html": options.upload_html or DefaultConfig.UPLOAD_HTML,
            "upload_traces": options.upload_traces or DefaultConfig.UPLOAD_TRACES,
            "upload_files": options.upload_files or DefaultConfig.UPLOAD_FILES,
            "upload_full_json": options.upload_full_json or DefaultConfig.UPLOAD_FULL_JSON,
            "verbose": options.verbose or DefaultConfig.VERBOSE,
            # Performance settings use defaults only
            "batch_size": DefaultConfig.BATCH_SIZE,
            "max_concurrent_uploads": DefaultConfig.MAX_CONCURRENT_UPLOADS,
            "upload_timeout": DefaultConfig.UPLOAD_TIMEOUT,
            "retry_attempts": DefaultConfig.RETRY_COUNT,
        }

        # Validate the final configuration
        try:
            validated_config = Config(**config_data)

            # Log configuration summary in verbose mode
            if validated_config.verbose:
                self._log_configuration_summary(validated_config, options)

            return validated_config
        except PydanticValidationError as error:
            issues = [f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in error.errors()]
            raise ConfigurationError(
                f"Invalid configuration: {', '.join(issues)}", error
            )
        except Exception as error:
            raise ConfigurationError("Configuration validation failed", error)

    def _log_configuration_summary(self, config: Config, options: CLIOptions) -> None:
        """Log configuration summary for debugging"""
        env_info = EnvironmentDetector.get_environment_info()

        print("🔧 Configuration Summary:")
        print(f"   Environment: {env_info['type']}")
        print(
            f"   CI/CD: {'Yes (' + env_info['ciProvider'] + ')' if env_info['isCI'] else 'No'}"
        )
        print(f"   API URL: {config.api_url}")
        print(f"   Report Directory: {options.report_directory}")
        print(f"   Upload Images: {'Yes' if config.upload_images else 'No'}")
        print(f"   Upload Videos: {'Yes' if config.upload_videos else 'No'}")
        print(f"   Upload HTML: {'Yes' if config.upload_html else 'No'}")
        print(f"   Upload Traces: {'Yes' if config.upload_traces else 'No'}")
        print(f"   Upload Files: {'Yes' if config.upload_files else 'No'}")
        print(f"   Upload Full JSON: {'Yes' if config.upload_full_json else 'No'}")

        if options.json_report:
            print(f"   Custom JSON Report: {options.json_report}")
        if options.html_report:
            print(f"   Custom HTML Report: {options.html_report}")
        if options.trace_dir:
            print(f"   Custom Trace Dir: {options.trace_dir}")

    def get_runtime_config(self) -> Dict[str, Any]:
        """Get runtime configuration with validation"""
        # Use only default values - no environment variable overrides
        timeout = DefaultConfig.TIMEOUT_MS
        retry_count = DefaultConfig.RETRY_COUNT
        max_file_size_mb = DefaultConfig.MAX_FILE_SIZE_MB
        log_level = "info"

        # Validate runtime values
        ValidationUtils.validate_timeout(timeout)
        ValidationUtils.validate_retry_count(retry_count)

        return {
            "timeout": timeout,
            "retryCount": retry_count,
            "maxFileSize": max_file_size_mb * 1024 * 1024,  # Convert MB to bytes
            "logLevel": log_level,
        }

    def validate_environment(self) -> None:
        """Validate environment for CLI operation"""
        try:
            # Validate environment variables
            EnvironmentUtils.get_environment()

            # Check Python version meets minimum requirement
            ValidationUtils.validate_python_version("3.9.0")

            # Validate API URL if present
            api_url = EnvironmentDetector.get_api_url()
            ValidationUtils.validate_url(api_url, "API")

        except (ConfigurationError, ValidationError):
            raise
        except Exception as error:
            raise ConfigurationError("Environment validation failed", error)


# Global configuration instances
config_loader = ConfigLoader()
EnvironmentDetector = EnvironmentDetectorClass()

__all__ = [
    "config_loader",
    "ConfigLoader",
    "EnvironmentDetector",
    "EnvironmentUtils",
    "DefaultConfig",
]
