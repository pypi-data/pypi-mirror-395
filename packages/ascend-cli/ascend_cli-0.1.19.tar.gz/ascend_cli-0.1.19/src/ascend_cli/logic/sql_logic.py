from pathlib import Path
import configparser
import subprocess
import shutil
import tempfile
import datetime
from google.cloud import storage
from google.api_core import exceptions
from rich.console import Console
from rich.prompt import IntPrompt, Confirm

from ..config import ConfigManager, ConfigError

console = Console()

class SQLConfigError(Exception):
    """Custom exception for errors related to SQL configuration."""
    pass

class MyDumperError(Exception):
    """Custom exception for errors during the mydumper backup process."""
    pass

class MyLoaderError(Exception):
    """Custom exception for errors during the myloader restore process."""
    pass

class GCSUploadError(Exception):
    """Custom exception for errors during the GCS upload process."""
    pass

def _check_mydumper_installed():
    """Checks if mydumper is installed and in the system's PATH."""
    if not shutil.which("mydumper"):
        raise MyDumperError(
            "'mydumper' command not found. Please install it and ensure it is in your system's PATH."
        )

def _check_myloader_installed():
    """Checks if myloader is installed and in the system's PATH."""
    if not shutil.which("myloader"):
        raise MyLoaderError(
            "'myloader' command not found. Please install it and ensure it is in your system's PATH."
        )

