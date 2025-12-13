"""Teams routing rules management commands for Opsgenie CLI."""

import json
from typing import Annotated, Any, Dict, List, Optional
import typer
from rich.console import Console
from opsgeniecli.helper import get_table

app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Manage Opsgenie teams routing rules",
)
console = Console()


def _get_team_id(
    ctx: typer.Context, team_id: Optional[str], team_name: Optional[str]
) -> str:
    """
    Get team ID from either team_id or team_name.

    Args:
        ctx: Typer context
        team_id: Optional team ID
        team_name: Optional team name

    Returns:
        Team ID string

    Raises:
        typer.Exit: If team cannot be resolved
    """
    if team_id:
        return team_id

    if team_name:
        console.print(f"[cyan]Fetching team '{team_name}'...[/cyan]")
        team_obj = ctx.obj.opsgenie.get_team_by_name(team_name)
        return team_obj.id

    # If neither provided, try to use team from context/config
    if hasattr(ctx.obj, "config") and ctx.obj.config:
        profile_data = ctx.obj.config.find_profile_by_name(ctx.obj.profile or "default")
        if profile_data and profile_data.name:
            console.print(
                f"[cyan]Using team from profile: {profile_data.name}[/cyan]"
            )
            team_obj = ctx.obj.opsgenie.get_team_by_name(profile_data.name)
            return team_obj.id

    console.print("[red]Error: Team ID or team name is required[/red]")
    console.print(
        "[dim]Use --team-id or --team-name, or configure a team in your profile[/dim]"
    )
    raise typer.Exit(code=1)


