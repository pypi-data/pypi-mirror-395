"""
Utility function to check if verbose mode is enabled via CLI flags
"""

import sys


def is_verbose_mode() -> bool:
    """
    Check if verbose mode is enabled via CLI flags.
    Checks for --verbose or -v flags in sys.argv
    """
    return "--verbose" in sys.argv or "-v" in sys.argv
