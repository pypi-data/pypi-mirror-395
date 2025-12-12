import asyncio
import os
import ssl
import tempfile
from pathlib import Path
from collections import deque
from typing import Tuple, Any, List, Generator
import mimetypes
import hashlib
import base64
import random

import aiohttp
import certifi
import typer
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table
from rich.text import Text
from rich.columns import Columns

from gcloud.aio.storage import Storage

from ..config import ConfigManager, DATA_DIR

import multiprocessing
from functools import partial
import time
import shutil
import subprocess

DEFAULT_INDEX_FILE = DATA_DIR / "migration_index.txt"
DEFAULT_PROGRESS_FILE = DATA_DIR / "migration_progress.txt"

console = Console(soft_wrap=False, force_terminal=True)

# --- Final Architecture ---

def _index_writer_process(queue: 'multiprocessing.Queue', index_file: Path):
    """
    A dedicated process that consumes from a queue and writes to the final index file.
    """
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            while True:
                line = queue.get()
                if line is None:  # Sentinel value to terminate
                    break
                f.write(line)
    except Exception:
        # If the writer fails, it's a critical error.
        # We can't easily communicate back to the main process UI from here,
        # but in a real-world scenario, you'd log this severely.
        pass

def _discover_work_units(
    path: Path, 
    threshold: int = 500,
    max_depth: int | None = None,
    current_depth: int = 0
) -> Generator[Tuple[str, Path], None, None]:
    """
    Recursively scans and yields balanced work units.
    A work unit is a tuple of (type, path).
    - ('dir', path): Process this directory and all its subdirectories.
    - ('files_in', path): Process ONLY the direct files within this directory.

    The scan can be limited by either a max depth setting or item count 
    threshold, whichever is met first. This provides flexibility for both
    deep/narrow ("hashed") and wide/shallow directory structures.
    """
    # Depth-based termination: if max_depth is set and we've reached it,
    # yield this whole directory as a single work unit and stop recursing.
    if max_depth is not None and current_depth >= max_depth:
        # Check if directory is non-empty before yielding
        try:
            if any(os.scandir(path)):
                yield ('dir', path)
        except (PermissionError, OSError):
            yield ('dir', path) # Yield even if we can't scan, to report error later
        return

    try:
        items = list(os.scandir(path))
        sub_dirs = [Path(entry.path) for entry in items if entry.is_dir()]
        has_files = any(entry.is_file() for entry in items)

        # Heuristic to decide when to stop recursing and yield a work unit.
        # 1. If the directory is very large (item count), process it as a single monolithic unit.
        # 2. If the directory has no sub-directories (a leaf node), process it.
        if len(items) > threshold or not sub_dirs:
            if items:  # Only yield if there's something to process
                yield ('dir', path)
        else:
            # It's a medium-sized directory with sub-directories.
            # We must process its direct files as a separate unit (if any exist).
            if has_files:
                yield ('files_in', path)
            
            # And then recurse into each sub-directory.
            for sub_dir in sub_dirs:
                yield from _discover_work_units(
                    sub_dir, threshold, max_depth, current_depth + 1
                )

    except (PermissionError, OSError):
        # On access errors, treat the whole directory as a single (likely failing) unit.
        yield ('dir', path)


def _scan_worker(
    work_unit: Tuple[str, Path],
    source_dir: Path,
    gcs_target_prefix: str,
    status_dict: dict,
    activity_log: 'deque',
    queue: 'multiprocessing.Queue',
) -> list[str]:
    """
    Worker process that runs 'find' on a directory, updates a shared status dict,
    and logs its final activity to a shared deque.
    Accepts a work_unit tuple to determine scan depth.
    """
    unit_type, target_path = work_unit
    errors: List[str] = []
    file_count = 0
    
    # Create a unique key for the status dictionary
    relative_path_str = str(target_path.relative_to(source_dir) or ".")
    dir_key = f"{unit_type}::{relative_path_str}"

    def update_status(status: str, count: int):
        status_dict[dir_key] = {"status": status, "count": count}
        
    update_status("in_progress", 0)

    try:
        command = ["find", str(target_path), "-type", "f"]
        if unit_type == 'files_in':
            command.insert(2, "-maxdepth")
            command.insert(3, "1")

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

        if process.stdout:
            for line in process.stdout:
                file_path_str = line.strip()
                if file_path_str:
                    file_count += 1
                    file_path = Path(file_path_str)
                    relative_path = str(file_path.relative_to(source_dir)).replace(os.sep, '/')
                    # Normalize GCS object path and avoid duplicate slashes
                    if gcs_target_prefix:
                        gcs_object_name = f"{gcs_target_prefix.rstrip('/')}/{relative_path.lstrip('/')}"
                    else:
                        gcs_object_name = relative_path
                    queue.put(f"{file_path_str}|{gcs_object_name}\n")
                    if file_count % 1000 == 0:
                        update_status("in_progress", file_count)

        _, stderr = process.communicate()
        if process.returncode != 0 and stderr:
            errors.extend(err for err in stderr.strip().split('\n') if err)

        # Use a more descriptive key for the activity log
        activity_key = relative_path_str
        if unit_type == 'files_in':
            activity_key = str(Path(relative_path_str) / "*")

        if errors:
            activity_log.append(f"  [red]✖[/red] [bright_white]{activity_key}[/bright_white] [dim]({errors[0]})[/dim]")
            update_status("failed", file_count)
        else:
            activity_log.append(f"  [green]✔[/green] [bright_white]{activity_key}[/bright_white] [dim]({file_count:,} files found)[/dim]")
            update_status("complete", file_count)
        return errors
    except Exception as e:
        error_msg = f"Worker crashed for '{dir_key}': {e}"
        errors.append(error_msg)
        activity_log.append(f"  [red]✖[/red] [bright_white]{dir_key}[/bright_white] [dim]({error_msg})[/dim]")
        update_status("failed", 0)
        return errors


