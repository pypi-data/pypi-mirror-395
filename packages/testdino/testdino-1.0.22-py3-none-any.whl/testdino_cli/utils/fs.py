"""File system utilities"""

import os
from pathlib import Path
from typing import List

from testdino_cli.types import FileSystemError
from testdino_cli.utils.validation import ValidationUtils


def resolve_path(p: str, context: str) -> str:
    """Validate and resolve a file or directory path"""
    ValidationUtils.validate_file_path(p, context)
    return str(Path(p).resolve())


async def exists(p: str) -> bool:
    """Check if a path exists"""
    return Path(p).exists()


async def is_directory(p: str) -> bool:
    """
    Check if the given path is a directory.
    Returns false if the path doesn't exist or is not accessible.
    """
    try:
        return Path(p).is_dir()
    except Exception:
        # Return false if path doesn't exist or is not accessible
        # This allows graceful handling in discovery logic
        return False


async def is_file(p: str) -> bool:
    """
    Check if the given path is a file.
    Returns false if the path doesn't exist or is not accessible.
    """
    try:
        return Path(p).is_file()
    except Exception:
        # Return false if path doesn't exist or is not accessible
        # This allows graceful handling in discovery logic
        return False


async def read_dir(p: str) -> List[str]:
    """Read directory contents and return full paths"""
    try:
        path = Path(p)
        return [str(path / name) for name in os.listdir(p)]
    except Exception as error:
        raise FileSystemError(f"Failed to read directory: {p}", error)


async def read_file(p: str) -> str:
    """Read file as text"""
    try:
        return Path(p).read_text(encoding="utf-8")
    except Exception as error:
        raise FileSystemError(f"Failed to read file: {p}", error)


async def read_file_buffer(p: str) -> bytes:
    """Read file as bytes"""
    try:
        return Path(p).read_bytes()
    except Exception as error:
        raise FileSystemError(f"Failed to read file buffer: {p}", error)
