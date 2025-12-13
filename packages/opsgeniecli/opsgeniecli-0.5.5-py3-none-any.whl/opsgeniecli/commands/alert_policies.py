from typing import Annotated, Any, List, Optional
import typer
from rich.console import Console
from opsgeniecli.helper import _apply_regex_filters, get_table, show_table_and_confirm

app = typer.Typer(
    rich_markup_mode="rich", no_args_is_help=True, help="Manage Opsgenie alert policies"
)
console = Console()


# Helper functions for alert policies


def _alert_policy_to_dict(policy) -> dict[str, Any]:
    """Convert an AlertPolicy object to a dictionary.

    Args:
        policy: AlertPolicy object from opsgenielib

    Returns:
        Dictionary with policy attributes
    """
    return {
        "id": policy.id,
        "name": policy.name,
        "enabled": policy.enabled,
        "policyDescription": policy.description or "",  # Use the description property
        "teamId": policy._data.get("teamId", ""),  # Access raw data for teamId
    }


def _get_alert_policies_table_data(
    policies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Convert alert policy data to flat dictionaries for table display.

    Args:
        policies: List of alert policy dictionaries

    Returns:
        List of flattened dictionaries ready for table display
    """
    return [
        {
            "id": policy["id"],
            "name": policy["name"],
            "enabled": str(policy["enabled"]),
            "description": policy.get("policyDescription", ""),
        }
        for policy in policies
    ]


def _fetch_policies_by_team(opsgenie, team_name: str) -> list[dict[str, Any]]:
    """Fetch alert policies for a specific team.

    Args:
        opsgenie: Opsgenie client instance
        team_name: Team name

    Returns:
        List of alert policy dictionaries
    """
    team = opsgenie.get_team_by_name(team_name)
    team_id = team.id  # Team object uses .id not .team_id

    # Get AlertPolicy objects and convert to dicts
    policy_objects = opsgenie.list_alert_policy(team_id=team_id)
    return [_alert_policy_to_dict(policy) for policy in policy_objects]


def _apply_filters_to_policies(
    policies: list[dict[str, Any]], filters: List[str]
) -> list[dict[str, Any]]:
    """Apply regex filters to alert policies data.

    Args:
        policies: List of alert policy dictionaries
        filters: List of filter strings in format "attribute:pattern"

    Returns:
        Filtered list of alert policies
    """
    if not filters:
        return policies

    filter_dict = {k: v for k, v in (filter.split(":", 1) for filter in filters)}
    table_data = _get_alert_policies_table_data(policies)
    filtered_data = _apply_regex_filters(data=table_data, filters=filter_dict)

    # Match filtered data back to original policies by ID
    filtered_ids = {item["id"] for item in filtered_data}
    return [policy for policy in policies if policy["id"] in filtered_ids]


def _update_policy_status(
    opsgenie, policy_id: str, team_id: str, enabled: bool
) -> dict[str, Any]:
    """Enable or disable an alert policy.

    Args:
        opsgenie: Opsgenie client instance
        policy_id: ID of the alert policy
        team_id: Team ID that owns the policy
        enabled: True to enable, False to disable

    Returns:
        API response dictionary
    """
    # Methods expect a list of IDs
    if enabled:
        return opsgenie.enable_policy(policy_id=[policy_id], team_id=team_id)
    else:
        return opsgenie.disable_policy(policy_id=[policy_id], team_id=team_id)


def _display_policy_update_result(
    policy_name: str, action: str, result: dict[str, Any]
) -> None:
    """Display the result of a policy update operation.

    Args:
        policy_name: Name of the policy that was updated
        action: Action performed (e.g., "enabled", "disabled", "deleted")
        result: API response dictionary
    """
    success = result.get("result") in ["Updated", "Deleted"]
    symbol = "✓" if success else "✗"
    typer.echo(f"{symbol} - Alert policy {action}: {policy_name}")


def _get_policy_by_id(opsgenie, policy_id: str, team_name: str) -> dict[str, Any]:
    """Fetch a single alert policy by ID with full details.

    Args:
        opsgenie: Opsgenie client instance
        policy_id: ID of the alert policy
        team_name: Team name

    Returns:
        Alert policy dictionary

    Raises:
        ValueError: If policy not found
    """
    # Get team ID first
    team = opsgenie.get_team_by_name(team_name)
    team_id = team.id

    # Use get_alert_policy to fetch full details including description
    try:
        policy_obj = opsgenie.get_alert_policy(id_=policy_id, team_id=team_id)
        return _alert_policy_to_dict(policy_obj)
    except Exception as e:
        raise ValueError(f"Alert policy with ID '{policy_id}' not found: {e}")


def _get_validation_table_data(alerts: list) -> list[dict[str, Any]]:
    """Convert Alert objects to table format for validation display.

    Args:
        alerts: List of Alert objects from opsgenielib

    Returns:
        List of dictionaries formatted for table display
    """
    import pytz

    timezone = pytz.timezone("UTC")

    return [
        {
            "id": alert.id[:12] + "...",  # Truncate for readability
            "message": (
                alert.message[:50] + "..." if len(alert.message) > 50 else alert.message
            ),
            "created": str(
                alert.created_at.astimezone(timezone).strftime("%Y-%m-%d %H:%M")
            ),
            "host": alert._data.get("details", {}).get("host", "")[:30] or "N/A",
        }
        for alert in alerts
    ]


def _validate_policy_filter(
    opsgenie, team_name: str, filter_pattern: str, limit: int = 500
) -> list:
    """Query recent alerts and return those matching the filter pattern.

    Args:
        opsgenie: Opsgenie client instance
        team_name: Team name to query alerts for
        filter_pattern: Regex pattern to match against alerts
        limit: Maximum number of alerts to query

    Returns:
        List of Alert objects that match the filter pattern
    """
    import re
    import datetime

    # Verify team exists
    opsgenie.get_team_by_name(team_name)

    # Query recent alerts for the team
    query = f"responders:{team_name}"
    alerts = opsgenie.query_alerts(query=query, limit=limit)

    # Filter to last 7 days
    seven_days_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        days=7
    )
    recent_alerts = [alert for alert in alerts if alert.created_at >= seven_days_ago]

    # Compile the regex pattern
    try:
        regex = re.compile(filter_pattern)
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {e}")

    # Filter alerts matching the pattern in description or host fields
    matching_alerts = []
    for alert in recent_alerts:
        # Check message/description field
        description = alert._data.get("description", "") or alert.message or ""

        # Check host field in extra-properties or details
        host = alert._data.get("details", {}).get("host", "")

        # Match if either field matches
        if regex.search(str(description)) or regex.search(str(host)):
            matching_alerts.append(alert)

    return matching_alerts


# Commands in alphabetical order: delete, disable, enable, get, list, set


@app.command(name="delete")
def delete(
    ctx: typer.Context,
    id: Annotated[
        Optional[str], typer.Option(help="Delete specific policy by ID")
    ] = None,
    team: Annotated[Optional[str], typer.Option(help="Team name (required)")] = None,
    all: Annotated[bool, typer.Option(help="Delete all policies for the team")] = False,
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Filter policies using 'attribute:pattern'"),
    ] = None,
):
    """Delete one or more alert policies.

    Deletes alert policies by ID, or multiple policies using --all or --filters.
    When using --all or --filters, shows a preview table and asks for confirmation.

    Args:
        id: Delete a specific policy by ID (requires --team)
        team: Team name (required)
        all: Delete all policies for the team (requires --team)
        filters: Delete policies matching filters (requires --team)

    Examples:
        Delete by ID:
            opsgeniecli alert-policies delete --id abc123 --team ops-team

        Delete all policies for a team (with confirmation):
            opsgeniecli alert-policies delete --all --team ops-team

        Delete filtered policies:
            opsgeniecli alert-policies delete --filters "name:.*test.*" --team ops-team
    """
    if not any([id, all, filters]):
        raise typer.BadParameter("Must specify one of: --id, --all, or --filters")

    if id and (all or filters):
        raise typer.BadParameter("Cannot use --id with --all or --filters")

    if not team:
        raise typer.BadParameter("Must specify --team")

    # Get team ID for API calls
    team_obj = ctx.obj.opsgenie.get_team_by_name(team)
    team_id = team_obj.id

    # Handle single policy deletion by ID
    if id:
        try:
            policy = _get_policy_by_id(ctx.obj.opsgenie, id, team)
            # delete_alert_policy expects a list of IDs
            result = ctx.obj.opsgenie.delete_alert_policy(
                alert_id=[id], team_id=team_id
            )
            _display_policy_update_result(policy["name"], "deleted", result)
        except ValueError as e:
            typer.echo(f"✗ - {e}")
            raise typer.Exit(code=1)
        return

    # Handle bulk deletion (all or filtered)
    policies = _fetch_policies_by_team(ctx.obj.opsgenie, team)

    if filters:
        policies = _apply_filters_to_policies(policies, filters)

    if not policies:
        typer.echo("No policies found matching criteria")
        return

    # Show preview and confirm
    show_table_and_confirm(
        data=_get_alert_policies_table_data(policies),
        title="Alert Policies to be Deleted",
        prompt="\nAre you sure you want to delete these policies?",
    )

    # Delete each policy
    for policy in policies:
        # delete_alert_policy expects a list of IDs
        result = ctx.obj.opsgenie.delete_alert_policy(
            alert_id=[policy["id"]], team_id=team_id
        )
        _display_policy_update_result(policy["name"], "deleted", result)


@app.command(name="disable")
def disable(
    ctx: typer.Context,
    id: Annotated[
        Optional[str], typer.Option(help="Disable specific policy by ID")
    ] = None,
    team: Annotated[Optional[str], typer.Option(help="Team name (required)")] = None,
    all: Annotated[
        bool, typer.Option(help="Disable all policies for the team")
    ] = False,
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Filter policies using 'attribute:pattern'"),
    ] = None,
):
    """Disable one or more alert policies.

    Disables alert policies by ID, or multiple policies using --all or --filters.
    When using --all or --filters, shows a preview table and asks for confirmation.

    Args:
        id: Disable a specific policy by ID (requires --team)
        team: Team name (required)
        all: Disable all policies for the team (requires --team)
        filters: Disable policies matching filters (requires --team)

    Examples:
        Disable by ID:
            opsgeniecli alert-policies disable --id abc123 --team ops-team

        Disable all policies for a team (with confirmation):
            opsgeniecli alert-policies disable --all --team ops-team

        Disable filtered policies:
            opsgeniecli alert-policies disable --filters "name:.*test.*" --team ops-team
    """
    if not any([id, all, filters]):
        raise typer.BadParameter("Must specify one of: --id, --all, or --filters")

    if id and (all or filters):
        raise typer.BadParameter("Cannot use --id with --all or --filters")

    if not team:
        raise typer.BadParameter("Must specify --team")

    # Get team ID for API calls
    team_obj = ctx.obj.opsgenie.get_team_by_name(team)
    team_id = team_obj.id

    # Handle single policy disable by ID
    if id:
        try:
            policy = _get_policy_by_id(ctx.obj.opsgenie, id, team)
            result = _update_policy_status(ctx.obj.opsgenie, id, team_id, enabled=False)
            _display_policy_update_result(policy["name"], "disabled", result)
        except ValueError as e:
            typer.echo(f"✗ - {e}")
            raise typer.Exit(code=1)
        return

    # Handle bulk disable (all or filtered)
    policies = _fetch_policies_by_team(ctx.obj.opsgenie, team)

    if filters:
        policies = _apply_filters_to_policies(policies, filters)

    if not policies:
        typer.echo("No policies found matching criteria")
        return

    # Show preview and confirm
    show_table_and_confirm(
        data=_get_alert_policies_table_data(policies),
        title="Alert Policies to be Disabled",
        prompt="\nAre you sure you want to disable these policies?",
    )

    # Disable each policy
    for policy in policies:
        result = _update_policy_status(
            ctx.obj.opsgenie, policy["id"], team_id, enabled=False
        )
        _display_policy_update_result(policy["name"], "disabled", result)


@app.command(name="enable")
def enable(
    ctx: typer.Context,
    id: Annotated[
        Optional[str], typer.Option(help="Enable specific policy by ID")
    ] = None,
    team: Annotated[Optional[str], typer.Option(help="Team name (required)")] = None,
    all: Annotated[bool, typer.Option(help="Enable all policies for the team")] = False,
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Filter policies using 'attribute:pattern'"),
    ] = None,
):
    """Enable one or more alert policies.

    Enables alert policies by ID, or multiple policies using --all or --filters.
    When using --all or --filters, shows a preview table and asks for confirmation.

    Args:
        id: Enable a specific policy by ID (requires --team)
        team: Team name (required)
        all: Enable all policies for the team (requires --team)
        filters: Enable policies matching filters (requires --team)

    Examples:
        Enable by ID:
            opsgeniecli alert-policies enable --id abc123 --team ops-team

        Enable all policies for a team (with confirmation):
            opsgeniecli alert-policies enable --all --team ops-team

        Enable filtered policies:
            opsgeniecli alert-policies enable --filters "name:.*prod.*" --team ops-team
    """
    if not any([id, all, filters]):
        raise typer.BadParameter("Must specify one of: --id, --all, or --filters")

    if id and (all or filters):
        raise typer.BadParameter("Cannot use --id with --all or --filters")

    if not team:
        raise typer.BadParameter("Must specify --team")

    # Get team ID for API calls
    team_obj = ctx.obj.opsgenie.get_team_by_name(team)
    team_id = team_obj.id

    # Handle single policy enable by ID
    if id:
        try:
            policy = _get_policy_by_id(ctx.obj.opsgenie, id, team)
            result = _update_policy_status(ctx.obj.opsgenie, id, team_id, enabled=True)
            _display_policy_update_result(policy["name"], "enabled", result)
        except ValueError as e:
            typer.echo(f"✗ - {e}")
            raise typer.Exit(code=1)
        return

    # Handle bulk enable (all or filtered)
    policies = _fetch_policies_by_team(ctx.obj.opsgenie, team)

    if filters:
        policies = _apply_filters_to_policies(policies, filters)

    if not policies:
        typer.echo("No policies found matching criteria")
        return

    # Show preview and confirm
    show_table_and_confirm(
        data=_get_alert_policies_table_data(policies),
        title="Alert Policies to be Enabled",
        prompt="\nAre you sure you want to enable these policies?",
    )

    # Enable each policy
    for policy in policies:
        result = _update_policy_status(
            ctx.obj.opsgenie, policy["id"], team_id, enabled=True
        )
        _display_policy_update_result(policy["name"], "enabled", result)


@app.command(name="get")
def get_policy(
    ctx: typer.Context,
    id: Annotated[str, typer.Option(help="Alert policy ID")],
    team: Annotated[str, typer.Option(help="Team name (required)")],
):
    """Get details of a specific alert policy by ID.

    Retrieves and displays detailed information about a single alert policy.

    Args:
        id: Alert policy ID (required)
        team: Team name (required)

    Examples:
        Get policy by ID:
            opsgeniecli alert-policies get --id abc123-def456 --team ops-team
    """
    try:
        policy = _get_policy_by_id(ctx.obj.opsgenie, id, team)
        data = _get_alert_policies_table_data([policy])
        console.print(get_table(data=data, title="Alert Policy"))
    except ValueError as e:
        typer.echo(f"✗ - {e}")
        raise typer.Exit(code=1)


@app.command(name="list")
def list_policies(
    ctx: typer.Context,
    team: Annotated[str, typer.Option(help="Team name (required)")],
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Filter using 'attribute:pattern' (e.g., 'name:.*test.*')"),
    ] = None,
):
    """List alert policies for a team with optional filtering.

    Retrieves alert policies for a specified team, optionally filtered by regex patterns.

    Args:
        team: Team name to list policies for (required)
        filters: Regex filters in format "field:pattern" (can be specified multiple times)

    Examples:
        List all policies for a team:
            opsgeniecli alert-policies list --team ops-team

        List with regex filter:
            opsgeniecli alert-policies list --team ops-team --filters "name:.*production.*"

        List enabled policies only:
            opsgeniecli alert-policies list --team ops-team --filters "enabled:True"
    """
    # Fetch policies
    policies = _fetch_policies_by_team(ctx.obj.opsgenie, team)

    # Apply filters if provided
    if filters:
        policies = _apply_filters_to_policies(policies, filters)

    # Display results
    if not policies:
        typer.echo("No alert policies found")
        return

    data = _get_alert_policies_table_data(policies)
    console.print(get_table(data=data, title="Alert Policies"))


@app.command(name="set")
def set_policy(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(help="Name for the alert policy")],
    filter: Annotated[str, typer.Option(help="Regex pattern to match alerts")],
    description: Annotated[str, typer.Option(help="Description for the alert policy")],
    team: Annotated[str, typer.Option(help="Team name (required)")],
    enabled: Annotated[
        bool, typer.Option(help="Enable the policy when created")
    ] = False,
    validation: Annotated[
        bool, typer.Option(help="Validate filter against recent alerts before creating")
    ] = False,
):
    """Create a new alert policy.

    Creates an alert policy with the specified name, filter regex pattern, and description.
    The filter is a regex pattern that matches against alert properties.
    The policy can be optionally enabled immediately upon creation.

    Args:
        name: Name for the alert policy (required)
        filter: Regex pattern to match alerts (required)
        description: Description for the alert policy (required)
        team: Team name (required)
        enabled: Enable the policy when created (default: False)
        validation: Validate filter against recent alerts before creating (default: False)

    Examples:
        Create a disabled policy with regex filter:
            opsgeniecli alert-policies set \\
                --name "Filter opensearch alerts" \\
                --filter "sbpp[13]osearch-apg" \\
                --description "Blocks opensearch APG alerts" \\
                --team ops-team

        Create an enabled policy with validation:
            opsgeniecli alert-policies set \\
                --name "Filter test alerts" \\
                --filter ".*test.*" \\
                --description "Filters all test-related alerts" \\
                --team ops-team \\
                --enabled \\
                --validation
    """
    # Get team ID
    team_obj = ctx.obj.opsgenie.get_team_by_name(team)
    team_id = team_obj.id

    # Validate filter against recent alerts if requested
    if validation:
        try:
            typer.echo(
                f"\nValidating filter pattern against recent alerts for team '{team}'..."
            )
            matching_alerts = _validate_policy_filter(
                ctx.obj.opsgenie, team, filter, limit=500
            )

            if not matching_alerts:
                typer.echo("No alerts matched the filter pattern in the last 7 days.")
                typer.echo("This policy would not have blocked any recent alerts.\n")
            else:
                typer.echo(
                    f"\nFound {len(matching_alerts)} alerts matching the filter pattern:\n"
                )
                validation_table_data = _get_validation_table_data(matching_alerts[:20])
                console.print(
                    get_table(
                        data=validation_table_data,
                        title="Matching Alerts (Last 7 Days)",
                    )
                )

                if len(matching_alerts) > 20:
                    typer.echo(
                        f"\n(Showing 20 of {len(matching_alerts)} matching alerts)"
                    )

            # Ask for confirmation
            if not typer.confirm("\nDo you want to create this policy?", default=True):
                typer.echo("Policy creation cancelled.")
                raise typer.Exit(code=0)

        except ValueError as e:
            typer.echo(f"✗ - Validation error: {e}")
            raise typer.Exit(code=1)

    # Create the policy
    try:
        result = ctx.obj.opsgenie.create_alert_policy(
            name=name,
            filter_condition=filter,
            policy_description=description,
            team_id=team_id,
            enabled=enabled,
        )

        # Display success message
        policy_data = result.get("data", {})
        typer.echo("✓ - Alert policy created:")
        typer.echo(f"    Name: {name}")
        typer.echo(f"    Filter: {filter}")
        typer.echo(f"    Description: {description}")
        typer.echo(f"    Team: {team}")
        typer.echo(f"    Enabled: {policy_data.get('enabled', enabled)}")
        if policy_data.get("id"):
            typer.echo(f"    ID: {policy_data.get('id')}")

    except Exception as e:
        typer.echo(f"✗ - Failed to create alert policy: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
