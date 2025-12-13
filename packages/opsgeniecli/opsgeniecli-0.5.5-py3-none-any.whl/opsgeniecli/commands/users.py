"""Users management commands for Opsgenie CLI."""

from typing import Any, Dict, List, Optional
from typing_extensions import Annotated
import typer
from rich.console import Console
from opsgeniecli import helper

app = typer.Typer(help="Manage Opsgenie users", no_args_is_help=True)
console = Console()


def _get_users_table_data(users: List[Any]) -> List[Dict[str, Any]]:
    """
    Transform user objects into a flat dictionary structure for table display.

    Args:
        users: List of user objects from the Opsgenie API

    Returns:
        List of dictionaries with user data suitable for table display
    """
    return [
        {
            "Username": user._data.get("username", ""),
            "Full Name": user._data.get("fullName", ""),
            "Role": (
                user._data.get("role", {}).get("name", "")
                if isinstance(user._data.get("role"), dict)
                else ""
            ),
            "Verified": str(user._data.get("verified", False)),
            "Blocked": str(user._data.get("blocked", False)),
            "Locale": user._data.get("locale", ""),
            "Timezone": user._data.get("timeZone", ""),
        }
        for user in users
    ]


@app.command(name="list")
def list_users(
    ctx: typer.Context,
    limit: Annotated[int, typer.Option(help="Maximum number of users to return")] = 100,
    filters: Annotated[
        Optional[List[str]],
        typer.Option(
            help="Filter users by attribute (format: attribute:regex_pattern)"
        ),
    ] = None,
) -> None:
    """
    List users in Opsgenie.

    The limit parameter controls how many users are returned from the API.
    Filters can be applied using regex patterns on any user attribute.

    Examples:
        List all users (up to 100):
            opsgeniecli users list

        List first 50 users:
            opsgeniecli users list --limit 50

        Filter by username:
            opsgeniecli users list --filters "Username:john.*"

        Multiple filters:
            opsgeniecli users list --filters "Role:Admin" --filters "Verified:True"
    """
    # Parse filters from command line format (attribute:pattern)
    filter_dict = {
        k: v for k, v in (filter_item.split(":", 1) for filter_item in (filters or []))
    }

    # Fetch users from API
    console.print(f"[cyan]Fetching users (limit: {limit})...[/cyan]")
    users = list(ctx.obj.opsgenie.list_users(limit))

    # Transform to table data
    users_table_data = _get_users_table_data(users)

    # Apply filters if provided
    if filter_dict:
        users_table_data = helper._apply_regex_filters(
            data=users_table_data, filters=filter_dict
        )

    # Display results
    if not users_table_data:
        console.print("[yellow]No users found matching the criteria.[/yellow]")
        return

    console.print(f"\n[green]Found {len(users_table_data)} user(s)[/green]")
    table = helper.get_table(data=users_table_data, title="Opsgenie Users")
    console.print(table)


if __name__ == "__main__":
    app()
