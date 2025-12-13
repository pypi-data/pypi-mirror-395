import json
from typing import Annotated, Any, List, Optional
import typer
from rich.console import Console
from opsgeniecli.helper import _apply_regex_filters, get_table

app = typer.Typer(
    rich_markup_mode="rich", no_args_is_help=True, help="Manage Opsgenie heartbeats"
)
console = Console()


def _get_heartbeats_table_data(
    heartbeats: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Convert heartbeats data to flat dict format for table display."""
    return [
        {
            "name": heartbeat.get("name", ""),
            "enabled": str(heartbeat.get("enabled", False)),
            "interval": str(heartbeat.get("interval", "")),
            "intervalUnit": heartbeat.get("intervalUnit", ""),
            "expired": str(heartbeat.get("expired", False)),
        }
        for heartbeat in heartbeats
    ]


@app.command(name="ping")
def ping_heartbeat(
    ctx: typer.Context,
    name: Annotated[str, typer.Option("--name", help="The name of the heartbeat")],
):
    """Ping a heartbeat to indicate it is still active.

    Sends a ping signal to the specified heartbeat. This is typically called
    by monitoring systems to indicate they are still running properly.

    Args:
        name: The name of the heartbeat to ping (required)

    Examples:
        Ping a heartbeat:
            opsgeniecli heartbeat ping --name "daily-backup-job"
    """
    result = ctx.obj.opsgenie.ping_heartbeat(name)
    console.print_json(json.dumps(result, indent=4, sort_keys=True))


@app.command(name="get")
def get_heartbeat(
    ctx: typer.Context,
    name: Annotated[str, typer.Option("--name", help="The name of the heartbeat")],
):
    """Get details of a specific heartbeat by name.

    Retrieves and displays detailed information about a single heartbeat including
    its status, interval, and expiration state.

    Args:
        name: The name of the heartbeat to retrieve (required)

    Examples:
        Get heartbeat details:
            opsgeniecli heartbeat get --name "daily-backup-job"
    """
    result = ctx.obj.opsgenie.get_heartbeat(name)
    console.print_json(json.dumps(result, indent=4, sort_keys=True))


@app.command(name="list")
def list_heartbeats(
    ctx: typer.Context,
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Regex filters in format 'field:pattern'"),
    ] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON instead of table")
    ] = False,
):
    """List all heartbeats with optional filtering.

    Retrieves all heartbeats and displays them in a table format or as JSON.
    Supports regex-based filtering on any field.

    Args:
        filters: Regex filters in format "field:pattern" (can be specified multiple times)
        json_output: Output as JSON instead of table (default: False)

    Examples:
        List all heartbeats:
            opsgeniecli heartbeat list

        List as JSON:
            opsgeniecli heartbeat list --json

        Filter by name pattern:
            opsgeniecli heartbeat list --filters "name:backup"

        Filter for expired heartbeats:
            opsgeniecli heartbeat list --filters "expired:True"
    """
    result = ctx.obj.opsgenie.list_heartbeats()

    if json_output:
        console.print_json(json.dumps(result, indent=4, sort_keys=True))
        return

    heartbeats_data = _get_heartbeats_table_data(result.get("data", []))

    if filters:
        filter_dict = {k: v for k, v in (filter.split(":", 1) for filter in filters)}
        heartbeats_data = _apply_regex_filters(
            data=heartbeats_data, filters=filter_dict
        )

    table = get_table(data=heartbeats_data, title="Heartbeats")
    console.print(table)


@app.command(name="enable")
def enable_heartbeat(
    ctx: typer.Context,
    name: Annotated[str, typer.Option("--name", help="The name of the heartbeat")],
):
    """Enable a heartbeat.

    Enables monitoring for the specified heartbeat. When enabled, Opsgenie will
    create alerts if the heartbeat is not pinged within its configured interval.

    Args:
        name: The name of the heartbeat to enable (required)

    Examples:
        Enable a heartbeat:
            opsgeniecli heartbeat enable --name "daily-backup-job"
    """
    result = ctx.obj.opsgenie.enable_heartbeat(name)
    console.print_json(json.dumps(result, indent=4, sort_keys=True))


@app.command(name="disable")
def disable_heartbeat(
    ctx: typer.Context,
    name: Annotated[str, typer.Option("--name", help="The name of the heartbeat")],
):
    """Disable a heartbeat.

    Disables monitoring for the specified heartbeat. When disabled, Opsgenie will
    not create alerts even if the heartbeat is not pinged.

    Args:
        name: The name of the heartbeat to disable (required)

    Examples:
        Disable a heartbeat:
            opsgeniecli heartbeat disable --name "daily-backup-job"
    """
    result = ctx.obj.opsgenie.disable_heartbeat(name)
    console.print_json(json.dumps(result, indent=4, sort_keys=True))