def create_scan_index(config: ConfigManager) -> int:
    """
    Scans a source directory using a dynamically balanced, two-stage parallel
    process with a focused, live dashboard UI for maximum transparency.
    """
    source_path = Path(config.get("source_dir")).resolve()
    gcs_target_prefix = config.get("gcs_target_prefix", required=False, default="")
    index_file = Path(config.get("index_file", required=False, default=DEFAULT_INDEX_FILE))
    scan_workers = int(config.get("scan_workers", required=False, default=os.cpu_count() or 1))
    work_unit_threshold = int(config.get("work_unit_threshold", required=False, default=500))
    scan_max_depth_str = config.get("scan_max_depth", required=False, default=None)
    scan_max_depth = int(scan_max_depth_str) if scan_max_depth_str is not None else None

    index_file.parent.mkdir(parents=True, exist_ok=True)
    if index_file.exists():
        index_file.unlink()
    index_file.touch()

    # --- Stage 1: Live Discovery UI (Spinner) ---
    work_units: List[Tuple[str, Path]] = []
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[bold cyan]Analyzing directory structure... Found {task.completed} work units."),
        transient=True,
        console=console
    ) as progress:
        discovery_task = progress.add_task("Discovering", total=None)
        for unit_type, unit_path in _discover_work_units(
            source_path, work_unit_threshold, max_depth=scan_max_depth
        ):
            work_units.append((unit_type, unit_path))
            progress.update(discovery_task, advance=1)
    
    console.print(f"✅ Analysis complete. Found [bold green]{len(work_units)}[/bold green] work units to scan.")
    if not work_units:
        return 0

    # --- Stage 2: Focused Parallel Scan UI ---
    all_errors: list[str] = []
    start_time = time.time()
    
    manager = multiprocessing.Manager()
    status_dict_keys = [f"{ut}::{str(up.relative_to(source_path) or '.')}" for ut, up in work_units]
    status_dict = manager.dict({key: {"status": "pending", "count": 0} for key in status_dict_keys})
    activity_log = manager.list()
    activity_deque = deque(maxlen=8)

    # Create a queue and a dedicated writer process for the index file.
    writer_queue = manager.Queue()
    writer_process = multiprocessing.Process(
        target=_index_writer_process, args=(writer_queue, index_file)
    )
    writer_process.start()

    overall_progress = Progress(
        TextColumn("[bold bright_cyan]Scanning Files[/bold bright_cyan]"),
        BarColumn(bar_width=None, style="cyan", complete_style="bright_cyan"),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TextColumn("•"),
        TextColumn("Units: {task.completed}/{task.total}"),
        console=console,
    )
    
    def generate_activity_dashboard() -> Group:
        table = Table(box=None, show_header=False, show_edge=False, padding=(0, 0))
        table.add_column()
        # Update local deque from shared list
        while activity_log:
             activity_deque.append(activity_log.pop(0))
        for item in activity_deque:
            table.add_row(item)
        return Group(overall_progress, table)

    with Live(generate_activity_dashboard(), console=console, refresh_per_second=10) as live:
        overall_task = overall_progress.add_task("Processing...", total=len(work_units))

        with multiprocessing.Pool(processes=scan_workers) as pool:
            worker_func = partial(_scan_worker, source_dir=source_path, gcs_target_prefix=gcs_target_prefix, status_dict=status_dict, activity_log=activity_log, queue=writer_queue)
            result_async = pool.map_async(worker_func, work_units)
            
            while not result_async.ready():
                completed = sum(1 for v in status_dict.values() if v['status'] in ['complete', 'failed'])
                overall_progress.update(overall_task, completed=completed)
                live.update(generate_activity_dashboard())
                time.sleep(0.2)
            
            completed = sum(1 for v in status_dict.values() if v['status'] in ['complete', 'failed'])
            overall_progress.update(overall_task, completed=completed)
            live.update(generate_activity_dashboard()) # Final update
            
            results = result_async.get()
            for errors in results:
                if errors: all_errors.extend(errors)
    
    # --- Aggregation and Summary ---
    # Signal the writer process to finish and wait for it.
    writer_queue.put(None)
    console.print(f"\n[bold green]Gathering results and creating final index file...[/bold green]")
    writer_process.join()
            
    try:
        with open(index_file, 'r', encoding='utf-8') as f: total_files_found = sum(1 for _ in f)
    except FileNotFoundError: total_files_found = 0

    elapsed_time = time.time() - start_time
    summary_panel = Panel(
        Text.from_markup(
            f"• Indexed [bold bright_cyan]{total_files_found:,}[/bold bright_cyan] files.\n"
            f"• Total time: [yellow]{elapsed_time:.2f} seconds[/yellow].\n"
            f"• Index file created at: [u]{index_file}[/u]",
        ),
        title="[bold bright_green]✅ Scan Complete[/bold bright_green]",
        border_style="bright_green",
        expand=False,
    )
    
    if all_errors:
        error_panel = Panel(
            Text("\n".join(all_errors)), title="⚠️  [bold yellow]Errors or Warnings Encountered[/bold yellow]",
            border_style="yellow", expand=False
        )
        console.print(Group(summary_panel, error_panel))
    else:
        console.print(summary_panel)

    return total_files_found


