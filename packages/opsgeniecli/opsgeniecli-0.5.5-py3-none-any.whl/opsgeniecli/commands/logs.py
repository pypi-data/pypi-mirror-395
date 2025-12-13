"""Logs management commands for Opsgenie CLI."""

from pathlib import Path
from typing import Optional

import typer
import urllib.request
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)

app = typer.Typer(help="Manage Opsgenie logs", no_args_is_help=True)
console = Console()


@app.command(name="download")
def download_logs(
    ctx: typer.Context,
    marker: str = typer.Option(
        ..., help="Download logs since this marker (date/identifier)"
    ),
    download_path: Path = typer.Option(..., help="Local directory to store log files"),
    limit: Optional[int] = typer.Option(
        None, help="Maximum number of files to download"
    ),
) -> None:
    """
    Download Opsgenie logs to a local directory.

    The marker parameter specifies a date or identifier from which to download logs.
    Files are downloaded sequentially with progress indication.
    """
    # Ensure download path exists
    download_path.mkdir(parents=True, exist_ok=True)

    # Get list of log files
    console.print(f"[cyan]Fetching log files since marker: {marker}...[/cyan]")

    if limit:
        result = ctx.obj.opsgenie.get_logs_filenames(marker, limit)
    else:
        result = ctx.obj.opsgenie.get_logs_filenames(marker)

    log_files = result.get("data", [])
    total_count = len(log_files)

    if total_count == 0:
        console.print("[yellow]No log files found for the specified marker.[/yellow]")
        return

    console.print(f"[green]Found {total_count} log file(s) to download[/green]\n")

    # Download files with progress tracking
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Downloading logs...", total=total_count)

        for idx, file_info in enumerate(log_files, start=1):
            filename = file_info["filename"]
            progress.update(
                task, description=f"[cyan]Downloading {filename} ({idx}/{total_count})"
            )

            try:
                # Get download URL for this file
                download_url_response = ctx.obj.opsgenie.get_logs_download_link(
                    filename
                )
                download_url = download_url_response.text

                # Download file
                destination = download_path / filename
                urllib.request.urlretrieve(download_url, destination)

                progress.advance(task)
            except Exception as e:
                console.print(f"[red]Error downloading {filename}: {e}[/red]")

    console.print(
        f"\n[green]✓ Successfully downloaded {total_count} log file(s) to {download_path}[/green]"
    )
