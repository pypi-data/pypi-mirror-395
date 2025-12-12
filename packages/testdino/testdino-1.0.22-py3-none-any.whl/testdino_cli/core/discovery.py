"""Playwright test report file discovery service

This module provides smart scanning to find Playwright test reports in a given directory
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from testdino_cli.core.validators import (
    validate_html_report_dir,
    validate_json_report,
    validate_trace_dir,
)
from testdino_cli.types import CLIOptions, FileSystemError
from testdino_cli.utils.fs import exists, is_directory, read_dir, read_file, resolve_path


@dataclass
class DiscoveryResult:
    """Result of the discovery process"""

    json_report: str
    html_report: Optional[str] = None
    trace_dir: Optional[str] = None


class ReportDiscoveryService:
    """Service to discover Playwright test report files with smart scanning"""

    def __init__(self, report_dir: str):
        self.report_dir = report_dir

    async def discover(self, options: CLIOptions) -> DiscoveryResult:
        """Discover report files based on CLI options with smart scanning"""
        base_dir = resolve_path(options.report_directory, 'Report directory')

        # JSON report discovery with manual override
        json_report_path = (
            options.json_report if options.json_report else await self.find_json_report(str(base_dir))
        )
        await validate_json_report(json_report_path)

        # HTML report discovery (only if upload requested)
        html_report_dir: Optional[str] = None
        if options.upload_html:
            html_report_dir = (
                options.html_report if options.html_report else await self.find_html_report(str(base_dir))
            )
            if html_report_dir:
                await validate_html_report_dir(html_report_dir)

        # Trace files discovery
        trace_directory: Optional[str] = None
        if options.upload_traces:
            # Check if traces are available in JSON attachments first
            has_traces_in_json = await self._check_traces_in_json_report(
                json_report_path
            )

            if not has_traces_in_json:
                # No traces in JSON, try to find trace directory
                if options.trace_dir:
                    await validate_trace_dir(options.trace_dir)
                    trace_directory = options.trace_dir
                else:
                    # Auto-discover traces
                    trace_directory = await self.find_trace_dir(str(base_dir))
                    if trace_directory:
                        await validate_trace_dir(trace_directory)

        return DiscoveryResult(
            json_report=json_report_path,
            html_report=html_report_dir,
            trace_dir=trace_directory,
        )

    async def find_json_report(self, base_dir: str) -> str:
        """Smart JSON report discovery - scan for valid Playwright JSON files"""
        base_path = Path(base_dir)

        # Try common patterns first
        common_patterns = [
            base_path / "report.json",
            base_path / "results.json",
            base_path / "test-results.json",
            base_path / "playwright-report" / "report.json",
            base_path / "playwright-report" / "results.json",
        ]

        for candidate in common_patterns:
            if candidate.exists() and await self._is_valid_playwright_json(
                str(candidate)
            ):
                return str(candidate)

        # If no common patterns found, scan all JSON files
        json_files = await self._scan_for_json_files(base_dir)
        for json_file in json_files:
            if await self._is_valid_playwright_json(json_file):
                return json_file

        raise FileSystemError(
            f"No valid Playwright JSON report found in {base_dir}.\n"
            "💡 Looked for: report.json, results.json, test-results.json\n"
            "💡 Use --json-report <path> to specify exact location"
        )

    async def find_html_report(self, base_dir: str) -> str:
        """Smart HTML report discovery - find directory containing index.html"""
        base_path = Path(base_dir)

        # Try common patterns
        common_patterns = [
            base_path,
            base_path / "html-report",
            base_path / "playwright-report",
            base_path / "report",
            base_path / "test-report",
            base_path / "html",
        ]

        for candidate in common_patterns:
            if candidate.is_dir() and (candidate / "index.html").exists():
                return str(candidate)

        # Scan for any directory containing index.html
        html_dirs = await self._scan_for_html_directories(base_dir)
        if html_dirs:
            return html_dirs[0]

        raise FileSystemError(
            f"No HTML report directory with index.html found in {base_dir}.\n"
            "💡 Use --html-report <path> to specify exact location"
        )

    async def find_trace_dir(self, base_dir: str) -> Optional[str]:
        """Smart trace directory discovery"""
        base_path = Path(base_dir)

        # Try common patterns
        common_patterns = [
            base_path / "trace",
            base_path / "traces",
            base_path / "test-results",
            base_path / "playwright-report" / "trace",
            base_path / "playwright-report" / "traces",
        ]

        for candidate in common_patterns:
            if candidate.is_dir() and await self._contains_trace_files(str(candidate)):
                return str(candidate)

        # Scan for directories containing trace files
        trace_dirs = await self._scan_for_trace_directories(base_dir)
        if trace_dirs:
            return trace_dirs[0]

        return None

    async def _check_traces_in_json_report(self, json_path: str) -> bool:
        """Check if JSON report contains trace files in attachments"""
        try:
            content = await read_file(json_path)
            data = json.loads(content)

            if not data.get("suites") or not isinstance(data["suites"], list):
                return False

            return self._has_trace_attachments(data["suites"])
        except Exception:
            return False

    def _has_trace_attachments(self, suites: list) -> bool:
        """Recursively check if suites contain trace attachments"""
        for suite in suites:
            # Check specs in this suite
            if isinstance(suite.get("specs"), list):
                for spec in suite["specs"]:
                    if self._has_trace_attachments_in_spec(spec):
                        return True

            # Check nested suites
            if isinstance(suite.get("suites"), list):
                if self._has_trace_attachments(suite["suites"]):
                    return True

        return False

    def _has_trace_attachments_in_spec(self, spec: dict) -> bool:
        """Check if a spec contains trace attachments"""
        if not isinstance(spec.get("tests"), list):
            return False

        for test in spec["tests"]:
            if not isinstance(test.get("results"), list):
                continue

            for result in test["results"]:
                if isinstance(result.get("attachments"), list):
                    for attachment in result["attachments"]:
                        if self._is_trace_attachment(attachment):
                            return True

        return False

    def _is_trace_attachment(self, attachment: dict) -> bool:
        """Check if an attachment is a trace file"""
        name = (attachment.get("name") or "").lower()
        content_type = (attachment.get("contentType") or "").lower()

        trace_content_types = [
            "application/zip",
            "application/x-zip-compressed",
            "application/octet-stream",
        ]

        if content_type in trace_content_types:
            if "trace" in name or name.endswith(".trace") or name.endswith(".zip"):
                return True

        return "trace" in name or name.endswith(".trace")

    async def _is_valid_playwright_json(self, file_path: str) -> bool:
        """Validate if a JSON file is a valid Playwright report"""
        try:
            content = await read_file(file_path)
            data = json.loads(content)

            return (
                isinstance(data, dict)
                and "config" in data
                and "suites" in data
                and "stats" in data
                and isinstance(data.get("suites"), list)
            )
        except Exception:
            return False

    async def _scan_for_json_files(
        self, directory: str, max_depth: int = 2
    ) -> List[str]:
        """Scan directory recursively for JSON files"""
        json_files: List[str] = []

        try:
            await self._scan_directory(
                directory, json_files, lambda f: f.endswith(".json"), 0, max_depth
            )
        except Exception:
            pass

        return json_files

    async def _scan_for_html_directories(
        self, directory: str, max_depth: int = 2
    ) -> List[str]:
        """Scan for directories containing index.html"""
        html_dirs: List[str] = []

        try:
            await self._scan_directory_for_html(directory, html_dirs, 0, max_depth)
        except Exception:
            pass

        return html_dirs

    async def _scan_for_trace_directories(
        self, directory: str, max_depth: int = 2
    ) -> List[str]:
        """Scan for directories containing trace files"""
        trace_dirs: List[str] = []

        try:
            await self._scan_directory_for_traces(directory, trace_dirs, 0, max_depth)
        except Exception:
            pass

        return trace_dirs

    async def _scan_directory(
        self,
        directory: str,
        results: List[str],
        file_filter,
        current_depth: int,
        max_depth: int,
    ) -> None:
        """Generic directory scanner for files"""
        if current_depth > max_depth:
            return

        entries = await read_dir(directory)

        for entry in entries:
            if await is_directory(entry):
                await self._scan_directory(
                    entry, results, file_filter, current_depth + 1, max_depth
                )
            elif file_filter(entry):
                results.append(entry)

    async def _scan_directory_for_html(
        self, directory: str, results: List[str], current_depth: int, max_depth: int
    ) -> None:
        """Scan for HTML directories"""
        if current_depth > max_depth:
            return

        # Check if current directory has index.html
        index_path = Path(directory) / "index.html"
        if index_path.exists():
            results.append(directory)
            return

        # Scan subdirectories
        entries = await read_dir(directory)
        for entry in entries:
            if await is_directory(entry):
                await self._scan_directory_for_html(
                    entry, results, current_depth + 1, max_depth
                )

    async def _scan_directory_for_traces(
        self, directory: str, results: List[str], current_depth: int, max_depth: int
    ) -> None:
        """Scan for trace directories"""
        if current_depth > max_depth:
            return

        # Check if current directory contains trace files
        if await self._contains_trace_files(directory):
            results.append(directory)
            return

        # Scan subdirectories
        entries = await read_dir(directory)
        for entry in entries:
            if await is_directory(entry):
                await self._scan_directory_for_traces(
                    entry, results, current_depth + 1, max_depth
                )

    async def _contains_trace_files(self, directory: str) -> bool:
        """Check if directory contains trace files"""
        try:
            entries = await read_dir(directory)
            return any(
                entry.endswith(".zip") or entry.endswith(".trace") or "trace" in entry.lower()
                for entry in entries
            )
        except Exception:
            return False
