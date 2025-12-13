"""Maintenance policies management commands for Opsgenie CLI."""

import json
from datetime import datetime, timezone, timedelta
from typing import Annotated, Any, Dict, List, Optional, Tuple
import typer
from rich.console import Console
from opsgeniecli.helper import _apply_regex_filters, get_table

app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Manage Opsgenie maintenance policies",
)
console = Console()


def _get_maintenance_policies_table_data(
    policies: List[Any], show_team: bool = False
) -> List[Dict[str, Any]]:
    """
    Transform maintenance policy data into a flat dictionary structure for table display.

    Args:
        policies: List of maintenance policy objects
        show_team: Include team information in the table

    Returns:
        List of dictionaries with policy data suitable for table display
    """
    result = []
    for policy in policies:
        row = {
            "ID": policy.id,
            "Status": policy.status,
            "Description": policy.description,
            "Type": policy.type,
            "Start Date": (
                str(policy.start_date) if hasattr(policy, "start_date") else ""
            ),
            "End Date": str(policy.end_date) if hasattr(policy, "end_date") else "",
        }

        # Add team info if requested and available
        if show_team and hasattr(policy, "_data") and policy._data:
            rules = policy._data.get("rules", [])
            if rules:
                # Get team from first rule's entity
                entity = rules[0].get("entity", {})
                row["Team"] = entity.get("name", "")

        result.append(row)

    return result


def _find_alert_policies_by_filter(
    opsgenie, team_id: str, filter_pattern: str
) -> List[Dict[str, Any]]:
    """
    Find alert policies matching a filter pattern.

    Args:
        opsgenie: Opsgenie client instance
        team_id: Team ID to search within
        filter_pattern: Pattern to match against policy names

    Returns:
        List of matching alert policies
    """
    policies = opsgenie.list_alert_policy(team_id)

    return [
        {
            "id": policy.id,
            "name": policy.name,
            "enabled": policy.enabled,
            "policyDescription": policy.description or "",
            "teamId": policy._data.get("teamId", ""),
        }
        for policy in policies
        if filter_pattern.lower() in policy.name.lower()
    ]


def _select_policy_interactively(
    policies: List[Dict[str, Any]], prompt_message: str
) -> Optional[str]:
    """
    Display policies in a table and prompt user to select one.

    Args:
        policies: List of policy dictionaries
        prompt_message: Message to display when prompting for selection

    Returns:
        Selected policy ID or None if invalid selection
    """
    # Display table of options
    policies_data = [
        {
            "ID": p.get("id", ""),
            "Name": p.get("name", ""),
            "Type": p.get("type", ""),
            "Enabled": str(p.get("enabled", "")),
        }
        for p in policies
    ]

    table = get_table(data=policies_data, title="Available Policies")
    console.print(table)

    # Prompt for selection
    policy_id = typer.prompt(f"\n{prompt_message}", type=str).strip()

    # Validate selection
    if policy_id and any(p["id"] == policy_id for p in policies):
        return policy_id
    else:
        console.print(f"[red]Invalid selection: '{policy_id}'[/red]")
        return None


def _resolve_policy_ids(
    opsgenie, team_id: str, filters: List[str]
) -> Tuple[List[str], List[str]]:
    """
    Resolve policy IDs from filter patterns with interactive disambiguation.

    Args:
        opsgenie: Opsgenie client instance
        team_id: Team ID to search within
        filters: List of filter patterns

    Returns:
        Tuple of (policy_ids, policy_names)
    """
    policy_ids = []
    policy_names = []

    for filter_pattern in filters:
        matching_policies = _find_alert_policies_by_filter(
            opsgenie, team_id, filter_pattern
        )

        if len(matching_policies) == 0:
            console.print(
                f"[yellow]No alert policies found for filter '{filter_pattern}'[/yellow]"
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
                f"[yellow]Multiple alert policies found for '{filter_pattern}':[/yellow]"
            )
            selected_id = _select_policy_interactively(
                matching_policies, "Enter the ID of the policy you want to use"
            )
            if selected_id:
                policy_ids.append(selected_id)
                selected_policy = next(
                    p for p in matching_policies if p["id"] == selected_id
                )
                policy_names.append(selected_policy["name"])

    return policy_ids, policy_names


