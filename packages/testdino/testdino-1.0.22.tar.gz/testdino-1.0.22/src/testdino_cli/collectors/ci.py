"""CI metadata collector

Official documentation for CI/CD environment variables:
- GitHub Actions: https://docs.github.com/en/actions/reference/workflows-and-actions/variables
- CircleCI: https://circleci.com/docs/reference/variables/
- GitLab CI: https://docs.gitlab.com/ci/variables/predefined_variables/
- Jenkins: https://devopsqa.wordpress.com/2019/11/19/list-of-available-jenkins-environment-variables/
- Azure DevOps: https://learn.microsoft.com/en-us/azure/devops/pipelines/build/variables
"""

import os
import platform
import sys
from dataclasses import dataclass
from typing import Dict
from urllib.parse import quote

from testdino_cli.utils.env import EnvironmentUtils


@dataclass
class PipelineInfo:
    """Pipeline information"""

    id: str
    name: str
    url: str


@dataclass
class BuildInfo:
    """Build information"""

    number: str
    trigger: str


@dataclass
class EnvironmentInfo:
    """Environment information"""

    name: str
    type: str
    os: str
    node: str


@dataclass
class CiMetadata:
    """CI metadata structure matching server schema"""

    provider: str
    pipeline: PipelineInfo
    build: BuildInfo
    environment: EnvironmentInfo


@dataclass
class CIProviderMetadata:
    """Internal structure for CI provider-specific metadata extraction"""

    pipeline_id: str
    pipeline_name: str
    pipeline_url: str
    build_number: str
    build_trigger: str
    environment_name: str


