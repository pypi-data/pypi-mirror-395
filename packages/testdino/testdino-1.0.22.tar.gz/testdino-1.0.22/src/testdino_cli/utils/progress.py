"""Clean, professional progress tracker with minimal styling"""

from testdino_cli.types import ProgressTracker


class ConsoleProgressTracker(ProgressTracker):
    """Clean, professional progress tracker with minimal styling"""

    def start(self, message: str) -> None:
        """Start progress tracking with a message"""
        print(f"   {message}")

    def update(self, message: str) -> None:
        """Update progress message"""
        print(f"   {message}")

    def succeed(self, message: str) -> None:
        """Mark progress as successful"""
        print(f"✓  {message}")

    def fail(self, message: str) -> None:
        """Mark progress as failed"""
        print(f"✗  {message}")

    def warn(self, message: str) -> None:
        """Show a warning message"""
        print(f"!  {message}")


def create_progress_tracker() -> ProgressTracker:
    """Factory to create a progress tracker"""
    return ConsoleProgressTracker()
