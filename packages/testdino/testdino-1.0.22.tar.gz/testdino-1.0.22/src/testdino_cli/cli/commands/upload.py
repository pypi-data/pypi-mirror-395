"""Upload command implementation with progress tracking"""

import asyncio
import sys

import click
from pydantic import ValidationError as PydanticValidationError

from testdino_cli.config.index import config_loader, EnvironmentDetector
from testdino_cli.core.discovery import ReportDiscoveryService
from testdino_cli.services.upload import UploadService
from testdino_cli.types import (
    AuthenticationError,
    CLIOptions,
    ExitCode,
    NetworkError,
    ValidationError,
)
from testdino_cli.utils.env import EnvironmentType, EnvironmentUtils
from testdino_cli.utils.progress import create_progress_tracker
from testdino_cli.version import VERSION


@click.command(name="upload")
@click.argument("report-directory", type=click.Path(exists=True), required=True)
@click.option("-t", "--token", help="TestDino API token", envvar="TESTDINO_TOKEN")
@click.option("--upload-images", is_flag=True, help="Upload image attachments")
@click.option("--upload-videos", is_flag=True, help="Upload video attachments")
@click.option("--upload-html", is_flag=True, help="Upload HTML reports")
@click.option("--upload-traces", is_flag=True, help="Upload trace files")
@click.option("--upload-files", is_flag=True, help="Upload file attachments")
@click.option("--upload-full-json", is_flag=True, help="Upload all attachments")
@click.option("--json-report", type=click.Path(exists=True), help="Specific JSON report path")
@click.option("--html-report", type=click.Path(exists=True), help="Specific HTML report path")
@click.option("--trace-dir", type=click.Path(exists=True), help="Specific trace directory path")
@click.option("-v", "--verbose", is_flag=True, help="Verbose logging")
def upload_command(
    report_directory: str,
    token: str,
    upload_images: bool,
    upload_videos: bool,
    upload_html: bool,
    upload_traces: bool,
    upload_files: bool,
    upload_full_json: bool,
    json_report: str,
    html_report: str,
    trace_dir: str,
    verbose: bool,
) -> None:
    """Upload Playwright test reports to TestDino

    \b
    Examples:
      $ testdino upload ./playwright-report --token="trx_dev_abc123..."
      $ testdino upload ./test-results --upload-images
      $ testdino upload ./reports --upload-html --verbose
      $ testdino upload ./test-results --upload-full-json

    \b
    Flag Combinations:
      No flags:                   Only JSON report uploaded
      --upload-images:            JSON + image attachments
      --upload-videos:            JSON + video attachments
      --upload-files:             JSON + file attachments
      --upload-traces:            JSON + trace files
      --upload-html:              JSON + HTML + images + videos
      --upload-full-json:         JSON + images + videos + files
    """
    # Build CLI options
    options = CLIOptions(
        report_directory=report_directory,
        token=token or "",
        upload_images=upload_images,
        upload_videos=upload_videos,
        upload_html=upload_html,
        upload_traces=upload_traces,
        upload_files=upload_files,
        upload_full_json=upload_full_json,
        json_report=json_report,
        html_report=html_report,
        trace_dir=trace_dir,
        verbose=verbose,
    )

    # Run async upload
    try:
        asyncio.run(execute_upload(options))
    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Upload cancelled by user")
        sys.exit(ExitCode.GENERAL_ERROR.value)


async def execute_upload(options: CLIOptions) -> None:
    """Execute the upload command with enhanced progress tracking"""
    tracker = create_progress_tracker()

    try:
        # Create configuration from CLI options
        tracker.start("Validating configuration...")
        config = config_loader.create_config(options)
        tracker.succeed("Configuration validated")

        # Discover report files
        tracker.start("Discovering report files...")
        discovery_service = ReportDiscoveryService(options.report_directory)
        discovery_result = await discovery_service.discover(options)

        discovered_files = []
        discovered_files.append(f"JSON: {discovery_result.json_report}")
        if discovery_result.html_report:
            discovered_files.append(f"HTML: {discovery_result.html_report}")
        if discovery_result.trace_dir:
            discovered_files.append(f"Traces: {discovery_result.trace_dir}")

        report_type_text = "report type" if len(discovered_files) == 1 else "report types"
        tracker.succeed(f"Found {len(discovered_files)} {report_type_text}")

        # Show verbose configuration if requested
        if config.verbose:
            log_verbose_info(config, options, discovery_result)

        # Perform actual upload with progress tracking
        upload_service = UploadService(config)

        # Use fallback method for graceful degradation
        upload_response = await upload_service.upload_with_fallback(
            discovery_result.json_report,
            discovery_result.html_report,
            discovery_result.trace_dir,
        )

        # Construct TestDino URL
        testdino_url = ""
        environment_type = EnvironmentUtils.detect_environment_type()

        # Construct URL with organization and project if available
        if upload_response.organization_id and upload_response.project_id:
            url_path = f"{upload_response.organization_id}/projects/{upload_response.project_id}/test-runs/{upload_response.test_run_id}"
        else:
            url_path = f"test-runs/{upload_response.test_run_id}"

        if environment_type == EnvironmentType.PRODUCTION:
            testdino_url = f"https://app.testdino.com/{url_path}"
        elif environment_type == EnvironmentType.STAGING:
            testdino_url = f"https://staging.testdino.com/{url_path}"
        else:
            testdino_url = f"http://localhost:3001/{url_path}"

        # Success output with actionable information
        click.echo()
        click.echo("Upload completed successfully!")
        click.echo()
        click.echo(f"   TestDino URL: {testdino_url}")

    except (AuthenticationError, NetworkError, ValidationError, PydanticValidationError) as error:
        handle_upload_error(error, tracker)
    except Exception as error:
        handle_upload_error(error, tracker)


