import datetime
import re
from typing import Annotated, Any, List, Optional
import pytz
import typer
from requests.exceptions import HTTPError
from rich.console import Console
from rich.table import Table
from opsgeniecli.helper import _apply_regex_filters, get_table, show_table_and_confirm
from opsgenielib.opsgenielib import Alert
from opsgenielib import Opsgenie
from collections import Counter

app = typer.Typer(
    rich_markup_mode="rich", no_args_is_help=True, help="Manage Opsgenie alerts"
)
console = Console()

# Shared helper functions used by multiple commands


def _get_alerts_table_data(
    alerts: list[Alert],
    timezone: pytz.BaseTzInfo,
) -> list[dict[str, Any]]:
    """Returning a flat dict to filter and output a table"""
    return [
        {
            "message": alert.message,
            "status": alert.status,
            "acknowledged": alert.acknowledged,
            "createdAt": str(alert.created_at.astimezone(timezone)),
            "tags": ", ".join(alert.tags),
            "id": alert.id,
        }
        for alert in alerts
    ]


def _create_query(
    team: Optional[str], filtered: Optional[bool], limit: Optional[int]
) -> dict[str, Any]:
    conditions = {
        "responders": team,
        "tag != filtered": "filtered" if filtered else None,
        "tag != Filtered": "Filtered" if filtered else None,
    }
    query = " AND ".join(f"{key}:{value}" for key, value in conditions.items() if value)
    return {"query": query, "limit": limit}


def _filter_by_last(alerts: list[Alert], last: str) -> list[Alert]:
    match = re.match(r"(\d+)([mwd])$", last)
    if not match:
        console.print(f"Invalid time period specified '{last}' for 'last'")
        raise typer.Exit(code=1)

    subtract_value, period_char = match.groups()
    subtract_value = int(subtract_value)

    period_map = {"m": "days", "w": "weeks", "d": "days"}
    period = period_map[period_char]

    if period_char == "m":
        subtract_value *= 30

    subtracted_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        **{period: subtract_value}
    )
    return [alert for alert in alerts if alert.created_at >= subtracted_date]


def _filter_by_out_of_office_hours(
    alerts: list[Alert], timezone: pytz.BaseTzInfo
) -> list[Alert]:
    return [
        alert
        for alert in alerts
        if alert.created_at.astimezone(timezone).hour < 8
        or alert.created_at.astimezone(timezone).hour >= 17
    ]


def _list_alerts(
    opsgenie: Opsgenie,
    team: str,
    filters: List[str],
    filtered: bool,
    out_of_office_hours: bool,
    last: str,
    limit: int,
    tz: str,
) -> Table:
    filter_dict = {k: v for k, v in (filter.split(":", 1) for filter in filters)}

    query = _create_query(team=team, filtered=filtered, limit=limit)
    alerts = opsgenie.query_alerts(**query)

    if tz == "local":
        tz = str(datetime.datetime.now().astimezone().tzinfo)
    timezone = pytz.timezone(tz)

    if last:
        alerts = _filter_by_last(alerts=alerts, last=last)
    if out_of_office_hours:
        alerts = _filter_by_out_of_office_hours(alerts=alerts, timezone=timezone)

    alerts_data = _get_alerts_table_data(alerts=alerts, timezone=timezone)
    alerts_data = _apply_regex_filters(data=alerts_data, filters=filter_dict)
    return get_table(data=alerts_data, title="Alerts")


# Commands in alphabetical order: acknowledge, close, count, create, get, list, query


def _get_alerts_to_acknowledge(
    opsgenie: Opsgenie, id: str, team: str, all: bool
) -> list[Alert]:
    """Get the list of alerts to acknowledge based on parameters.

    Args:
        opsgenie: Opsgenie client instance
        id: Single alert ID to acknowledge
        team: Team name for bulk acknowledge
        all: Whether to acknowledge all alerts for the team

    Returns:
        List of Alert objects to acknowledge

    Raises:
        ValueError: If invalid parameters are provided
    """
    if not any([id, all]):
        raise ValueError("Either --id <alert-id> or --all --team <team> is required.")

    if id:
        return [opsgenie.get_alert_by_id(id_=id)]

    if all:
        if not team:
            raise ValueError("Team name is required when using --all.")
        alerts_result = opsgenie.query_alerts(
            query=f"responders:{team} AND NOT status: closed AND acknowledged: false"
        )
        return alerts_result if isinstance(alerts_result, list) else []

    return []


