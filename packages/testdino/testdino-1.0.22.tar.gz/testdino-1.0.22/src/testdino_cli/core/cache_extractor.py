"""Test failure extraction for cache functionality

This module extracts test failure data from Playwright reports for caching
"""

import hashlib
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from testdino_cli.collectors.ci import CiCollector
from testdino_cli.collectors.git import GitCollector


@dataclass
class CacheIdInfo:
    """Cache identification information"""

    cache_id: str
    pipeline_id: str
    commit: str
    branch: str
    repository: str
    ci_provider: str
    source: str


class CacheIdDetector:
    """Service for detecting and generating cache IDs"""

    @staticmethod
    async def detect_cache_id(
        custom_cache_id: Optional[str] = None,
        custom_branch: Optional[str] = None,
        custom_commit: Optional[str] = None,
    ) -> CacheIdInfo:
        """
        Detect cache ID and related metadata from environment
        Format: <ciProvider>_<repoName>_<branch>
        """
        try:
            # Check for custom cache ID
            env_custom_id = os.getenv("TESTDINO_CACHE_ID")
            if custom_cache_id or env_custom_id:
                final_custom_id = custom_cache_id or env_custom_id or "unknown"

                # Still need git/ci metadata
                metadata = await CacheIdDetector._collect_metadata()

                return CacheIdInfo(
                    cache_id=final_custom_id,
                    pipeline_id=metadata["pipelineId"],
                    commit=custom_commit or metadata["commit"],
                    branch=custom_branch or metadata["branch"],
                    repository=metadata["repository"],
                    ci_provider=metadata["ciProvider"],
                    source="custom",
                )

            # Auto-detect cache ID from environment
            return await CacheIdDetector._generate_cache_id(
                custom_branch, custom_commit
            )

        except Exception as error:
            print(
                f"⚠️  Cache ID detection failed: {error}"
            )

            # Fallback
            return CacheIdInfo(
                cache_id=f"local_unknown_{CacheIdDetector._generate_hash('fallback', 6)}",
                pipeline_id="unknown",
                commit=custom_commit or "unknown",
                branch=custom_branch or "unknown",
                repository="unknown/unknown",
                ci_provider="local",
                source="local",
            )

    @staticmethod
    async def _collect_metadata() -> dict:
        """Collect metadata from Git and CI collectors"""
        git_collector = GitCollector(os.getcwd())
        git_metadata = await git_collector.get_metadata()
        ci_metadata = CiCollector.collect()

        return {
            "commit": git_metadata.commit.hash or "unknown",
            "branch": git_metadata.branch or "unknown",
            "repository": git_metadata.repository.name or "unknown/unknown",
            "pipelineId": ci_metadata.pipeline.id or "unknown",
            "ciProvider": ci_metadata.provider or "unknown",
        }

    @staticmethod
    async def _generate_cache_id(
        custom_branch: Optional[str] = None, custom_commit: Optional[str] = None
    ) -> CacheIdInfo:
        """Generate cache ID from environment"""
        metadata = await CacheIdDetector._collect_metadata()

        # Use custom values if provided
        final_branch = custom_branch or metadata["branch"]
        final_commit = custom_commit or metadata["commit"]

        # Extract repo name
        repo_name = CacheIdDetector._extract_repo_name(metadata["repository"])

        # If repo name is unknown, add hash
        if repo_name == "unknown":
            hash_val = CacheIdDetector._generate_hash("unknown", 6)
            repo_name = f"unknown{hash_val}"
            print("⚠️  Repository name could not be detected")
            print("💡 Use a Git repository or set TESTDINO_CACHE_ID explicitly")

        # Get CI provider prefix
        ci_prefix = CacheIdDetector._get_ci_provider_prefix(metadata["ciProvider"])

        # Sanitize branch name
        sanitized_branch = CacheIdDetector._sanitize_component(final_branch)

        # Build cache ID
        cache_id = f"{ci_prefix}_{repo_name}_{sanitized_branch}"

        return CacheIdInfo(
            cache_id=cache_id,
            pipeline_id=metadata["pipelineId"],
            commit=final_commit,
            branch=final_branch,
            repository=metadata["repository"],
            ci_provider=metadata["ciProvider"],
            source="ci" if metadata["ciProvider"] != "unknown" else "local",
        )

    @staticmethod
    def _extract_repo_name(full_repo: str) -> str:
        """Extract repository name from full repo string"""
        if not full_repo or full_repo == "unknown/unknown":
            return "unknown"

        parts = full_repo.split("/")
        return parts[-1] if parts else "unknown"

    @staticmethod
    def _get_ci_provider_prefix(provider: str) -> str:
        """Get CI provider prefix for cache ID"""
        prefixes = {
            "github-actions": "gh",
            "gitlab-ci": "gl",
            "jenkins": "jenkins",
            "azure-devops": "az",
            "circleci": "circle",
            "unknown": "local",
        }

        return prefixes.get(provider, "local")

    @staticmethod
    def _sanitize_component(component: str) -> str:
        """Sanitize component for cache ID"""
        import re

        return (
            re.sub(r"[^a-z0-9]+", "-", component.lower())
            .strip("-")
            [:50]
        )

    @staticmethod
    def _generate_hash(input_str: str, length: int) -> str:
        """Generate hash from string"""
        hash_val = hashlib.sha256(
            (input_str + str(datetime.now().timestamp())).encode()
        ).hexdigest()
        return hash_val[:length]

    @staticmethod
    def validate_cache_id(cache_id: str) -> bool:
        """Validate cache ID format"""
        if not cache_id or not isinstance(cache_id, str):
            return False

        import re

        return (
            5 <= len(cache_id) <= 150
            and bool(re.match(r"^[a-zA-Z0-9\-_]+$", cache_id))
        )

    @staticmethod
    async def get_cache_context() -> dict:
        """Get cache context information for logging"""
        try:
            cache_id_info = await CacheIdDetector.detect_cache_id()

            return {
                "cacheId": cache_id_info.cache_id,
                "pipelineId": cache_id_info.pipeline_id,
                "commit": cache_id_info.commit,
                "branch": cache_id_info.branch,
                "repository": cache_id_info.repository,
                "ciProvider": cache_id_info.ci_provider,
                "source": cache_id_info.source,
            }
        except Exception:
            return {
                "cacheId": "unknown",
                "pipelineId": "unknown",
                "commit": "unknown",
                "branch": "unknown",
                "repository": "unknown",
                "ciProvider": "local",
                "source": "local",
            }


