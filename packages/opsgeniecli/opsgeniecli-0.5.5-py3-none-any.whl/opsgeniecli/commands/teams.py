import json
from typing import Annotated, Any, List, Optional
import typer
from rich.console import Console
from opsgeniecli.helper import _apply_regex_filters, get_table

app = typer.Typer(
    rich_markup_mode="rich", no_args_is_help=True, help="Manage Opsgenie teams"
)
console = Console()


def _get_team_members_table_data(
    members: list[dict[str, Any]], team_name: str
) -> list[dict[str, Any]]:
    """Convert team members data to flat dict format for table display."""
    return [
        {
            f"{team_name} id": member.get("user", {}).get("id", ""),
            f"{team_name} username": member.get("user", {}).get("username", ""),
        }
        for member in members
    ]


@app.command(name="get")
def get_team(
    ctx: typer.Context,
    id: Annotated[Optional[str], typer.Option("--id", help="Team ID")] = None,
    name: Annotated[Optional[str], typer.Option("--name", help="Team name")] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON instead of table")
    ] = False,
):
    """Get details and members of a specific team by ID or name.

    Retrieves and displays information about a team including all team members.
    You must specify either --id or --name (mutually exclusive).

    Args:
        id: Team ID to retrieve
        name: Team name to retrieve
        json_output: Output as JSON instead of table (default: False)

    Examples:
        Get team by name:
            opsgeniecli teams get --name "ops-team"

        Get team by ID:
            opsgeniecli teams get --id "abc123-def456"

        Get team as JSON:
            opsgeniecli teams get --name "ops-team" --json
    """
    if not id and not name:
        raise typer.BadParameter("Either --id or --name is required")

    if id and name:
        raise typer.BadParameter(
            "--id and --name are mutually exclusive. Please specify only one."
        )

    # Get team details
    if id:
        team = ctx.obj.opsgenie.get_team_by_id(id)
    else:
        assert name is not None
        team = ctx.obj.opsgenie.get_team_by_name(name)

    if json_output:
        console.print_json(
            json.dumps(team.__dict__, indent=4, sort_keys=True, default=str)
        )
        return

    # Display team members in a table
    team_name = team.name
    members_data = _get_team_members_table_data(team.members, team_name)

    if members_data:
        table = get_table(data=members_data, title=f"Team: {team_name}")
        console.print(table)
    else:
        console.print(f"[yellow]Team '{team_name}' has no members[/yellow]")


@app.command(name="list")
def list_teams(
    ctx: typer.Context,
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Regex filters in format 'field:pattern'"),
    ] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON instead of table")
    ] = False,
):
    """List all teams with optional filtering.

    Retrieves all teams and displays them in a table format or as JSON.
    Supports regex-based filtering on any field.

    Args:
        filters: Regex filters in format "field:pattern" (can be specified multiple times)
        json_output: Output as JSON instead of table (default: False)

    Examples:
        List all teams:
            opsgeniecli teams list

        List as JSON:
            opsgeniecli teams list --json

        Filter by name pattern:
            opsgeniecli teams list --filters "name:ops"

        Filter by description:
            opsgeniecli teams list --filters "description:production"
    """
    result = ctx.obj.opsgenie.list_teams()

    if json_output:
        # Convert Team objects to dicts for JSON output
        teams_json = [team.__dict__ for team in result]
        console.print_json(
            json.dumps(teams_json, indent=4, sort_keys=True, default=str)
        )
        return

    # Transform data for table display
    teams_data = [
        {
            "id": getattr(team, "id", ""),
            "name": getattr(team, "name", ""),
            "description": getattr(team, "description", ""),
        }
        for team in result
    ]

    if filters:
        filter_dict = {k: v for k, v in (filter.split(":", 1) for filter in filters)}
        teams_data = _apply_regex_filters(data=teams_data, filters=filter_dict)

    table = get_table(data=teams_data, title="Teams")
    console.print(table)
