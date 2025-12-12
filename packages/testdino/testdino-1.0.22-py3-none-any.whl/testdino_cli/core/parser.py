"""Playwright JSON report parser"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from testdino_cli.types import ValidationError
from testdino_cli.utils.fs import read_file


class PlaywrightStats(BaseModel):
    """Playwright test statistics"""

    startTime: str
    duration: float
    expected: int
    skipped: int
    unexpected: int
    flaky: int


class PlaywrightReport(BaseModel):
    """Playwright report structure"""

    config: Any
    suites: List[Any]
    stats: PlaywrightStats
    errors: Optional[List[Any]] = Field(default_factory=list)
    metadata: Optional[Any] = None


async def parse_playwright_json(json_path: str) -> PlaywrightReport:
    """
    Read, parse, and validate a Playwright JSON report from disk

    Args:
        json_path: Absolute path to the Playwright JSON report

    Raises:
        ValidationError: If reading, parsing, or validation fails

    Returns:
        Validated PlaywrightReport object
    """
    try:
        raw = await read_file(json_path)
    except Exception as error:
        raise ValidationError(
            f'Failed to read JSON report at "{json_path}": {error}'
        )

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValidationError(f"Invalid JSON format in report: {error}")

    try:
        return PlaywrightReport(**parsed)
    except Exception as error:
        raise ValidationError(f"Playwright report validation failed: {error}")
