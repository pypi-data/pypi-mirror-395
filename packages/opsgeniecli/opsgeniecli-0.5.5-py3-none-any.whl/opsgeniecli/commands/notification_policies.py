"""Notification policies management commands for Opsgenie CLI."""

import json
from typing import Annotated, Any, Dict, List, Optional, Tuple
import typer
from rich.console import Console
from opsgeniecli.helper import get_table

app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Manage Opsgenie notification policies",
)
console = Console()


def _get_notification_policies_table_data(
    policies: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Transform notification policy data into a flat dictionary structure for table display.

    Args:
        policies: List of notification policy dictionaries

    Returns:
        List of dictionaries with policy data suitable for table display
    """
    result = []
    for policy in policies:
        row = {
            "ID": policy.get("id", ""),
            "Name": policy.get("name", ""),
            "Type": policy.get("type", ""),
            "Enabled": str(policy.get("enabled", "")),
        }
        result.append(row)

    return result


def _find_notification_policies_by_filter(
    policies: List[Dict[str, Any]], filter_pattern: str
) -> List[Dict[str, Any]]:
    """
    Find notification policies matching a filter pattern.

    Args:
        policies: List of notification policy dictionaries
        filter_pattern: Pattern to match against policy names

    Returns:
        List of matching notification policies
    """
    return [
        policy
        for policy in policies
        if filter_pattern.lower() in policy.get("name", "").lower()
    ]


def _select_notification_policy_interactively(
    policies: List[Dict[str, Any]], action: str
) -> Optional[str]:
    """
    Display notification policies in a table and prompt user to select one.

    Args:
        policies: List of notification policy dictionaries
        action: Action to perform (for prompt message)

    Returns:
        Selected policy ID or None if invalid selection
    """
    # Display table of options
    policies_data = _get_notification_policies_table_data(policies)
    table = get_table(data=policies_data, title="Notification Policies")
    console.print(table)

    # Prompt for selection
    policy_id = typer.prompt(
        f"\nEnter the ID of the policy you want to {action}", type=str
    ).strip()

    # Validate selection
    if policy_id and any(p["id"] == policy_id for p in policies):
        return policy_id
    else:
        console.print(f"[red]Invalid selection: '{policy_id}'[/red]")
        return None


def _resolve_notification_policy_ids(
    policies: List[Dict[str, Any]], filters: List[str], action: str
) -> Tuple[List[str], List[str]]:
    """
    Resolve policy IDs from filter patterns with interactive disambiguation.

    Args:
        policies: List of all notification policy dictionaries
        filters: List of filter patterns
        action: Action to perform (for prompt message)

    Returns:
        Tuple of (policy_ids, policy_names)
    """
    policy_ids = []
    policy_names = []

    for filter_pattern in filters:
        matching_policies = _find_notification_policies_by_filter(
            policies, filter_pattern
        )

        if len(matching_policies) == 0:
            console.print(
                f"[yellow]No notification policies found for filter '{filter_pattern}'[/yellow]"
            )
            continue

        if len(matching_policies) == 1:
            policy_ids.append(matching_policies[0]["id"])
            policy_names.append(matching_policies[0]["name"])
            console.print(
                f"[green]Found policy: {matching_policies[0]['name']}[/green]"
            )
        else:
            console.print(
                f"[yellow]Multiple notification policies found for '{filter_pattern}':[/yellow]"
            )
            selected_id = _select_notification_policy_interactively(
                matching_policies, action
            )
            if selected_id:
                policy_ids.append(selected_id)
                selected_policy = next(
                    p for p in matching_policies if p["id"] == selected_id
                )
                policy_names.append(selected_policy["name"])

    return policy_ids, policy_names


def _get_team_id(ctx: typer.Context, team_name: Optional[str]) -> str:
    """
    Get team ID from team name.

    Args:
        ctx: Typer context
        team_name: Optional team name

    Returns:
        Team ID string

    Raises:
        typer.Exit: If team cannot be resolved
    """
    if team_name:
        console.print(f"[cyan]Fetching team '{team_name}'...[/cyan]")
        team_obj = ctx.obj.opsgenie.get_team_by_name(team_name)
        return team_obj.id

    # If not provided, use team from context/config
    if hasattr(ctx.obj, "config") and ctx.obj.config:
        # Try to get team from current profile
        profile_data = ctx.obj.config.find_profile_by_name(ctx.obj.profile or "default")
        if profile_data and profile_data.name:
            console.print(
                f"[cyan]Using team from profile: {profile_data.name}[/cyan]"
            )
            team_obj = ctx.obj.opsgenie.get_team_by_name(profile_data.name)
            return team_obj.id

    console.print("[red]Error: Team name is required[/red]")
    console.print(
        "[dim]Use --team or configure a team in your profile[/dim]"
    )
    raise typer.Exit(code=1)


@app.command(name="list")
def list_notification_policies(
    ctx: typer.Context,
    team: Annotated[Optional[str], typer.Option(help="Team name")] = None,
    active: Annotated[
        bool, typer.Option("--active", help="Show only enabled policies")
    ] = False,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON instead of table")
    ] = False,
) -> None:
    """
    List notification policies for a team.

    Args:
        team: Team name to list policies for
        active: Show only enabled policies
        json_output: Output as JSON instead of table

    Examples:
        List all notification policies:
            opsgeniecli notification-policies list --team "ops-team"

        List only active policies:
            opsgeniecli notification-policies list --team "ops-team" --active
    """
    resolved_team_id = _get_team_id(ctx, team)

    console.print("[cyan]Fetching notification policies...[/cyan]")
    result = ctx.obj.opsgenie.list_notification_policy(resolved_team_id)
    policies = result.get("data", [])

    if not policies:
        console.print("[yellow]No notification policies found[/yellow]")
        return

    # Filter by active if requested
    if active:
        policies = [p for p in policies if p.get("enabled", False)]

    if not policies:
        console.print("[yellow]No active notification policies found[/yellow]")
        return

    # Sort by name
    policies = sorted(policies, key=lambda x: x.get("name", ""))

    if json_output:
        console.print_json(json.dumps(policies, indent=4, sort_keys=True))
        return

    # Transform to table data
    policies_data = _get_notification_policies_table_data(policies)

    console.print(f"\n[green]Found {len(policies_data)} policy/policies[/green]")
    table = get_table(data=policies_data, title="Notification Policies")
    console.print(table)


@app.command(name="get")
def get_notification_policy(
    ctx: typer.Context,
    id: Annotated[
        str, typer.Option("--id", help="Notification policy ID", prompt=True)
    ],
    team: Annotated[Optional[str], typer.Option(help="Team name")] = None,
) -> None:
    """
    Get detailed information about a specific notification policy.

    Args:
        id: The ID of the notification policy to retrieve
        team: Team name

    Examples:
        Get policy by ID (with prompt):
            opsgeniecli notification-policies get --team "ops-team"

        Get policy by ID (direct):
            opsgeniecli notification-policies get --id "abc123" --team "ops-team"
    """
    resolved_team_id = _get_team_id(ctx, team)

    try:
        console.print(f"[cyan]Fetching notification policy '{id}'...[/cyan]")
        result = ctx.obj.opsgenie.get_notification_policy(id, resolved_team_id)
        console.print_json(json.dumps(result, indent=4, sort_keys=True))
    except Exception as e:
        console.print("[red]Error: Failed to retrieve notification policy[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command(name="enable")
def enable_notification_policy(
    ctx: typer.Context,
    team: Annotated[Optional[str], typer.Option(help="Team name")] = None,
    id: Annotated[
        Optional[List[str]],
        typer.Option(
            "--id", help="Policy IDs to enable (can be specified multiple times)"
        ),
    ] = None,
    filter: Annotated[
        Optional[List[str]],
        typer.Option(
            "--filter", help="Filter by policy name (can be specified multiple times)"
        ),
    ] = None,
) -> None:
    """
    Enable one or more notification policies.

    You must specify either --id or --filter.

    Args:
        team: Team name
        id: IDs of notification policies to enable
        filter: Filter patterns to find policies by name

    Examples:
        Enable by ID:
            opsgeniecli notification-policies enable --team "ops-team" --id "policy-id-1" --id "policy-id-2"

        Enable by filter:
            opsgeniecli notification-policies enable --team "ops-team" --filter "production"
    """
    # Validate input
    if not id and not filter:
        console.print("[red]Error: Either --id or --filter is required[/red]")
        raise typer.Exit(code=1)

    if id and filter:
        console.print("[red]Error: --id and --filter are mutually exclusive[/red]")
        raise typer.Exit(code=1)

    resolved_team_id = _get_team_id(ctx, team)

    policy_ids = list(id) if id else []
    policy_names = []

    # Resolve IDs from filters if needed
    if filter:
        console.print("[cyan]Fetching notification policies...[/cyan]")
        result = ctx.obj.opsgenie.list_notification_policy(resolved_team_id)
        all_policies = result.get("data", [])

        resolved_ids, resolved_names = _resolve_notification_policy_ids(
            all_policies, list(filter), "enable"
        )
        policy_ids.extend(resolved_ids)
        policy_names.extend(resolved_names)

    if not policy_ids:
        console.print("[red]Error: No valid policies found[/red]")
        raise typer.Exit(code=1)

    # Enable policies
    try:
        result = ctx.obj.opsgenie.enable_policy(policy_ids, resolved_team_id)

        if result.get("result") == "Enabled":
            console.print("[green]✓ Notification policies enabled successfully[/green]")
            if policy_names:
                console.print(f"  [cyan]Policies:[/cyan] {', '.join(policy_names)}")
            else:
                console.print(f"  [cyan]Policy IDs:[/cyan] {', '.join(policy_ids)}")
        else:
            console.print(f"[red]Failed to enable policies: {result}[/red]")
            raise typer.Exit(code=1)

    except Exception as e:
        console.print("[red]Error: Failed to enable notification policies[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command(name="disable")
def disable_notification_policy(
    ctx: typer.Context,
    team: Annotated[Optional[str], typer.Option(help="Team name")] = None,
    id: Annotated[
        Optional[List[str]],
        typer.Option(
            "--id", help="Policy IDs to disable (can be specified multiple times)"
        ),
    ] = None,
    filter: Annotated[
        Optional[List[str]],
        typer.Option(
            "--filter", help="Filter by policy name (can be specified multiple times)"
        ),
    ] = None,
) -> None:
    """
    Disable one or more notification policies.

    You must specify either --id or --filter.

    Args:
        team: Team name
        id: IDs of notification policies to disable
        filter: Filter patterns to find policies by name

    Examples:
        Disable by ID:
            opsgeniecli notification-policies disable --team "ops-team" --id "policy-id-1" --id "policy-id-2"

        Disable by filter:
            opsgeniecli notification-policies disable --team "ops-team" --filter "production"
    """
    # Validate input
    if not id and not filter:
        console.print("[red]Error: Either --id or --filter is required[/red]")
        raise typer.Exit(code=1)

    if id and filter:
        console.print("[red]Error: --id and --filter are mutually exclusive[/red]")
        raise typer.Exit(code=1)

    resolved_team_id = _get_team_id(ctx, team)

    policy_ids = list(id) if id else []
    policy_names = []

    # Resolve IDs from filters if needed
    if filter:
        console.print("[cyan]Fetching notification policies...[/cyan]")
        result = ctx.obj.opsgenie.list_notification_policy(resolved_team_id)
        all_policies = result.get("data", [])

        resolved_ids, resolved_names = _resolve_notification_policy_ids(
            all_policies, list(filter), "disable"
        )
        policy_ids.extend(resolved_ids)
        policy_names.extend(resolved_names)

    if not policy_ids:
        console.print("[red]Error: No valid policies found[/red]")
        raise typer.Exit(code=1)

    # Disable policies
    try:
        result = ctx.obj.opsgenie.disable_policy(policy_ids, resolved_team_id)

        if result.get("result") == "Disabled":
            console.print(
                "[green]✓ Notification policies disabled successfully[/green]"
            )
            if policy_names:
                console.print(f"  [cyan]Policies:[/cyan] {', '.join(policy_names)}")
            else:
                console.print(f"  [cyan]Policy IDs:[/cyan] {', '.join(policy_ids)}")
        else:
            console.print(f"[red]Failed to disable policies: {result}[/red]")
            raise typer.Exit(code=1)

    except Exception as e:
        console.print("[red]Error: Failed to disable notification policies[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command(name="delete")
def delete_notification_policy(
    ctx: typer.Context,
    team: Annotated[Optional[str], typer.Option(help="Team name")] = None,
    id: Annotated[
        Optional[List[str]],
        typer.Option(
            "--id", help="Policy IDs to delete (can be specified multiple times)"
        ),
    ] = None,
    filter: Annotated[
        Optional[List[str]],
        typer.Option(
            "--filter", help="Filter by policy name (can be specified multiple times)"
        ),
    ] = None,
    all: Annotated[
        bool,
        typer.Option("--all", help="Delete ALL notification policies for the team"),
    ] = False,
    force: Annotated[
        bool, typer.Option("--force", help="Skip confirmation prompt")
    ] = False,
) -> None:
    """
    Delete one or more notification policies.

    You must specify one of: --id, --filter, or --all.

    WARNING: This permanently deletes policies!

    Args:
        team: Team name
        id: IDs of policies to delete
        filter: Filter patterns to find policies by name
        all: Delete all notification policies for the team
        force: Skip confirmation prompt

    Examples:
        Delete by ID:
            opsgeniecli notification-policies delete --team "ops-team" --id "policy-id"

        Delete by filter:
            opsgeniecli notification-policies delete --team "ops-team" --filter "test"

        Delete all (with confirmation):
            opsgeniecli notification-policies delete --team "ops-team" --all
    """
    # Validate input
    options_count = sum([bool(id), bool(filter), all])
    if options_count == 0:
        console.print("[red]Error: Must specify --id, --filter, or --all[/red]")
        raise typer.Exit(code=1)

    if options_count > 1:
        console.print(
            "[red]Error: --id, --filter, and --all are mutually exclusive[/red]"
        )
        raise typer.Exit(code=1)

    resolved_team_id = _get_team_id(ctx, team)

    policy_ids = []
    policy_names = []

    if all:
        # Get all policies
        console.print("[cyan]Fetching notification policies...[/cyan]")
        result = ctx.obj.opsgenie.list_notification_policy(resolved_team_id)
        all_policies = result.get("data", [])

        if not all_policies:
            console.print("[yellow]No notification policies found[/yellow]")
            return

        # Show what will be deleted
        policies_data = [
            {
                "ID": p.get("id", ""),
                "Name": p.get("name", ""),
                "Enabled": str(p.get("enabled", "")),
            }
            for p in all_policies
        ]

        console.print(
            "[yellow]The following notification policies will be deleted:[/yellow]\n"
        )
        table = get_table(data=policies_data, title="Policies to Delete")
        console.print(table)

        if not force and not typer.confirm("\nDo you want to continue?"):
            console.print("Operation cancelled")
            raise typer.Exit()

        policy_ids = [p.get("id") for p in all_policies]

    elif id:
        policy_ids = list(id)

    elif filter:
        # Get all policies for filtering
        console.print("[cyan]Fetching notification policies...[/cyan]")
        result = ctx.obj.opsgenie.list_notification_policy(resolved_team_id)
        all_policies = result.get("data", [])

        # Resolve IDs from filters
        resolved_ids, resolved_names = _resolve_notification_policy_ids(
            all_policies, list(filter), "delete"
        )
        policy_ids.extend(resolved_ids)
        policy_names.extend(resolved_names)

    if not policy_ids:
        console.print("[red]No valid policies to delete[/red]")
        raise typer.Exit(code=1)

    # Delete policies
    try:
        for policy_id in policy_ids:
            result = ctx.obj.opsgenie.delete_notification_policy(
                policy_id, resolved_team_id
            )
            if result.status_code == 200:
                console.print(f"[green]✓ Deleted policy: {policy_id}[/green]")
            else:
                console.print(f"[red]✗ Failed to delete policy: {policy_id}[/red]")

        console.print(
            f"\n[green]Successfully deleted {len(policy_ids)} policy/policies[/green]"
        )

    except Exception as e:
        console.print("[red]Error: Failed to delete notification policies[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
