import json
import os
from typing import Sequence
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table
import typer

app = typer.Typer(
    rich_markup_mode="rich", no_args_is_help=True, help="Manage configuration profiles"
)
console = Console()


class ConfigProfile:
    def __init__(self, profile_name: str, data: dict):
        self.profile_name = profile_name
        self._data = data

    @property
    def name(self) -> str:
        return self._data.get("name", "")

    @name.setter
    def name(self, value: str) -> None:
        self._data["name"] = value

    @property
    def api_key(self) -> str:
        return self._data.get("api_key", "")

    @api_key.setter
    def api_key(self, value: str) -> None:
        self._data["api_key"] = value

    def __str__(self) -> str:
        return f"Profile Name: {self.profile_name}\n\tName: {self.name}\n\tAPI Key: {self.api_key}"

    def __bool__(self) -> bool:
        return all((self.profile_name, self._data))


class Config:
    def __init__(self, file_loc: str, profiles: list[ConfigProfile]) -> None:
        self.file = file_loc
        self.profiles = profiles

    def find_profile_by_name(self, profile_name: str) -> ConfigProfile:
        for profile in self.profiles:
            if profile.profile_name == profile_name:
                return profile
        return ConfigProfile(profile_name="", data={})

    def __bool__(self) -> bool:
        return all((self.file, self.profiles))


def read_config(config_file: str) -> Config:
    if not os.path.isfile(path=config_file):
        return Config(file_loc="", profiles=[ConfigProfile(profile_name="", data={})])

    try:
        with open(file=config_file, mode="r") as _file:
            data = json.load(fp=_file)
    except ValueError as error:
        data = {}
        print(f"invalid json: {error}")
    return Config(
        file_loc=config_file,
        profiles=[
            ConfigProfile(profile_name=profile_name, data=data[profile_name])
            for profile_name in data.keys()
        ],
    )


def _get_profiles_table(profiles: Sequence[ConfigProfile]) -> Table:
    table = Table(show_header=True, header_style="cyan")
    table.add_column(header="Profile Name")
    table.add_column(header="Team Name")
    table.add_column(header="API key")
    for profile in profiles:
        table.add_row(
            f"{profile.profile_name}", f"{profile.name}", f"{profile.api_key}"
        )
    return table


@app.command(name="list")
def list_profiles(ctx: typer.Context) -> None:
    """List all configuration profiles.

    Display a table showing all configured profiles with their
    team names and API keys.
    """
    console.print(_get_profiles_table(profiles=ctx.obj.config.profiles))


@app.command(
    name="show",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def show_profile(ctx: typer.Context, profile_name: str = "default") -> None:
    """Show details for a specific configuration profile.

    Display the team name and API key for the specified profile.
    If no profile name is provided, shows the 'default' profile.

    Args:
        profile_name: Name of the profile to display (default: "default")
    """
    _profile = ctx.obj.config.find_profile_by_name(profile_name)
    if not _profile:
        typer.echo(message=f"No profile found for: {profile_name}")
        return None
    console.print(_get_profiles_table(profiles=[_profile]))


def _create_config_data(team_name: str, api_key: str) -> dict[str, dict[str, str]]:
    return {"default": {"name": team_name, "api_key": api_key}}


@app.command(name="create")
def create_config(
    ctx: typer.Context,
    api_key: Annotated[str, typer.Option(prompt=True, hide_input=True)],
    team_name: Annotated[str, typer.Option(prompt=True)],
) -> None:
    """Create a new configuration file with default profile.

    This command will prompt for API key and team name, then create
    a configuration file with a 'default' profile.
    """
    config_file = ctx.obj.config_file_path

    if os.path.isfile(path=config_file):
        console.print(f"[red]Config already exists at {config_file}.[/red]")
        raise typer.Exit(code=1)

    config_data = _create_config_data(team_name=team_name, api_key=api_key)

    os.makedirs(name=os.path.dirname(config_file), exist_ok=True)
    with open(file=config_file, mode="w") as _file:
        json.dump(config_data, _file, indent=4)

    console.print(
        f"[green]✓ Configuration created successfully at {config_file}[/green]"
    )


if __name__ == "__main__":
    app()
