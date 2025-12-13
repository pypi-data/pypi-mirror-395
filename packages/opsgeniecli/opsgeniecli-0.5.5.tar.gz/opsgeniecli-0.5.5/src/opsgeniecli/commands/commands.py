"""
Commands introspection module.

Provides commands to list and explore all available CLI commands.
"""

from typing_extensions import Annotated
import typer
from rich.console import Console
from rich.tree import Tree
from rich.table import Table
from rich import box


app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Introspect available CLI commands",
)
console = Console()


def _get_command_info(command) -> dict:
    """Extract information from a Typer command."""
    # Get help text from various sources
    help_text = ""
    if hasattr(command, "help") and command.help:
        help_text = command.help
    elif hasattr(command, "callback") and command.callback:
        doc = command.callback.__doc__
        if doc:
            # Get first line of docstring
            help_text = doc.strip().split("\n")[0]

    # Get command name
    name = ""
    if hasattr(command, "name") and command.name:
        name = command.name
    elif hasattr(command, "callback"):
        name = command.callback.__name__.replace("_", "-")

    return {
        "name": name,
        "help": help_text,
        "callback": getattr(command, "callback", None),
    }


def _get_typer_commands(typer_instance: typer.Typer) -> list[dict]:
    """Recursively get all commands from a Typer instance."""
    commands = []

    # Get registered commands
    if hasattr(typer_instance, "registered_commands"):
        for command in typer_instance.registered_commands:
            commands.append({**_get_command_info(command), "type": "command"})

    # Get registered groups (sub-typers)
    if hasattr(typer_instance, "registered_groups"):
        for group in typer_instance.registered_groups:
            # Skip if typer_instance is None
            if not group.typer_instance:
                continue

            # Get group name
            group_name = group.name
            if (
                not group_name
                and hasattr(group.typer_instance, "info")
                and group.typer_instance.info
            ):
                group_name = group.typer_instance.info.name

            # Get group help
            group_help = group.help
            if (
                not group_help
                and hasattr(group.typer_instance, "info")
                and group.typer_instance.info
            ):
                info_help = getattr(group.typer_instance.info, "help", None)
                # Only use if it's not a DefaultPlaceholder
                if info_help and not str(info_help).startswith("<"):
                    group_help = info_help

            group_info = {
                "name": group_name or "unknown",
                "help": group_help or "",
                "type": "group",
                "commands": _get_typer_commands(group.typer_instance),
            }
            commands.append(group_info)

    return commands


def _build_tree(commands: list[dict], tree: Tree, prefix: str = "") -> None:
    """Recursively build a Rich Tree from command structure."""
    for cmd in sorted(commands, key=lambda x: x["name"]):
        if cmd["type"] == "group":
            # Add a branch for command groups
            help_text = f" - [dim]{cmd['help']}[/dim]" if cmd.get("help") else ""
            branch = tree.add(f"[bold cyan]{cmd['name']}[/bold cyan]{help_text}")
            # Recursively add subcommands
            if cmd.get("commands"):
                _build_tree(cmd["commands"], branch, prefix=f"{prefix}{cmd['name']} ")
        else:
            # Add a leaf for individual commands
            help_text = f" - [dim]{cmd['help']}[/dim]" if cmd.get("help") else ""
            tree.add(f"[green]{cmd['name']}[/green]{help_text}")


def _build_flat_list(commands: list[dict], prefix: str = "") -> list[dict]:
    """Build a flat list of all commands with their full paths."""
    flat_list = []

    for cmd in sorted(commands, key=lambda x: x["name"]):
        if cmd["type"] == "group":
            group_path = f"{prefix}{cmd['name']}"
            flat_list.append(
                {"command": group_path, "type": "group", "help": cmd["help"]}
            )
            # Recursively add subcommands
            if cmd.get("commands"):
                flat_list.extend(
                    _build_flat_list(cmd["commands"], prefix=f"{group_path} ")
                )
        else:
            command_path = f"{prefix}{cmd['name']}"
            flat_list.append(
                {"command": command_path, "type": "command", "help": cmd["help"]}
            )

    return flat_list


@app.command(name="list")
def list_commands(
    flat: Annotated[
        bool, typer.Option("--flat", help="Show as flat list instead of tree")
    ] = False,
):
    """
    List all available CLI commands.

    Shows a tree view of all commands and subcommands by default.
    Use --flat to show as a flat list with full command paths.
    """
    # Get the root typer app
    # We need to access the parent context to get the root app
    from opsgeniecli import cli

    # Get all commands from the root app
    commands = _get_typer_commands(cli.app)

    if flat:
        # Build flat list
        flat_list = _build_flat_list(commands)

        # Create table for flat view
        table = Table(
            title="Available Commands",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Type", style="yellow", width=10)
        table.add_column("Description", style="white")

        for item in flat_list:
            type_display = "group" if item["type"] == "group" else "command"
            table.add_row(item["command"], type_display, item["help"])

        console.print(table)
    else:
        # Build tree view
        tree = Tree(
            "[bold blue]opsgeniecli[/bold blue] - Opsgenie CLI", guide_style="dim"
        )
        _build_tree(commands, tree)

        console.print("\n")
        console.print(tree)
        console.print("\n[dim]Use --flat for a flat list view[/dim]\n")


if __name__ == "__main__":
    app()
