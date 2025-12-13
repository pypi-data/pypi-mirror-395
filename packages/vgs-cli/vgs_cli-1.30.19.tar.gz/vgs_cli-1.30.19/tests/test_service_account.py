import json
from tempfile import NamedTemporaryFile
from textwrap import dedent
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner
from simple_rest_client.exceptions import ClientError
from simple_rest_client.models import Response
from vgscli import testing
from vgscli.cli.commands.apply import apply_service_account
from vgscli.cli.commands.generate import generate_service_account
from vgscli.click_extensions import Config
from vgscli.vgs import delete_service_account

create_client_response = json.loads(
    open("tests/create_service_account_response.json").read()
)


@testing.patch("vgscli.cli.commands.apply.create_account_mgmt_api")
def test_apply_service_account(create_account_mgmt_api: Mock) -> None:
    create_account_mgmt_api().service_accounts.create().body = create_client_response

    runner = CliRunner()
    result = runner.invoke(
        apply_service_account,
        ["-O", "ACtTmnC6VoRHU1JdxouH9vdc", "-f", "tests/apply_service_account.yaml"],
        obj=Config(False, "production"),
    )

    expected = open("tests/create_service_account_cmd_output.yaml").read()
    assert result.exit_code == 0
    assert result.output == expected
    call_args = create_account_mgmt_api().service_accounts.create.call_args
    assert call_args[0][0] == "ACtTmnC6VoRHU1JdxouH9vdc"
    assert call_args.kwargs["body"] == {
        "data": {
            "attributes": {
                "name": "vgs-cli",
                "annotations": {},
                "scopes": [
                    {"name": "access-logs:read"},
                    {"name": "routes:read"},
                    {"name": "routes:write"},
                    {"name": "vaults:read"},
                ],
                "access_token_lifespan": None,
                "vaults": ["tnthlp1rehx"],
            }
        }
    }


@testing.patch("vgscli.cli.commands.apply.create_account_mgmt_api")
def test_apply_service_account_with_valid_access_token_lifespan(
    create_account_mgmt_api: Mock,
) -> None:
    create_account_mgmt_api().service_accounts.create().body = create_client_response

    access_token_lifespan = 300
    with NamedTemporaryFile("w") as file:
        file.write(
            dedent(
                f"""
            apiVersion: 1.0.0
            kind: ServiceAccount
            data:
              accessTokenLifespan: {access_token_lifespan}
              name: route-reader
              scopes:
                - name: routes:read
        """
            )
        )
        file.flush()

        args = ["-O", "ACtTmnC6VoRHU1JdxouH9vdc", "-f", file.name]
        CliRunner().invoke(apply_service_account, args, obj=Config(False, "production"))

    call_args = create_account_mgmt_api().service_accounts.create.call_args
    assert (
        call_args.kwargs["body"]["data"]["attributes"]["access_token_lifespan"]
        == access_token_lifespan
    )


@testing.patch("vgscli.cli.commands.apply.create_account_mgmt_api")
def test_apply_service_account_with_invalid_access_token_lifespan(
    create_account_mgmt_api: Mock,
) -> None:
    create_account_mgmt_api().service_accounts.create().body = create_client_response

    with NamedTemporaryFile("w") as file:
        file.write(
            dedent(
                """
            apiVersion: 1.0.0
            kind: ServiceAccount
            data:
              accessTokenLifespan: 30 # Too short
              name: route-reader
              scopes:
                - name: routes:read
        """
            )
        )
        file.flush()

        args = ["-O", "ACtTmnC6VoRHU1JdxouH9vdc", "-f", file.name]

        result = CliRunner().invoke(
            apply_service_account, args, obj=Config(False, "production")
        )
        assert result.exit_code == 2
        assert "Error during validation of the file input" in result.output


@testing.patch("vgscli.cli.commands.apply.create_account_mgmt_api")
def test_apply_service_account_missing_scope(create_account_mgmt_api: Mock) -> None:
    create_account_mgmt_api.service_accounts.create().body = create_client_response

    runner = CliRunner()
    result = runner.invoke(
        apply_service_account,
        [
            "-O",
            "ACtTmnC6VoRHU1JdxouH9vdc",
            "-f",
            "tests/apply_service_account_missing_scope.yaml",
        ],
        obj=Config(False, "production"),
    )

    assert result.exit_code == 2
    assert (
        "Error during validation of the file input: 'scopes' is a required property"
        in result.output
    )


@testing.patch("vgscli.cli.commands.apply.create_account_mgmt_api")
def test_apply_service_account_account_management_error(
    create_account_mgmt_api: Mock,
) -> None:
    detail = "Oops, something bad happened"
    response = Response(
        url="https://marketplace.verygoodsecurity.io/verygoodsecurity/stripe/instances",
        method="POST",
        body={"errors": [{"detail": detail}]},
        headers={},
        status_code=400,
        client_response="400",
    )
    create_account_mgmt_api().service_accounts.create.side_effect = ClientError(
        "400", response
    )

    runner = CliRunner()
    result = runner.invoke(
        apply_service_account,
        ["-O", "ACtTmnC6VoRHU1JdxouH9vdc", "-f", "tests/apply_service_account.yaml"],
        obj=Config(False, "production"),
    )

    assert result.exit_code == 2
    assert f"Service Account creation failed with error: ['{detail}']" in result.output