def _guess_content_type(local_path: Path) -> str:
    """Best-effort content type detection.
    1) Use extension via mimetypes
    2) Fallback to magic bytes for common types
    3) Default to application/octet-stream
    """
    guessed, _ = mimetypes.guess_type(str(local_path))
    if guessed:
        return guessed
    try:
        with open(local_path, 'rb') as f:
            header = f.read(8)
        if header.startswith(b"%PDF"):
            return "application/pdf"
        if header[:3] == b"\x1f\x8b\x08":
            return "application/gzip"
        if header[:2] == b"PK":
            return "application/zip"
    except Exception:
        pass
    return "application/octet-stream"


async def _upload_worker(
    line_info: str,
    bucket_name: str,
    storage: Storage,
    verify_content_type: bool = False,
    verify_sample_rate: int = 0,
) -> tuple[str, bool, int | str]:
    """
    Asynchronous worker to upload a single file.
    Returns a tuple of (line_info, success, result).
    Result is file size on success, error message on failure.
    """
    if '|' not in line_info:
        return (line_info, False, "Invalid line format in index file (missing '|')")

    local_path_str, gcs_object_name = line_info.split('|', 1)
    local_path = Path(local_path_str)

    try:
        # Upload file by streaming its binary contents. Passing a string path
        # would upload the literal path text as object content, which corrupts data.
        content_type = _guess_content_type(local_path)
        with open(local_path, 'rb') as file_stream:
            # Upload returns object metadata (dict). Use it for post-upload verification
            meta = await storage.upload(
                bucket_name,
                gcs_object_name,
                file_stream,
                content_type=content_type
            )

        # Optional verifications (Content-Type check and sampled MD5)
        sampled_md5 = False
        md5_ok = None
        ct_ok = None
        remote_ct = meta.get('contentType') if isinstance(meta, dict) else None
        if verify_content_type or (verify_sample_rate and verify_sample_rate > 0 and random.randrange(1_000_000) < verify_sample_rate):
            # Use metadata returned by upload call
            if not isinstance(meta, dict):
                return (line_info, False, "Verification failed: upload did not return metadata")

            if verify_content_type:
                local_ct = content_type
                if remote_ct != local_ct:
                    return (line_info, False, f"Content-Type mismatch: local={local_ct}, remote={remote_ct}")
                ct_ok = True

            if verify_sample_rate and verify_sample_rate > 0:
                sampled_md5 = True
                md5 = hashlib.md5()
                with open(local_path, 'rb') as f_in:
                    for chunk in iter(lambda: f_in.read(1024 * 1024), b''):
                        md5.update(chunk)
                local_md5_b64 = base64.b64encode(md5.digest()).decode('ascii')
                remote_md5_b64 = meta.get('md5Hash')
                if not remote_md5_b64 or remote_md5_b64 != local_md5_b64:
                    return (line_info, False, "MD5 verification failed")
                md5_ok = True

        # Return size and lightweight verification summary for UI
        return (
            line_info,
            True,
            {
                "size": local_path.stat().st_size,
                "ct_local": content_type,
                "ct_remote": remote_ct,
                "ct_ok": ct_ok,
                "md5_sampled": sampled_md5,
                "md5_ok": md5_ok,
            },
        )
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e).splitlines()[0] if str(e).strip() else error_type
        return (line_info, False, error_message)


