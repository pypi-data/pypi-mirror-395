"""Validators for Playwright reports"""

import json
from pathlib import Path

from testdino_cli.types import FileSystemError, ValidationError


async def validate_json_report(json_path: str) -> None:
    """Validate that the JSON report exists and is parsable"""
    path = Path(json_path)

    try:
        if not path.exists():
            raise FileSystemError(f"JSON report not found: {json_path}")
        if not path.is_file():
            raise ValidationError(f"JSON report path is not a file: {json_path}")
    except (FileSystemError, ValidationError):
        raise
    except Exception as error:
        raise FileSystemError(f"JSON report not found: {json_path}", error)

    try:
        content = path.read_text(encoding="utf-8")
        json.loads(content)
    except json.JSONDecodeError as error:
        raise ValidationError(f"Failed to parse JSON report: {error}")
    except Exception as error:
        raise FileSystemError(f"Failed to read JSON report: {json_path}", error)


async def validate_html_report_dir(html_dir: str) -> None:
    """Validate that the HTML report directory exists and contains index.html"""
    path = Path(html_dir)

    try:
        if not path.exists():
            raise FileSystemError(f"HTML report directory not found: {html_dir}")
        if not path.is_dir():
            raise ValidationError(f"HTML report path is not a directory: {html_dir}")
    except (FileSystemError, ValidationError):
        raise
    except Exception as error:
        raise FileSystemError(f"HTML report directory not found: {html_dir}", error)

    index_path = path / "index.html"
    if not index_path.exists() or not index_path.is_file():
        raise ValidationError(
            f"index.html not found in HTML report directory: {html_dir}"
        )


async def validate_trace_dir(trace_dir: str) -> None:
    """Validate that the trace directory exists"""
    path = Path(trace_dir)

    try:
        if not path.exists():
            raise FileSystemError(f"Trace directory not found: {trace_dir}")
        if not path.is_dir():
            raise ValidationError(f"Trace path is not a directory: {trace_dir}")
    except (FileSystemError, ValidationError):
        raise
    except Exception as error:
        raise FileSystemError(f"Trace directory not found: {trace_dir}", error)
