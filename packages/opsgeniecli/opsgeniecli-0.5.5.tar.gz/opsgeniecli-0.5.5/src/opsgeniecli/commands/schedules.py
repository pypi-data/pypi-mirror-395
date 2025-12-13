"""Schedules management commands for Opsgenie CLI."""

import json
import re
from datetime import datetime, timezone
from typing import Annotated, Any, Dict, List, Optional
import typer
from rich.console import Console
from opsgeniecli.helper import _apply_regex_filters, get_table

app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Manage Opsgenie schedules",
)
console = Console()


def _get_schedules_table_data(schedules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transform schedule data into a flat dictionary structure for table display.

    Args:
        schedules: List of schedule dictionaries from the Opsgenie API

    Returns:
        List of dictionaries with schedule data suitable for table display
    """
    return [
        {
            "ID": schedule.get("id", ""),
            "Name": schedule.get("name", ""),
            "Enabled": str(schedule.get("enabled", False)),
            "Owner Team": (
                schedule.get("ownerTeam", {}).get("name", "")
                if isinstance(schedule.get("ownerTeam"), dict)
                else ""
            ),
        }
        for schedule in schedules
    ]


def _get_timeline_table_data(
    periods: List[Dict[str, Any]], tz_name: str
) -> List[Dict[str, Any]]:
    """
    Transform timeline period data into a flat dictionary structure for table display.

    Args:
        periods: List of period dictionaries from the schedule timeline
        tz_name: Timezone name for display (e.g., 'UTC', 'Europe/Amsterdam')

    Returns:
        List of dictionaries with period data suitable for table display
    """
    from datetime import datetime
    import pytz

    # Try to get the timezone, fallback to UTC if invalid
    try:
        tz = pytz.timezone(tz_name)
    except pytz.exceptions.UnknownTimeZoneError:
        console.print(f"[yellow]Unknown timezone '{tz_name}', using UTC[/yellow]")
        tz = pytz.UTC

    result = []
    for period in periods:
        # Parse dates and convert to target timezone
        start_dt = datetime.fromisoformat(
            period["startDate"].replace("Z", "+00:00")
        ).astimezone(tz)
        end_dt = datetime.fromisoformat(
            period["endDate"].replace("Z", "+00:00")
        ).astimezone(tz)

        result.append(
            {
                "User": period.get("recipient", {}).get("name", ""),
                "Start Date": start_dt.strftime("%a %Y-%m-%d %H:%M:%S"),
                "End Date": end_dt.strftime("%a %Y-%m-%d %H:%M:%S"),
            }
        )
    return result


def _find_schedule_by_team_name(opsgenie, team_name: str) -> Optional[str]:
    """
    Find a schedule name by searching for a team name pattern.

    Searches schedules where the team name matches either the schedule name
    or the ownerTeam name. If multiple matches are found, prompts the user
    to choose one.

    Args:
        opsgenie: Opsgenie client instance
        team_name: Team name pattern to search for

    Returns:
        Schedule name if found, None otherwise
    """
    console.print(
        f"[cyan]Searching for schedules matching team '{team_name}'...[/cyan]"
    )

    # Get all schedules
    schedules_result = opsgenie.list_schedules()
    all_schedules = schedules_result.get("data", [])

    # Filter schedules that have ownerTeam key
    schedules_with_owner = [s for s in all_schedules if "ownerTeam" in s]

    # Filter by team name pattern (case-insensitive word boundary match)
    filtered_schedules = [
        schedule
        for schedule in schedules_with_owner
        if re.findall(rf"\b{team_name}\b", schedule.get("name", ""), re.IGNORECASE)
        or re.findall(
            rf"\b{team_name}\b",
            schedule.get("ownerTeam", {}).get("name", ""),
            re.IGNORECASE,
        )
    ]

    # Handle different numbers of matches
    if len(filtered_schedules) == 0:
        console.print(f"[yellow]No schedules found for team '{team_name}'[/yellow]")
        return None

    if len(filtered_schedules) == 1:
        schedule_name = filtered_schedules[0]["name"]
        console.print(f"[green]Found schedule: {schedule_name}[/green]")
        return schedule_name

    # Multiple matches - prompt user to choose
    console.print(
        f"[yellow]Multiple schedules found for team '{team_name}':[/yellow]\n"
    )

    # Display table of matches
    choices_data = [
        {
            "Schedule Name": schedule.get("name", ""),
            "Team Name": schedule.get("ownerTeam", {}).get("name", ""),
        }
        for schedule in filtered_schedules
    ]
    table = get_table(data=choices_data, title=f"Schedules matching '{team_name}'")
    console.print(table)

    # Prompt for selection
    schedule_name = typer.prompt(
        "\nEnter the schedule name you want to use", type=str
    ).strip()

    # Validate the selection
    if schedule_name and any(s["name"] == schedule_name for s in filtered_schedules):
        console.print(f"[green]Selected schedule: {schedule_name}[/green]")
        return schedule_name
    else:
        console.print(f"[red]Invalid selection: '{schedule_name}'[/red]")
        return None


@app.command(name="list")
def list_schedules(
    ctx: typer.Context,
    filters: Annotated[
        Optional[List[str]],
        typer.Option(help="Regex filters in format 'field:pattern'"),
    ] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON instead of table")
    ] = False,
) -> None:
    """
    List all schedules.

    Retrieves all schedules and displays them sorted by name.

    Args:
        filters: Regex filters in format "field:pattern" (can be specified multiple times)
        json_output: Output as JSON instead of table (default: False)

    Examples:
        List all schedules:
            opsgeniecli schedules list

        Filter by name pattern:
            opsgeniecli schedules list --filters "Name:ops.*"

        Output as JSON:
            opsgeniecli schedules list --json
    """
    console.print("[cyan]Fetching schedules...[/cyan]")
    result = ctx.obj.opsgenie.list_schedules()
    schedules_list = result.get("data", [])

    if not schedules_list:
        console.print("[yellow]No schedules found[/yellow]")
        return

    # Sort by name
    schedules_list = sorted(schedules_list, key=lambda x: x.get("name", ""))

    if json_output:
        console.print_json(json.dumps(schedules_list, indent=4, sort_keys=True))
        return

    # Transform to table data
    schedules_data = _get_schedules_table_data(schedules_list)

    # Apply filters if provided
    if filters:
        filter_dict = {k: v for k, v in (filter.split(":", 1) for filter in filters)}
        schedules_data = _apply_regex_filters(data=schedules_data, filters=filter_dict)

    # Display results
    if not schedules_data:
        console.print("[yellow]No schedules found matching the criteria.[/yellow]")
        return

    console.print(f"\n[green]Found {len(schedules_data)} schedule(s)[/green]")
    table = get_table(data=schedules_data, title="Schedules")
    console.print(table)


@app.command(name="get")
def get_schedule(
    ctx: typer.Context,
    id: Annotated[Optional[str], typer.Option("--id", help="Schedule ID")] = None,
    name: Annotated[
        Optional[str], typer.Option("--name", help="Exact schedule name")
    ] = None,
    team: Annotated[
        Optional[str], typer.Option("--team", help="Team name to search for schedule")
    ] = None,
) -> None:
    """
    Get detailed information about a specific schedule.

    You must specify exactly one of: --id, --name, or --team.
    Output is always in JSON format.

    Args:
        id: The ID of the schedule to retrieve
        name: The exact name of the schedule to retrieve
        team: Team name to search for (uses regex matching with disambiguation)

    Examples:
        Get schedule by ID:
            opsgeniecli schedules get --id "abc123-def456"

        Get schedule by exact name:
            opsgeniecli schedules get --name "ops-schedule"

        Get schedule by team name (with fuzzy search):
            opsgeniecli schedules get --team "ops-team"
    """
    # Validate that exactly one option is provided
    options_provided = sum([bool(id), bool(name), bool(team)])

    if options_provided == 0:
        console.print("[red]Error: One of --id, --name, or --team is required[/red]")
        raise typer.Exit(code=1)

    if options_provided > 1:
        console.print(
            "[red]Error: --id, --name, and --team are mutually exclusive. "
            "Please specify only one.[/red]"
        )
        raise typer.Exit(code=1)

    try:
        # Determine schedule name
        schedule_name = None
        result = None

        if id:
            console.print(f"[cyan]Fetching schedule with ID '{id}'...[/cyan]")
            result = ctx.obj.opsgenie.get_schedules_by_id(id)
        elif name:
            schedule_name = name
        elif team:
            schedule_name = _find_schedule_by_team_name(ctx.obj.opsgenie, team)
            if not schedule_name:
                raise typer.Exit(code=1)

        # Fetch by name if not already fetched by ID
        if schedule_name:
            console.print(f"[cyan]Fetching schedule '{schedule_name}'...[/cyan]")
            result = ctx.obj.opsgenie.get_schedules_by_name(schedule_name)

        if result:
            console.print_json(json.dumps(result, indent=4, sort_keys=True))

    except Exception as e:
        console.print("[red]Error: Failed to retrieve schedule[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command(name="timeline")
def schedule_timeline(
    ctx: typer.Context,
    name: Annotated[
        Optional[str], typer.Option("--name", help="Exact schedule name")
    ] = None,
    team: Annotated[
        Optional[str], typer.Option("--team", help="Team name to search for schedule")
    ] = None,
    expand: Annotated[
        Optional[str],
        typer.Option(help="Expand timeline type: base, forwarding, or override"),
    ] = None,
    interval: Annotated[int, typer.Option(help="Time interval for the timeline")] = 2,
    interval_unit: Annotated[
        str,
        typer.Option("--interval-unit", help="Unit for interval (days, weeks, months)"),
    ] = "months",
    history: Annotated[
        bool, typer.Option("--history", help="Include historical entries")
    ] = False,
    tz: Annotated[
        str,
        typer.Option(
            help="Timezone for displaying times (e.g., UTC, Europe/Amsterdam)"
        ),
    ] = "UTC",
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON instead of table")
    ] = False,
) -> None:
    """
    Show schedule timeline with on-call rotations.

    Displays the on-call schedule timeline for a specific schedule, showing
    who is on call during different time periods.

    You must specify either --name or --team.

    Args:
        name: The exact name of the schedule
        team: Team name to search for (uses regex matching with disambiguation)
        expand: Timeline type to expand (base, forwarding, override)
        interval: Time interval for the timeline (default: 2)
        interval_unit: Unit for interval - days, weeks, or months (default: months)
        history: Include historical entries (default: False)
        tz: Timezone for displaying times (default: UTC)
        json_output: Output as JSON instead of table (default: False)

    Examples:
        Show timeline for a schedule by name:
            opsgeniecli schedules timeline --name "ops-schedule"

        Show timeline by team name:
            opsgeniecli schedules timeline --team "ops-team"

        Show with override timeline:
            opsgeniecli schedules timeline --name "ops-schedule" --expand override

        Show in specific timezone:
            opsgeniecli schedules timeline --team "ops-team" --tz "Europe/Amsterdam"

        Include history:
            opsgeniecli schedules timeline --name "ops-schedule" --history
    """
    # Validate that exactly one option is provided
    if not name and not team:
        console.print("[red]Error: Either --name or --team is required[/red]")
        raise typer.Exit(code=1)

    if name and team:
        console.print(
            "[red]Error: --name and --team are mutually exclusive. "
            "Please specify only one.[/red]"
        )
        raise typer.Exit(code=1)

    # Validate expand option
    if expand and expand.lower() not in ["base", "forwarding", "override"]:
        console.print(
            "[red]Error: --expand must be one of: base, forwarding, override[/red]"
        )
        raise typer.Exit(code=1)

    # Determine schedule name
    schedule_name = None
    if name:
        schedule_name = name
    elif team:
        schedule_name = _find_schedule_by_team_name(ctx.obj.opsgenie, team)
        if not schedule_name:
            raise typer.Exit(code=1)

    console.print(f"[cyan]Fetching timeline for schedule '{schedule_name}'...[/cyan]")

    try:
        result = ctx.obj.opsgenie.list_schedule_timeline_by_team_name(
            schedule_name, expand, interval, interval_unit
        )

        if json_output:
            console.print_json(json.dumps(result, indent=4, sort_keys=True))
            return

        # Determine which timeline to use
        rotation_name = "finalTimeline"
        if expand:
            rotation_name = f"{expand}Timeline"

        timeline_data = result.get("data", {})
        rotations = timeline_data.get(rotation_name, {}).get("rotations", [])

        if not rotations:
            console.print("[yellow]No rotations found in schedule timeline[/yellow]")
            return

        # Get current time for filtering historical entries
        now = datetime.now(timezone.utc)

        # Display each rotation
        for rotation in rotations:
            periods = rotation.get("periods", [])
            if not periods:
                continue

            # Filter historical periods if needed
            if not history:
                periods = [
                    p
                    for p in periods
                    if datetime.fromisoformat(p["startDate"].replace("Z", "+00:00"))
                    >= now
                ]

            if not periods:
                continue

            rotation_display_name = rotation.get("name", "Unknown")
            console.print(
                f"\n[bold cyan]On-call schedule - {rotation_display_name}[/bold cyan]"
            )

            # Transform to table data
            timeline_table_data = _get_timeline_table_data(periods, tz)

            if timeline_table_data:
                table = get_table(
                    data=timeline_table_data, title=f"Rotation: {rotation_display_name}"
                )
                console.print(table)

    except Exception as e:
        console.print("[red]Error: Failed to retrieve schedule timeline[/red]")
        console.print(f"[red]{str(e)}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