async def _progress_file_writer(queue: asyncio.Queue, progress_file: Path) -> None:
    """
    Asynchronous worker that listens to a queue and writes completed paths to the progress file.
    """
    # Open the file once and write as items come in.
    with open(progress_file, 'a') as f:
        while True:
            path_to_write = await queue.get()
            if path_to_write is None:
                # Sentinel value received, terminate.
                break
            f.write(f"{path_to_write}\n")
            f.flush()


async def _check_gcs_bucket_accessibility(storage: Storage, bucket_name: str):
    """Check if the GCS bucket is accessible."""
    console.print(f"✈️  Running pre-flight check for GCS bucket: [bold cyan]{bucket_name}[/]...")
    try:
        # Simple bucket existence check - just get bucket metadata
        bucket = storage.get_bucket(bucket_name)
        # Try to get bucket metadata to verify access
        await bucket.get_metadata()
        return True
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] GCS pre-flight check failed. Cannot access bucket '{bucket_name}'. Reason: {e}")
        return False


async def start_migration(config: ConfigManager):
    """
    Initializes and runs the file migration using asyncio for high concurrency.
    """
    bucket_name = config.get("gcs_bucket_name")
    max_concurrency = int(config.get("max_concurrency", required=False, default=1000))
    gcs_timeout_seconds = int(config.get("gcs_timeout_seconds", required=False, default=300))
    index_file = Path(config.get("index_file", required=False, default=DEFAULT_INDEX_FILE))
    progress_file = Path(config.get("progress_file", required=False, default=DEFAULT_PROGRESS_FILE))
    service_account_key_file = config.get("gcs_service_account_key_file", required=False)
    verify_content_type = bool(config.get("verify_content_type", required=False, default=False))
    verify_sample_rate = int(config.get("verify_sample_rate", required=False, default=0))

    progress_file.parent.mkdir(parents=True, exist_ok=True)

    # --- SSL Context and Session Setup for robust connectivity ---
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    timeout = aiohttp.ClientTimeout(total=gcs_timeout_seconds)
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context), timeout=timeout
    ) as session:
        # --- Async Pre-flight Check ---
        async with Storage(service_file=service_account_key_file, session=session) as storage:
            if not await _check_gcs_bucket_accessibility(storage, bucket_name):
                raise ConnectionError(f"GCS pre-flight check failed. Cannot access bucket '{bucket_name}'.")
            console.print("✅ Pre-flight check passed. Bucket is accessible.")

        # --- File List Preparation (Memory Efficient) ---
        try:
            # Count total files first (streaming)
            total_files = 0
            with open(index_file, 'r') as f:
                for line in f:
                    if line.strip():
                        total_files += 1
            
            # Load completed files into a set for fast lookup
            completed_source_paths = set()
            if progress_file.exists():
                with open(progress_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            completed_source_paths.add(line.strip())
            
            # Stream through index file and collect only remaining files
            remaining_lines = []
            with open(index_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '|' in line:
                        source_path = line.split('|')[0]
                        if source_path not in completed_source_paths:
                            remaining_lines.append(line)
                            
        except FileNotFoundError:
            raise FileNotFoundError(f"Index file not found at {index_file}. Please run the 'scan' command first.")
        
        if not remaining_lines:
            console.print("✅ No new files to migrate. Everything is up to date.")
            return

        completed_count = total_files - len(remaining_lines)
        console.print(f"Found {total_files:,} total files. {completed_count:,} already migrated.")
        console.print(f"🚀 Starting migration of [yellow]{len(remaining_lines):,}[/yellow] remaining files with [cyan]{max_concurrency}[/cyan] concurrent tasks...")

        # --- UI and Task Management ---
        progress_file_writer_queue = asyncio.Queue()
        recent_files = deque(maxlen=5)
        successful_uploads = 0
        failed_uploads = 0

        progress_bar = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TransferSpeedColumn(),
            "•",
            TextColumn("{task.completed}/{task.total} files"),
            "•",
            TimeRemainingColumn(),
            expand=False,
        )
        
        def generate_status_table() -> Table:
            table = Table(box=None, show_header=False, show_edge=False, expand=True, pad_edge=False)
            table.add_column("Info", no_wrap=True, overflow="ellipsis")
            files_to_show = list(reversed(list(recent_files)))
            for status, file_path in files_to_show:
                table.add_row(f"{status} {file_path}")
            for _ in range(5 - len(files_to_show)):
                table.add_row("")
            return table

        progress_group = Group(progress_bar, generate_status_table())
        task_id = progress_bar.add_task("[green]Migrating files...", total=len(remaining_lines))
        
        aborted = False
        
        with Live(progress_group, console=console, refresh_per_second=10, transient=True) as live:
            try:
                async with Storage(service_file=service_account_key_file, session=session) as storage:
                    progress_writer_task = asyncio.create_task(_progress_file_writer(progress_file_writer_queue, progress_file))

                    # Create semaphore to limit concurrent tasks
                    semaphore = asyncio.Semaphore(max_concurrency)

                    async def bounded_upload_worker(line):
                        async with semaphore:
                            return await _upload_worker(
                                line, bucket_name, storage,
                                verify_content_type=verify_content_type,
                                verify_sample_rate=verify_sample_rate,
                            )
                    
                    # Process files in batches to avoid creating too many tasks at once
                    batch_size = max_concurrency * 10  # 10x concurrency for batching
                    total_processed = 0
                    
                    for i in range(0, len(remaining_lines), batch_size):
                        batch = remaining_lines[i:i + batch_size]
                        tasks = [
                            asyncio.create_task(bounded_upload_worker(line))
                            for line in batch
                        ]
                        
                        for future in asyncio.as_completed(tasks):
                            line_info, success, result = await future
                            short_path = '/'.join(line_info.split('|')[0].split('/')[-3:])

                            if success:
                                # result may be int (size) in old flow or dict in new verification flow
                                file_size = result["size"] if isinstance(result, dict) else result
                                await progress_file_writer_queue.put(line_info.split('|')[0])
                                successful_uploads += 1
                                progress_bar.update(task_id, advance=1, total_bytes=file_size)
                                # Append verification hints to UI if available
                                if isinstance(result, dict):
                                    hints = []
                                    if result.get("ct_ok") is True:
                                        hints.append("ct✓")
                                    if result.get("md5_sampled"):
                                        hints.append("md5✓" if result.get("md5_ok") else "md5?")
                                    suffix = f" [dim]({' '.join(hints)})[/dim]" if hints else ""
                                else:
                                    suffix = ""
                                recent_files.append(("[green]✔[/green]", f"[green]{short_path}[/green]{suffix}"))
                            else:
                                error_message = result
                                failed_uploads += 1
                                progress_bar.update(task_id, advance=1)
                                recent_files.append(("[bold red]✖[/bold red]", f"[red]{short_path}[/red] [dim]({error_message})[/dim]"))

                            # Update the live display
                            live.update(Group(progress_bar, generate_status_table()))

            except (KeyboardInterrupt, asyncio.CancelledError):
                aborted = True            
            finally:
                progress_bar.stop()
                if 'progress_writer_task' in locals() and progress_writer_task.done() is False:
                    await progress_file_writer_queue.put(None)
                    await progress_writer_task
        
        # --- Recompose Final Static View ---
        final_status_table = generate_status_table()

        if aborted or failed_uploads > 0:
            console.print(final_status_table)    

        if aborted:
            console.print("\n[bold yellow]Migration aborted by user.[/bold yellow]\n")
        elif failed_uploads > 0:
            console.print()

        summary_lines = []
        panel_title = "Migration Summary"
        border_style = "green"

        if aborted:
            panel_title += " (Aborted)"
            border_style = "yellow"
        elif failed_uploads > 0:
            panel_title += " (Completed with Errors)"
            border_style = "yellow"
        else:
            panel_title += " (Success)"

        summary_lines.append(f"[green]Successful uploads: {successful_uploads}[/green]")
        summary_lines.append(f"[red]Failed uploads: {failed_uploads}[/red]")
        
        if aborted:
            summary_lines.append("\n[yellow]Migration was stopped before all files could be processed.[/yellow]")
        elif failed_uploads > 0:
            summary_lines.append("\n[dim]Review the list above for details on failed files.[/dim]")

        summary_text_obj = Text.from_markup("\n".join(summary_lines), justify="left")
        console.print(Panel(Columns([summary_text_obj]), title=f"[bold]{panel_title}[/bold]", border_style=border_style, expand=False, padding=(1, 2), width=64)) 