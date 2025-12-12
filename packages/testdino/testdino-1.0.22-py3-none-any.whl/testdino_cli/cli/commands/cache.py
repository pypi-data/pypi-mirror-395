"""Cache command - Store test execution metadata after Playwright runs"""

import asyncio
import sys
from datetime import datetime
from typing import Optional

import click
from pydantic import BaseModel, Field

from testdino_cli.collectors.ci import CiCollector
from testdino_cli.collectors.git import GitCollector
from testdino_cli.collectors.system import SystemCollector
from testdino_cli.core.cache_extractor import CacheExtractor, CacheIdDetector
from testdino_cli.core.shard_detection import PlaywrightShardDetector
from testdino_cli.services.cache_api import CacheApiClient
from testdino_cli.types import ExitCode
from testdino_cli.utils.progress import ConsoleProgressTracker
from testdino_cli.config import ConfigLoader


class CacheOptions(BaseModel):
    """CLI options for cache command"""
    cache_id: Optional[str] = Field(default=None)
    working_dir: Optional[str] = Field(default=None)
    token: Optional[str] = Field(default=None)
    verbose: bool = Field(default=False)


@click.command(name="cache")
@click.option("--cache-id", help="Custom cache ID override")
@click.option("--working-dir", type=click.Path(exists=True), help="Working directory")
@click.option("-t", "--token", help="TestDino API token")
@click.option("-v", "--verbose", is_flag=True, help="Verbose logging")
def cache_command(cache_id: Optional[str], working_dir: Optional[str], token: Optional[str], verbose: bool) -> None:
    """Store test execution metadata after Playwright runs"""
    options = CacheOptions(
        cache_id=cache_id,
        working_dir=working_dir,
        token=token,
        verbose=verbose,
    )

    try:
        asyncio.run(execute_cache(options))
    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Cache operation cancelled by user")
        sys.exit(ExitCode.GENERAL_ERROR.value)


async def execute_cache(options: CacheOptions) -> None:
    """Execute the cache command"""
    tracker = ConsoleProgressTracker()

    try:
        tracker.start("🔍 Caching test execution metadata...")

        # Load configuration
        config_loader = ConfigLoader()
        config = config_loader.create_cache_config(options.token)

        working_dir = options.working_dir or "."

        if options.verbose:
            click.echo(f"\n📊 Cache configuration:")
            click.echo(f"   Working directory: {working_dir}")
            click.echo(f"   Custom cache ID: {options.cache_id or 'auto-detect'}")

        tracker.update(f"📁 Working directory: {working_dir}")

        # Step 1: Detect shard information
        tracker.update("🔍 Detecting Playwright configuration...")
        shard_info = await PlaywrightShardDetector.detect_shard_info(working_dir)

        if options.verbose and shard_info:
            click.echo(f"📊 Detected shard configuration: {shard_info}")

        # Step 2: Extract test failure data
        tracker.update("📋 Discovering and extracting test data...")
        extractor = CacheExtractor(working_dir, config.token)
        failure_data = await extractor.extract_failure_data()

        if not failure_data.report_paths:
            tracker.warn("No test reports found - tests may not have completed yet")
            click.echo("💡 Run this command after your Playwright tests complete")
            return

        if options.verbose:
            click.echo(f"📋 Found {len(failure_data.failures)} failed tests from {len(failure_data.report_paths)} reports")

        # Step 3: Collect build and CI metadata
        tracker.update("🏗️ Collecting build metadata...")
        cache_id_info = await CacheIdDetector.detect_cache_id(options.cache_id)

        git_collector = GitCollector(working_dir)
        git_metadata = await git_collector.get_metadata()

        ci_metadata = CiCollector.collect()
        system_metadata = SystemCollector.collect()

        # Step 4: Prepare cache payload
        effective_shard_info = shard_info or PlaywrightShardDetector.create_default_shard_info()

        cache_payload = {
            # Cache identification
            "cacheId": cache_id_info.cache_id,
            "pipelineId": cache_id_info.pipeline_id,
            "commit": cache_id_info.commit,

            # Git metadata
            "branch": cache_id_info.branch,
            "repository": cache_id_info.repository,

            # CI information
            "ci": {
                "provider": ci_metadata.provider or "unknown",
                "pipelineId": ci_metadata.pipeline.id if ci_metadata.pipeline else "unknown",
                "buildNumber": ci_metadata.build.number if ci_metadata.build else "unknown",
            },

            # Shard information
            "isSharded": effective_shard_info.shard_total > 1,
            "shardIndex": effective_shard_info.shard_index if effective_shard_info.shard_total > 1 else None,
            "shardTotal": effective_shard_info.shard_total if effective_shard_info.shard_total > 1 else None,

            # Test failure data
            "failures": [
                {"file": f.file, "testTitle": f.test_title}
                for f in failure_data.failures
            ],

            # Test summary
            "summary": {
                "total": failure_data.summary.total,
                "passed": failure_data.summary.passed,
                "failed": failure_data.summary.failed,
                "skipped": failure_data.summary.skipped,
                "duration": failure_data.summary.duration,
            },

            # Timestamp
            "timestamp": datetime.now().isoformat(),
        }

        if options.verbose:
            click.echo(f"\n📤 Cache payload summary:")
            click.echo(f"   Cache ID: {cache_payload['cacheId']}")
            click.echo(f"   Pipeline ID: {cache_payload['pipelineId']}")
            click.echo(f"   Commit: {cache_payload['commit']}")
            click.echo(f"   Branch: {cache_payload['branch']}")
            click.echo(f"   Is Sharded: {cache_payload['isSharded']}")
            if cache_payload['isSharded']:
                click.echo(f"   Shard: {cache_payload['shardIndex']}/{cache_payload['shardTotal']}")
            click.echo(f"   Failures: {len(cache_payload['failures'])}")
            click.echo(f"   Total Tests: {cache_payload['summary']['total']}")

        # Step 5: Send to API
        tracker.update("📤 Sending cache data to TestDino API...")
        api_client = CacheApiClient(config)
        result = await api_client.submit_cache_data(cache_payload)

        if result.success:
            tracker.succeed("✅ Test execution metadata cached successfully")
            if result.message:
                click.echo(f"   {result.message}")
        else:
            raise Exception(f"Cache submission failed for cache: {result.cache_id}")

    except Exception as error:
        error_message = str(error)

        # Special handling for cache conflicts (409)
        if "already exists" in error_message:
            tracker.warn("Cache data already exists for this shard")
            click.echo("ℹ️  This shard has already been cached - skipping")
            click.echo("💡 This warning will not affect your CI pipeline")
            return

        # CI-friendly error handling - warn but don't fail
        tracker.warn(f"Failed to cache test metadata: {error_message}")

        if options.verbose:
            click.echo(f"🔍 Full error details: {error}", err=True)

        click.echo("💡 This warning will not affect your CI pipeline")
        # Exit with success code to avoid breaking CI
