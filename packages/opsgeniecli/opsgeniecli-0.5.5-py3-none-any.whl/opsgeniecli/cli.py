import os
from pathlib import Path
import typer
from rich.console import Console
from typing_extensions import Annotated
from opsgeniecli.commands import (
    on_call,
    config,
    alerts,
    commands,
    alert_policies,
    escalations,
    heartbeat,
    teams,
    logs,
    users,
    integrations,
    schedules,
    maintenance_policies,
    notification_policies,
    teams_routing_rules,
)
from opsgenielib import Opsgenie

console = Console()
app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)
app.add_typer(typer_instance=on_call.app, name="on-call")
app.add_typer(typer_instance=config.app, name="config")
app.add_typer(typer_instance=alerts.app, name="alerts")
app.add_typer(typer_instance=alert_policies.app, name="alert-policies")
app.add_typer(typer_instance=commands.app, name="commands")
app.add_typer(typer_instance=escalations.app, name="escalations")
app.add_typer(typer_instance=heartbeat.app, name="heartbeat")
app.add_typer(typer_instance=teams.app, name="teams")
app.add_typer(typer_instance=logs.app, name="logs")
app.add_typer(typer_instance=users.app, name="users")
app.add_typer(typer_instance=integrations.app, name="integrations")
app.add_typer(typer_instance=schedules.app, name="schedules")
app.add_typer(typer_instance=maintenance_policies.app, name="maintenance-policies")
app.add_typer(typer_instance=notification_policies.app, name="notification-policies")
app.add_typer(typer_instance=teams_routing_rules.app, name="teams-routing-rules")


class OpsgenieCli:
    def __init__(
        self,
        config: config.Config,
        profile: config.ConfigProfile,
        config_file_path: str,
    ) -> None:
        self._opsgenie = None
        self.config = config
        self.profile = profile
        self.config_file_path = config_file_path

    @property
    def opsgenie(self) -> Opsgenie:
        """Lazy instantiation of Opsgenie client."""
        if self._opsgenie is None:
            if not self.profile.api_key:
                console.print("[red]Error: No API key configured.[/red]")
                console.print("\nTo set up your configuration, run:")
                console.print("  [cyan]opsgeniecli config create[/cyan]")
                raise typer.Exit(code=1)
            self._opsgenie = Opsgenie(api_key=self.profile.api_key)
        return self._opsgenie


def version_callback(value: bool) -> None:
    """Display version and exit."""
    if value:
        try:
            from opsgeniecli._version import __version__
        except ImportError:
            __version__ = "unknown (not installed)"
        console.print(f"opsgeniecli version: {__version__}")
        raise typer.Exit()


@app.callback()
def common(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit",
        ),
    ] = False,
    config_file: Annotated[str, typer.Option()] = os.path.expanduser(
        path=f"{Path.home()}/.config/opsgenie-cli/config.json"
    ),
    team_name: Annotated[str, typer.Option(envvar="OPSGENIE_TEAM_NAME")] = "",
    api_key: Annotated[str, typer.Option(envvar="OPSGENIE_API_KEY")] = "",
    profile: Annotated[str, typer.Option(envvar="OPSGENIE_PROFILE")] = "default",
) -> None:
    """Common Entry Point"""
    _config = config.read_config(config_file=config_file)
    _profile = _config.find_profile_by_name(profile_name=profile)

    # Override profile values with CLI options if provided
    _profile.name = team_name if team_name else _profile.name
    _profile.api_key = api_key if api_key else _profile.api_key

    ctx.obj = OpsgenieCli(
        config=_config, profile=_profile, config_file_path=config_file
    )


if __name__ == "__main__":
    app()