def _acknowledge_alert(opsgenie: Opsgenie, alert: Alert) -> None:
    """Acknowledge a single alert and display result."""
    response = opsgenie.acknowledge_alerts(alert.id)
    symbol = (
        "✓ - alert acknowledged"
        if response["result"] == "Request will be processed"
        else "✗ - alert not acknowledged"
    )
    typer.echo(f"{symbol}: {alert.id} - {alert.message}")


@app.command(name="acknowledge")
def acknowledge(
    ctx: typer.Context,
    id: Annotated[str, typer.Option()] = "",
    team: Annotated[str, typer.Option()] = "",
    all: Annotated[bool, typer.Option()] = False,
    force: Annotated[bool, typer.Option()] = False,
    tz: Annotated[str, typer.Option()] = "local",
):
    """Acknowledge one or all open alerts for a team.

    Acknowledges alerts to indicate that someone is working on them. When using --all,
    shows a preview table and asks for confirmation before acknowledging.

    Args:
        id: Single alert ID to acknowledge
        team: Team name (required when using --all)
        all: Acknowledge all open, unacknowledged alerts for the team
        tz: Timezone for displaying alert times (default: local)

    Examples:
        Acknowledge a single alert:
            opsgeniecli alerts acknowledge --id abc123

        Acknowledge all unacknowledged alerts for a team:
            opsgeniecli alerts acknowledge --all --team ops-team
    """
    try:
        alerts = _get_alerts_to_acknowledge(ctx.obj.opsgenie, id, team, all)
    except ValueError as e:
        raise typer.BadParameter(str(e))

    # Show preview and confirm for bulk operations
    if all:
        if tz == "local":
            tz = str(datetime.datetime.now().astimezone().tzinfo)
        timezone = pytz.timezone(tz)

        show_table_and_confirm(
            data=_get_alerts_table_data(alerts=alerts, timezone=timezone),
            title="Alerts to be Acknowledged",
            force=force,
        )

    [_acknowledge_alert(ctx.obj.opsgenie, alert) for alert in alerts]


def _get_alerts_to_close(
    opsgenie: Opsgenie, id: str, team: str, all: bool
) -> list[Alert]:
    """Get the list of alerts to close based on parameters.

    Args:
        opsgenie: Opsgenie client instance
        id: Single alert ID to close
        team: Team name for bulk close
        all: Whether to close all alerts for the team

    Returns:
        List of Alert objects to close

    Raises:
        ValueError: If invalid parameters are provided
    """
    if not any([id, all]):
        raise ValueError("Either --id <alert-id> or --all --team <team> is required.")

    if id:
        return [opsgenie.get_alert_by_id(id_=id)]

    if all:
        if not team:
            raise ValueError("Team name is required when using --all.")
        alerts_result = opsgenie.query_alerts(
            query=f"responders:{team} AND NOT status: closed AND acknowledged: true"
        )
        return alerts_result if isinstance(alerts_result, list) else []

    return []


def _close_alert(opsgenie: Opsgenie, alert: Alert) -> None:
    result = opsgenie.close_alerts(alert.id)
    symbol = (
        "✓ - alert closed"
        if result["result"] == "Request will be processed"
        else "✗ - alert not closed"
    )
    typer.echo(f"{symbol}: {alert.id} - {alert.message}")


@app.command(name="close")
def close(
    ctx: typer.Context,
    id: Annotated[str, typer.Option()] = "",
    team: Annotated[str, typer.Option()] = "",
    all: Annotated[bool, typer.Option()] = False,
    tz: Annotated[str, typer.Option()] = "local",
):
    """Close one or all acknowledged alerts for a team.

    Closes alerts that have been resolved. When using --all, only closes alerts that
    are already acknowledged, shows a preview table, and asks for confirmation.

    Args:
        id: Single alert ID to close
        team: Team name (required when using --all)
        all: Close all open, acknowledged alerts for the team
        tz: Timezone for displaying alert times (default: local)

    Examples:
        Close a single alert:
            opsgeniecli alerts close --id abc123

        Close all acknowledged alerts for a team:
            opsgeniecli alerts close --all --team ops-team
    """
    try:
        alerts = _get_alerts_to_close(ctx.obj.opsgenie, id, team, all)
    except ValueError as e:
        raise typer.BadParameter(str(e))

    if all:
        if tz == "local":
            tz = str(datetime.datetime.now().astimezone().tzinfo)
        timezone = pytz.timezone(tz)

        show_table_and_confirm(
            data=_get_alerts_table_data(alerts=alerts, timezone=timezone),
            title="Alerts to be Closed",
        )

    [_close_alert(ctx.obj.opsgenie, alert) for alert in alerts]