@dataclass
class TestFailure:
    """Test failure data structure"""

    file: str
    test_title: str
    error: Optional[str] = None
    duration: Optional[int] = None


@dataclass
class TestSummary:
    """Test summary data structure"""

    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    duration: int = 0


@dataclass
class CacheExtractionResult:
    """Cache extraction result"""

    failures: List[TestFailure] = field(default_factory=list)
    summary: TestSummary = field(default_factory=TestSummary)
    report_paths: List[str] = field(default_factory=list)
    has_data: bool = False


def _get(obj: any, key: str, default: any = None) -> any:
    """Get value from dict or object attribute"""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class CacheExtractor:
    """Service for extracting test failure data for caching"""

    def __init__(self, working_dir: str, token: str = ""):
        self.working_dir = working_dir
        self.token = token

    async def extract_failure_data(self) -> CacheExtractionResult:
        """Extract test failures and metadata for caching"""
        try:
            # Step 1: Discover JSON reports
            report_paths = await self._discover_reports()

            if not report_paths:
                return self._create_empty_result()

            # Step 2: Parse reports and extract failures
            failures: List[TestFailure] = []
            total_summary = TestSummary()

            for report_path in report_paths:
                try:
                    from testdino_cli.core.parser import parse_playwright_json

                    report_data = await parse_playwright_json(report_path)

                    # Extract failures from this report
                    report_failures = self._extract_failures_from_report(report_data, report_path)
                    failures.extend(report_failures)

                    # Aggregate summary data from stats
                    if hasattr(report_data, "stats") and report_data.stats:
                        stats = report_data.stats
                        total_summary.total += (stats.expected or 0) + (stats.unexpected or 0) + (stats.skipped or 0)
                        total_summary.passed += stats.expected or 0
                        total_summary.failed += stats.unexpected or 0
                        total_summary.skipped += stats.skipped or 0
                        total_summary.duration += int(round(stats.duration or 0))

                except Exception as error:
                    # Log but continue with other reports
                    print(f"⚠️  Failed to parse report {report_path}: {error}")
                    continue

            return CacheExtractionResult(
                failures=failures,
                summary=total_summary,
                report_paths=report_paths,
                has_data=len(failures) > 0 or total_summary.total > 0,
            )

        except Exception as error:
            from testdino_cli.types import FileSystemError
            raise FileSystemError(f"Failed to extract test failure data: {error}")

    async def _discover_reports(self) -> List[str]:
        """Discover JSON reports using the existing discovery service"""
        try:
            from testdino_cli.core.discovery import ReportDiscoveryService
            from testdino_cli.types import CLIOptions

            discovery_service = ReportDiscoveryService(self.working_dir)

            # Create minimal options for discovery (only need JSON report)
            options = CLIOptions(
                report_directory=self.working_dir,
                token=self.token,
                upload_images=False,
                upload_videos=False,
                upload_html=False,
                upload_traces=False,
                upload_files=False,
                upload_full_json=False,
                verbose=False,
            )

            discovery_result = await discovery_service.discover(options)

            # Return the discovered JSON report path
            if discovery_result.json_report:
                return [discovery_result.json_report]

            return []
        except Exception:
            return []

    def _extract_failures_from_report(self, report_data: any, report_path: str) -> List[TestFailure]:
        """Extract failures from a parsed report"""
        failures: List[TestFailure] = []

        try:
            # Handle Playwright report structure - suites contain the test information
            suites = getattr(report_data, "suites", [])

            if isinstance(suites, list):
                for suite in suites:
                    self._extract_failures_from_suite(suite, failures, "", None)

            return failures
        except Exception as error:
            print(f"⚠️  Failed to extract failures from {report_path}: {error}")
            return []

    def _extract_failures_from_suite(self, suite: any, failures: List[TestFailure], parent_path: str = "", parent_file: Optional[str] = None) -> None:
        """Recursively extract failures from suite structure"""
        try:
            # Extract file from suite if available
            suite_file = _get(suite, "file") or parent_file

            # Build test path
            suite_title = _get(suite, "title", "")
            should_include_in_path = suite_title and (not _get(suite, "file") or suite_title != _get(suite, "file"))
            suite_path = f"{parent_path} > {suite_title}" if parent_path and should_include_in_path else (suite_title if should_include_in_path else parent_path)

            # Handle nested suites (recursive)
            nested_suites = _get(suite, "suites", [])
            if isinstance(nested_suites, list):
                for nested_suite in nested_suites:
                    self._extract_failures_from_suite(nested_suite, failures, suite_path, suite_file)

            # Handle specs in this suite
            specs = _get(suite, "specs", [])
            if isinstance(specs, list):
                for spec in specs:
                    self._extract_failures_from_spec(spec, failures, suite_path, suite_file)

            # Handle individual tests in this suite (fallback)
            tests = _get(suite, "tests", [])
            if isinstance(tests, list):
                for test in tests:
                    self._extract_failures_from_test(test, failures, suite_path, suite_file)

        except Exception as error:
            print(f"⚠️  Error processing suite: {error}")

    def _extract_failures_from_spec(self, spec: any, failures: List[TestFailure], parent_path: str = "", suite_file: Optional[str] = None) -> None:
        """Extract failures from spec structure"""
        try:
            spec_title = _get(spec, "title", "")
            spec_ok = _get(spec, "ok", True)
            spec_failed = spec_ok is False

            # Handle individual tests in this spec
            tests = _get(spec, "tests", [])
            if isinstance(tests, list) and spec_failed and tests:
                # Only process the first test (all tests in a spec are the same test with retries)
                test = tests[0]
                failure = self._create_test_failure(test, parent_path, suite_file, spec_title)
                if failure:
                    # Check for duplicates
                    is_duplicate = any(f.file == failure.file and f.test_title == failure.test_title for f in failures)
                    if not is_duplicate:
                        failures.append(failure)

        except Exception as error:
            print(f"⚠️  Error processing spec: {error}")

    def _extract_failures_from_test(self, test: any, failures: List[TestFailure], parent_path: str = "", suite_file: Optional[str] = None, spec_title: Optional[str] = None) -> None:
        """Extract failures from individual test"""
        try:
            if self._is_failed_test(test):
                failure = self._create_test_failure(test, parent_path, suite_file, spec_title)
                if failure:
                    # Check for duplicates
                    is_duplicate = any(f.file == failure.file and f.test_title == failure.test_title for f in failures)
                    if not is_duplicate:
                        failures.append(failure)

        except Exception as error:
            print(f"⚠️  Error processing test: {error}")

    def _is_failed_test(self, item: any) -> bool:
        """Check if a test item represents a failed test"""
        if not item:
            return False

        status = _get(item, "status")
        outcome = _get(item, "outcome")
        state = _get(item, "state")
        results = _get(item, "results", [])

        return (
            status == "failed"
            or outcome == "failed"
            or state == "failed"
            or (isinstance(results, list) and any(_get(r, "status") == "failed" for r in results))
        )

    def _create_test_failure(self, test: any, parent_path: str = "", suite_file: Optional[str] = None, spec_title: Optional[str] = None) -> Optional[TestFailure]:
        """Create TestFailure object from test data"""
        try:
            # Extract file path
            test_file = _get(test, "file")
            test_location = _get(test, "location")
            location_file = _get(test_location, "file") if test_location else None
            file_path = test_file or location_file or suite_file or ""

            # Clean up file path
            if file_path:
                cwd = os.getcwd()
                if file_path.startswith(cwd):
                    file_path = file_path[len(cwd) + 1:]
                if file_path.startswith("tests/"):
                    file_path = file_path[6:]

            # Extract test title - use spec title only
            test_title = spec_title or _get(test, "title") or _get(test, "name") or "Unknown test"

            # Extract error information
            error: Optional[str] = None
            results = _get(test, "results", [])
            if isinstance(results, list):
                failed_result = next((r for r in results if _get(r, "status") == "failed"), None)
                if failed_result:
                    result_error = _get(failed_result, "error")
                    if result_error:
                        error = self._format_error(result_error)
            elif _get(test, "error"):
                error = self._format_error(_get(test, "error"))

            # Extract duration
            duration: Optional[int] = None
            if isinstance(results, list):
                duration = sum(_get(r, "duration", 0) or 0 for r in results)
            else:
                test_duration = _get(test, "duration")
                if isinstance(test_duration, (int, float)):
                    duration = int(test_duration)

            # Only create failure if we have meaningful data
            if not file_path and not test_title:
                return None

            return TestFailure(
                file=file_path or "unknown",
                test_title=test_title,
                error=error,
                duration=duration,
            )

        except Exception as error:
            print(f"⚠️  Failed to create test failure object: {error}")
            return None

    def _format_error(self, error: any) -> str:
        """Format error message for storage"""
        try:
            if isinstance(error, str):
                return error

            if hasattr(error, "message"):
                return str(getattr(error, "message"))

            if hasattr(error, "name"):
                return str(getattr(error, "name"))

            if isinstance(error, dict):
                return error.get("message") or error.get("name") or str(error)

            return str(error)
        except Exception:
            return "Error formatting failed"

    def _create_empty_result(self) -> CacheExtractionResult:
        """Create empty result for cases with no data"""
        return CacheExtractionResult(
            failures=[],
            summary=TestSummary(),
            report_paths=[],
            has_data=False,
        )