def log_verbose_info(config, options: CLIOptions, discovery_result) -> None:
    """Log verbose configuration information"""
    click.echo("\n📋 Upload Configuration:")
    click.echo(f"   Report Directory: {options.report_directory}")
    click.echo(f"   API Endpoint: {config.api_url}")
    click.echo(f"   Upload Images: {'Yes' if config.upload_images else 'No'}")
    click.echo(f"   Upload Videos: {'Yes' if config.upload_videos else 'No'}")
    click.echo(f"   Upload HTML: {'Yes' if config.upload_html else 'No'}")
    click.echo(f"   Upload Traces: {'Yes' if config.upload_traces else 'No'}")
    click.echo(f"   Verbose Mode: {'Yes' if config.verbose else 'No'}")

    click.echo("\n📁 Discovered Files:")
    click.echo(f"   JSON Report: {discovery_result.json_report}")
    if discovery_result.html_report:
        click.echo(f"   HTML Report: {discovery_result.html_report}")
    if discovery_result.trace_dir:
        click.echo(f"   Trace Directory: {discovery_result.trace_dir}")

    env_info = EnvironmentDetector.get_environment_info()
    click.echo("\n🌍 Environment Info:")
    click.echo(f"   testdino Version: {VERSION}")
    click.echo(f"   Type: {env_info['type']}")
    click.echo(f"   CI/CD: {'Yes (' + env_info['ciProvider'] + ')' if env_info['isCI'] else 'No'}")
    import sys

    click.echo(f"   Python: {sys.version.split()[0]}")


def handle_upload_error(error: Exception, tracker) -> None:
    """Enhanced error handling with actionable feedback"""
    tracker.fail("Upload failed")

    if isinstance(error, AuthenticationError):
        click.echo("\nAuthentication Failed", err=True)
        click.echo("Solutions:", err=True)
        click.echo("   Verify your API token is correct", err=True)
        click.echo("   Check that your token has upload permissions", err=True)
        click.echo("   Ensure you're using the right environment token", err=True)
        click.echo("\nGet help: https://docs.testdino.com/authentication", err=True)
        sys.exit(ExitCode.AUTHENTICATION_ERROR.value)

    if isinstance(error, NetworkError):
        click.echo("\nNetwork Error", err=True)
        click.echo(f"   {error.message}", err=True)
        click.echo("\nTroubleshooting:", err=True)
        click.echo("   Check your internet connection", err=True)
        click.echo("   Verify the API endpoint is accessible", err=True)
        click.echo("   Verify your configuration and try again", err=True)
        sys.exit(ExitCode.NETWORK_ERROR.value)

    # Generic error handling
    error_message = str(error) if error else "Unknown error occurred"
    click.echo(f"\nUpload Error: {error_message}", err=True)

    # Show stack trace in development mode
    import os

    if os.getenv("TESTDINO_RUNTIME") == "development":
        click.echo("\nDebug Information:", err=True)
        import traceback

        click.echo(traceback.format_exc(), err=True)
    else:
        click.echo("\nRun with --verbose for detailed error information", err=True)

    click.echo("\nNeed help?", err=True)
    click.echo("   Documentation: https://docs.testdino.com", err=True)
    click.echo("   Support: support@testdino.com", err=True)
    click.echo(
        "   Issues: https://github.com/testdino-inc/testdino-cli/issues", err=True
    )

    sys.exit(ExitCode.GENERAL_ERROR.value)
