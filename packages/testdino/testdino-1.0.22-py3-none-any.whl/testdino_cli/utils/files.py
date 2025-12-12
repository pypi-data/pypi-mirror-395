"""File collection and filtering utilities"""

import os
from typing import List, Optional, Set

from testdino_cli.types import FileSystemError
from testdino_cli.utils.fs import is_directory, is_file, read_dir
from testdino_cli.utils.verbose import is_verbose_mode


async def collect_file_paths(dir_path: str) -> List[str]:
    """Recursively collect all file paths under a directory"""
    files: List[str] = []
    try:
        entries = await read_dir(dir_path)
        for entry in entries:
            if await is_directory(entry):
                nested = await collect_file_paths(entry)
                files.extend(nested)
            elif await is_file(entry):
                files.append(entry)
        return files
    except Exception as error:
        raise FileSystemError(
            f"Failed to collect files from directory: {dir_path}", error
        )


# File extension sets for filtering HTML report uploads
HTML_REPORT_ALLOWED_EXTENSIONS: Set[str] = {
    # HTML files
    "html",
    "htm",
    # CSS and JavaScript (needed for HTML reports)
    "css",
    "js",
    "mjs",
    # Images
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
    "svg",
    "bmp",
    "tiff",
    # Videos
    "webm",
    "mp4",
    "avi",
    "mov",
    "mkv",
    # Other web assets (excluding json)
    "ico",
    "woff",
    "woff2",
    "ttf",
    "eot",
}


def is_allowed_for_html_upload(
    file_path: str,
    config: Optional[dict] = None,
) -> bool:
    """Check if a file should be included in HTML report uploads"""
    ext = file_path.lower().split(".")[-1] if "." in file_path else ""

    # If no config provided, use the default behavior (all allowed extensions)
    if not config:
        return ext in HTML_REPORT_ALLOWED_EXTENSIONS

    upload_images = config.get("uploadImages", False)
    upload_videos = config.get("uploadVideos", False)
    upload_html = config.get("uploadHtml", False)

    # HTML, CSS, JS, and web assets only allowed with --upload-html
    web_assets = ["html", "htm", "css", "js", "mjs", "ico", "woff", "woff2", "ttf", "eot"]
    if ext in web_assets:
        return upload_html

    # Exclude files with "trace" in the name for HTML uploads
    file_name = file_path.lower().split("/")[-1]
    if upload_html and "trace" in file_name:
        return False

    # Apply filtering based on config for media files
    image_extensions = ["png", "jpg", "jpeg", "gif", "webp", "svg", "bmp", "tiff"]
    video_extensions = ["webm", "mp4", "avi", "mov", "mkv"]

    if ext in image_extensions:
        return upload_images or upload_html

    if ext in video_extensions:
        return upload_videos or upload_html

    # Other extensions not allowed
    return False


async def collect_file_paths_for_html(
    dir_path: str,
    filter_for_html: bool = False,
    config: Optional[dict] = None,
    _is_top_level: bool = True,
) -> List[str]:
    """Recursively collect file paths with optional filtering for HTML uploads"""
    files: List[str] = []
    skipped_count = 0

    try:
        entries = await read_dir(dir_path)
        for entry in entries:
            if await is_directory(entry):
                # Skip trace directories when uploading HTML
                dir_name = entry.lower().split("/")[-1]
                if config and config.get("uploadHtml") and "trace" in dir_name:
                    continue  # Skip trace directories silently

                nested = await collect_file_paths_for_html(
                    entry, filter_for_html, config, _is_top_level=False
                )
                files.extend(nested)
            elif await is_file(entry):
                # Apply filtering if requested
                if not filter_for_html or is_allowed_for_html_upload(entry, config):
                    files.append(entry)
                elif filter_for_html:
                    skipped_count += 1

        # Only print at top level to avoid multiple messages
        if (
            _is_top_level
            and filter_for_html
            and skipped_count > 0
            and (os.environ.get("LOG_LEVEL") == "debug" or is_verbose_mode())
        ):
            print(f"🚫 Filtered {skipped_count} files (traces, logs, etc.)")

        return files
    except Exception as error:
        raise FileSystemError(
            f"Failed to collect files from directory: {dir_path}", error
        )


def get_content_type(file_path: str) -> str:
    """Basic content-type detection based on file extension"""
    ext = file_path.lower().split(".")[-1] if "." in file_path else ""

    content_types = {
        "html": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "json": "application/json",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "svg": "image/svg+xml",
        "webm": "video/webm",
        "webp": "image/webp",
        "zip": "application/zip",
        "txt": "text/plain",
        "md": "text/plain; charset=utf-8",
        "pdf": "application/pdf",
        "log": "text/plain; charset=utf-8",
    }

    return content_types.get(ext, "application/octet-stream")
