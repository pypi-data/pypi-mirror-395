"""Enhanced Upload Service - Complete Integration

Implements the full upload flow: Azure files → JSON + URLs → TestDino API
This is an exact port of the TypeScript version.
"""

import asyncio
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from testdino_cli.collectors.ci import CiCollector, CiMetadata
from testdino_cli.collectors.git import GitCollector, GitMetadata
from testdino_cli.collectors.system import SystemCollector, SystemMetadata
from testdino_cli.config.index import Config
from testdino_cli.core.attachments import AttachmentInfo, AttachmentScanner
from testdino_cli.core.parser import parse_playwright_json, PlaywrightReport
from testdino_cli.services.api import ApiClient, ReportUploadResponse
from testdino_cli.services.azure import AzureStorageClient, AzureUploadService
from testdino_cli.services.sas import SasTokenService
from testdino_cli.types import NetworkError
from testdino_cli.utils.progress import create_progress_tracker
from testdino_cli.utils.retry import with_retry, RetryOptions


@dataclass
class AzureUploadResult:
    """Azure upload result for HTML reports and attachment URL mappings"""

    status: str  # 'uploaded', 'disabled', 'failed', 'not-found'
    url: str
    url_mapping: Dict[str, str] = field(default_factory=dict)


@dataclass
class TestMetadata:
    """Test configuration metadata extracted from Playwright report"""

    framework: Dict[str, str]
    config: Dict[str, Any]
    custom_tags: List[str] = field(default_factory=list)


@dataclass
class CompleteMetadata:
    """Complete metadata structure matching sample-report.json"""

    git: Any  # GitMetadata or dict
    ci: Any  # CiMetadata or dict
    system: Any  # SystemMetadata or dict
    test: TestMetadata
    azure_upload: Optional[AzureUploadResult] = None


@dataclass
class FinalPayload:
    """Final payload structure matching sample-report.json format"""

    config: Dict[str, Any]
    suites: List[Any]
    stats: Dict[str, Any]
    errors: List[Any]
    metadata: Dict[str, Any]


