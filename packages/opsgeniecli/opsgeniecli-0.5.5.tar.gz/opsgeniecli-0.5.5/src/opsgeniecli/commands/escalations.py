import json
from typing import Annotated, Any, List, Optional
import typer
from rich.console import Console
from opsgeniecli.helper import _apply_regex_filters, get_table

app = typer.Typer(
    rich_markup_mode="rich", no_args_is_help=True, help="Manage Opsgenie escalations"
)
console = Console()


def _get_escalations_table_data(
    escalations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Convert escalations data to flat dict format for table display."""
    return [
        {
            "id": escalation["id"],
            "name": escalation["name"],
            "ownerTeam": escalation.get("ownerTeam", {}).get("name", ""),
        }
        for escalation in escalations
    ]


@app.command(name="get")
def get_escalation(
    ctx: typer.Context,
    id: Annotated[Optional[str], typer.Option(help="Escalation ID")] = None,
    name: Annotated[Optional[str], typer.Option(help="Escalation name")] = None,
):
    """Get details of a specific escalation by ID or name.

    Retrieve and display detailed information about a single escalation.
    You must specify either --id or --name (mutually exclusive).

    Args:
        id: Escalation ID to retrieve
        name: Escalation name to retrieve

    Examples:
        Get escalation by ID:
            opsgeniecli escalations get --id abc123

        Get escalation by name:
            opsgeniecli escalations get --name "L2 Escalation"
    """
    if not id and not name:
        raise typer.BadParameter("Either --id or --name is required")

    if id and name:
        raise typer.BadParameter(
            "--id and --name are mutually exclusive. Please specify only one."
        )

    if id:
        result = ctx.obj.opsgenie.get_escalations_by_id(id)
    else:
        assert name is not None
        result = ctx.obj.opsgenie.get_escalations_by_name(name)

    console.print_json(json.dumps(result, indent=4, sort_keys=True))


@app.command(name="list")
def list_escalations(
    ctx: typer.Context,
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Regex filters in format 'field:pattern'"),
    ] = None,
):
    """List all escalations with optional filtering.

    Retrieves all escalations and displays them in a table format.
    Supports regex-based filtering on any field.

    Args:
        filters: Regex filters in format "field:pattern" (can be specified multiple times)

    Examples:
        List all escalations:
            opsgeniecli escalations list

        Filter by name pattern:
            opsgeniecli escalations list --filters "name:^L[0-9]"

        Filter by owner team:
            opsgeniecli escalations list --filters "ownerTeam:ops"
    """
    result = ctx.obj.opsgenie.list_escalations()
    escalations_data = _get_escalations_table_data(result.get("data", []))

    if filters:
        filter_dict = {k: v for k, v in (filter.split(":", 1) for filter in filters)}
        escalations_data = _apply_regex_filters(
            data=escalations_data, filters=filter_dict
        )

    table = get_table(data=escalations_data, title="Escalations")
    console.print(table)
