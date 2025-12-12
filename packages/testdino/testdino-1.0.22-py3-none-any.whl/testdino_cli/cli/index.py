"""Main CLI entry point for TestDino CLI

This is an exact port of the TypeScript cli/index.ts with full error handling.
"""

import asyncio
import sys
import traceback
from typing import List, NoReturn

import click

from testdino_cli.cli.commands.upload import upload_command
from testdino_cli.cli.commands.cache import cache_command
from testdino_cli.cli.commands.last_failed import last_failed_command
from testdino_cli.types import (
    BaseError,
    ConfigurationError,
    ValidationError,
    AuthenticationError,
    NetworkError,
    FileSystemError,
    ExitCode,
)
from testdino_cli.version import VERSION


def handle_legacy_syntax(args: List[str]) -> List[str]:
    """
    Handle legacy syntax for backward compatibility.

    Transforms:
      Old: testdino ./path --flags
      To:  testdino upload ./path --flags

    This allows users who are used to the old syntax to continue using it
    while showing a deprecation warning.
    """
    # If no args, return as-is
    if not args:
        return args

    first_arg = args[0] if args else None

    # Known subcommands - not legacy syntax
    known_commands = ['cache', 'last-failed', 'upload', 'help', '--help', '-h', '--version']

    # If first arg is a known command, return as-is
    if first_arg and first_arg in known_commands:
        return args

    # If first arg is a flag, return as-is
    if first_arg and first_arg.startswith('-'):
        return args

    # Check if there are any upload-related flags
    upload_flags = [
        '--upload-images',
        '--upload-videos',
        '--upload-html',
        '--upload-traces',
        '--upload-files',
        '--upload-full-json',
        '--json-report',
        '--html-report',
        '--trace-dir',
        '--token',
        '-t',
    ]

    has_upload_flag = any(
        arg in upload_flags or arg.startswith('--token=') or arg.startswith('-t=')
        for arg in args
    )

    # Legacy syntax detected: path provided without 'upload' command
    if has_upload_flag or (first_arg and not first_arg.startswith('-')):
        click.echo('⚠️  DEPRECATION WARNING: Legacy syntax detected.', err=True)
        click.echo('   Old: testdino ./path --flags', err=True)
        click.echo('   New: testdino upload ./path --flags', err=True)
        click.echo('   Legacy syntax will be removed in a future version.\n', err=True)

        # Transform: insert 'upload' command at the beginning
        return ['upload'] + args

    return args


def is_verbose_mode() -> bool:
    """Check if verbose mode is enabled via command line args"""
    return '--verbose' in sys.argv or '-v' in sys.argv


def get_exit_code(error: BaseError) -> int:
    """Get appropriate exit code for error type"""
    if isinstance(error, AuthenticationError):
        return ExitCode.AUTHENTICATION_ERROR.value
    if isinstance(error, NetworkError):
        return ExitCode.NETWORK_ERROR.value
    if isinstance(error, FileSystemError):
        return ExitCode.FILE_NOT_FOUND_ERROR.value
    return ExitCode.GENERAL_ERROR.value


def handle_error(error: Exception) -> NoReturn:
    """
    Professional error handling with appropriate messaging.

    This is an exact port of the TypeScript handleError() method.
    Shows helpful suggestions based on error type and only displays
    stack traces in verbose mode.
    """
    verbose = is_verbose_mode()

    if isinstance(error, BaseError):
        click.echo(f"❌ {error}", err=True)

        # Show helpful suggestions without being verbose
        if isinstance(error, ConfigurationError):
            click.echo("💡 Check your API token and configuration", err=True)
        elif isinstance(error, ValidationError):
            click.echo("💡 Use --help for correct usage", err=True)
        elif isinstance(error, AuthenticationError):
            click.echo("💡 Verify your API token has proper permissions", err=True)
        elif isinstance(error, NetworkError):
            click.echo("💡 Check your internet connection", err=True)
        elif isinstance(error, FileSystemError):
            click.echo("💡 Verify the specified paths exist and are readable", err=True)

        # Show stack trace only in verbose mode
        if verbose:
            click.echo("\nStack trace:", err=True)
            click.echo(traceback.format_exc(), err=True)

        sys.exit(get_exit_code(error))

    elif isinstance(error, Exception):
        click.echo(f"❌ {error}", err=True)

        if not verbose:
            click.echo("💡 Use --verbose for detailed error information", err=True)
        else:
            click.echo("\nStack trace:", err=True)
            click.echo(traceback.format_exc(), err=True)

        sys.exit(ExitCode.GENERAL_ERROR.value)

    else:
        click.echo("❌ An unexpected error occurred", err=True)
        if verbose:
            click.echo(f"Error details: {error}", err=True)
        sys.exit(ExitCode.GENERAL_ERROR.value)


@click.group(invoke_without_command=True)
@click.version_option(version=VERSION, prog_name="testdino")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """TestDino CLI - Upload reports and cache test metadata

    \b
    Main Commands:
      cache                               Store test execution metadata after Playwright runs
      last-failed                         Get last failed test cases for Playwright execution
      upload [report-directory]          Upload test reports to TestDino

    \b
    Quick Start:
      $ testdino cache --token="your-token"                       # Cache test metadata
      $ testdino last-failed --token="your-token"                 # Get failed tests
      $ testdino upload ./playwright-report --token="your-token"  # Upload reports

    \b
    Environment Variables:
      TESTDINO_API_URL      API endpoint override
      TESTDINO_TOKEN        API authentication token

    \b
    For command-specific help:
      $ testdino cache --help
      $ testdino last-failed --help
      $ testdino upload --help

    \b
    Documentation: https://docs.testdino.com/cli
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        sys.exit(ExitCode.SUCCESS.value)


# Register commands
cli.add_command(upload_command)
cli.add_command(cache_command)
cli.add_command(last_failed_command)


def main() -> None:
    """Main entry point for the CLI

    This is an exact port of the TypeScript main() function.
    Handles legacy syntax transformation and comprehensive error handling.
    """
    try:
        # Handle legacy syntax by transforming arguments before Click processes them
        # sys.argv[0] is the script name, sys.argv[1:] are the actual arguments
        original_args = sys.argv[1:]
        transformed_args = handle_legacy_syntax(original_args)

        # If args were transformed, update sys.argv
        if transformed_args != original_args:
            sys.argv = [sys.argv[0]] + transformed_args

        cli()

        # If we reach here without exception, exit with success
        sys.exit(ExitCode.SUCCESS.value)

    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Operation cancelled by user", err=True)
        sys.exit(ExitCode.GENERAL_ERROR.value)

    except click.ClickException as error:
        # Let Click handle its own exceptions (like missing arguments)
        error.show()
        sys.exit(ExitCode.GENERAL_ERROR.value)

    except Exception as error:
        # Use our comprehensive error handler
        handle_error(error)


if __name__ == "__main__":
    main()
