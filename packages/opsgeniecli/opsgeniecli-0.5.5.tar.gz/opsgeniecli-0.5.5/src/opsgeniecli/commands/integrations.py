"""Integrations management commands for Opsgenie CLI."""

import json
from typing import Annotated, Any, List, Optional
import typer
from rich.console import Console
from opsgeniecli.helper import _apply_regex_filters, get_table

app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Manage Opsgenie integrations",
)
console = Console()


def _get_integrations_table_data(
    integrations: List[dict[str, Any]],
) -> List[dict[str, Any]]:
    """
    Transform integration data into a flat dictionary structure for table display.

    Args:
        integrations: List of integration dictionaries from the Opsgenie API

    Returns:
        List of dictionaries with integration data suitable for table display
    """
    return [
        {
            "Type": integration.get("type", ""),
            "ID": integration.get("id", ""),
            "Name": integration.get("name", ""),
            "Team ID": integration.get("teamId", ""),
            "Enabled": str(integration.get("enabled", False)),
        }
        for integration in integrations
    ]


@app.command(name="list")
def list_integrations(
    ctx: typer.Context,
    team: Annotated[str, typer.Option(help="Team name to filter integrations")],
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Regex filters in format 'field:pattern'"),
    ] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON instead of table")
    ] = False,
) -> None:
    """
    List integrations for a team.

    The command retrieves all integrations associated with the specified team.

    Args:
        team: The name of the team to list integrations for
        filters: Regex filters in format "field:pattern" (can be specified multiple times)
        json_output: Output as JSON instead of table (default: False)

    Examples:
        List integrations by team name:
            opsgeniecli integrations list --team "ops-team"

        Filter by integration type:
            opsgeniecli integrations list --team "ops-team" --filters "Type:Email"

        Output as JSON:
            opsgeniecli integrations list --team "ops-team" --json
    """
    # Get team object to extract team_id
    console.print(f"[cyan]Fetching team '{team}'...[/cyan]")
    team_obj = ctx.obj.opsgenie.get_team_by_name(team)
    team_id = team_obj.id

    # Fetch integrations for the team
    console.print("[cyan]Fetching integrations for team...[/cyan]")
    result = ctx.obj.opsgenie.list_integrations_by_team_id(team_id)
    integrations_list = result.get("data", [])

    if not integrations_list:
        console.print(
            f"[yellow]No integrations found for team '{team_obj.name}'[/yellow]"
        )
        return

    if json_output:
        console.print_json(json.dumps(integrations_list, indent=4, sort_keys=True))
        return

    # Transform to table data
    integrations_data = _get_integrations_table_data(integrations_list)

    # Apply filters if provided
    if filters:
        filter_dict = {k: v for k, v in (filter.split(":", 1) for filter in filters)}
        integrations_data = _apply_regex_filters(
            data=integrations_data, filters=filter_dict
        )

    # Display results
    if not integrations_data:
        console.print("[yellow]No integrations found matching the criteria.[/yellow]")
        return

    console.print(f"\n[green]Found {len(integrations_data)} integration(s)[/green]")
    table = get_table(
        data=integrations_data, title=f"Integrations for Team: {team_obj.name}"
    )
    console.print(table)


@app.command(name="get")
def get_integration(
    ctx: typer.Context,
    id: Annotated[str, typer.Option("--id", help="Integration ID")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON (default behavior)")
    ] = True,
) -> None:
    """
    Get detailed information about a specific integration.

    Retrieves complete details about an integration by its ID.

    Args:
        id: The ID of the integration to retrieve
        json_output: Output as JSON (always enabled for this command)

    Examples:
        Get integration details:
            opsgeniecli integrations get --id "abc123-def456"
    """
    try:
        console.print(f"[cyan]Fetching integration with ID '{id}'...[/cyan]")
        result = ctx.obj.opsgenie.get_integration_by_id(id)

        console.print_json(json.dumps(result, indent=4, sort_keys=True))

    except Exception as e:
        console.print("[red]Error: Failed to retrieve integration[/red]")
        console.print(f"[red]{str(e)}[/red]")
        console.print(
            "\n[yellow]Make sure the API key has the required permissions.[/yellow]"
        )
        console.print(
            "[yellow]Use --profile <name> to specify a different profile.[/yellow]"
        )
        console.print(
            "[yellow]Use 'opsgeniecli config list' to see available profiles.[/yellow]"
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
