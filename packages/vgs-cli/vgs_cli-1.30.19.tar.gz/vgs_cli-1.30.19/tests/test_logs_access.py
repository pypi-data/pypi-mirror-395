import json
from unittest.mock import patch
from click.testing import CliRunner

from vgscli.access_logs import (
    prepare_filter,
    calculate_start_page,
    calculate_start_index,
)
from vgs.sdk.serializers import dump_yaml, format_logs
from freezegun import freeze_time

from vgscli.click_extensions import Config
from vgscli.vgs import logs

access_logs_response = json.loads(open("tests/access_logs_response.json").read())


def test_access_no_options():
    runner = CliRunner()
    result = runner.invoke(logs, ["access"])
    assert result.exit_code == 2
    assert (
        "Usage: logs access [OPTIONS]\nTry 'logs access --help' for help.\n\nError: Missing option '--vault' / '-V'.\n"
        == result.output
    )


@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.vgs.create_audits_api")
def test_access_only_vault(create_audits_api, *args):

    create_audits_api().access_logs.list().body = access_logs_response

    runner = CliRunner()
    result = runner.invoke(
        logs, ["access", "--vault", "tntbnqdfizv"], obj=Config(False, "production")
    )

    expected = dump_yaml(
        {
            "version": 1,
            "data": access_logs_response["data"],
        }
    )
    assert result.exit_code == 0
    assert result.output == "{}\n".format(expected)


@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.vgs.create_audits_api")
def test_access_tail_10(create_audits_api, *args):
    create_audits_api().access_logs.list().body = access_logs_response

    runner = CliRunner()
    result = runner.invoke(
        logs,
        ["access", "--vault", "tntbnqdfizv", "--tail", 10],
        obj=Config(False, "production"),
    )

    expected = dump_yaml(
        {
            "version": 1,
            "data": access_logs_response["data"][-10:],
        }
    )
    assert result.exit_code == 0
    assert result.output == "{}\n".format(expected)


@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.vgs.create_audits_api")
@patch("vgscli.vgs.fetch_logs")
@patch("vgscli.vgs.format_logs")
@patch("vgscli.vgs.prepare_filter")
def test_access_since(mock_prepare_filter, *args):
    tenant_value = "tntbnqdfizv"
    since_value = "2020-08-18T10:11:06"

    runner = CliRunner()
    result = runner.invoke(
        logs,
        ["access", "--vault", tenant_value, "--since", since_value],
        obj=Config(False, "production"),
    )

    expected = {
        "tenant_id": tenant_value,
        "protocol": None,
        "from": since_value,
        "to": None,
    }
    assert result.exit_code == 0
    assert mock_prepare_filter.call_args[0][0] == expected


@freeze_time("2020-08-18T10:11:06")
@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.vgs.create_audits_api")
@patch("vgscli.vgs.fetch_logs")
@patch("vgscli.vgs.format_logs")
@patch("vgscli.vgs.prepare_filter")
def test_access_since_duration(mock_prepare_filter, *args):
    tenant_value = "tntbnqdfizv"

    runner = CliRunner()
    result = runner.invoke(
        logs,
        ["access", "--vault", tenant_value, "--since", "2h"],
        obj=Config(False, "production"),
    )

    expected = {
        "tenant_id": tenant_value,
        "protocol": None,
        "from": "2020-08-18T08:11:06",
        "to": None,
    }
    assert result.exit_code == 0
    assert mock_prepare_filter.call_args[0][0] == expected


@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.vgs.create_audits_api")
@patch("vgscli.vgs.fetch_logs")
@patch("vgscli.vgs.format_logs")
@patch("vgscli.vgs.prepare_filter")
def test_access_until(mock_prepare_filter, *args):
    tenant_value = "tntbnqdfizv"
    until_value = "2020-08-18T10:11:06"

    runner = CliRunner()
    result = runner.invoke(
        logs,
        ["access", "--vault", tenant_value, "--until", until_value],
        obj=Config(False, "production"),
    )

    expected = {
        "tenant_id": tenant_value,
        "protocol": None,
        "from": None,
        "to": until_value,
    }
    assert result.exit_code == 0
    assert mock_prepare_filter.call_args[0][0] == expected


