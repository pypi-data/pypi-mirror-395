from typing import Optional
import typer
from rich.console import Console

from . import __app_name__, __version__
from .files import app as files_app
from .sql import app as sql_app

console = Console()

app = typer.Typer(
    name="ascend",
    no_args_is_help=True,
    help="A CLI for migrating large-scale filesystems and databases to the GCS."
)

def _version_callback(value: bool) -> None:
    if value:
        console.print(f"[bold green]{__app_name__}[/bold green] version [cyan]{__version__}[/cyan]")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

app.add_typer(files_app)
app.add_typer(sql_app)


if __name__ == "__main__":
    app() 