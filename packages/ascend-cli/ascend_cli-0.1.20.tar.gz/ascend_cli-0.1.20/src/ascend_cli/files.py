import os
import typer
import asyncio
from rich.console import Console
from pathlib import Path
from .logic import files_logic
from .config import ConfigManager, get_config_path, ConfigError, DATA_DIR

console = Console()
app = typer.Typer(
    name="files",
    help="Commands for file system migration.",
    no_args_is_help=True
)

DEFAULT_INDEX_FILE = DATA_DIR / "migration_index.txt"

@app.command()
def scan(
    source: Path = typer.Option(
        None,
        "--source",
        "-s",
        help="Source directory to scan. Overrides config file.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    gcs_target_prefix: str = typer.Option(
        None,
        "--gcs-target-prefix",
        "-p",
        help="Optional GCS prefix (folder). Overrides config file.",
    ),
    config_file: Path = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to a custom configuration file.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
    scan_workers: int = typer.Option(
        None,
        "--scan-workers",
        "-w",
        help="Number of parallel scan processes. Overrides config file.",
    ),
    scan_max_depth: int = typer.Option(
        None,
        "--scan-max-depth",
        "-d",
        help="Maximum directory depth to scan. Useful for 'hashed' directory structures.",
    ),
    work_unit_threshold: int = typer.Option(
        None,
        "--work-unit-threshold",
        "-t",
        help="Maximum items in a directory before it becomes a work unit.",
    ),
    index_file: Path = typer.Option(
        DEFAULT_INDEX_FILE,
        "--index-file",
        "-i",
        help="Path to the file to store the scan index.",
        writable=True,
        resolve_path=True,
    )
):
    """
    Scans a source directory and creates an index of files to be migrated.
    """
    try:
        effective_config_path = get_config_path(config_file)
        config = ConfigManager(effective_config_path, section="files")
        config.load(source_dir=source, gcs_target_prefix=gcs_target_prefix, scan_workers=scan_workers, scan_max_depth=scan_max_depth, work_unit_threshold=work_unit_threshold)

        file_count = files_logic.create_scan_index(config)
        console.print(f"✅ Scan complete. Found and indexed {file_count:,} files.")
    except (ConfigError, IOError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

DEFAULT_PROGRESS_FILE = DATA_DIR / "migration_progress.txt"

@app.command()
def migrate(
    bucket: str = typer.Option(None, "--bucket", "-b", help="Target GCS bucket name. Overrides config file."),
    max_concurrency: int = typer.Option(None, "--max-concurrency", "-mc", help="Max concurrent uploads. Overrides config file."),
    gcs_timeout_seconds: int = typer.Option(None, "--timeout", "-t", help="GCS upload timeout in seconds. Overrides config file."),
    config_file: Path = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to a custom configuration file.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
    verify_content_type: bool = typer.Option(
        False,
        "--verify-content-type/--no-verify-content-type",
        help="Verify uploaded object's Content-Type against local detection (optional).",
    ),
    verify_sample_rate: int = typer.Option(
        0,
        "--verify-sample-rate",
        min=0,
        max=1000000,
        help="Sample rate per-million for hash verification (0 disables). Example: 10000 = ~1%.",
    ),
    progress_file: Path = typer.Option(
        DEFAULT_PROGRESS_FILE,
        "--progress-file",
        "-pf",
        help="Path to the file to store migration progress.",
        writable=True,
        resolve_path=True,
    ),
):
    """
    Migrates files to Google Cloud Storage based on the generated index.
    """
    try:
        effective_config_path = get_config_path(config_file)

        config = ConfigManager(effective_config_path, section="files")
        config.load(
            gcs_bucket_name=bucket,
            max_concurrency=max_concurrency,
            gcs_timeout_seconds=gcs_timeout_seconds,
            verify_content_type=verify_content_type,
            verify_sample_rate=verify_sample_rate,
        )

        asyncio.run(files_logic.start_migration(config))
    except (ConfigError, FileNotFoundError, ConnectionError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1) 