def _find_maintenance_policies_by_filter(
    opsgenie, filter_pattern: str, non_expired: bool = True
) -> List[Dict[str, Any]]:
    """
    Find maintenance policies matching a filter pattern.

    Args:
        opsgenie: Opsgenie client instance
        filter_pattern: Pattern to match against policy descriptions
        non_expired: Only return non-expired policies

    Returns:
        List of matching maintenance policies
    """
    policies = opsgenie.list_maintenance(non_expired=non_expired)

    return [
        {
            "id": policy.id,
            "description": policy.description or "",
            "status": policy.status,
            "type": policy.type,
            "start_date": policy.start_date,
            "end_date": policy.end_date,
        }
        for policy in policies
        if filter_pattern.lower() in (policy.description or "").lower()
    ]


def _select_maintenance_policy_interactively(
    policies: List[Dict[str, Any]], action: str
) -> Optional[str]:
    """
    Display maintenance policies in a table and prompt user to select one.

    Args:
        policies: List of maintenance policy dictionaries
        action: Action to perform (for prompt message)

    Returns:
        Selected policy ID or None if invalid selection
    """
    # Display table of options
    policies_data = [
        {
            "ID": p.get("id", ""),
            "Description": p.get("description", ""),
            "Status": p.get("status", ""),
            "Type": p.get("time", {}).get("type", ""),
        }
        for p in policies
    ]

    table = get_table(data=policies_data, title="Maintenance Policies")
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


@app.command(name="list")
def list_maintenance_policies(
    ctx: typer.Context,
    team: Annotated[Optional[str], typer.Option(help="Filter by team name")] = None,
    active: Annotated[
        bool, typer.Option("--active", help="Show only active/scheduled policies")
    ] = False,
    past: Annotated[
        bool, typer.Option("--past", help="Show only past/expired policies")
    ] = False,
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Regex filters in format 'field:pattern'"),
    ] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON instead of table")
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", help="Show debug information about policy structure"),
    ] = False,
) -> None:
    """
    List maintenance policies.

    By default shows all policies. Use --active to show only non-expired policies
    or --past to show only expired policies.

    Note: Team filtering is not supported because the Opsgenie API does not include
    team information in the list response. Use --filters to search by description.

    Args:
        team: (Not supported - displays warning and shows all policies)
        active: Show only active or scheduled policies
        past: Show only past/expired policies
        filters: Regex filters in format "field:pattern"
        json_output: Output as JSON instead of table

    Examples:
        List all maintenance policies:
            opsgeniecli maintenance-policies list

        List only active policies:
            opsgeniecli maintenance-policies list --active

        List past policies:
            opsgeniecli maintenance-policies list --past

        Filter by description:
            opsgeniecli maintenance-policies list --filters "Description:deployment"

        Filter active policies by description:
            opsgeniecli maintenance-policies list --active --filters "Description:holiday"
    """
    # Validate mutually exclusive options
    if active and past:
        console.print("[red]Error: --active and --past are mutually exclusive[/red]")
        raise typer.Exit(code=1)

    # Check if team filtering is requested - this is not supported due to API limitations
    if team:
        console.print(
            "[yellow]Warning: Team filtering is not available for maintenance policies.[/yellow]"
        )
        console.print(
            "[yellow]The Opsgenie API does not include team information in the list_maintenance response.[/yellow]\n"
        )
        console.print(
            "[cyan]To filter maintenance policies by team, use a profile with a team-specific API key:[/cyan]"
        )
        console.print(
            "  opsgeniecli --profile <team-profile> maintenance-policies list\n"
        )
        console.print(
            "[dim]Alternatively, use --filters to filter by description.[/dim]"
        )
        raise typer.Exit(code=1)

    console.print("[cyan]Fetching maintenance policies...[/cyan]")

    # Fetch policies based on filter
    non_expired = active if active else not past
    policies = ctx.obj.opsgenie.list_maintenance(non_expired=non_expired)

    if not policies:
        console.print("[yellow]No maintenance policies found[/yellow]")
        return

    # Debug mode: show raw policy structure
    if debug and policies:
        console.print(
            f"\n[yellow]DEBUG: Showing first policy structure (total: {len(policies)} policies)[/yellow]"
        )
        first_policy = policies[0]
        console.print("\n[cyan]Policy attributes:[/cyan]")
        console.print(
            f"  - dir(policy): {[attr for attr in dir(first_policy) if not attr.startswith('_')]}"
        )

        if hasattr(first_policy, "_data"):
            console.print("\n[cyan]Policy._data structure:[/cyan]")
            console.print_json(json.dumps(first_policy._data, indent=2, default=str))

        if hasattr(first_policy, "rules"):
            console.print(f"\n[cyan]Policy.rules:[/cyan] {first_policy.rules}")

        console.print("\n")

    # Additional time-based filtering if needed
    if active or past:
        current_time = datetime.now(timezone.utc)
        filtered_policies = []
        for policy in policies:
            if hasattr(policy, "end_date") and policy.end_date is not None:
                if active and policy.end_date > current_time:
                    filtered_policies.append(policy)
                elif past and policy.end_date <= current_time:
                    filtered_policies.append(policy)
            else:
                # If no end_date, include in non-filtered results
                if not active and not past:
                    filtered_policies.append(policy)
        policies = filtered_policies

    if not policies:
        console.print("[yellow]No maintenance policies match the criteria[/yellow]")
        return

    if json_output:
        policies_json = [
            {
                "id": p.id,
                "status": p.status,
                "description": p.description,
                "type": p.type,
                "start_date": str(p.start_date) if hasattr(p, "start_date") else None,
                "end_date": str(p.end_date) if hasattr(p, "end_date") else None,
            }
            for p in policies
        ]
        console.print_json(json.dumps(policies_json, indent=4, sort_keys=True))
        return

    # Transform to table data (team info not available from API)
    policies_data = _get_maintenance_policies_table_data(policies, show_team=False)

    # Apply filters if provided
    if filters:
        filter_dict = {k: v for k, v in (f.split(":", 1) for f in filters)}
        policies_data = _apply_regex_filters(data=policies_data, filters=filter_dict)

    if not policies_data:
        console.print("[yellow]No policies match the filter criteria[/yellow]")
        return

    console.print(f"\n[green]Found {len(policies_data)} policy/policies[/green]")
    table = get_table(data=policies_data, title="Maintenance Policies")
    console.print(table)