@freeze_time("2020-08-18T12:11:06")
@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.vgs.create_audits_api")
@patch("vgscli.vgs.fetch_logs")
@patch("vgscli.vgs.format_logs")
@patch("vgscli.vgs.prepare_filter")
def test_access_until_duration(mock_prepare_filter, *args):
    tenant_value = "tntbnqdfizv"

    runner = CliRunner()
    result = runner.invoke(
        logs,
        ["access", "--vault", tenant_value, "--until", "2h"],
        obj=Config(False, "production"),
    )

    expected = {
        "tenant_id": tenant_value,
        "protocol": None,
        "from": None,
        "to": "2020-08-18T10:11:06",
    }
    assert result.exit_code == 0
    assert mock_prepare_filter.call_args[0][0] == expected


@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.vgs.create_audits_api")
@patch("vgscli.vgs.fetch_logs")
@patch("vgscli.vgs.format_logs")
@patch("vgscli.vgs.prepare_filter")
def test_access_since_until(mock_prepare_filter, *args):
    tenant_value = "tntbnqdfizv"
    since_value = "2020-08-10T8:12:06"
    until_value = "2020-08-18T10:11:06"

    runner = CliRunner()
    result = runner.invoke(
        logs,
        [
            "access",
            "--vault",
            tenant_value,
            "--since",
            since_value,
            "--until",
            until_value,
        ],
        obj=Config(False, "production"),
    )

    expected = {
        "tenant_id": tenant_value,
        "protocol": None,
        "from": since_value,
        "to": until_value,
    }
    assert result.exit_code == 0
    assert mock_prepare_filter.call_args[0][0] == expected


@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.vgs.create_audits_api")
@patch("vgscli.vgs.prepare_filter")
@patch("vgscli.vgs.fetch_logs")
@patch("vgscli.vgs.format_logs")
def test_access_output(mock_format_logs, mock_fetch_logs, *args):
    mock_fetch_logs.return_value = [1]

    runner = CliRunner()
    result = runner.invoke(
        logs,
        ["access", "--vault", "tntbnqdfizv", "--output", "json"],
        obj=Config(False, "production"),
    )

    assert result.exit_code == 0
    assert mock_format_logs.call_args[0][1] == "json"


def test_format_logs():
    data = {
        "data": [{"attributes": {"id": "123456"}}],
        "enabled": None,
    }
    expected_json = '{"data": [{"attributes": {"id": "123456"}}], "enabled": null}'
    expected_yaml = "data:\n- attributes:\n    id: '123456'\nenabled: null\n"

    assert format_logs(data, "json") == expected_json
    assert format_logs(data, "yaml") == expected_yaml


def test_prepare_filter():
    data = {
        "tenant_id": "tenant_value",
        "protocol": "protocol_value",
        "from": "since_value",
        "to": "until_value",
    }
    expected = {
        "filter[tenant_id]": "tenant_value",
        "filter[protocol]": "protocol_value",
        "filter[from]": "since_value",
        "filter[to]": "until_value",
    }
    assert prepare_filter(data) == expected


def test_calculate_start_page():
    assert calculate_start_page(31, 1, 30) == 2
    assert calculate_start_page(31, 2, 30) == 1
    assert calculate_start_page(31, 30, 30) == 1
    assert calculate_start_page(65, 3, 30) == 3
    assert calculate_start_page(65, 30, 30) == 2
    assert calculate_start_page(65, 60, 30) == 1
    assert calculate_start_page(10, 20, 30) == 1
    assert calculate_start_page(20, 20, 30) == 1
    assert calculate_start_page(30, 10, 30) == 1


def test_calculate_start_index():
    assert calculate_start_index(31, 1, 30) == 0
    assert calculate_start_index(31, 2, 30) == -1
    assert calculate_start_index(31, 30, 30) == 1
    assert calculate_start_index(65, 3, 30) == 2
    assert calculate_start_index(65, 30, 30) == 5
    assert calculate_start_index(65, 60, 30) == 5
    assert calculate_start_index(65, 39, 30) == -4
    assert calculate_start_index(10, 20, 30) == 0
    assert calculate_start_index(20, 20, 30) == 0
    assert calculate_start_index(30, 10, 30) == -10
