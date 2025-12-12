"""Azure storage client for uploading files using SAS-based authentication"""

import asyncio
from pathlib import Path
from typing import Callable, List, Optional

import httpx

from testdino_cli.services.sas import SasTokenResponse
from testdino_cli.utils.files import collect_file_paths, collect_file_paths_for_html, get_content_type
from testdino_cli.utils.fs import read_file_buffer
from testdino_cli.utils.retry import with_file_upload_retry
from testdino_cli.utils.verbose import is_verbose_mode

# Type for progress callback
ProgressCallback = Callable[[int, int, str], None]


class AzureStorageClient:
    """Azure storage client configured with SAS-based authentication"""

    def __init__(self, sas_response: SasTokenResponse):
        self.sas_response = sas_response

    async def upload_file(self, file_path: str, blob_path: str) -> str:
        """Upload a single file using the SAS token response format"""
        # Pre-validate file type before attempting upload
        allowed_types = self.sas_response.upload_instructions.allowed_file_types
        file_extension = file_path.split(".")[-1].lower() if "." in file_path else ""

        if allowed_types and file_extension not in allowed_types:
            raise Exception(
                f"File type '{file_extension}' not allowed. Allowed types: {', '.join(allowed_types)}"
            )

        # Build the complete upload URL using the SAS response format
        base_url = self.sas_response.upload_instructions.base_url
        path_prefix = self.sas_response.upload_instructions.path_prefix

        # Combine path prefix with blob path
        full_blob_path = f"{path_prefix}/{blob_path}"

        # Build upload URL (baseUrl already contains SAS token)
        upload_url = (
            f"{base_url.split('?')[0]}/{full_blob_path}?{self.sas_response.sas_token}"
        )

        # Read file data
        data = await read_file_buffer(file_path)

        # Detect content type
        content_type = get_content_type(file_path)

        # Validate file size
        if len(data) > self.sas_response.upload_instructions.max_file_size:
            size_mb = round(len(data) / (1024 * 1024))
            max_size_mb = round(
                self.sas_response.upload_instructions.max_file_size / (1024 * 1024)
            )
            raise Exception(f"File too large: {size_mb}MB (max: {max_size_mb}MB)")

        # Prepare headers based on Azure Blob Storage requirements
        headers = {
            "x-ms-blob-type": "BlockBlob",
            "Content-Type": content_type,
            "Content-Length": str(len(data)),
        }

        # Upload file using PUT request
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.put(upload_url, headers=headers, content=data)

            if not response.is_success:
                error_text = response.text
                raise Exception(
                    f"TestDino platform upload failed: {response.status_code} {error_text}"
                )

        # Return the public URL (without SAS token for public access)
        return f"{self.sas_response.container_url}/{full_blob_path}"


