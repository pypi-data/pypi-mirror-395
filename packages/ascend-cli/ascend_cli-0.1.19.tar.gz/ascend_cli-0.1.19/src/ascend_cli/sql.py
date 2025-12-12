import typer
from rich.console import Console
from pathlib import Path

from .logic import sql_logic
from .config import ConfigManager, get_config_path, ConfigError

app = typer.Typer(
    name="sql",
    help="Commands for database backup and restore using mydumper/myloader.",
    no_args_is_help=True
)

@app.command()
def backup(
    gcs_target_prefix: str = typer.Option(
        None, "--gcs-target-prefix", "-p", help="Optional GCS prefix (folder). Overrides config file."
    ),
    config_file: Path = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to the configuration file. Overrides default 'config.conf'.",
        exists=True,
        readable=True,
        resolve_path=True,
    )
):
    """
    Backs up a Cloud SQL database using mydumper and uploads it to GCS.
    """
    try:
        effective_config_path = get_config_path(config_file)
        config = ConfigManager(effective_config_path, section="sql")
        config.load(gcs_target_prefix=gcs_target_prefix)

        sql_logic.run_backup(config)

    except (ConfigError, sql_logic.SQLConfigError, sql_logic.MyDumperError, sql_logic.GCSUploadError) as e:
        raise typer.Exit(code=1)
    except Exception:
        raise typer.Exit(code=1)

@app.command()
def restore(
    backup_file: str = typer.Argument(None, help="The specific backup file from GCS to restore. If omitted, a list will be shown."),
    gcs_target_prefix: str = typer.Option(
        None, "--gcs-target-prefix", "-p", help="Optional GCS prefix (folder). Overrides config file."
    ),
    config_file: Path = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to the configuration file. Overrides default 'config.conf'.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Restores a database backup from GCS to a target MySQL server using myloader.
    """
    try:
        effective_config_path = get_config_path(config_file)
        config = ConfigManager(effective_config_path, section="sql")
        config.load(gcs_target_prefix=gcs_target_prefix)

        sql_logic.run_restore(config, backup_file)
    except (ConfigError, Exception) as e:
        raise typer.Exit(code=1) 