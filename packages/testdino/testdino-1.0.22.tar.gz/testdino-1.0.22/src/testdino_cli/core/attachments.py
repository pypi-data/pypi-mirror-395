"""Attachment processing utilities for Playwright reports

This module handles scanning, classifying, and processing attachments from Playwright test reports
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Literal, Optional

from testdino_cli.core.parser import PlaywrightReport
from testdino_cli.utils.fs import exists

AttachmentType = Literal["image", "video", "trace", "file", "other"]


@dataclass
class AttachmentInfo:
    """Attachment information extracted from Playwright report"""

    name: str
    content_type: str
    original_path: str
    relative_path: str
    absolute_path: str
    type: AttachmentType


@dataclass
class AttachmentScanResult:
    """Result of attachment scanning process"""

    images: List[AttachmentInfo] = field(default_factory=list)
    videos: List[AttachmentInfo] = field(default_factory=list)
    traces: List[AttachmentInfo] = field(default_factory=list)
    files: List[AttachmentInfo] = field(default_factory=list)
    other: List[AttachmentInfo] = field(default_factory=list)
    total: int = 0


# Content type mappings
CONTENT_TYPE_MAPPING = {
    "image": [
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/gif",
        "image/webp",
        "image/svg+xml",
        "image/bmp",
        "image/tiff",
    ],
    "video": ["video/webm", "video/mp4", "video/avi", "video/mov", "video/mkv"],
    "trace": [
        "application/zip",
        "application/x-zip-compressed",
        "application/octet-stream",
    ],
    "file": [
        "text/markdown",
        "text/plain",
        "application/pdf",
        "text/x-log",
        "application/octet-stream",
    ],
}


class AttachmentScanner:
    """Service for scanning and processing attachments from Playwright reports"""

    def __init__(self, base_directory: str):
        self.base_directory = base_directory

    async def scan_attachments(
        self, report: PlaywrightReport
    ) -> AttachmentScanResult:
        """Scan Playwright report for all attachments"""
        attachments: List[AttachmentInfo] = []

        # Recursively scan all test suites and specs
        for suite in report.suites or []:
            await self._scan_suite(suite, attachments)

        # Classify attachments by type
        result = AttachmentScanResult(total=len(attachments))

        for attachment in attachments:
            if attachment.type == "image":
                result.images.append(attachment)
            elif attachment.type == "video":
                result.videos.append(attachment)
            elif attachment.type == "trace":
                result.traces.append(attachment)
            elif attachment.type == "file":
                result.files.append(attachment)
            else:
                result.other.append(attachment)

        return result

    async def _scan_suite(self, suite: dict, attachments: List[AttachmentInfo]) -> None:
        """Recursively scan a test suite for attachments"""
        # Scan specs in this suite
        if isinstance(suite.get("specs"), list):
            for spec in suite["specs"]:
                await self._scan_spec(spec, attachments)

        # Scan nested suites
        if isinstance(suite.get("suites"), list):
            for nested_suite in suite["suites"]:
                await self._scan_suite(nested_suite, attachments)

    async def _scan_spec(self, spec: dict, attachments: List[AttachmentInfo]) -> None:
        """Scan a spec for attachments"""
        if not isinstance(spec.get("tests"), list):
            return

        for test in spec["tests"]:
            if not isinstance(test.get("results"), list):
                continue

            for result in test["results"]:
                if isinstance(result.get("attachments"), list):
                    for attachment in result["attachments"]:
                        attachment_info = await self._process_attachment(attachment)
                        if attachment_info:
                            attachments.append(attachment_info)

    async def _process_attachment(
        self, attachment: dict
    ) -> Optional[AttachmentInfo]:
        """Process a single attachment and resolve its paths"""
        name = attachment.get("name")
        content_type = attachment.get("contentType")
        path = attachment.get("path")

        if not all([name, content_type, path]):
            return None

        # Resolve paths
        absolute_path = (
            path if os.path.isabs(path) else os.path.join(self.base_directory, path)
        )

        # Check if file exists
        if not await exists(absolute_path):
            print(f"⚠️  Attachment file not found: {absolute_path}")
            return None

        # Calculate relative path
        relative_path = os.path.relpath(absolute_path, self.base_directory)

        # Determine attachment type
        attachment_type = self._classify_attachment(content_type, name)

        return AttachmentInfo(
            name=name,
            content_type=content_type,
            original_path=path,
            relative_path=relative_path,
            absolute_path=absolute_path,
            type=attachment_type,
        )

    def _classify_attachment(
        self, content_type: str, name: str
    ) -> AttachmentType:
        """Classify attachment by content type and name"""
        lower_content_type = content_type.lower()
        lower_name = name.lower()

        # Check content type mappings
        if lower_content_type in CONTENT_TYPE_MAPPING["image"]:
            return "image"

        if lower_content_type in CONTENT_TYPE_MAPPING["video"]:
            return "video"

        if lower_content_type in CONTENT_TYPE_MAPPING["trace"]:
            # Additional check for trace files
            if (
                "trace" in lower_name
                or lower_name.endswith(".trace")
                or lower_name.endswith(".zip")
            ):
                return "trace"

        if lower_content_type in CONTENT_TYPE_MAPPING["file"]:
            return "file"

        # Fallback classification by file extension
        if any(
            lower_name.endswith(ext)
            for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]
        ):
            return "image"

        if any(
            lower_name.endswith(ext) for ext in [".webm", ".mp4", ".avi", ".mov"]
        ):
            return "video"

        if (
            "trace" in lower_name
            or lower_name.endswith(".trace")
            or lower_name.endswith(".zip")
        ):
            return "trace"

        if any(
            lower_name.endswith(ext) for ext in [".md", ".pdf", ".txt", ".log"]
        ):
            return "file"

        return "other"

    @staticmethod
    def filter_attachments(
        scan_result: AttachmentScanResult, config: dict
    ) -> List[AttachmentInfo]:
        """Filter attachments based on configuration flags"""
        filtered: List[AttachmentInfo] = []

        # uploadFullJson overrides all other flags
        if config.get("upload_full_json"):
            filtered.extend(scan_result.images)
            filtered.extend(scan_result.videos)
            filtered.extend(scan_result.files)
            return filtered

        # HTML flag includes images and videos
        if config.get("upload_html"):
            filtered.extend(scan_result.images)
            filtered.extend(scan_result.videos)

        # Individual flags
        if config.get("upload_images") and not config.get("upload_html"):
            filtered.extend(scan_result.images)

        if config.get("upload_videos") and not config.get("upload_html"):
            filtered.extend(scan_result.videos)

        if config.get("upload_files"):
            filtered.extend(scan_result.files)

        if config.get("upload_traces"):
            filtered.extend(scan_result.traces)

        return filtered

    @staticmethod
    def update_attachment_paths(
        report: PlaywrightReport, url_mapping: Dict[str, str], config: Optional[dict] = None
    ) -> PlaywrightReport:
        """Update attachment paths in the JSON report to use Azure URLs"""
        import json

        # Deep clone the report
        updated_report_data = json.loads(report.model_dump_json())

        # Recursively update attachment paths
        def update_suite(suite: dict) -> None:
            if isinstance(suite.get("specs"), list):
                for spec in suite["specs"]:
                    update_spec(spec)

            if isinstance(suite.get("suites"), list):
                for nested_suite in suite["suites"]:
                    update_suite(nested_suite)

        def update_spec(spec: dict) -> None:
            if not isinstance(spec.get("tests"), list):
                return

            for test in spec["tests"]:
                if not isinstance(test.get("results"), list):
                    continue

                for result in test["results"]:
                    if isinstance(result.get("attachments"), list):
                        for attachment in result["attachments"]:
                            if attachment.get("path"):
                                original_path = attachment["path"]

                                # If we have the uploaded URL, use it
                                if original_path in url_mapping:
                                    attachment["path"] = url_mapping[original_path]
                                elif config:
                                    # Determine what action to take based on config
                                    action = AttachmentScanner._get_attachment_path_action(
                                        attachment, config
                                    )
                                    if action == "not-enabled":
                                        attachment["path"] = "Not Enabled"
                                    elif action == "not-supported":
                                        attachment["path"] = "Not Supported"

        # Update all suites
        for suite in updated_report_data.get("suites", []):
            update_suite(suite)

        # Return updated report
        return PlaywrightReport(**updated_report_data)

    @staticmethod
    def _get_attachment_path_action(attachment: dict, config: dict) -> str:
        """Determine what should happen to an attachment path based on config"""
        content_type = attachment.get("contentType", "").lower()
        name = attachment.get("name", "").lower()

        # Classify the attachment type
        scanner = AttachmentScanner("")
        attachment_type = scanner._classify_attachment(content_type, name)

        # uploadFullJson overrides everything
        if config.get("upload_full_json"):
            if attachment_type in ["image", "video", "file"]:
                return "upload"
            elif attachment_type == "trace":
                return "not-supported"
            return "unchanged"

        # Determine action based on type and config
        if attachment_type == "image":
            return (
                "upload"
                if config.get("upload_images") or config.get("upload_html")
                else "not-enabled"
            )
        elif attachment_type == "video":
            return (
                "upload"
                if config.get("upload_videos") or config.get("upload_html")
                else "not-enabled"
            )
        elif attachment_type == "file":
            return "upload" if config.get("upload_files") else "not-enabled"
        elif attachment_type == "trace":
            return "upload" if config.get("upload_traces") else "not-enabled"

        return "unchanged"