@app.command(name="count")
def count(
    ctx: typer.Context,
    team: Annotated[str, typer.Option()],
    filtered: Annotated[bool, typer.Option()] = False,
    out_of_office_hours: Annotated[bool, typer.Option()] = False,
    last: Annotated[str, typer.Option()] = "",
    limit: Annotated[int, typer.Option()] = 100,
    tz: Annotated[str, typer.Option()] = "local",
):
    """Count alert occurrences to identify noisy alerts.

    Groups alerts by message and counts how many times each alert occurred.
    Useful for identifying recurring issues or noisy alerting rules.

    Args:
        team: Team name to count alerts for (required)
        filtered: Exclude alerts tagged as "filtered" or "Filtered" (default: False)
        out_of_office_hours: Only count alerts created outside 8am-5pm (default: False)
        last: Count alerts from time period (e.g., "7d" for 7 days, "2w", "1m")
        limit: Maximum number of alerts to retrieve (default: 100)
        tz: Timezone for out-of-office hours calculation (default: local)

    Examples:
        Count all alerts for a team:
            opsgeniecli alerts count --team ops-team

        Count alerts from last week:
            opsgeniecli alerts count --team ops-team --last 7d --limit 500

        Count only out-of-office hours alerts:
            opsgeniecli alerts count --team ops-team --out-of-office-hours
    """
    if last and limit == 100:
        typer.echo(
            "Note: You might need to increase --limit to see all alerts for the period.\n"
        )

    # Query alerts
    query = _create_query(team=team, filtered=filtered, limit=limit)
    alerts = ctx.obj.opsgenie.query_alerts(**query)

    # Apply filters
    if tz == "local":
        tz = str(datetime.datetime.now().astimezone().tzinfo)
    timezone = pytz.timezone(tz)

    if last:
        alerts = _filter_by_last(alerts=alerts, last=last)
    if out_of_office_hours:
        alerts = _filter_by_out_of_office_hours(alerts=alerts, timezone=timezone)

    # Count occurrences
    message_counts = Counter(
        alert.message.replace("\n", "").replace("\r", "") for alert in alerts
    )

    # Display results sorted by count
    typer.echo(
        f"\nFound {len(alerts)} alerts with {len(message_counts)} unique messages:\n"
    )
    for message, count in message_counts.most_common():
        typer.echo(f"{count:4d} - {message}")


@app.command(name="create")
def create(
    ctx: typer.Context,
    message: Annotated[str, typer.Option()],
    responders: Annotated[str, typer.Option()],
    description: Annotated[str, typer.Option()] = "",
    priority: Annotated[str, typer.Option()] = "P3",
    tags: Annotated[Optional[List[str]], typer.Option()] = None,
    alias: Annotated[str, typer.Option()] = "",
    entity: Annotated[str, typer.Option()] = "",
):
    """Create a new alert in Opsgenie.

    Creates an alert with specified message and responders. Responders should be team names
    separated by commas. Currently only supports team responders.

    Args:
        message: Alert message (required)
        responders: Comma-separated list of team names (required)
        description: Detailed description of the alert
        priority: Alert priority - P1 (Critical) to P5 (Informational) (default: P3)
        tags: Tags to add to the alert (can be specified multiple times)
        alias: Custom alias for the alert
        entity: Entity that the alert is related to

    Examples:
        Create a basic alert:
            opsgeniecli alerts create --message "Server is down" --responders "ops-team"

        Create alert with multiple teams and tags:
            opsgeniecli alerts create \\
                --message "Database connection lost" \\
                --responders "ops-team,dba-team" \\
                --priority "P1" \\
                --tags "production" \\
                --tags "database" \\
                --description "Cannot connect to primary database server"
    """
    _responders = [
        {"type": "team", "name": responder} for responder in responders.split(",")
    ]
    try:
        response = ctx.obj.opsgenie.create_alert(
            message=message,
            description=description,
            priority=priority,
            responders=_responders,
            tags=tags or [],
            alias=alias,
            entity=entity,
        )

        alert_id = response.get("data", {}).get("id", "unknown")
        typer.echo(f"✓ - Alert created successfully: {alert_id} Message: {message}")
    except HTTPError as e:
        typer.echo(
            f"✗ - Failed to create alert: HTTP {e.response.status_code} {e.response.text}"
        )
        raise typer.Exit(code=1)


