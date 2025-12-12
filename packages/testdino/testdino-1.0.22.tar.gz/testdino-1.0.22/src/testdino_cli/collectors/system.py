"""System metadata collector"""

import os
import platform
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class CPUInfo:
    """CPU information"""

    count: int
    model: str


@dataclass
class MemoryInfo:
    """Memory information"""

    total: str


@dataclass
class SystemMetadata:
    """System metadata structure matching server schema

    Note: The 'nodejs' field is named for API compatibility with the TypeScript CLI.
    In the Python CLI, this field contains the Python version instead of Node.js version.
    The server API expects this field name, so we keep it for backwards compatibility.
    """

    hostname: str
    cpu: CPUInfo
    memory: MemoryInfo
    os: str
    # Named 'nodejs' for API compatibility - contains Python version in Python CLI
    nodejs: str
    playwright: str


class SystemCollector:
    """Collector for system metadata"""

    @staticmethod
    def collect() -> SystemMetadata:
        """Gather system metadata"""
        hostname = platform.node() or "unknown"

        # CPU information
        try:
            cpu_count = os.cpu_count() or 0
        except Exception:
            cpu_count = 0

        try:
            # Try to get CPU model (platform-specific)
            if platform.system() == "Linux":
                with open("/proc/cpuinfo") as f:
                    for line in f:
                        if line.strip().startswith("model name"):
                            cpu_model = line.split(":", 1)[1].strip()
                            break
                    else:
                        cpu_model = platform.processor() or "unknown"
            else:
                cpu_model = platform.processor() or "unknown"
        except Exception:
            cpu_model = "unknown"

        # Memory information
        try:
            import psutil

            total_mem_bytes = psutil.virtual_memory().total
            total_mem_gb = round(total_mem_bytes / (1024**3))
            memory_total = (
                f"{total_mem_gb} GB" if total_mem_bytes > 0 else "unknown"
            )
        except ImportError:
            # Fallback if psutil is not available
            memory_total = "unknown"

        os_info = f"{platform.system()} {platform.release()}"
        python_version = f"Python {sys.version.split()[0]}"

        playwright_version = SystemCollector._get_playwright_version()

        return SystemMetadata(
            hostname=hostname,
            cpu=CPUInfo(count=cpu_count, model=cpu_model),
            memory=MemoryInfo(total=memory_total),
            os=os_info,
            nodejs=python_version,  # Changed from Node.js to Python version
            playwright=playwright_version,
        )

    @staticmethod
    def _get_playwright_version() -> str:
        """Attempt to get Playwright version"""
        try:
            import importlib.metadata

            return importlib.metadata.version("playwright")
        except Exception:
            try:
                # Try pytest-playwright
                import importlib.metadata

                return importlib.metadata.version("pytest-playwright")
            except Exception:
                return "unknown"
