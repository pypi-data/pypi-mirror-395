"""Last Failed command - Retrieve cached test failure data"""

import asyncio
import os
import re
import sys
from typing import List, Optional, Dict

import click
from pydantic import BaseModel, Field

from testdino_cli.core.cache_extractor import CacheIdDetector
from testdino_cli.services.cache_api import CacheApiClient
from testdino_cli.types import ExitCode
from testdino_cli.config import ConfigLoader


class LastFailedOptions(BaseModel):
    """CLI options for last-failed command"""
    cache_id: Optional[str] = Field(default=None)
    branch: Optional[str] = Field(default=None)
    commit: Optional[str] = Field(default=None)
    token: Optional[str] = Field(default=None)
    verbose: bool = Field(default=False)


@click.command(name="last-failed")
@click.option("--cache-id", help="Custom cache ID override")
@click.option("--branch", help="Custom branch name override")
@click.option("--commit", help="Custom commit hash override")
@click.option("-t", "--token", help="TestDino API token")
@click.option("-v", "--verbose", is_flag=True, help="Verbose logging")
def last_failed_command(
    cache_id: Optional[str],
    branch: Optional[str],
    commit: Optional[str],
    token: Optional[str],
    verbose: bool
) -> None:
    """Get last failed test cases for Playwright execution"""
    options = LastFailedOptions(
        cache_id=cache_id,
        branch=branch,
        commit=commit,
        token=token,
        verbose=verbose,
    )

    try:
        asyncio.run(execute_last_failed(options))
    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Last-failed operation cancelled by user", err=True)
        sys.exit(ExitCode.GENERAL_ERROR.value)


async def execute_last_failed(options: LastFailedOptions) -> None:
    """Execute the last-failed command"""
    is_debug_mode = options.verbose or os.getenv("TESTDINO_RUNTIME") == "development"

    try:
        if is_debug_mode:
            click.echo("🔍 Retrieving last failed tests...", err=True)
            if options.cache_id or options.branch or options.commit:
                click.echo("📊 Custom overrides:", err=True)
                click.echo(f"   Cache ID: {options.cache_id or 'auto-detect'}", err=True)
                click.echo(f"   Branch: {options.branch or 'auto-detect'}", err=True)
                click.echo(f"   Commit: {options.commit or 'auto-detect'}", err=True)

        # Step 1: Determine cache ID with custom overrides
        cache_id = await determine_cache_id(options.cache_id, options.branch, options.commit)

        if is_debug_mode and cache_id:
            click.echo(f"   Cache ID: {cache_id}", err=True)

        # Step 2: Get cached failure data
        failure_data = await get_cached_failures(cache_id, options, is_debug_mode)

        if not failure_data or not failure_data.get("failures"):
            if is_debug_mode:
                click.echo("ℹ️  No last failed test cases found", err=True)
            sys.exit(0)
            return

        if is_debug_mode:
            failures = failure_data["failures"]
            click.echo(f"   Found: {len(failures)} failed tests", err=True)
            click.echo(f"   Branch: {failure_data.get('branch', 'unknown')}", err=True)
            click.echo(f"   Repository: {failure_data.get('repository', 'unknown')}", err=True)

        # Step 3: Format output for Playwright
        playwright_args = format_playwright_args(failure_data["failures"])

        # Step 4: Output result (to stdout for shell substitution)
        click.echo(playwright_args)

    except Exception as error:
        if is_debug_mode:
            error_message = str(error)
            click.echo(f"❌ Failed to retrieve cached failures: {error_message}", err=True)
        sys.exit(1)


async def determine_cache_id(
    custom_cache_id: Optional[str],
    custom_branch: Optional[str],
    custom_commit: Optional[str]
) -> Optional[str]:
    """Determine cache ID using same logic as cache store command"""
    try:
        cache_id_info = await CacheIdDetector.detect_cache_id(
            custom_cache_id,
            custom_branch,
            custom_commit
        )
        return cache_id_info.cache_id
    except Exception:
        return None


async def get_cached_failures(
    cache_id: Optional[str],
    options: LastFailedOptions,
    is_debug_mode: bool
) -> Optional[Dict]:
    """Get cached failure data from API"""
    # Load configuration
    config_loader = ConfigLoader()
    config = config_loader.create_cache_config(options.token)

    api_client = CacheApiClient(config)

    try:
        # Get cache for specific cache ID
        if cache_id:
            # Determine query parameters based on whether cache ID is custom
            query_params: Dict[str, str] = {}

            # If custom cache ID is provided, pass branch/commit as query params
            if options.cache_id:
                if options.branch:
                    query_params["branch"] = options.branch
                if options.commit:
                    query_params["commit"] = options.commit
            else:
                # If auto-generated cache ID, commit is passed as query param only
                if options.commit:
                    query_params["commit"] = options.commit

            if is_debug_mode:
                click.echo(f"   Fetching cache for: {cache_id}", err=True)
                if query_params:
                    click.echo(f"   Query parameters: {query_params}", err=True)

            cache = await api_client.get_cache_data(cache_id, query_params)
            if cache:
                return cache

            if is_debug_mode:
                click.echo(f"   No cache found for {cache_id}", err=True)

        return None
    except Exception as error:
        error_message = str(error)
        click.echo(f"⚠️  API error: {error_message}", err=True)
        return None


def format_playwright_args(failures: List[Dict[str, str]]) -> str:
    """Format failure data for pytest -k option"""
    if not failures:
        return ""

    # Extract unique test names (without browser suffix like [chromium])
    test_names = set()
    for failure in failures:
        test_title = failure.get("testTitle", "")
        if test_title:
            # Remove browser suffix like [chromium], [firefox], etc.
            clean_name = re.sub(r'\s*\[.*?\]\s*$', '', test_title).strip()
            if clean_name:
                test_names.add(clean_name)

    if not test_names:
        return ""

    # Format for pytest -k: "test1 or test2 or test3"
    # Quote the expression so it works in shell without eval
    escaped_names = [escape_for_pytest(name) for name in test_names]
    k_expression = " or ".join(escaped_names)

    return f'-k "{k_expression}"'


def escape_for_pytest(test_title: str) -> str:
    """Escape test title for pytest's -k option"""
    # pytest -k uses simple substring matching, escape quotes
    escaped = test_title.replace('"', '\\"')
    # Remove any special pytest expression characters
    escaped = re.sub(r'[()]', '', escaped)
    return escaped.strip()