@app.command(name="get")
def get_alert(
    ctx: typer.Context,
    id: Annotated[str, typer.Option()],
    tz: Annotated[str, typer.Option()] = "local",
) -> None:
    """Get details of a specific alert by ID.

    Retrieves and displays detailed information about a single alert.

    Args:
        id: Alert ID to retrieve (required)
        tz: Timezone for displaying alert times (default: local)

    Examples:
        Get alert details:
            opsgeniecli alerts get --id abc123-def456

        Get alert with specific timezone:
            opsgeniecli alerts get --id abc123 --tz "America/New_York"
    """
    alert = ctx.obj.opsgenie.get_alert_by_id(id_=id)
    if tz == "local":
        tz = str(datetime.datetime.now().astimezone().tzinfo)
    timezone = pytz.timezone(tz)
    data = _get_alerts_table_data(alerts=[alert], timezone=timezone)
    console.print(get_table(data=data, title="Alert"))


@app.command(name="list")
def list_alerts(
    ctx: typer.Context,
    team: Annotated[str, typer.Option()],
    filters: Annotated[Optional[List[str]], typer.Option()] = None,
    filtered: Annotated[bool, typer.Option()] = False,
    out_of_office_hours: Annotated[bool, typer.Option()] = False,
    last: Annotated[str, typer.Option()] = "",
    limit: Annotated[int, typer.Option()] = 100,
    tz: Annotated[str, typer.Option()] = "local",
):
    """List alerts for a team with flexible filtering options.

    Retrieves alerts for a specified team with various filtering capabilities including
    regex filters, time-based filters, and out-of-office hours filtering.

    Args:
        team: Team name to list alerts for (required)
        filters: Regex filters in format "field:pattern" (can be specified multiple times)
        filtered: Exclude alerts tagged as "filtered" or "Filtered" (default: False)
        out_of_office_hours: Only show alerts created outside 8am-5pm (default: False)
        last: Filter by time period (e.g., "7d" for 7 days, "2w" for 2 weeks, "1m" for 1 month)
        limit: Maximum number of alerts to return (default: 100)
        tz: Timezone for displaying alert times (default: local)

    Examples:
        List all alerts for a team:
            opsgeniecli alerts list --team ops-team

        Filter by message pattern and last 7 days:
            opsgeniecli alerts list --team ops-team --filters "message:database" --last 7d

        Show only out-of-office hours alerts:
            opsgeniecli alerts list --team ops-team --out-of-office-hours
    """
    console.print(
        _list_alerts(
            opsgenie=ctx.obj.opsgenie,
            team=team,
            filters=filters or [],
            filtered=filtered,
            out_of_office_hours=out_of_office_hours,
            last=last,
            limit=limit,
            tz=tz,
        )
    )


@app.command(name="query")
def query(
    ctx: typer.Context,
    query: Annotated[str, typer.Option()],
    limit: Annotated[int, typer.Option()] = 1000,
    tz: Annotated[str, typer.Option()] = "local",
):
    """Query alerts using Opsgenie query syntax.

    Retrieves alerts matching the provided query string using Opsgenie's query language.

    Args:
        query: Opsgenie query string (e.g., "status: open AND priority: P1")
        limit: Maximum number of alerts to return (default: 1000)
        tz: Timezone for displaying alert times (default: local)

    Examples:
        Query by status and priority:
            opsgeniecli alerts query --query "status: open AND priority: P1"

        Query by team:
            opsgeniecli alerts query --query "responders: ops-team" --limit 50
    """
    if tz == "local":
        tz = str(datetime.datetime.now().astimezone().tzinfo)
    timezone = pytz.timezone(tz)
    alerts = ctx.obj.opsgenie.query_alerts(**{"query": query, "limit": limit})
    table = get_table(
        data=_get_alerts_table_data(alerts=alerts, timezone=timezone), title="Alerts"
    )
    console.print(table)
