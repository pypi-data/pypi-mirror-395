import re
from typing import Any, Dict, List

import typer
from rich.table import Table
from rich import box
from rich.console import Console

console = Console()


def _apply_regex_filters(
    data: list[dict[str, Any]], filters: Dict[str, str]
) -> list[dict[str, Any]]:
    filtered_data = data
    for attr, pattern in filters.items():
        regex = re.compile(pattern)
        filtered_data = [
            _dict for _dict in filtered_data if regex.search(str(_dict.get(attr, "")))
        ]
    return filtered_data


def get_table(
    data: list[dict[str, Any]], title: str, row_style: List[str] = ["blue", "white"]
) -> Table:
    table = Table(title=title, show_lines=True, row_styles=row_style, box=box.MINIMAL)
    for header in next(iter(data), {}).keys():
        table.add_column(str(header))

    for row in data:
        table.add_row(*[str(value) for value in row.values()])
    return table


def show_table_and_confirm(
    data: list[dict[str, Any]],
    title: str,
    prompt: str = "\nDo you want to continue?",
    force: bool = False,
) -> bool:
    """Display a table and ask for user confirmation.

    Args:
        data: List of dictionaries to display in table
        title: Table title
        prompt: Confirmation prompt text

    Returns:
        True if user confirms, raises typer.Exit() if user cancels
    """
    typer.echo(f"\n{len(data)} items found")
    table = get_table(data=data, title=title)
    console.print(table)

    if not force and not typer.confirm(prompt):
        typer.echo("Operation cancelled")
        raise typer.Exit()

    return True
