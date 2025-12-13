import datetime
from typing import Any, Dict, List, Optional
from typing_extensions import Annotated
import typer
from rich.console import Console
from rich.table import Table
from rich import box
from opsgenielib.opsgenielib import OnCallSchedule
from requests.exceptions import HTTPError
from opsgeniecli.commands.schedules import _find_schedule_by_team_name

app = typer.Typer(
    rich_markup_mode="rich", no_args_is_help=True, help="Manage on-call schedules"
)
console = Console()


def get_on_call_table(on_call_schedules: list[dict[str, Any]]) -> Table:
    table = Table(
        title="On-Call", show_lines=True, row_styles=["blue", "white"], box=box.MINIMAL
    )
    for schedule in next(iter(on_call_schedules), {}).keys():
        table.add_column(schedule)

    for schedule in on_call_schedules:
        table.add_row(*schedule.values())
    return table


def _get_schedules_table_data(
    on_call_schedules: List[OnCallSchedule],
) -> list[dict[str, Any]]:
    """Returning a flat dict to filter and output a table"""
    return [
        {
            "Schedule": schedule.name,
            "onCallParticipants": getattr(
                next(iter(schedule.onCallParticipants), None), "name", ""
            ),
            "Enabled": str(schedule.enabled),
        }
        for schedule in on_call_schedules
    ]


def _apply_filters(
    schedules: list[dict[str, Any]], filters: Dict[str, Any]
) -> list[dict[str, Any]]:
    filtered_schedules = schedules
    for attr, value in filters.items():
        filtered_schedules = [
            schedule
            for schedule in filtered_schedules
            if value in str(schedule.get(attr, ""))
        ]
    return filtered_schedules


@app.command(name="on-call")
def on_call(
    ctx: typer.Context, filters: Annotated[Optional[List[str]], typer.Option()] = None
):
    """List on-call schedules with optional filtering."""
    filter_dict = {k: v for k, v in (filter.split(":") for filter in (filters or []))}
    all_schedules = _get_schedules_table_data(
        on_call_schedules=ctx.obj.opsgenie.get_users_on_call()
    )
    filtered_schedules = _apply_filters(schedules=all_schedules, filters=filter_dict)
    console.print(get_on_call_table(on_call_schedules=filtered_schedules))


def _validate_override_params(
    hours: Optional[int], start_date: Optional[str], end_date: Optional[str]
) -> None:
    """Validate that override parameters are mutually exclusive and complete."""
    if hours and (start_date or end_date):
        typer.echo("✗ - Error: Cannot use --hours with --start-date or --end-date")
        raise typer.Exit(code=1)

    if not hours and not (start_date and end_date):
        typer.echo(
            "✗ - Error: Must specify either --hours OR both --start-date and --end-date"
        )
        raise typer.Exit(code=1)


def _parse_iso_datetime(date_string: str) -> datetime.datetime:
    """Parse ISO format datetime string and add UTC timezone."""
    try:
        return datetime.datetime.fromisoformat(date_string).replace(
            tzinfo=datetime.timezone.utc
        )
    except ValueError as e:
        typer.echo(f"✗ - Error parsing date '{date_string}': {e}")
        typer.echo("    Use ISO format: 2024-03-15T14:34:09")
        raise typer.Exit(code=1)


def _set_override_by_hours(
    opsgenie, team: str, engineer: str, hours: int
) -> tuple[Any, datetime.datetime, datetime.datetime]:
    """Set override for specified hours from now."""
    start_dt = datetime.datetime.now(datetime.timezone.utc)
    end_dt = start_dt + datetime.timedelta(hours=hours)
    response = opsgenie.set_override_for_hours(team, engineer, hours)
    return response, start_dt, end_dt


def _set_override_by_dates(
    opsgenie, team: str, engineer: str, start_date: str, end_date: str
) -> tuple[Any, datetime.datetime, datetime.datetime]:
    """Set override for specific date range."""
    start_dt = _parse_iso_datetime(start_date)
    end_dt = _parse_iso_datetime(end_date)

    start_str = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_str = end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    response = opsgenie.set_override_scheduled(team, start_str, end_str, engineer)
    return response, start_dt, end_dt


@app.command(name="override")
def override(
    ctx: typer.Context,
    team: Annotated[str, typer.Option(help="Team name (will search for matching schedule)")],
    engineer: Annotated[
        str, typer.Option(help="Username of engineer who will be on call")
    ],
    hours: Annotated[
        Optional[int], typer.Option(help="Hours from now for override duration")
    ] = None,
    start_date: Annotated[
        Optional[str], typer.Option(help="Start date (ISO format: 2019-03-15T14:34:09)")
    ] = None,
    end_date: Annotated[
        Optional[str], typer.Option(help="End date (ISO format: 2019-03-15T15:34:09)")
    ] = None,
):
    """Override the on-call schedule with another user.

    You must specify EITHER --hours OR both --start-date and --end-date.

    The --team parameter will search for schedules matching that team name.
    If multiple schedules match, you'll be prompted to choose one.

    Args:
        team: Team name to search for (matches schedule name or owner team)
        engineer: Username of the engineer who will take on-call duty
        hours: Set override starting now for this many hours (mutually exclusive with dates)
        start_date: Start date/time in ISO format (mutually exclusive with hours)
        end_date: End date/time in ISO format (mutually exclusive with hours)

    Examples:
        Override for 8 hours starting now:
            opsgeniecli on-call override --team saas --engineer john --hours 8

        Override for specific time period:
            opsgeniecli on-call override \\
                --team saas \\
                --engineer john \\
                --start-date 2024-03-15T14:00:00 \\
                --end-date 2024-03-15T22:00:00
    """
    _validate_override_params(hours, start_date, end_date)

    # Look up the schedule name from the team
    schedule_name = _find_schedule_by_team_name(ctx.obj.opsgenie, team)
    if not schedule_name:
        raise typer.Exit(code=1)

    try:
        if hours:
            response, start_dt, end_dt = _set_override_by_hours(
                ctx.obj.opsgenie, schedule_name, engineer, hours
            )
        else:
            assert start_date is not None and end_date is not None
            response, start_dt, end_dt = _set_override_by_dates(
                ctx.obj.opsgenie, schedule_name, engineer, start_date, end_date
            )

        if response.status_code == 201:
            start_display = start_dt.strftime("%Y-%m-%d %H:%M:%S")
            end_display = end_dt.strftime("%Y-%m-%d %H:%M:%S")
            typer.echo(
                f"✓ - Override set to {engineer} between {start_display} and {end_display}"
            )
        else:
            typer.echo(f"✗ - Failed to set override: {response.text}")
            raise typer.Exit(code=1)

    except HTTPError as e:
        typer.echo(f"✗ - HTTP Error: {e.response.status_code} {e.response.text}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
