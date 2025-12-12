"""Playwright configuration and shard detection utilities"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from testdino_cli.utils.fs import exists, read_file_buffer


@dataclass
class ShardInfo:
    """Shard information detected from Playwright configuration"""

    shard_index: int
    shard_total: int
    shard_id: str


class PlaywrightShardDetector:
    """Playwright configuration parser for shard detection"""

    @staticmethod
    async def detect_shard_info(working_dir: str) -> Optional[ShardInfo]:
        """Auto-detect shard information from Playwright configuration and environment"""
        try:
            # Strategy 1: Check environment variables first (most reliable in CI)
            env_shard = PlaywrightShardDetector._detect_from_environment()
            if env_shard:
                return env_shard

            # Strategy 2: Read from Playwright configuration files
            config_shard = await PlaywrightShardDetector._detect_from_playwright_config(
                working_dir
            )
            if config_shard:
                return config_shard

            # Strategy 3: Analyze JSON reports for shard indicators
            report_shard = await PlaywrightShardDetector._detect_from_reports(
                working_dir
            )
            if report_shard:
                return report_shard

            return None
        except Exception:
            return None

    @staticmethod
    def _detect_from_environment() -> Optional[ShardInfo]:
        """Detect shard info from environment variables"""
        try:
            env = os.environ

            # GitHub Actions matrix strategy
            if env.get("GITHUB_ACTIONS") and env.get("SHARD_INDEX") and env.get(
                "SHARD_TOTAL"
            ):
                shard_index = int(env["SHARD_INDEX"])
                shard_total = int(env["SHARD_TOTAL"])

                if shard_index > 0 and shard_total > 0:
                    return ShardInfo(
                        shard_index=shard_index,
                        shard_total=shard_total,
                        shard_id=f"{shard_index}/{shard_total}",
                    )

            # GitLab CI parallel jobs
            if env.get("GITLAB_CI") and env.get("CI_NODE_INDEX") and env.get(
                "CI_NODE_TOTAL"
            ):
                shard_index = int(env["CI_NODE_INDEX"]) + 1  # GitLab is 0-indexed
                shard_total = int(env["CI_NODE_TOTAL"])

                if shard_index > 0 and shard_total > 0:
                    return ShardInfo(
                        shard_index=shard_index,
                        shard_total=shard_total,
                        shard_id=f"{shard_index}/{shard_total}",
                    )

            # CircleCI parallelism
            if env.get("CIRCLECI") and env.get("CIRCLE_NODE_INDEX") and env.get(
                "CIRCLE_NODE_TOTAL"
            ):
                shard_index = int(env["CIRCLE_NODE_INDEX"]) + 1  # CircleCI is 0-indexed
                shard_total = int(env["CIRCLE_NODE_TOTAL"])

                if shard_index > 0 and shard_total > 0:
                    return ShardInfo(
                        shard_index=shard_index,
                        shard_total=shard_total,
                        shard_id=f"{shard_index}/{shard_total}",
                    )

            # Generic environment variables
            if env.get("SHARD_INDEX") and env.get("SHARD_TOTAL"):
                shard_index = int(env["SHARD_INDEX"])
                shard_total = int(env["SHARD_TOTAL"])

                if shard_index > 0 and shard_total > 0:
                    return ShardInfo(
                        shard_index=shard_index,
                        shard_total=shard_total,
                        shard_id=f"{shard_index}/{shard_total}",
                    )

            return None
        except Exception:
            return None

    @staticmethod
    async def _detect_from_playwright_config(
        working_dir: str,
    ) -> Optional[ShardInfo]:
        """Detect shard info from Playwright configuration files"""
        config_files = [
            "playwright.config.ts",
            "playwright.config.js",
            "playwright.config.mjs",
            "playwright.config.cjs",
        ]

        for config_file in config_files:
            config_path = Path(working_dir) / config_file

            if await exists(str(config_path)):
                try:
                    config_content = await read_file_buffer(str(config_path))
                    config_text = config_content.decode()

                    # Look for shard configuration patterns
                    shard_match = re.search(r"shard:\s*(\d+)\s*/\s*(\d+)", config_text)
                    if shard_match:
                        shard_index = int(shard_match.group(1))
                        shard_total = int(shard_match.group(2))

                        return ShardInfo(
                            shard_index=shard_index,
                            shard_total=shard_total,
                            shard_id=f"{shard_index}/{shard_total}",
                        )

                    # Look for CLI shard argument patterns
                    cli_shard_match = re.search(
                        r"--shard[=\s]+(\d+)/(\d+)", config_text
                    )
                    if cli_shard_match:
                        shard_index = int(cli_shard_match.group(1))
                        shard_total = int(cli_shard_match.group(2))

                        return ShardInfo(
                            shard_index=shard_index,
                            shard_total=shard_total,
                            shard_id=f"{shard_index}/{shard_total}",
                        )

                except Exception:
                    continue

        return None

    @staticmethod
    async def _detect_from_reports(working_dir: str) -> Optional[ShardInfo]:
        """Detect shard info from JSON reports"""
        try:
            # Common report locations
            report_paths = [
                Path(working_dir) / "playwright-report" / "report.json",
                Path(working_dir) / "playwright-report" / "results.json",
                Path(working_dir) / "test-results" / "results.json",
                Path(working_dir) / "test-results" / "report.json",
                Path(working_dir) / "results.json",
                Path(working_dir) / "report.json",
            ]

            for report_path in report_paths:
                if await exists(str(report_path)):
                    try:
                        report_content = await read_file_buffer(str(report_path))
                        report_text = report_content.decode()

                        # Parse JSON to extract shard information
                        try:
                            report_json = json.loads(report_text)

                            # Check for Playwright's config.shard structure
                            if (
                                report_json.get("config", {}).get("shard")
                                and isinstance(
                                    report_json["config"]["shard"], dict
                                )
                            ):
                                shard = report_json["config"]["shard"]

                                if isinstance(shard.get("current"), int) and isinstance(
                                    shard.get("total"), int
                                ):
                                    shard_index = shard["current"]
                                    shard_total = shard["total"]

                                    if (
                                        shard_index > 0
                                        and shard_total > 0
                                        and shard_index <= shard_total
                                    ):
                                        return ShardInfo(
                                            shard_index=shard_index,
                                            shard_total=shard_total,
                                            shard_id=f"{shard_index}/{shard_total}",
                                        )
                        except Exception:
                            pass

                    except Exception:
                        continue

            return None
        except Exception:
            return None

    @staticmethod
    def validate_shard_info(shard_info: ShardInfo) -> bool:
        """Validate shard information"""
        return (
            shard_info.shard_index > 0
            and shard_info.shard_total > 0
            and shard_info.shard_index <= shard_info.shard_total
            and shard_info.shard_id
            == f"{shard_info.shard_index}/{shard_info.shard_total}"
        )

    @staticmethod
    def create_default_shard_info() -> ShardInfo:
        """Create default shard info (single shard)"""
        return ShardInfo(shard_index=1, shard_total=1, shard_id="1/1")