@app.command(name="get")
def get_maintenance_policy(
    ctx: typer.Context,
    id: Annotated[str, typer.Option("--id", help="Maintenance policy ID", prompt=True)],
) -> None:
    """
    Get detailed information about a specific maintenance policy.

    Args:
        id: The ID of the maintenance policy to retrieve

    Examples:
        Get policy by ID (with prompt):
            opsgeniecli maintenance-policies get

        Get policy by ID (direct):
            opsgeniecli maintenance-policies get --id "abc123-def456"
    """
    try:
        console.print(f"[cyan]Fetching maintenance policy '{id}'...[/cyan]")
        result = ctx.obj.opsgenie.get_maintenance(id)
        console.print_json(json.dumps(result, indent=4, sort_keys=True))
    except Exception as e:
        console.print("[red]Error: Failed to retrieve maintenance policy[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command(name="set")
def set_maintenance_policy(
    ctx: typer.Context,
    description: Annotated[
        str,
        typer.Option(prompt=True, help="Description/name of the maintenance policy"),
    ],
    team: Annotated[str, typer.Option(help="Team name")],
    id: Annotated[
        Optional[List[str]],
        typer.Option(
            "--id", help="Policy/integration IDs (can be specified multiple times)"
        ),
    ] = None,
    filter: Annotated[
        Optional[List[str]],
        typer.Option(
            "--filter", help="Filter by policy name (can be specified multiple times)"
        ),
    ] = None,
    hours: Annotated[
        Optional[int], typer.Option(help="Duration in hours from now")
    ] = None,
    start_date: Annotated[
        Optional[str], typer.Option(help="Start date (ISO format: 2019-03-15T14:34:09)")
    ] = None,
    end_date: Annotated[
        Optional[str], typer.Option(help="End date (ISO format: 2019-03-15T15:34:09)")
    ] = None,
    state: Annotated[
        str, typer.Option(help="State of the rule (enabled/disabled)")
    ] = "enabled",
    entity: Annotated[
        str, typer.Option(help="Entity type (integration/policy)")
    ] = "policy",
) -> None:
    """
    Create a maintenance policy.

    You must specify either --id or --filter for the policies/integrations to maintain.
    You must specify either --hours OR both --start-date and --end-date.

    Args:
        description: Description/name of the maintenance policy
        team: Team name
        id: IDs of policies/integrations to maintain
        filter: Filter patterns to find policies by name
        hours: Duration in hours from now
        start_date: Start date and time
        end_date: End date and time
        state: State of the rule (enabled/disabled)
        entity: Entity type (integration/policy)

    Examples:
        Create maintenance for 8 hours using policy IDs:
            opsgeniecli maintenance-policies set --team "ops-team" --description "Deployment" --hours 8 --id "policy-id-1" --id "policy-id-2"

        Create maintenance with specific dates using filters:
            opsgeniecli maintenance-policies set --team "ops-team" --description "Planned maintenance" --filter "production" --start-date "2024-03-15T14:00:00" --end-date "2024-03-15T16:00:00"
    """
    # Validate entity type
    if entity not in ["integration", "policy"]:
        console.print("[red]Error: --entity must be 'integration' or 'policy'[/red]")
        raise typer.Exit(code=1)

    # Validate state
    if state not in ["enabled", "disabled"]:
        console.print("[red]Error: --state must be 'enabled' or 'disabled'[/red]")
        raise typer.Exit(code=1)

    # Validate ID or filter provided
    if not id and not filter:
        console.print("[red]Error: Either --id or --filter is required[/red]")
        raise typer.Exit(code=1)

    if id and filter:
        console.print("[red]Error: --id and --filter are mutually exclusive[/red]")
        raise typer.Exit(code=1)

    # Validate time parameters
    if hours and (start_date or end_date):
        console.print(
            "[red]Error: --hours cannot be used with --start-date or --end-date[/red]"
        )
        raise typer.Exit(code=1)

    if not hours and not (start_date and end_date):
        console.print(
            "[red]Error: Must specify either --hours OR both --start-date and --end-date[/red]"
        )
        raise typer.Exit(code=1)

    # Get team to retrieve team_id
    console.print(f"[cyan]Fetching team '{team}'...[/cyan]")
    team_obj = ctx.obj.opsgenie.get_team_by_name(team)
    team_id = team_obj.id

    # Resolve policy IDs from filters if needed
    policy_ids = list(id) if id else []
    policy_names = []

    if filter:
        resolved_ids, resolved_names = _resolve_policy_ids(
            ctx.obj.opsgenie, team_id, list(filter)
        )
        policy_ids.extend(resolved_ids)
        policy_names.extend(resolved_names)

    if not policy_ids:
        console.print("[red]Error: No valid policies found[/red]")
        raise typer.Exit(code=1)

    # Calculate dates
    if hours:
        start_dt = datetime.now(timezone.utc)
        end_dt = start_dt + timedelta(hours=hours)
        start_iso = start_dt.isoformat()
        end_iso = end_dt.isoformat()
    else:
        # Parse and validate dates
        # These are guaranteed to be non-None by validation above
        assert start_date is not None
        assert end_date is not None
        try:
            start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

            if start_dt >= end_dt:
                console.print("[red]Error: Start date must be before end date[/red]")
                raise typer.Exit(code=1)

            start_iso = start_dt.isoformat()
            end_iso = end_dt.isoformat()
        except ValueError as e:
            console.print(f"[red]Error parsing dates: {e}[/red]")
            raise typer.Exit(code=1)

    # Create maintenance policy
    try:
        if hours:
            result = ctx.obj.opsgenie.set_maintenance_hours(
                team_id, hours, entity, description, state, policy_ids
            )
        else:
            result = ctx.obj.opsgenie.set_maintenance_schedule(
                team_id, start_iso, end_iso, entity, description, state, policy_ids
            )

        if result.status_code == 201:
            console.print("[green]✓ Maintenance policy created successfully[/green]\n")
            console.print(f"  [cyan]Description:[/cyan] {description}")
            if hours:
                console.print(f"  [cyan]Duration:[/cyan] {hours} hours")
            else:
                console.print(f"  [cyan]Start:[/cyan] {start_dt}")
                console.print(f"  [cyan]End:[/cyan] {end_dt}")
            if policy_names:
                console.print(f"  [cyan]Policies:[/cyan] {', '.join(policy_names)}")
        else:
            console.print(
                f"[red]Failed to create maintenance policy: {result.status_code}[/red]"
            )
            raise typer.Exit(code=1)

    except Exception as e:
        console.print("[red]Error: Failed to create maintenance policy[/red]")
        console.print(f"[red]{str(e)}[/red]")
        # Try to get more details from the response if available
        response = getattr(e, 'response', None)
        if response is not None:
            try:
                error_details = response.json()
                console.print(f"[red]API Response: {json.dumps(error_details, indent=2)}[/red]")
            except:
                console.print(f"[red]Response text: {response.text}[/red]")
        raise typer.Exit(code=1)


@app.command(name="cancel")
def cancel_maintenance_policy(
    ctx: typer.Context,
    id: Annotated[
        Optional[List[str]],
        typer.Option(
            "--id", help="Policy IDs to cancel (can be specified multiple times)"
        ),
    ] = None,
    filter: Annotated[
        Optional[List[str]],
        typer.Option(
            "--filter", help="Filter by description (can be specified multiple times)"
        ),
    ] = None,
) -> None:
    """
    Cancel one or more maintenance policies.

    You must specify either --id or --filter.

    Args:
        id: IDs of maintenance policies to cancel
        filter: Filter patterns to find policies by description

    Examples:
        Cancel by ID:
            opsgeniecli maintenance-policies cancel --id "policy-id-1" --id "policy-id-2"

        Cancel by filter:
            opsgeniecli maintenance-policies cancel --filter "deployment"
    """
    # Validate input
    if not id and not filter:
        console.print("[red]Error: Either --id or --filter is required[/red]")
        raise typer.Exit(code=1)

    if id and filter:
        console.print("[red]Error: --id and --filter are mutually exclusive[/red]")
        raise typer.Exit(code=1)

    policy_ids = list(id) if id else []
    policy_descriptions = []

    # Resolve IDs from filters if needed
    if filter:
        for filter_pattern in filter:
            matching = _find_maintenance_policies_by_filter(
                ctx.obj.opsgenie, filter_pattern, non_expired=True
            )

            if len(matching) == 0:
                console.print(
                    f"[yellow]No policies found for filter '{filter_pattern}'[/yellow]"
                )
                continue

            if len(matching) == 1:
                policy_ids.append(matching[0]["id"])
                policy_descriptions.append(matching[0]["description"])
                console.print(
                    f"[green]Found policy: {matching[0]['description']}[/green]"
                )
            else:
                console.print(
                    f"[yellow]Multiple policies found for '{filter_pattern}':[/yellow]"
                )
                selected_id = _select_maintenance_policy_interactively(
                    matching, "cancel"
                )
                if selected_id:
                    policy_ids.append(selected_id)
                    selected = next(p for p in matching if p["id"] == selected_id)
                    policy_descriptions.append(selected["description"])

    if not policy_ids:
        console.print("[red]No valid policies to cancel[/red]")
        raise typer.Exit(code=1)

    # Cancel policies
    cancelled_count = 0
    failed_count = 0

    for policy_id in policy_ids:
        try:
            result = ctx.obj.opsgenie.cancel_maintenance(policy_id)

            if result.get("result") == "Cancelled":
                cancelled_count += 1
            else:
                console.print(f"[yellow]Warning: Unexpected response for {policy_id}: {result}[/yellow]")
                failed_count += 1
        except Exception as e:
            console.print(f"[red]Error cancelling policy {policy_id}: {str(e)}[/red]")
            failed_count += 1

    # Summary
    if cancelled_count > 0:
        console.print(
            f"[green]✓ Successfully cancelled {cancelled_count} maintenance policy/policies[/green]"
        )
        if policy_descriptions:
            console.print(
                f"  [cyan]Policies:[/cyan] {', '.join(policy_descriptions)}"
            )

    if failed_count > 0:
        console.print(f"[red]Failed to cancel {failed_count} policy/policies[/red]")
        raise typer.Exit(code=1)


@app.command(name="delete")
def delete_maintenance_policy(
    ctx: typer.Context,
    team: Annotated[str, typer.Option(help="Team name")],
    id: Annotated[
        Optional[List[str]],
        typer.Option(
            "--id", help="Policy IDs to delete (can be specified multiple times)"
        ),
    ] = None,
    filter: Annotated[
        Optional[List[str]],
        typer.Option(
            "--filter", help="Filter by description (can be specified multiple times)"
        ),
    ] = None,
    all: Annotated[
        bool, typer.Option("--all", help="Delete ALL maintenance policies for the team")
    ] = False,
    force: Annotated[
        bool, typer.Option("--force", help="Skip confirmation prompt")
    ] = False,
) -> None:
    """
    Delete one or more maintenance policies.

    You must specify one of: --id, --filter, or --all.

    WARNING: This permanently deletes policies!

    Args:
        team: Team name
        id: IDs of policies to delete
        filter: Filter patterns to find policies by description
        all: Delete all maintenance policies for the team
        force: Skip confirmation prompt

    Examples:
        Delete by ID:
            opsgeniecli maintenance-policies delete --team "ops-team" --id "policy-id"

        Delete by filter:
            opsgeniecli maintenance-policies delete --team "ops-team" --filter "test"

        Delete all (with confirmation):
            opsgeniecli maintenance-policies delete --team "ops-team" --all
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

    # Get team
    console.print(f"[cyan]Fetching team '{team}'...[/cyan]")
    team_obj = ctx.obj.opsgenie.get_team_by_name(team)

    policy_ids = []
    policy_descriptions = []

    if all:
        # Get all policies
        all_policies = ctx.obj.opsgenie.list_maintenance()

        if not all_policies:
            console.print("[yellow]No maintenance policies found[/yellow]")
            return

        # Show what will be deleted
        policies_data = [
            {"ID": p.id, "Description": p.description or ""}
            for p in all_policies
        ]

        console.print(
            "[yellow]The following maintenance policies will be deleted:[/yellow]\n"
        )
        table = get_table(data=policies_data, title="Policies to Delete")
        console.print(table)

        if not force and not typer.confirm("\nDo you want to continue?"):
            console.print("Operation cancelled")
            raise typer.Exit()

        policy_ids = [p.id for p in all_policies]

    elif id:
        policy_ids = list(id)

    elif filter:
        # Resolve IDs from filters
        for filter_pattern in filter:
            matching = _find_maintenance_policies_by_filter(
                ctx.obj.opsgenie, filter_pattern, non_expired=True
            )

            if len(matching) == 0:
                console.print(
                    f"[yellow]No policies found for filter '{filter_pattern}'[/yellow]"
                )
                continue

            if len(matching) == 1:
                policy_ids.append(matching[0]["id"])
                policy_descriptions.append(matching[0]["description"])
            else:
                console.print(
                    f"[yellow]Multiple policies found for '{filter_pattern}':[/yellow]"
                )
                selected_id = _select_maintenance_policy_interactively(
                    matching, "delete"
                )
                if selected_id:
                    policy_ids.append(selected_id)
                    selected = next(p for p in matching if p["id"] == selected_id)
                    policy_descriptions.append(selected["description"])

    if not policy_ids:
        console.print("[red]No valid policies to delete[/red]")
        raise typer.Exit(code=1)

    # Delete policies
    try:
        for policy_id in policy_ids:
            result = ctx.obj.opsgenie.delete_maintenance(policy_id)
            if result.status_code == 200:
                console.print(
                    f"[green]✓ Deleted policy: {policy_id} (team: {team_obj.name})[/green]"
                )
            else:
                console.print(f"[red]✗ Failed to delete policy: {policy_id}[/red]")

        console.print(
            f"\n[green]Successfully deleted {len(policy_ids)} policy/policies[/green]"
        )

    except Exception as e:
        console.print("[red]Error: Failed to delete maintenance policies[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