def run_backup(config: ConfigManager):
    """
    Orchestrates the database backup process.
    1. Parses the configuration file.
    2. Runs mydumper to create a local backup.
    3. Compresses the backup.
    4. Uploads the compressed file to GCS.
    5. Cleans up local files.
    """
    try:
        console.log(f"🔩 Parsing configuration from [cyan]{config.config_file}[/cyan]...")
        
        console.log("🔍 Checking for 'mydumper' executable...")
        _check_mydumper_installed()
        console.log("✅ 'mydumper' is installed.")

        gcs_bucket_name = config.get("gcs_bucket_name")
        db_host = config.get("host")
        db_user = config.get("user")
        db_password = config.get("password")
        db_name = config.get("db_name")
        gcs_target_prefix = config.get("gcs_target_prefix", required=False) # Optional prefix
        gcs_storage_class = config.get("gcs_storage_class", required=False, default="STANDARD").upper()
        mydumper_threads = config.get("threads", required=False, default=4)

        console.log("☁️  Authenticating with Google Cloud Storage...")
        storage_client = storage.Client()
        
        console.log(f"Verifying access to GCS bucket: [cyan]{gcs_bucket_name}[/cyan]...")
        
        bucket = storage_client.get_bucket(gcs_bucket_name)
        console.log(f"✅ Verified access to GCS bucket: [green]{gcs_bucket_name}[/green]")
        
        console.log("[bold green]Configuration and prerequisites verified.[/bold green]")
        
        app_data_dir = config.get_app_data_dir()
        temp_backup_dir = app_data_dir / "temp_sql_backup"
        if temp_backup_dir.exists():
            shutil.rmtree(temp_backup_dir)
        temp_backup_dir.mkdir(parents=True)

        try:
            output_dir = temp_backup_dir
            console.log(f"🏭 Created temporary directory for backup: [cyan]{output_dir}[/cyan]")

            command = [
                "mydumper",
                "--host", db_host,
                "--user", db_user,
                "--password", db_password,
                "--database", db_name,
                "--outputdir", str(output_dir),
                "--threads", str(mydumper_threads),
                "--verbose", "3", # More detailed output
            ]

            console.log("🚀 Starting mydumper backup process...")
            console.log(f"[dim]Executing: {' '.join(command)}[/dim]")

            try:
                with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', bufsize=1) as process:
                    console.log("[bold cyan]--- Mydumper Output ---[/bold cyan]")
                    if process.stdout:
                        for line in iter(process.stdout.readline, ''):
                            console.print(line.strip())
                    console.log("[bold cyan]-----------------------[/bold cyan]")
                
                if process.returncode != 0:
                    raise MyDumperError(f"Mydumper process failed with exit code {process.returncode}. See logs above for details.")

            except FileNotFoundError:
                raise MyDumperError("'mydumper' command not found. Is it installed and in your PATH?")
            
            console.log("✅ Mydumper process completed successfully.")

            # --- Compression ---
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_basename = f"{db_name}_{timestamp}"
            archive_path = Path(tempfile.gettempdir()) / archive_basename
            
            console.log(f"📦 Compressing backup files into a single archive: [cyan]{archive_path}.tar.gz[/cyan]")
            shutil.make_archive(
                base_name=str(archive_path),
                format='gztar',      # tar.gz
                root_dir=output_dir
            )
            archive_file = Path(f"{archive_path}.tar.gz")
            console.log("✅ Compression complete.")

            # --- GCS Upload ---
            if gcs_target_prefix:
                blob_name = f"{gcs_target_prefix.strip('/')}/{archive_file.name}"
            else:
                blob_name = archive_file.name

            console.log(f"☁️ Uploading [cyan]{archive_file.name}[/cyan] to GCS path [cyan]gs://{gcs_bucket_name}/{blob_name}[/cyan]...")
            
            blob = bucket.blob(blob_name)
            blob.storage_class = gcs_storage_class
            blob.upload_from_filename(str(archive_file))
            
            console.log(f"✅ Successfully uploaded to GCS: [green]gs://{gcs_bucket_name}/{blob_name}[/green]")

            # --- Cleanup ---
            console.log(f"🧹 Cleaning up local archive file: [cyan]{archive_file}[/cyan]")
            archive_file.unlink()
            
            console.log("[bold green]🏆 Backup process finished successfully![/bold green]")

        finally:
            if temp_backup_dir.exists():
                shutil.rmtree(temp_backup_dir)

    except (ConfigError, MyDumperError, GCSUploadError) as e:
        console.log(f"[bold red]Error:[/bold red] {e}")
        raise  # Re-raise to be caught by the UI layer and trigger exit
    except exceptions.NotFound:
        console.log(f"[bold red]Error:[/bold red] The GCS bucket '{config.get('gcs_bucket_name', required=False)}' was not found.")
        raise GCSUploadError("Bucket not found.")
    except exceptions.Forbidden:
        console.log(f"[bold red]Error:[/bold red] Permission denied for GCS bucket '{config.get('gcs_bucket_name', required=False)}'.")
        raise GCSUploadError("Permission denied.")
    except Exception as e:
        console.log(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        raise MyDumperError(f"An unexpected error occurred during backup preparation: {e}")

def run_restore(config: ConfigManager, backup_file: str | None):
    """
    Orchestrates the database restore process.
    1. Lists available backups in GCS if no specific file is provided.
    2. Asks for user confirmation.
    3. Downloads the specified backup file from GCS.
    4. Decompresses the backup file.
    5. Runs myloader to restore the database.
    6. Cleans up local files.
    """
    try:
        console.log("🔩 Parsing configuration...")
        gcs_bucket_name = config.get("gcs_bucket_name")
        gcs_target_prefix = config.get("gcs_target_prefix", required=False)
        db_host = config.get("host")
        db_user = config.get("user")
        db_password = config.get("password")
        db_name = config.get("db_name")

        console.log("🔍 Checking for 'myloader' executable...")
        _check_myloader_installed()
        console.log("✅ 'myloader' is installed.")

        console.log("☁️  Authenticating with Google Cloud Storage...")
        storage_client = storage.Client()
        
        console.log(f"Verifying access to GCS bucket: [cyan]{gcs_bucket_name}[/cyan]...")
        bucket = storage_client.get_bucket(gcs_bucket_name)
        console.log(f"✅ Verified access to GCS bucket: [green]{gcs_bucket_name}[/green]")

        blob_to_restore = None

        if backup_file:
            # When a backup file is specified, we must construct the full blob path
            # if a prefix is also in use.
            full_blob_path = f"{gcs_target_prefix.strip('/')}/{backup_file}" if gcs_target_prefix else backup_file
            console.log(f"🔍 Locating specified backup file: [cyan]{full_blob_path}[/cyan]...")
            blob_to_restore = bucket.get_blob(full_blob_path)
            if not blob_to_restore:
                raise GCSUploadError(f"Specified backup file '{full_blob_path}' not found in bucket '{gcs_bucket_name}'.")
            console.log("✅ Backup file located.")
        else:
            prefix_to_list = f"{gcs_target_prefix.strip('/')}/" if gcs_target_prefix else ""
            console.log(f"🔎 Listing available backups in [cyan]gs://{gcs_bucket_name}/{prefix_to_list}[/cyan]...")
            
            blobs = storage_client.list_blobs(gcs_bucket_name, prefix=prefix_to_list)
            
            backup_blobs = [b for b in blobs if b.name.endswith(".tar.gz")]

            if not backup_blobs:
                console.log("[yellow]No backups found at the specified location.[/yellow]")
                return

            console.log("[bold]Available backups:[/bold]")
            for i, blob in enumerate(backup_blobs):
                display_name = blob.name.replace(prefix_to_list, "")
                size_mb = blob.size / 1024 / 1024
                updated_time = blob.updated.strftime('%Y-%m-%d %H:%M')
                console.print(f"  [cyan][{i+1}][/cyan] {display_name} ([dim]size: {size_mb:.2f} MB, updated: {updated_time}[/dim])")
            
            choice = IntPrompt.ask(
                "\n[bold]Enter the number of the backup to restore[/bold]",
                choices=[str(i+1) for i in range(len(backup_blobs))],
                show_choices=False,
                default=1
            )
            blob_to_restore = backup_blobs[choice - 1]

        console.log(f"🎯 Selected for restore: [green]{blob_to_restore.name}[/green]")

        if not Confirm.ask(f"\nThis will [bold red]OVERWRITE[/bold red] the database '[bold yellow]{db_name}[/bold yellow]' on host '[bold yellow]{db_host}[/bold yellow]'.\nAre you sure you want to continue?", default=False):
            console.print("\n[yellow]Restore operation cancelled by user.[/yellow]")
            return

        app_data_dir = config.get_app_data_dir()
        temp_restore_dir = app_data_dir / "temp_sql_restore"
        if temp_restore_dir.exists():
            shutil.rmtree(temp_restore_dir)
        temp_restore_dir.mkdir(parents=True)

        try:
            temp_path = temp_restore_dir
            # Use the last part of the blob name as the local filename
            local_filename = blob_to_restore.name.split("/")[-1]
            download_path = temp_path / local_filename
            extract_dir = temp_path / "extracted"
            extract_dir.mkdir()

            console.log(f"📥 Downloading [cyan]{blob_to_restore.name}[/cyan] to [dim]{download_path}[/dim]...")
            blob_to_restore.download_to_filename(download_path)
            console.log("✅ Download complete.")
            
            console.log(f"📦 Decompressing archive to [cyan]{extract_dir}[/cyan]...")
            shutil.unpack_archive(download_path, extract_dir)
            console.log("✅ Decompression complete.")
            
            command = [
                "myloader",
                "--host", db_host,
                "--user", db_user,
                "--password", db_password,
                "--database", db_name,
                "--directory", str(extract_dir),
                "--overwrite-tables",
                "--verbose", "3"
            ]
            
            console.log("🚀 Starting myloader restore process...")
            console.log(f"[dim]Executing: {' '.join(command)}[/dim]")

            try:
                with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', bufsize=1) as process:
                    console.log("[bold cyan]--- Myloader Output ---[/bold cyan]")
                    if process.stdout:
                        for line in iter(process.stdout.readline, ''):
                            console.print(line.strip())
                    console.log("[bold cyan]-----------------------[/bold cyan]")

                if process.returncode != 0:
                    raise MyLoaderError(f"Myloader process failed with exit code {process.returncode}. See logs above for details.")
            except FileNotFoundError:
                 raise MyLoaderError("'myloader' command not found. Is it installed and in your PATH?")

            console.log("✅ Myloader process completed successfully.")
            console.log("[bold green]🏆 Restore process finished successfully![/bold green]")

        finally:
            if temp_restore_dir.exists():
                shutil.rmtree(temp_restore_dir)

    except (ConfigError, GCSUploadError, MyLoaderError) as e:
        console.log(f"[bold red]Error:[/bold red] {e}")
        raise
    except exceptions.NotFound:
        console.log(f"[bold red]Error:[/bold red] The GCS bucket '{gcs_bucket_name}' was not found.")
        raise GCSUploadError("Bucket not found.")
    except exceptions.Forbidden:
        console.log(f"[bold red]Error:[/bold red] Permission denied for GCS bucket '{gcs_bucket_name}'.")
        raise GCSUploadError("Permission denied.")
    except Exception as e:
        console.log(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        raise 