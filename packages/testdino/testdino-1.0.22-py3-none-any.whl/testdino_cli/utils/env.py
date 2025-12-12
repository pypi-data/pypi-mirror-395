"""
Environment detection and validation utilities
"""

import os
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, HttpUrl

from testdino_cli.types import ConfigurationError, string_to_boolean


class EnvVars(BaseModel):
    """Environment variable schema with validation"""

    # Core configuration - Only 3 supported environment variables
    TESTDINO_RUNTIME: Optional[str] = Field(default=None, pattern="^(development|staging|production|test)$")
    TESTDINO_API_URL: Optional[HttpUrl] = None
    TESTDINO_TOKEN: Optional[str] = None

    # CI/CD detection variables (auto-detected, not user-configurable)
    CI: Optional[str] = None
    GITHUB_ACTIONS: Optional[str] = None
    GITLAB_CI: Optional[str] = None
    JENKINS_URL: Optional[str] = None
    AZURE_HTTP_USER_AGENT: Optional[str] = None
    CIRCLECI: Optional[str] = None

    model_config = {"extra": "allow"}  # Allow extra env vars


class EnvironmentType(str, Enum):
    """Environment type detection"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class CIProvider(str, Enum):
    """CI/CD provider detection"""

    GITHUB_ACTIONS = "github-actions"
    GITLAB_CI = "gitlab-ci"
    JENKINS = "jenkins"
    AZURE_DEVOPS = "azure-devops"
    CIRCLECI = "circleci"
    UNKNOWN = "unknown"


class EnvironmentUtils:
    """Environment utilities class"""

    _env_cache: Optional[EnvVars] = None

    @classmethod
    def get_environment(cls) -> EnvVars:
        """Get and validate environment variables with caching"""
        if cls._env_cache:
            return cls._env_cache

        try:
            cls._env_cache = EnvVars(**os.environ)
            return cls._env_cache
        except Exception as error:
            raise ConfigurationError(
                f"Failed to validate environment: {error}",
                error if isinstance(error, Exception) else None,
            )

    @classmethod
    def clear_cache(cls) -> None:
        """Clear environment cache (useful for testing)"""
        cls._env_cache = None

    @classmethod
    def detect_environment_type(cls) -> EnvironmentType:
        """Detect current environment type"""
        env = cls.get_environment()

        if env.TESTDINO_RUNTIME == "development":
            return EnvironmentType.DEVELOPMENT
        elif env.TESTDINO_RUNTIME == "staging":
            return EnvironmentType.STAGING
        elif env.TESTDINO_RUNTIME == "production":
            return EnvironmentType.PRODUCTION
        elif env.TESTDINO_RUNTIME == "test":
            return EnvironmentType.TEST
        else:
            # Default to production for safety
            return EnvironmentType.PRODUCTION

    @classmethod
    def detect_ci_provider(cls) -> CIProvider:
        """Detect CI/CD provider"""
        env = cls.get_environment()

        if env.GITHUB_ACTIONS:
            return CIProvider.GITHUB_ACTIONS

        if env.GITLAB_CI:
            return CIProvider.GITLAB_CI

        if env.JENKINS_URL:
            return CIProvider.JENKINS

        if env.AZURE_HTTP_USER_AGENT:
            return CIProvider.AZURE_DEVOPS

        if env.CIRCLECI:
            return CIProvider.CIRCLECI

        return CIProvider.UNKNOWN

    @classmethod
    def is_ci(cls) -> bool:
        """Check if running in CI environment"""
        env = cls.get_environment()
        return string_to_boolean(env.CI) or cls.detect_ci_provider() != CIProvider.UNKNOWN

    @classmethod
    def is_development(cls) -> bool:
        """Check if in development mode"""
        return cls.detect_environment_type() == EnvironmentType.DEVELOPMENT

    @classmethod
    def is_production(cls) -> bool:
        """Check if in production mode"""
        return cls.detect_environment_type() == EnvironmentType.PRODUCTION

    @classmethod
    def is_test(cls) -> bool:
        """Check if in test mode"""
        return cls.detect_environment_type() == EnvironmentType.TEST

    @classmethod
    def get_string_env(cls, key: str, default_value: Optional[str] = None) -> Optional[str]:
        """Get string value from environment variable"""
        env = cls.get_environment()
        return getattr(env, key, default_value)

    @classmethod
    def get_environment_summary(cls) -> Dict[str, Any]:
        """Get environment summary for debugging"""
        env = cls.get_environment()

        return {
            "type": cls.detect_environment_type().value,
            "ci": cls.is_ci(),
            "provider": cls.detect_ci_provider().value,
            "runtime": env.TESTDINO_RUNTIME,
            "hasToken": bool(env.TESTDINO_TOKEN),
            "hasApiUrl": bool(env.TESTDINO_API_URL),
        }