def _get_routing_rules_table_data(
    routing_rules: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Transform routing rules data into a flat dictionary structure for table display.

    Args:
        routing_rules: Dictionary containing routing rules data from the API

    Returns:
        List of dictionaries with routing rule data suitable for table display
    """
    result = []

    # Extract the routing rules from the data
    rules = routing_rules.get("data", {}).get("routingRules", [])

    for idx, rule in enumerate(rules, start=1):
        row = {
            "Order": str(idx),
            "ID": rule.get("id", ""),
            "Name": rule.get("name", ""),
            "Is Default": "Yes" if rule.get("isDefault", False) else "No",
            "Timezone": rule.get("timezone", ""),
            "Notify": rule.get("notify", {}).get("type", ""),
        }

        # Add criteria if available
        criteria = rule.get("criteria", {})
        if criteria:
            conditions = criteria.get("conditions", [])
            if conditions:
                # Show first condition as preview
                first_condition = conditions[0]
                row["Condition"] = (
                    f"{first_condition.get('field', '')} {first_condition.get('operation', '')}"
                )

        result.append(row)

    return result


def _format_routing_rule_details(rule: Dict[str, Any]) -> str:
    """
    Format a single routing rule for detailed display.

    Args:
        rule: Dictionary containing a single routing rule

    Returns:
        Formatted string representation of the rule
    """
    lines = []
    lines.append(f"[cyan]Name:[/cyan] {rule.get('name', 'N/A')}")
    lines.append(f"[cyan]ID:[/cyan] {rule.get('id', 'N/A')}")
    lines.append(f"[cyan]Is Default:[/cyan] {rule.get('isDefault', False)}")
    lines.append(f"[cyan]Timezone:[/cyan] {rule.get('timezone', 'N/A')}")

    # Notify information
    notify = rule.get("notify", {})
    lines.append(f"[cyan]Notify Type:[/cyan] {notify.get('type', 'N/A')}")
    if notify.get("name"):
        lines.append(f"[cyan]Notify Name:[/cyan] {notify.get('name')}")
    if notify.get("id"):
        lines.append(f"[cyan]Notify ID:[/cyan] {notify.get('id')}")

    # Criteria
    criteria = rule.get("criteria", {})
    if criteria:
        lines.append("\n[cyan]Criteria:[/cyan]")
        conditions = criteria.get("conditions", [])
        for idx, condition in enumerate(conditions, start=1):
            lines.append(
                f"  {idx}. {condition.get('field', '')} {condition.get('operation', '')} {condition.get('expectedValue', '')}"
            )

    # Time restrictions
    time_restriction = rule.get("timeRestriction")
    if time_restriction:
        lines.append("\n[cyan]Time Restriction:[/cyan]")
        lines.append(f"  Type: {time_restriction.get('type', 'N/A')}")
        if time_restriction.get("restrictions"):
            for restriction in time_restriction["restrictions"]:
                lines.append(
                    f"  - Start: {restriction.get('startHour', '')}:{restriction.get('startMin', '')} "
                    f"End: {restriction.get('endHour', '')}:{restriction.get('endMin', '')}"
                )

    return "\n".join(lines)


@app.command(name="list")
def list_routing_rules(
    ctx: typer.Context,
    team_id: Annotated[Optional[str], typer.Option(help="Team ID")] = None,
    team_name: Annotated[Optional[str], typer.Option(help="Team name")] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON instead of table")
    ] = False,
    detailed: Annotated[
        bool, typer.Option("--detailed", help="Show detailed view of each routing rule")
    ] = False,
) -> None:
    """
    List all routing rules for a team.

    Routing rules determine how alerts are routed to team members based on
    various criteria such as alert properties, time restrictions, and more.

    Args:
        team_id: Team ID to list routing rules for
        team_name: Team name (alternative to team_id)
        json_output: Output as JSON instead of table
        detailed: Show detailed view of each routing rule

    Examples:
        List routing rules for a team:
            opsgeniecli teams-routing-rules list --team-name "ops-team"

        List with JSON output:
            opsgeniecli teams-routing-rules list --team-id "abc123" --json

        List with detailed view:
            opsgeniecli teams-routing-rules list --team-name "ops-team" --detailed
    """
    resolved_team_id = _get_team_id(ctx, team_id, team_name)

    try:
        console.print("[cyan]Fetching routing rules...[/cyan]")
        result = ctx.obj.opsgenie.get_routing_rules_by_id(resolved_team_id)

        if json_output:
            console.print_json(json.dumps(result, indent=4, sort_keys=True))
            return

        # Extract routing rules
        routing_data = result.get("data", {})
        rules = routing_data.get("routingRules", [])

        if not rules:
            console.print("[yellow]No routing rules found for this team[/yellow]")
            return

        console.print(f"\n[green]Found {len(rules)} routing rule(s)[/green]")

        if detailed:
            # Show detailed view of each rule
            for idx, rule in enumerate(rules, start=1):
                console.print(f"\n[bold]Routing Rule #{idx}[/bold]")
                console.print("─" * 60)
                formatted = _format_routing_rule_details(rule)
                console.print(formatted)
        else:
            # Show table view
            rules_data = _get_routing_rules_table_data(result)
            table = get_table(data=rules_data, title="Routing Rules")
            console.print(table)

            console.print(
                "\n[dim]Tip: Use --detailed for more information about each rule[/dim]"
            )
            console.print("[dim]Tip: Use --json for full JSON output[/dim]")

    except Exception as e:
        console.print("[red]Error: Failed to retrieve routing rules[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command(name="get")
def get_routing_rule(
    ctx: typer.Context,
    rule_id: Annotated[
        str, typer.Option("--rule-id", help="Routing rule ID", prompt=True)
    ],
    team_id: Annotated[Optional[str], typer.Option(help="Team ID")] = None,
    team_name: Annotated[Optional[str], typer.Option(help="Team name")] = None,
    json_output: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """
    Get detailed information about a specific routing rule.

    Args:
        team_id: Team ID
        team_name: Team name (alternative to team_id)
        rule_id: The ID of the routing rule to retrieve
        json_output: Output as JSON

    Examples:
        Get specific routing rule:
            opsgeniecli teams-routing-rules get --team-name "ops-team" --rule-id "abc123"

        Get with prompt:
            opsgeniecli teams-routing-rules get --team-name "ops-team"
    """
    resolved_team_id = _get_team_id(ctx, team_id, team_name)

    try:
        console.print("[cyan]Fetching routing rules...[/cyan]")
        result = ctx.obj.opsgenie.get_routing_rules_by_id(resolved_team_id)

        # Find the specific rule
        rules = result.get("data", {}).get("routingRules", [])
        matching_rule = None

        for rule in rules:
            if rule.get("id") == rule_id:
                matching_rule = rule
                break

        if not matching_rule:
            console.print(f"[red]Error: Routing rule '{rule_id}' not found[/red]")

            # Show available rule IDs
            if rules:
                console.print("\n[yellow]Available routing rule IDs:[/yellow]")
                for rule in rules:
                    console.print(
                        f"  - {rule.get('id')} ({rule.get('name', 'Unnamed')})"
                    )

            raise typer.Exit(code=1)

        if json_output:
            console.print_json(json.dumps(matching_rule, indent=4, sort_keys=True))
        else:
            console.print("\n[bold]Routing Rule Details[/bold]")
            console.print("─" * 60)
            formatted = _format_routing_rule_details(matching_rule)
            console.print(formatted)

    except typer.Exit:
        raise
    except Exception as e:
        console.print("[red]Error: Failed to retrieve routing rule[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