class CiCollector:
    """Collector for CI/CD metadata from environment variables"""

    @staticmethod
    def collect() -> CiMetadata:
        """
        Collects comprehensive CI metadata from the current environment
        Returns: Structured CI metadata including provider, pipeline, build, and environment info
        """
        provider_key = EnvironmentUtils.detect_ci_provider()
        provider = provider_key.value if provider_key else "unknown"
        metadata = CiCollector._get_provider_metadata(provider)
        system_info = CiCollector._get_system_info()

        return CiMetadata(
            provider=provider,
            pipeline=PipelineInfo(
                id=metadata.pipeline_id,
                name=metadata.pipeline_name,
                url=metadata.pipeline_url,
            ),
            build=BuildInfo(
                number=metadata.build_number, trigger=metadata.build_trigger
            ),
            environment=EnvironmentInfo(
                name=metadata.environment_name,
                type=system_info["platform"],
                os=system_info["os_release"],
                node=system_info["python_version"],
            ),
        )

    @staticmethod
    def _get_system_info() -> Dict[str, str]:
        """Extracts system information common to all CI providers"""
        return {
            "platform": platform.system() or "",
            "os_release": f"{platform.system()} {platform.release()}",
            "python_version": f"Python {sys.version.split()[0]}",
        }

    @staticmethod
    def _get_provider_metadata(provider: str) -> CIProviderMetadata:
        """Routes to the appropriate metadata extractor based on CI provider"""
        extractors = {
            "github-actions": CiCollector._get_github_actions_metadata,
            "gitlab-ci": CiCollector._get_gitlab_ci_metadata,
            "circleci": CiCollector._get_circleci_metadata,
            "jenkins": CiCollector._get_jenkins_metadata,
            "azure-devops": CiCollector._get_azure_devops_metadata,
        }

        extractor = extractors.get(provider)
        return extractor() if extractor else CiCollector._get_generic_metadata()

    @staticmethod
    def _get_github_actions_metadata() -> CIProviderMetadata:
        """Extracts GitHub Actions specific metadata"""
        env = os.environ

        server_url = env.get("GITHUB_SERVER_URL", "")
        repository = env.get("GITHUB_REPOSITORY", "")
        run_id = env.get("GITHUB_RUN_ID", "")

        pipeline_url = (
            f"{server_url}/{repository}/actions/runs/{run_id}"
            if server_url and repository and run_id
            else ""
        )

        return CIProviderMetadata(
            pipeline_id=env.get("GITHUB_RUN_ID", "unknown"),
            pipeline_name=env.get("GITHUB_WORKFLOW", "GitHub Actions"),
            pipeline_url=pipeline_url,
            build_number=env.get("GITHUB_RUN_NUMBER", "unknown"),
            build_trigger=env.get("GITHUB_EVENT_NAME", ""),
            environment_name=env.get("RUNNER_OS", "github-actions"),
        )

    @staticmethod
    def _get_gitlab_ci_metadata() -> CIProviderMetadata:
        """Extracts GitLab CI specific metadata"""
        env = os.environ

        pipeline_name = CiCollector._get_gitlab_pipeline_name()
        build_number = env.get("CI_JOB_ID") or env.get("CI_PIPELINE_IID") or "unknown"
        environment_name = (
            env.get("CI_ENVIRONMENT_NAME")
            or env.get("CI_JOB_STAGE")
            or "gitlab-ci"
        )

        return CIProviderMetadata(
            pipeline_id=env.get("CI_PIPELINE_ID", "unknown"),
            pipeline_name=pipeline_name,
            pipeline_url=env.get("CI_PIPELINE_URL", ""),
            build_number=build_number,
            build_trigger=env.get("CI_PIPELINE_SOURCE", ""),
            environment_name=environment_name,
        )

    @staticmethod
    def _get_gitlab_pipeline_name() -> str:
        """Determines GitLab pipeline name using fallback strategy"""
        env = os.environ

        pipeline_source = env.get("CI_PIPELINE_SOURCE")
        if pipeline_source:
            return f"{pipeline_source} pipeline"

        return (
            env.get("CI_COMMIT_TITLE")
            or env.get("CI_PIPELINE_NAME")
            or "GitLab Pipeline"
        )

    @staticmethod
    def _get_circleci_metadata() -> CIProviderMetadata:
        """Extracts CircleCI specific metadata"""
        env = os.environ

        build_trigger = CiCollector._get_circleci_build_trigger()
        pipeline_id = (
            env.get("CIRCLE_PIPELINE_ID") or env.get("CIRCLE_BUILD_NUM") or "unknown"
        )
        job_name = env.get("CIRCLE_JOB", "CircleCI Pipeline")

        return CIProviderMetadata(
            pipeline_id=pipeline_id,
            pipeline_name=job_name,
            pipeline_url=env.get("CIRCLE_BUILD_URL", ""),
            build_number=env.get("CIRCLE_BUILD_NUM", "unknown"),
            build_trigger=build_trigger,
            environment_name=env.get("CIRCLE_JOB", "circleci"),
        )

    @staticmethod
    def _get_circleci_build_trigger() -> str:
        """Determines CircleCI build trigger based on environment variables"""
        env = os.environ

        if env.get("CIRCLE_TAG"):
            return "tag"

        if env.get("CIRCLE_PR_NUMBER") or env.get("CIRCLE_PULL_REQUEST"):
            return "pr"

        return "push"

    @staticmethod
    def _get_jenkins_metadata() -> CIProviderMetadata:
        """Extracts Jenkins specific metadata"""
        env = os.environ

        return CIProviderMetadata(
            pipeline_id=env.get("BUILD_ID", "unknown"),
            pipeline_name=env.get("JOB_NAME", "Jenkins Pipeline"),
            pipeline_url=env.get("BUILD_URL", ""),
            build_number=env.get("BUILD_NUMBER", "unknown"),
            build_trigger=env.get("BUILD_CAUSE", ""),
            environment_name=env.get("NODE_NAME", "jenkins"),
        )

    @staticmethod
    def _get_azure_devops_metadata() -> CIProviderMetadata:
        """Extracts Azure DevOps specific metadata"""
        env = os.environ

        pipeline_url = CiCollector._build_azure_devops_pipeline_url()
        environment_name = CiCollector._get_azure_devops_environment_name()

        return CIProviderMetadata(
            pipeline_id=env.get("BUILD_BUILDID", "unknown"),
            pipeline_name=env.get("BUILD_DEFINITIONNAME", "Azure Pipeline"),
            pipeline_url=pipeline_url,
            build_number=env.get("BUILD_BUILDNUMBER", "unknown"),
            build_trigger=env.get("BUILD_REASON", ""),
            environment_name=environment_name,
        )

    @staticmethod
    def _build_azure_devops_pipeline_url() -> str:
        """Constructs Azure DevOps pipeline URL from environment variables"""
        env = os.environ

        server_uri = env.get("SYSTEM_TEAMFOUNDATIONSERVERURI")
        team_project = env.get("SYSTEM_TEAMPROJECT")
        build_id = env.get("BUILD_BUILDID")

        if not server_uri or not team_project or not build_id:
            return ""

        try:
            base_url = server_uri.rstrip("/")
            encoded_project = quote(team_project)
            return f"{base_url}/{encoded_project}/_build/results?buildId={build_id}"
        except Exception:
            return ""

    @staticmethod
    def _get_azure_devops_environment_name() -> str:
        """Determines Azure DevOps environment name with fallback strategy"""
        env = os.environ

        return (
            env.get("SYSTEM_STAGENAME")
            or env.get("AGENT_JOBNAME")
            or env.get("AGENT_MACHINENAME")
            or "azure-devops"
        )

    @staticmethod
    def _get_generic_metadata() -> CIProviderMetadata:
        """Fallback metadata extraction for unknown or generic CI providers"""
        env = os.environ

        build_number = (
            env.get("CI_BUILD_NUMBER") or env.get("BUILD_NUMBER") or "unknown"
        )

        return CIProviderMetadata(
            pipeline_id=env.get("CI_PIPELINE_ID", "unknown"),
            pipeline_name=env.get("CI_PIPELINE_NAME", "CI Pipeline"),
            pipeline_url=env.get("CI_PIPELINE_URL", ""),
            build_number=build_number,
            build_trigger=env.get("CI_PIPELINE_SOURCE", ""),
            environment_name="local",
        )