class AzureUploadService:
    """Service to upload files to Azure Blob Storage using SAS credentials with optimal concurrency"""

    def __init__(self, storage_client: AzureStorageClient):
        self.storage_client = storage_client
        self.max_concurrent_uploads = 5  # Optimal for most scenarios

    async def upload_directory(
        self,
        local_dir: str,
        prefix: str = "",
        on_progress: Optional[ProgressCallback] = None,
        pre_filtered_paths: Optional[List[str]] = None,
    ) -> List[str]:
        """Upload an entire directory of files with concurrent uploads and progress tracking"""
        # Use provided file paths or collect all files recursively
        file_paths = (
            pre_filtered_paths if pre_filtered_paths else await collect_file_paths(local_dir)
        )

        uploaded_urls: List[str] = []
        uploaded_count = 0

        # Upload files in batches for optimal performance
        batches = self._create_batches(file_paths, self.max_concurrent_uploads)

        for batch in batches:
            # Upload batch concurrently
            tasks = []
            for file_path in batch:
                task = self._upload_file_with_progress(
                    file_path,
                    local_dir,
                    prefix,
                    uploaded_urls,
                    on_progress,
                    len(file_paths),
                )
                tasks.append(task)

            # Wait for current batch to complete before starting next
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Count successful uploads
            for result in results:
                if result is not None and not isinstance(result, Exception):
                    uploaded_count += 1

        return uploaded_urls

    async def _upload_file_with_progress(
        self,
        file_path: str,
        local_dir: str,
        prefix: str,
        uploaded_urls: List[str],
        on_progress: Optional[ProgressCallback],
        total_files: int,
    ) -> Optional[str]:
        """Upload a single file with progress tracking"""
        try:
            # Compute blob path: prefix + relative path from directory
            relative_path = self._get_relative_path(file_path, local_dir)
            blob_path = f"{prefix}/{relative_path}" if prefix else relative_path

            # Upload with retry logic
            upload_url = await with_file_upload_retry(
                lambda: self.storage_client.upload_file(file_path, blob_path),
                file_path,
            )

            uploaded_urls.append(upload_url)

            # Report progress
            if on_progress:
                on_progress(len(uploaded_urls), total_files, relative_path)

            return upload_url
        except Exception:
            # Show warnings only for critical files or if verbose is enabled
            is_important_file = "index.html" in file_path or ".json" in file_path
            if is_important_file or is_verbose_mode():
                file_name = Path(file_path).name
                print(f"⚠️  Skipped: {file_name}")
            return None

    def _get_relative_path(self, file_path: str, local_dir: str) -> str:
        """Get relative path from a local directory"""
        # Normalize paths to handle different OS separators
        normalized_file_path = file_path.replace("\\", "/")
        normalized_local_dir = local_dir.replace("\\", "/").rstrip("/")

        # Remove the local directory prefix to get relative path
        relative_path = normalized_file_path.replace(f"{normalized_local_dir}/", "")

        # Handle edge case where local dir doesn't end with /
        if relative_path == normalized_file_path:
            relative_path = normalized_file_path.replace(normalized_local_dir, "")
            if relative_path.startswith("/"):
                relative_path = relative_path[1:]

        return relative_path

    def _create_batches(self, items: List[str], batch_size: int) -> List[List[str]]:
        """Create batches of files for concurrent upload"""
        batches: List[List[str]] = []
        for i in range(0, len(items), batch_size):
            batches.append(items[i : i + batch_size])
        return batches

    async def upload_directory_with_progress(
        self, local_dir: str, prefix: str = ""
    ) -> List[str]:
        """Upload with progress reporting and detailed feedback"""
        file_paths = await collect_file_paths(local_dir)
        print(f"📁 Uploading {len(file_paths)} files to TestDino platform...")

        last_progress_time = asyncio.get_event_loop().time()

        def progress_callback(uploaded: int, total: int, current_file: str) -> None:
            nonlocal last_progress_time
            now = asyncio.get_event_loop().time()

            # Update progress every 500ms to avoid spam
            if now - last_progress_time > 0.5:
                percentage = round((uploaded / total) * 100)
                print(f"   📤 {percentage}% ({uploaded}/{total}) - {current_file}")
                last_progress_time = now

        uploaded_urls = await self.upload_directory(
            local_dir, prefix, progress_callback
        )

        print(f"✅ {len(uploaded_urls)} files uploaded successfully")
        return uploaded_urls

    async def upload_html_directory_with_progress(
        self,
        local_dir: str,
        prefix: str = "",
        config: Optional[dict] = None,
    ) -> List[str]:
        """Upload HTML directory with filtering based on upload configuration"""
        file_paths = await collect_file_paths_for_html(local_dir, True, config)

        # Create descriptive message based on config
        parts = []
        if config and config.get("uploadHtml"):
            parts.append("HTML")
        if config and config.get("uploadImages"):
            parts.append("images")
        if config and config.get("uploadVideos"):
            parts.append("videos")

        filter_description = " + ".join(parts) if parts else "files"

        print(
            f"📁 Uploading {len(file_paths)} files ({filter_description}) to TestDino platform..."
        )

        last_progress_time = asyncio.get_event_loop().time()

        def progress_callback(uploaded: int, total: int, current_file: str) -> None:
            nonlocal last_progress_time
            now = asyncio.get_event_loop().time()

            # Update progress every 500ms to avoid spam
            if now - last_progress_time > 0.5:
                percentage = round((uploaded / total) * 100)
                print(f"   📤 {percentage}% ({uploaded}/{total}) - {current_file}")
                last_progress_time = now

        uploaded_urls = await self.upload_directory(
            local_dir, prefix, progress_callback, file_paths
        )

        print(f"✅ {len(uploaded_urls)} HTML report files uploaded successfully")
        return uploaded_urls