class UploadService:
    """Service to upload Playwright report and metadata to TestDino"""

    def __init__(self, config: Config):
        self.config = config
        self.api_client = ApiClient(config)
        self.sas_service = SasTokenService(config)

    def _get_report_directory(self, json_path: str) -> str:
        """Get report directory from JSON file path"""
        return str(Path(json_path).parent)

    def _generate_unique_id(self) -> str:
        """Generate a unique identifier for attachments
        Uses timestamp + random string for uniqueness (matching TypeScript implementation)
        """
        import random
        import string

        # Base36 timestamp (matching TypeScript's Date.now().toString(36))
        timestamp_ms = int(datetime.now().timestamp() * 1000)
        timestamp = self._to_base36(timestamp_ms)
        # 6 random base36 chars (matching TypeScript's Math.random().toString(36).substring(2, 8))
        random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"{timestamp}_{random_str}"

    @staticmethod
    def _to_base36(n: int) -> str:
        """Convert integer to base36 string (matching JavaScript's Number.toString(36))"""
        if n == 0:
            return "0"
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        result = ""
        while n:
            result = chars[n % 36] + result
            n //= 36
        return result

    def _get_file_extension(self, attachment: AttachmentInfo) -> str:
        """Extract file extension from attachment info"""
        # First try to get extension from original path
        path_parts = attachment.original_path.split(".")
        if len(path_parts) > 1:
            extension = path_parts[-1]
            if extension:
                return f".{extension.lower()}"

        # Fallback: derive from content type
        content_type = attachment.content_type.lower()
        if "png" in content_type:
            return ".png"
        if "jpeg" in content_type or "jpg" in content_type:
            return ".jpg"
        if "gif" in content_type:
            return ".gif"
        if "webp" in content_type:
            return ".webp"
        if "svg" in content_type:
            return ".svg"
        if "webm" in content_type:
            return ".webm"
        if "mp4" in content_type:
            return ".mp4"
        if "zip" in content_type:
            return ".zip"

        # Default fallback
        return ".bin"

    def _create_json_attachment_path(self, attachment: AttachmentInfo) -> str:
        """Generate unique Azure blob path for attachment using UUID
        This eliminates any possibility of path collisions regardless of directory structure
        """
        unique_id = self._generate_unique_id()
        file_extension = self._get_file_extension(attachment)
        # Create clean, unique path: json/attachments/{uniqueId}.{extension}
        return f"json/attachments/{unique_id}{file_extension}"

    def _create_json_trace_attachment_path(self, attachment: AttachmentInfo) -> str:
        """Generate unique Azure blob path for trace attachment using UUID
        Places traces in the same location as other attachments
        """
        unique_id = self._generate_unique_id()
        # Ensure trace files have .zip extension for proper viewer compatibility
        file_extension = self._get_file_extension(attachment)
        if ".zip" not in file_extension:
            file_extension = ".zip"
        # Create clean, unique path: json/traces/{uniqueId}.zip
        return f"json/traces/{unique_id}{file_extension}"

    async def upload_report(
        self,
        json_path: str,
        html_dir: Optional[str] = None,
        trace_dir: Optional[str] = None,
    ) -> ReportUploadResponse:
        """Main upload orchestration method
        Flow: Collect Metadata → Upload Azure Files → Send JSON + URLs to API
        """
        tracker = create_progress_tracker()

        try:
            # Step 1: Parse the base Playwright report
            tracker.start("Parsing Playwright report...")
            base_report = await parse_playwright_json(json_path)
            tracker.succeed("Report parsed successfully")

            # Step 2: Scan for attachments
            tracker.start("Scanning for attachments...")
            report_directory = self._get_report_directory(json_path)
            attachment_scanner = AttachmentScanner(report_directory)
            attachment_scan_result = await attachment_scanner.scan_attachments(
                base_report
            )

            # Filter attachments based on configuration
            attachments_to_upload = AttachmentScanner.filter_attachments(
                attachment_scan_result, self.config.__dict__
            )

            if attachments_to_upload:
                tracker.succeed(
                    f"Found {len(attachments_to_upload)} attachments to upload"
                )
            else:
                tracker.succeed("No attachments to upload based on current flags")

            # Step 3: Collect all metadata
            tracker.start("Collecting environment metadata...")
            metadata = await self._collect_metadata(base_report)
            tracker.succeed("Metadata collected")

            # Step 4: Upload files to Azure with STRICT validation after auto-discovery
            azure_upload_result: Optional[AzureUploadResult] = None
            should_upload_to_azure = (
                self.config.upload_images
                or self.config.upload_videos
                or self.config.upload_html
                or self.config.upload_traces
                or self.config.upload_files
                or self.config.upload_full_json
            )

            if should_upload_to_azure:
                # STRICT ENFORCEMENT: After auto-discovery, validate we have what user requested
                self._enforce_strict_upload_requirements(
                    html_dir, trace_dir, attachments_to_upload
                )

                tracker.start("Uploading files to TestDino platform...")
                azure_upload_result = await self._upload_to_azure(
                    html_dir, trace_dir, attachments_to_upload
                )

                if azure_upload_result.status == "uploaded":
                    tracker.succeed("TestDino platform upload completed successfully")
                elif azure_upload_result.status == "failed":
                    tracker.fail("TestDino platform upload failed")
                    raise Exception("Upload failed when uploads were explicitly enabled")
                else:
                    tracker.succeed("TestDino platform upload skipped")

            # Step 5: Build final payload with Azure URLs
            tracker.start("Uploading to TestDino API...")

            # Update attachment paths with Azure URLs or status markers
            url_mapping = (
                azure_upload_result.url_mapping if azure_upload_result else {}
            )
            final_report = AttachmentScanner.update_attachment_paths(
                base_report, url_mapping, self.config.__dict__
            )

            final_payload = self._build_final_payload(
                final_report, metadata, azure_upload_result
            )

            if self.config.verbose:
                test_count = (
                    len(final_payload["suites"])
                    if isinstance(final_payload.get("suites"), list)
                    else 0
                )
                print(f"📦 Uploading report: {test_count} test suites")

            # Step 6: Upload to TestDino API with retry
            response = await with_retry(
                lambda: self.api_client.upload_report(final_payload),
                RetryOptions(max_attempts=3, base_delay=1000),
            )

            tracker.succeed("Report uploaded successfully")
            return response

        except Exception as error:
            tracker.fail("Upload failed")
            raise error

    async def _collect_metadata(
        self, base_report: PlaywrightReport
    ) -> Dict[str, Any]:
        """Collect all metadata with ZERO data loss guarantee
        CRITICAL: Each collector has fallbacks - never fails completely
        """
        # Collect metadata in parallel with fallbacks using asyncio equivalent of Promise.allSettled
        results: List[Tuple[str, Any, Optional[Exception]]] = []

        async def collect_git():
            try:
                return await self._collect_git_metadata_with_fallback()
            except Exception as e:
                return e

        async def collect_ci():
            try:
                return await self._collect_ci_metadata_with_fallback()
            except Exception as e:
                return e

        async def collect_system():
            try:
                return await self._collect_system_metadata_with_fallback()
            except Exception as e:
                return e

        # Run all collectors in parallel
        collection_results = await asyncio.gather(
            collect_git(),
            collect_ci(),
            collect_system(),
            return_exceptions=True,
        )

        # Extract results, using fallbacks for any failures
        if isinstance(collection_results[0], Exception):
            git_meta = self._get_git_metadata_fallback()
        else:
            git_meta = collection_results[0]

        if isinstance(collection_results[1], Exception):
            ci_meta = self._get_ci_metadata_fallback()
        else:
            ci_meta = collection_results[1]

        if isinstance(collection_results[2], Exception):
            system_meta = self._get_system_metadata_fallback()
        else:
            system_meta = collection_results[2]

        # Extract test configuration from the base report
        test_meta = self._extract_test_metadata(base_report)

        # Convert dataclasses to dicts if needed
        def to_dict(obj: Any) -> Any:
            if hasattr(obj, "__dict__"):
                result = {}
                for key, value in obj.__dict__.items():
                    result[key] = to_dict(value)
                return result
            elif isinstance(obj, dict):
                return {k: to_dict(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [to_dict(v) for v in obj]
            return obj

        metadata = {
            "git": to_dict(git_meta),
            "ci": to_dict(ci_meta),
            "system": to_dict(system_meta),
            "test": test_meta,
        }

        # Log any collection failures
        failures = []
        types = ["git", "ci", "system"]
        for i, result in enumerate(collection_results):
            if isinstance(result, Exception):
                failures.append(f"{types[i]}: {str(result)}")

        if failures:
            print(
                f"⚠️  Metadata collection issues (using fallbacks): {', '.join(failures)}"
            )

        if self.config.verbose:
            branch = (
                git_meta.branch
                if hasattr(git_meta, "branch")
                else git_meta.get("branch", "unknown")
                if isinstance(git_meta, dict)
                else "unknown"
            )
            provider = (
                ci_meta.provider
                if hasattr(ci_meta, "provider")
                else ci_meta.get("provider", "local")
                if isinstance(ci_meta, dict)
                else "local"
            )
            print(f"📋 Metadata: {branch}, {provider} environment")

        # STRICT ENFORCEMENT: Validate critical metadata when uploads are enabled
        self._enforce_strict_metadata_requirements(metadata)

        return metadata

    async def _collect_git_metadata_with_fallback(self) -> Any:
        """Collect Git metadata with comprehensive error handling"""
        try:
            return await GitCollector(os.getcwd()).get_metadata()
        except Exception as error:
            if self.config.verbose:
                print(f"⚠️  Git metadata collection failed: {error}")
            return self._get_git_metadata_fallback()

    async def _collect_ci_metadata_with_fallback(self) -> Any:
        """Collect CI metadata with error handling"""
        try:
            return CiCollector.collect()
        except Exception as error:
            if self.config.verbose:
                print(f"⚠️  CI metadata collection failed: {error}")
            return self._get_ci_metadata_fallback()

    async def _collect_system_metadata_with_fallback(self) -> Any:
        """Collect System metadata with error handling"""
        try:
            return SystemCollector.collect()
        except Exception as error:
            if self.config.verbose:
                print(f"⚠️  System metadata collection failed: {error}")
            return self._get_system_metadata_fallback()

    def _get_git_metadata_fallback(self) -> Dict[str, Any]:
        """Fallback Git metadata when all collection methods fail"""
        env = os.environ
        return {
            "branch": env.get("CI_COMMIT_REF_NAME")
            or env.get("GITHUB_HEAD_REF")
            or env.get("BRANCH_NAME")
            or "unknown",
            "commit": {
                "hash": env.get("CI_COMMIT_SHA")
                or env.get("GITHUB_SHA")
                or env.get("GIT_COMMIT")
                or "unknown",
                "message": env.get("CI_COMMIT_MESSAGE", ""),
                "author": env.get("CI_COMMIT_AUTHOR")
                or env.get("GITHUB_ACTOR")
                or env.get("GIT_AUTHOR_NAME")
                or "",
                "email": env.get("CI_COMMIT_AUTHOR_EMAIL")
                or env.get("GIT_AUTHOR_EMAIL")
                or "",
                "timestamp": datetime.now().isoformat(),
            },
            "repository": {
                "name": env.get("CI_PROJECT_PATH")
                or env.get("GITHUB_REPOSITORY")
                or "unknown",
                "url": env.get("CI_PROJECT_URL")
                or env.get("GITHUB_REPOSITORY_URL")
                or env.get("GIT_URL")
                or "",
            },
            "pr": {
                "id": env.get("CI_MERGE_REQUEST_ID")
                or env.get("GITHUB_PR_NUMBER")
                or "",
                "title": env.get("CI_MERGE_REQUEST_TITLE") or "",
                "url": env.get("CI_MERGE_REQUEST_URL") or "",
                "status": "",
            },
        }

    def _get_ci_metadata_fallback(self) -> Dict[str, Any]:
        """Fallback CI metadata when collection fails"""
        import sys

        env = os.environ
        return {
            "provider": "unknown",
            "pipeline": {
                "id": env.get("CI_PIPELINE_ID")
                or env.get("GITHUB_RUN_ID")
                or "unknown",
                "name": env.get("CI_PIPELINE_NAME")
                or env.get("GITHUB_WORKFLOW")
                or "CI Pipeline",
                "url": env.get("CI_PIPELINE_URL") or "",
            },
            "build": {
                "number": env.get("CI_BUILD_NUMBER")
                or env.get("GITHUB_RUN_NUMBER")
                or "unknown",
                "trigger": env.get("CI_PIPELINE_TRIGGER")
                or env.get("GITHUB_EVENT_NAME")
                or "",
            },
            "environment": {
                "name": env.get("CI_ENVIRONMENT_NAME") or "local",
                "type": "",
                "os": "unknown",
                "node": f"Python {sys.version.split()[0]}",
            },
        }

    def _get_system_metadata_fallback(self) -> Dict[str, Any]:
        """Fallback System metadata when collection fails"""
        import platform
        import sys

        return {
            "hostname": "unknown",
            "cpu": {
                "count": 1,
                "model": "unknown",
            },
            "memory": {
                "total": "unknown",
            },
            "os": "unknown",
            "nodejs": f"Python {sys.version.split()[0]}",
            "playwright": "unknown",
        }

    def _enforce_strict_upload_requirements(
        self,
        html_dir: Optional[str],
        trace_dir: Optional[str],
        attachments: List[AttachmentInfo],
    ) -> None:
        """STRICT ENFORCEMENT: Validate we have required files/directories after auto-discovery
        FAILS HARD if user enabled options but we can't deliver what they requested
        """
        violations: List[str] = []

        # Strict HTML upload validation
        if self.config.upload_html and not html_dir:
            violations.append(
                "❌ HTML upload enabled (--upload-html) but no HTML report directory found\n"
                "💡 Auto-discovery failed - ensure HTML report exists or use --html-report <path>"
            )

        # Trace upload validation - graceful handling for missing traces
        # NOTE: Traces are only generated on test failures by default, so missing traces is normal when tests pass
        trace_attachments = [att for att in attachments if att.type == "trace"]
        if self.config.upload_traces and len(trace_attachments) == 0 and not trace_dir:
            # Only warn, don't fail - missing traces is normal when tests pass
            print(
                "⚠️  Trace upload enabled (--upload-traces) but no trace files found.\n"
                "💡 This is normal when all tests pass. Traces are only generated on test failures."
            )

        # Strict attachment validation
        if (
            self.config.upload_images
            or self.config.upload_videos
            or self.config.upload_files
            or self.config.upload_full_json
        ) and len(attachments) == 0:
            enabled_types = []
            if self.config.upload_images:
                enabled_types.append("images")
            if self.config.upload_videos:
                enabled_types.append("videos")
            if self.config.upload_files:
                enabled_types.append("files")
            if self.config.upload_full_json:
                enabled_types.append("all attachments")

            violations.append(
                f"❌ {' and '.join(enabled_types)} upload enabled but no {'/'.join(enabled_types)} found\n"
                "💡 Auto-discovery failed - ensure test attachments exist in the report"
            )

        # STRICT FAILURE: If any enabled option cannot be fulfilled, fail hard
        if violations:
            error_message = (
                "🚫 STRICT VALIDATION FAILED - Cannot fulfill explicitly enabled upload options:\n\n"
                + "\n\n".join(violations)
                + "\n\n💡 Either provide the missing files/directories or remove the corresponding upload flags."
            )
            raise Exception(error_message)

        # Additional validation: Check directory accessibility
        if html_dir and self.config.upload_html:
            self._validate_directory_access(html_dir, "HTML report directory")

        if trace_dir and self.config.upload_traces:
            self._validate_directory_access(trace_dir, "trace directory")

    def _validate_directory_access(self, dir_path: str, description: str) -> None:
        """Validate directory is accessible and contains expected content"""
        try:
            # Basic accessibility check
            if not Path(dir_path).exists():
                raise Exception(f"Directory does not exist: {dir_path}")
            if not Path(dir_path).is_dir():
                raise Exception(f"Path is not a directory: {dir_path}")

            if self.config.verbose:
                print(f"✅ {description} validated: {dir_path}")
        except Exception as error:
            raise Exception(
                f"❌ {description} validation failed: {dir_path}\n"
                f"💡 {error}"
            )

    def _enforce_strict_metadata_requirements(
        self, metadata: Dict[str, Any]
    ) -> None:
        """STRICT ENFORCEMENT: Validate critical metadata is available
        FAILS HARD if essential metadata is missing when uploads are enabled
        """
        is_upload_enabled = (
            self.config.upload_images
            or self.config.upload_videos
            or self.config.upload_html
            or self.config.upload_traces
            or self.config.upload_files
            or self.config.upload_full_json
        )

        if not is_upload_enabled:
            return  # No strict requirements for JSON-only uploads

        violations: List[str] = []
        git_meta = metadata.get("git", {})

        # Strict Git metadata validation
        commit = git_meta.get("commit", {})
        commit_hash = commit.get("hash") if isinstance(commit, dict) else None
        if not commit_hash or commit_hash == "unknown":
            violations.append(
                "❌ Git commit hash missing or unknown\n"
                "💡 Required for upload tracking - ensure you're in a git repository with commits"
            )

        branch = git_meta.get("branch")
        if not branch or branch == "unknown":
            violations.append(
                "❌ Git branch information missing or unknown\n"
                "💡 Required for upload organization - ensure you're on a valid git branch"
            )

        # Strict repository metadata validation
        repository = git_meta.get("repository", {})
        repo_name = repository.get("name") if isinstance(repository, dict) else None
        if not repo_name or repo_name == "unknown":
            violations.append(
                "❌ Repository name missing or unknown\n"
                "💡 Required for upload categorization - ensure git remote is configured"
            )

        # STRICT FAILURE: If critical metadata is missing during uploads, fail hard
        if violations:
            error_message = (
                "🚫 STRICT METADATA VALIDATION FAILED - Missing critical information for uploads:\n\n"
                + "\n\n".join(violations)
                + "\n\n💡 Either fix the git repository setup or disable upload options for JSON-only uploads."
            )
            raise Exception(error_message)

        if self.config.verbose:
            print(
                "✅ Strict metadata validation passed - all critical information available"
            )

    def _validate_and_sanitize_path_prefix(self, sas_response: Any) -> str:
        """Validate and sanitize path prefix from SAS response
        CRITICAL: Ensures reliable URL generation even with malformed server responses
        """
        path_prefix = None

        # Try to extract pathPrefix from response
        if hasattr(sas_response, "upload_instructions"):
            upload_instructions = sas_response.upload_instructions
            if hasattr(upload_instructions, "path_prefix"):
                path_prefix = upload_instructions.path_prefix
        elif isinstance(sas_response, dict):
            upload_instructions = sas_response.get("uploadInstructions", {})
            if isinstance(upload_instructions, dict):
                path_prefix = upload_instructions.get("pathPrefix")

        if not path_prefix or not isinstance(path_prefix, str):
            # Generate fallback path prefix based on current timestamp
            now = datetime.now()
            year = now.year
            month = str(now.month).zfill(2)
            day = str(now.day).zfill(2)
            random_id = self._generate_unique_id()[:8]

            fallback_prefix = f"{year}/{month}/{day}/{random_id}"

            if self.config.verbose:
                print(
                    f"⚠️  Invalid or missing pathPrefix from server, using fallback: {fallback_prefix}"
                )

            return fallback_prefix

        # Sanitize path prefix to ensure it's safe
        sanitized = path_prefix
        # Remove leading/trailing slashes
        sanitized = re.sub(r"^/+|/+$", "", sanitized)
        # Replace multiple slashes with single slash
        sanitized = re.sub(r"/+", "/", sanitized)
        # Remove unsafe characters
        sanitized = re.sub(r"[^a-zA-Z0-9/\-_]", "", sanitized)

        if not sanitized:
            # If sanitization resulted in empty string, use fallback
            now = datetime.now()
            fallback_prefix = f"{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)}/fallback_{int(now.timestamp() * 1000)}"

            if self.config.verbose:
                print(
                    f"⚠️  Path prefix sanitization resulted in empty string, using fallback: {fallback_prefix}"
                )

            return fallback_prefix

        if sanitized != path_prefix and self.config.verbose:
            print(f"⚠️  Path prefix sanitized: '{path_prefix}' → '{sanitized}'")

        return sanitized

    def _validate_sas_response(self, sas_response: Any) -> None:
        """Validate SAS response completeness and generate safe fallbacks"""
        required = [
            "sasToken",
            "containerUrl",
            "uploadInstructions",
            "uploadInstructions.baseUrl",
            "uploadInstructions.allowedFileTypes",
            "uploadInstructions.maxFileSize",
        ]

        missing = []

        for field_path in required:
            parts = field_path.split(".")
            current = sas_response

            for part in parts:
                if hasattr(current, part):
                    current = getattr(current, part)
                elif isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    # Try snake_case conversion
                    snake_part = re.sub(r"([A-Z])", r"_\1", part).lower().lstrip("_")
                    if hasattr(current, snake_part):
                        current = getattr(current, snake_part)
                    elif isinstance(current, dict) and snake_part in current:
                        current = current[snake_part]
                    else:
                        missing.append(field_path)
                        break

        if missing:
            raise Exception(
                f"Invalid SAS response from server - missing required fields: {', '.join(missing)}\n"
                "This indicates a server-side issue. Please contact support."
            )

        # Validate data types and ranges
        upload_instructions = (
            sas_response.upload_instructions
            if hasattr(sas_response, "upload_instructions")
            else sas_response.get("uploadInstructions", {})
        )

        max_file_size = (
            upload_instructions.max_file_size
            if hasattr(upload_instructions, "max_file_size")
            else upload_instructions.get("maxFileSize")
        )
        if not isinstance(max_file_size, (int, float)) or max_file_size <= 0:
            raise Exception("Invalid maxFileSize in SAS response")

        allowed_file_types = (
            upload_instructions.allowed_file_types
            if hasattr(upload_instructions, "allowed_file_types")
            else upload_instructions.get("allowedFileTypes")
        )
        if not isinstance(allowed_file_types, list):
            raise Exception("Invalid allowedFileTypes in SAS response")

    def _extract_test_metadata(self, report: PlaywrightReport) -> Dict[str, Any]:
        """Extract test configuration metadata from Playwright report"""
        config = report.config if hasattr(report, "config") else {}
        if not isinstance(config, dict):
            config = {}

        projects = config.get("projects", [])
        if not isinstance(projects, list):
            projects = []

        # Get Playwright version
        playwright_version = "unknown"
        try:
            import importlib.metadata

            playwright_version = importlib.metadata.version("playwright")
        except Exception:
            try:
                import importlib.metadata

                playwright_version = importlib.metadata.version("pytest-playwright")
            except Exception:
                pass

        # Build browser configurations
        browsers = []
        for project in projects:
            if not isinstance(project, dict):
                continue

            browsers.append(
                {
                    "browserId": project.get("id") or project.get("name") or "unknown",
                    "name": project.get("name") or "unknown",
                    "version": config.get("version") or "unknown",
                    "viewport": "1280x720",  # Default, could be extracted from project config
                    "headless": True,  # Default assumption
                    "repeatEach": project.get("repeatEach", 1),
                    "retries": project.get("retries", 0),
                    "testDir": project.get("testDir")
                    or config.get("rootDir")
                    or "unknown",
                    "outputDir": project.get("outputDir") or "unknown",
                }
            )

        return {
            "framework": {
                "name": "playwright",
                "version": playwright_version,
            },
            "config": {
                "browsers": browsers,
                "actualWorkers": config.get("metadata", {}).get("actualWorkers")
                or config.get("workers")
                or 1,
                "timeout": projects[0].get("timeout", config.get("timeout", 30000))
                if projects
                else config.get("timeout", 30000),
                "preserveOutput": config.get("preserveOutput") or "always",
                "reporters": self._extract_reporter_config(config.get("reporter")),
                "grep": config.get("grep") or {},
                "grepInvert": config.get("grepInvert"),
                "fullyParallel": config.get("fullyParallel") or False,
                "forbidOnly": config.get("forbidOnly") or False,
                "projects": len(projects),
                "shard": config.get("shard"),
            },
            "customTags": [],
        }

    def _extract_reporter_config(self, reporters: Any) -> List[Dict[str, Any]]:
        """Extract reporter configuration from Playwright config"""
        if not isinstance(reporters, list):
            return []

        result = []
        for reporter in reporters:
            if isinstance(reporter, list):
                result.append(
                    {
                        "name": reporter[0] if reporter else "unknown",
                        "options": reporter[1] if len(reporter) > 1 else {},
                    }
                )
            elif isinstance(reporter, str):
                result.append({"name": reporter, "options": {}})

        return result

    async def _upload_to_azure(
        self,
        html_dir: Optional[str],
        trace_dir: Optional[str],
        attachments: List[AttachmentInfo],
    ) -> AzureUploadResult:
        """Upload HTML, trace files, and attachments to Azure storage with proper directory structure"""
        try:
            # Request SAS token with retry (ONE TOKEN PER COMMAND)
            sas_response = await with_retry(
                lambda: self.sas_service.request_sas_token(),
                RetryOptions(max_attempts=3, base_delay=1000),
            )

            # Validate SAS response completeness
            self._validate_sas_response(sas_response)

            # Validate and sanitize path prefix
            sanitized_path_prefix = self._validate_and_sanitize_path_prefix(sas_response)

            if self.config.verbose:
                expiry_minutes = self.sas_service.get_time_until_expiry(sas_response)
                print(f"🔐 Token acquired (expires in {expiry_minutes} minutes)")
                container_url = (
                    sas_response.container_url
                    if hasattr(sas_response, "container_url")
                    else sas_response.get("containerUrl", "")
                )
                print(f"📁 Upload path: {container_url}/{sanitized_path_prefix}/")

            # Create Azure storage client with validated path prefix
            storage_client = AzureStorageClient(sas_response)
            upload_service = AzureUploadService(storage_client)

            html_url = ""
            url_mapping: Dict[str, str] = {}

            # Upload attachments (images, videos, etc.) and collect URL mappings
            if attachments:
                try:
                    print(f"📎 Uploading {len(attachments)} attachments...")

                    # Upload attachments in configurable batches for better performance
                    batch_size = self.config.batch_size
                    for i in range(0, len(attachments), batch_size):
                        batch = attachments[i : i + batch_size]

                        # Upload batch in parallel and collect results
                        async def upload_attachment(attachment: AttachmentInfo):
                            try:
                                # Create clean blob path for JSON attachments with directory structure
                                clean_path = self._create_json_attachment_path(attachment)
                                uploaded_url = await storage_client.upload_file(
                                    attachment.absolute_path, clean_path
                                )

                                if self.config.verbose:
                                    print(f"   ✅ {attachment.name}: {uploaded_url}")

                                return (attachment, uploaded_url)
                            except Exception as error:
                                print(
                                    f"⚠️  Failed to upload attachment {attachment.name}: {error}"
                                )
                                return None

                        results = await asyncio.gather(
                            *[upload_attachment(att) for att in batch],
                            return_exceptions=True,
                        )

                        # Collect successful uploads into URL mapping
                        for result in results:
                            if result and not isinstance(result, Exception):
                                attachment, uploaded_url = result
                                if uploaded_url:
                                    url_mapping[attachment.original_path] = uploaded_url

                    print("✅ Attachments upload completed")

                except Exception as error:
                    print(f"⚠️  Attachment upload failed: {error}")

            # Upload HTML report if enabled and directory exists
            should_upload_html_dir = self.config.upload_html and html_dir
            if should_upload_html_dir:
                try:
                    print(f"📁 Uploading HTML report from: {html_dir}")

                    # Upload directory contents with filtering based on flags
                    html_config = {
                        "uploadImages": self.config.upload_images
                        or self.config.upload_html,
                        "uploadVideos": self.config.upload_videos
                        or self.config.upload_html,
                        "uploadHtml": self.config.upload_html,
                    }
                    uploaded_urls = await upload_service.upload_html_directory_with_progress(
                        html_dir, "html", html_config
                    )

                    # Build HTML URL - find the index.html in uploaded URLs
                    index_url = next(
                        (url for url in uploaded_urls if url.endswith("index.html")),
                        None,
                    )
                    if index_url:
                        html_url = index_url
                    else:
                        # Fallback: construct URL manually using validated path prefix
                        container_url = (
                            sas_response.container_url
                            if hasattr(sas_response, "container_url")
                            else sas_response.get("containerUrl", "")
                        )
                        html_url = f"{container_url}/{sanitized_path_prefix}/html/index.html"

                        if self.config.verbose:
                            print(f"🔗 Generated fallback HTML URL: {html_url}")

                    print("✅ HTML report uploaded successfully")

                except Exception as error:
                    print(f"❌ HTML upload failed: {error}")
                    # html_url remains empty, which will result in 'failed' status

            # Upload trace files - try JSON attachments first, then fallback to trace directory
            if self.config.upload_traces:
                trace_attachments = [att for att in attachments if att.type == "trace"]

                if trace_attachments:
                    # Upload individual trace files from JSON attachments
                    try:
                        print(
                            f"📦 Uploading {len(trace_attachments)} trace files from JSON attachments..."
                        )

                        for trace_attachment in trace_attachments:
                            try:
                                # Create clean blob path for trace files with proper naming and .zip extension
                                clean_path = self._create_json_trace_attachment_path(
                                    trace_attachment
                                )
                                uploaded_url = await storage_client.upload_file(
                                    trace_attachment.absolute_path, clean_path
                                )

                                if self.config.verbose:
                                    print(
                                        f"   ✅ {trace_attachment.name}: {uploaded_url}"
                                    )

                                # Add to URL mapping so it gets updated in the JSON
                                url_mapping[trace_attachment.original_path] = uploaded_url
                            except Exception as error:
                                print(
                                    f"⚠️  Failed to upload trace {trace_attachment.name}: {error}"
                                )

                        print("✅ Trace files from JSON attachments uploaded")

                    except Exception as error:
                        print(f"⚠️  Trace attachment upload failed: {error}")

                elif trace_dir:
                    # Fallback: Upload trace files from directory if no traces found in JSON
                    try:
                        print(f"📦 Uploading trace files from directory: {trace_dir}")

                        # Upload traces with 'json/traces' prefix to match JSON attachment structure
                        trace_urls = await upload_service.upload_directory_with_progress(
                            trace_dir, "json/traces"
                        )

                        print(f"✅ {len(trace_urls)} trace files from directory uploaded")

                    except Exception as error:
                        print(f"⚠️  Trace directory upload failed: {error}")
                else:
                    print(
                        "⚠️  Trace upload enabled but no trace files found in test results or trace directory"
                    )

            # Return result based on HTML upload status only
            if self.config.upload_html:
                if html_url:
                    return AzureUploadResult(
                        status="uploaded", url=html_url, url_mapping=url_mapping
                    )
                else:
                    return AzureUploadResult(
                        status="failed", url="", url_mapping=url_mapping
                    )
            else:
                return AzureUploadResult(
                    status="disabled", url="", url_mapping=url_mapping
                )

        except Exception as error:
            error_message = str(error)

            # If Azure upload fails completely and HTML upload was enabled, return failed
            if self.config.upload_html:
                print(f"❌ TestDino platform upload failed completely: {error_message}")
                return AzureUploadResult(status="failed", url="", url_mapping={})
            else:
                print(f"⚠️  TestDino platform upload failed: {error_message}")
                return AzureUploadResult(status="disabled", url="", url_mapping={})

    def _build_final_payload(
        self,
        base_report: PlaywrightReport,
        metadata: Dict[str, Any],
        azure_upload: Optional[AzureUploadResult],
    ) -> Dict[str, Any]:
        """Build the final payload combining base report + metadata + Azure URLs
        This must match the exact structure from sample-report.json
        """
        # Attach Azure upload result to metadata if available
        if azure_upload:
            metadata["azureUpload"] = {
                "status": azure_upload.status,
                "url": azure_upload.url,
                "urlMapping": azure_upload.url_mapping,
            }
        else:
            # No Azure upload attempted - use default
            metadata["azureUpload"] = {
                "status": "not-found",
                "url": "",
                "urlMapping": {},
            }

        # Get config, suites, stats, errors from report
        config = base_report.config if hasattr(base_report, "config") else {}
        suites = base_report.suites if hasattr(base_report, "suites") else []
        stats = base_report.stats if hasattr(base_report, "stats") else {}
        errors = base_report.errors if hasattr(base_report, "errors") else []

        # Convert stats to dict if it's a dataclass
        if hasattr(stats, "__dict__"):
            stats = stats.__dict__

        # Build the payload EXACTLY matching sample-report.json structure
        return {
            "config": config,
            "suites": suites,
            "stats": stats,
            "errors": errors,
            "metadata": metadata,
        }

    async def upload_with_fallback(
        self,
        json_path: str,
        html_dir: Optional[str] = None,
        trace_dir: Optional[str] = None,
    ) -> ReportUploadResponse:
        """Upload with graceful fallback for failed Azure uploads"""
        try:
            # Try full upload first
            return await self.upload_report(json_path, html_dir, trace_dir)

        except NetworkError:
            if html_dir or trace_dir:
                print("⚠️  Full upload failed, attempting JSON-only upload...")

                # Fallback: try JSON-only upload
                try:
                    return await self.upload_report(json_path)  # No HTML/traces
                except Exception as fallback_error:
                    print("❌ Fallback upload also failed")
                    raise fallback_error

            raise