def test_generate_vgs_cli_service_account_no_vaults(*args):
    runner = CliRunner()
    result = runner.invoke(
        generate_service_account, ["-t", "vgs-cli"], obj=Config(False, "production")
    )
    expected = "Warning! Service Account won't have access to any vaults inside organization. If you need it to access vault(s) please use --vault <vault-identifier>.\n"
    expected += open("tests/generate_vgs_cli_service_account.yaml").read()

    assert result.exit_code == 0
    assert result.output == expected


def test_generate_vgs_cli_service_account_multiple_vaults(*args):
    runner = CliRunner()
    result = runner.invoke(
        generate_service_account,
        ["-t", "vgs-cli", "--vault", "vault-id", "--vault", "vault-id2"],
        obj=Config(False, "production"),
    )

    expected = open(
        "tests/generate_vgs_cli_service_account_multiple_vaults.yaml"
    ).read()

    assert result.exit_code == 0
    assert result.output == expected


def test_generate_rendered_calm_service_account(*args):
    runner = CliRunner()
    result = runner.invoke(
        generate_service_account,
        ["-t", "calm", "--vault", "vault-id"],
        obj=Config(False, "production"),
    )
    expected = open("tests/generate_rendered_calm_service_account.yaml").read()

    assert result.exit_code == 0
    assert result.output == expected


def test_generate_rendered_calm_service_account_undefined_variable(*args):
    result = CliRunner().invoke(
        generate_service_account, ["-t", "calm"], obj=Config(False, "production")
    )
    assert result.exit_code == 1
    assert (
        "Error! This template needs single vault to be specified. "
        "Please use '--vault <vault-identifier>' to pass the vault" in result.output
    )


@pytest.mark.parametrize(
    "template,rendered_template",
    [
        ("checkout", "generate_rendered_checkout_service_account.yaml"),
        (
            "sub-account-checkout",
            "generate_rendered_sub_account_checkout_service_account.yaml",
        ),
        ("payments-admin", "generate_rendered_payments_admin_service_account.yaml"),
    ],
)
def test_generate_rendered_payment_orchestration_service_account(
    *args, template, rendered_template
):
    runner = CliRunner()
    result = runner.invoke(
        generate_service_account,
        [
            "-t",
            template,
            "--vault",
            "vault-id",
            "--var",
            "name=name",
            "--var",
            "sub_account_id=sub-account",
        ],
        obj=Config(False, "production"),
    )
    expected = open(f"tests/{rendered_template}").read()

    assert result.exit_code == 0
    assert result.output == expected


@pytest.mark.parametrize(
    "template",
    [
        "payments-admin",
    ],
)
def test_generate_rendered_payment_orchestration_service_account_undefined_variable(
    *args, template
):
    result = CliRunner().invoke(
        generate_service_account, ["-t", template], obj=Config(False, "production")
    )
    assert result.exit_code == 1
    assert (
        "Error! This template needs single vault to be specified. "
        "Please use '--vault <vault-identifier>' to pass the vault" in result.output
    )


def test_generate_service_account_wrong_template(*args):
    runner = CliRunner()
    result = runner.invoke(
        generate_service_account, ["-t", "prometheus"], obj=Config(False, "production")
    )

    assert result.exit_code == 2
    assert (
        """Error: Invalid value for '--template' / '-t': 'prometheus'"""
        in result.output
    )


@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.cli.create_account_mgmt_api")
def test_delete_service_account(mock_create_account_mgmt_api, mock_get_access_token, mock_handshake):
    mock_api = Mock()
    mock_create_account_mgmt_api.return_value = mock_api

    runner = CliRunner()
    result = runner.invoke(
        delete_service_account,
        ["-O", "AC7YyuLH3kW64AQ1ujbEin2t", "AC7YyuLH3-vgs-cli-dZV9a"],
        obj=Config(False, "production"),
    )

    assert result.exit_code == 0
    assert result.output == ""
    
    # Verify the correct method was called
    mock_api.service_accounts.delete.assert_called_once_with(
        "AC7YyuLH3kW64AQ1ujbEin2t",
        "AC7YyuLH3-vgs-cli-dZV9a"
    )


@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.cli.create_account_mgmt_api")
def test_delete_service_account_error(mock_create_account_mgmt_api, mock_get_access_token, mock_handshake):
    detail = "Oops, something bad happened"
    response = Response(
        url="https://marketplace.verygoodsecurity.io/verygoodsecurity/stripe/instances",
        method="POST",
        body={"errors": [{"detail": detail}]},
        headers={},
        status_code=400,
        client_response="400",
    )
    
    mock_api = Mock()
    mock_api.service_accounts.delete.side_effect = ClientError("400", response)
    mock_create_account_mgmt_api.return_value = mock_api

    runner = CliRunner()
    result = runner.invoke(
        delete_service_account,
        ["-O", "AC7YyuLH3kW64AQ1ujbEin2t", "AC7YyuLH3-vgs-cli-dZV9a"],
        obj=Config(False, "production"),
    )

    assert result.exit_code == 2
    assert f"Service Account deletion failed with error: ['{detail}']" in result.output


if __name__ == "__main__":
    test_apply_service_account()
    test_apply_service_account_with_valid_access_token_lifespan()
    test_apply_service_account_with_invalid_access_token_lifespan()
    test_apply_service_account_missing_scope()
    test_apply_service_account_account_management_error()
    test_generate_vgs_cli_service_account()
    test_generate_service_account_wrong_template()
    test_delete_service_account()
    test_delete_service_account_error()
