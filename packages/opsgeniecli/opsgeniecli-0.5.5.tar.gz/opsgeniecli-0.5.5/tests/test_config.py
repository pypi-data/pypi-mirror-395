import json
import tempfile
import pytest
from unittest.mock import MagicMock, mock_open, patch
from rich.table import Table

import typer

from opsgeniecli.commands import config
from opsgeniecli.commands.config import (
    ConfigProfile,
    _create_config_data,
    _get_profiles_table,
    read_config,
    Config,
    show_profile,
)
from typer.testing import CliRunner

from opsgeniecli.cli import OpsgenieCli

runner = CliRunner()

### Function: read_config


def test_read_config_file_not_found():
    with patch("os.path.isfile", return_value=False):
        _config = read_config(config_file="non_existent_file.json")
        assert not bool(_config)


def test_read_config_invalid_json():
    invalid_json_content = "{invalid_json}"
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data=invalid_json_content)),
        patch("builtins.print") as mock_print,
    ):

        read_config(config_file="invalid.json")
        mock_print.assert_called_once_with(
            "invalid json: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"
        )


def test_read_config_valid_json():
    valid_json_content = json.dumps(
        obj={
            "profile1": {"name": "team1", "api_key": "key1"},
            "profile2": {"name": "team2", "api_key": "key2"},
        }
    )
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data=valid_json_content)),
    ):
        result = read_config(config_file="valid.json")
        assert isinstance(result, Config)
        assert len(result.profiles) == 2
        assert result.profiles[0].profile_name == "profile1"
        assert result.profiles[0].name == "team1"
        assert result.profiles[0].api_key == "key1"
        assert result.profiles[1].profile_name == "profile2"
        assert result.profiles[1].name == "team2"
        assert result.profiles[1].api_key == "key2"


def test_read_config_empty_json():
    empty_json_content = "{}"
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data=empty_json_content)),
    ):
        result = read_config("empty.json")
        assert isinstance(result, Config)
        assert len(result.profiles) == 0


### Function: _create_config_data


def test_create_config_data_valid_json():
    team_name = "test_team_name_1"
    api_key = "test_api_key_1"
    config_data = _create_config_data(team_name=team_name, api_key=api_key)

    # Check if the returned data can be serialized to JSON
    try:
        json_str = json.dumps(config_data)
        assert isinstance(json_str, str)
    except (TypeError, ValueError) as e:
        pytest.fail(f"Function returned invalid JSON: {e}")

    # Additional checks to ensure the structure is correct
    assert "default" in config_data
    assert config_data["default"]["name"] == team_name
    assert config_data["default"]["api_key"] == api_key


### Function: _create_config_data


def test_create_config_data_valid():
    team_name = "test_team_name"
    api_key = "test_api_key"
    expected_data = {"default": {"name": team_name, "api_key": api_key}}

    config_data = _create_config_data(team_name=team_name, api_key=api_key)

    assert config_data == expected_data


def test_create_config_data_empty_values():
    team_name = ""
    api_key = ""
    expected_data = {"default": {"name": team_name, "api_key": api_key}}

    config_data = _create_config_data(team_name=team_name, api_key=api_key)

    assert config_data == expected_data


### Function: show_config


def test_show_config_with_existing_team(profile_name="default"):
    existing_content = json.dumps(
        obj={"default": {"name": "existing_team", "api_key": "existing_api_key"}}
    )

    with (
        tempfile.NamedTemporaryFile(delete=False) as temp_file,
        patch("builtins.open", mock_open(read_data=existing_content)),
        patch("opsgeniecli.commands.config.console.print") as mock_console_print,
    ):
        temp_file.write(existing_content.encode("utf-8"))
        _config = config.read_config(config_file=temp_file.name)
        profile = _config.find_profile_by_name(profile_name=profile_name)

        # Create a mock context with obj attribute
        ctx = MagicMock(spec=typer.Context)
        ctx.obj = OpsgenieCli(
            config=_config, profile=profile, config_file_path=temp_file.name
        )

        show_profile(ctx, profile_name)

        # assert a table is printed
        mock_console_print.assert_called_once()


def test_show_config_with_non_existing_team(profile_name="ergergergege"):
    existing_content = json.dumps(
        obj={"default": {"name": "existing_team", "api_key": "existing_api_key"}}
    )

    with (
        tempfile.NamedTemporaryFile(delete=False) as temp_file,
        patch("builtins.open", mock_open(read_data=existing_content)),
        patch("typer.echo") as mock_typer_echo,
    ):
        temp_file.write(existing_content.encode("utf-8"))
        _config = config.read_config(config_file=temp_file.name)
        profile = _config.find_profile_by_name(profile_name=profile_name)

        # Create a mock context with obj attribute
        ctx = MagicMock(spec=typer.Context)
        ctx.obj = OpsgenieCli(
            config=_config, profile=profile, config_file_path=temp_file.name
        )

        show_profile(ctx, profile_name)

        # assert that it mentions which profile name wasn't found in the config
        mock_typer_echo.assert_called_once_with(
            message=f"No profile found for: {profile_name}"
        )


### Function: list_config


def test_get_profiles_table_empty():
    profiles = []
    table = _get_profiles_table(profiles)

    assert isinstance(table, Table)
    assert table.row_count == 0
    assert table.columns[0].header == "Profile Name"
    assert table.columns[1].header == "Team Name"
    assert table.columns[2].header == "API key"


def test_get_profiles_table_single_profile():
    profile = MagicMock(spec=ConfigProfile)
    profile.profile_name = "default"
    profile.name = "team1"
    profile.api_key = "key1"
    profiles = [profile]

    table = _get_profiles_table(profiles)

    assert isinstance(table, Table)
    assert table.row_count == 1


def test_get_profiles_table_multiple_profiles():
    profile1 = MagicMock(spec=ConfigProfile)
    profile1.profile_name = "default"
    profile1.name = "team1"
    profile1.api_key = "key1"

    profile2 = MagicMock(spec=ConfigProfile)
    profile2.profile_name = "profile2"
    profile2.name = "team2"
    profile2.api_key = "key2"

    profiles = [profile1, profile2]

    table = _get_profiles_table(profiles)

    assert isinstance(table, Table)
    assert table.row_count == 2
