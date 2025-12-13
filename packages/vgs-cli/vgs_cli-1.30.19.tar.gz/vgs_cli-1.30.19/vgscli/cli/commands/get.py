import click
from click_plugins import with_plugins
from vgscli.cli_utils import iter_entry_points
from simple_rest_client.exceptions import ClientError, ServerError
from vgscli.auth import handshake, token_util
from vgscli.cli import create_account_mgmt_api, create_vault_mgmt_api
from vgscli.cli.types import ResourceId, ResourceIdParamType
from vgscli.cli_utils import dump_camelized_yaml
from vgscli.errors import ServiceClientListingError, handle_errors

from vgs.sdk.routes import dump_all_routes, normalize
from vgs.sdk.serializers import yaml  # this one correctly outputs blocks
from vgs.sdk.vaults_api import create_api as create_vault_mgmt_api_routes

from .apply import wrap_in_http_envelope


@with_plugins(iter_entry_points("vgs.get.plugins"))
@click.group("get")
def get() -> None:
    """
    Get VGS resource.
    """
    pass


@get.command("service-accounts")
@click.option(
    "-O",
    "--organization",
    "org_id",
    type=ResourceIdParamType(prefix="AC"),
    help="Organization ID which service accounts will be listed",
)
@click.pass_context
@handle_errors()
def get_service_accounts(ctx: click.Context, org_id: ResourceId):
    """
    Get service accounts from the organization.
    """

    account_mgmt = create_account_mgmt_api(ctx)
    try:
        # noinspection PyUnresolvedReferences
        response = account_mgmt.service_accounts.get(org_id.base58)
    except (ClientError, ServerError) as e:
        raise ServiceClientListingError(e)

    accounts = response.body["data"]["attributes"]["service_accounts"]

    for account in accounts:
        click.echo("---")
        click.echo(
            dump_camelized_yaml(
                {
                    "apiVersion": "1.0.0",
                    "kind": "ServiceAccount",
                    "data": account,
                }
            )
        )


@get.command("access-credentials")
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.pass_context
@handle_errors()
def get_access_credentials(ctx, vault):
    """
    Get access-credentials
    """

    account_mgmt = create_account_mgmt_api(ctx)

    response = account_mgmt.vaults.get_by_id(vault)

    vault_mgmt = create_vault_mgmt_api(
        ctx, response.body["data"][0]["links"]["vault_management_api"]
    )

    response = vault_mgmt.credentials.list(headers={"VGS-Tenant": vault})

    click.echo(
        dump_camelized_yaml(
            {
                "apiVersion": "1.0.0",
                "kind": "AccessCredentials",
                "data": response.body["data"],
            }
        )
    )


@get.command("organizations")
@click.pass_context
@handle_errors()
def get_organizations(ctx):
    """
    Get organizations
    """

    account_mgmt = create_account_mgmt_api(ctx)

    response = account_mgmt.organizations.list()

    click.echo(
        dump_camelized_yaml(
            {
                "apiVersion": "1.0.0",
                "kind": "Organizations",
                "data": response.body["data"],
            }
        )
    )


@get.command("vaults")
@click.pass_context
@handle_errors()
def get_vaults(ctx):
    """
    Get vaults
    """

    account_mgmt = create_account_mgmt_api(ctx)

    response = account_mgmt.vaults.list()

    click.echo(
        dump_camelized_yaml(
            {
                "apiVersion": "1.0.0",
                "kind": "Vaults",
                "data": response.body["data"],
            }
        )
    )


@get.command("http-routes")
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.pass_context
@handle_errors()
def get_http_routes(ctx, vault):
    """
    Get HTTP routes
    """

    handshake(ctx, ctx.obj.env)

    vault_management_api = create_vault_mgmt_api_routes(
        ctx, vault, ctx.obj.env, token_util.get_access_token()
    )

    response = vault_management_api.routes.list()
    routes = normalize(response.body["data"])

    # for each route, wrap in envelope and return
    wrapped = [wrap_in_http_envelope(route) for route in routes]

    click.echo(yaml.dump_all(wrapped, indent=2))


@get.command("routes")
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.pass_context
@handle_errors()
def get_routes(ctx, vault):
    """
    Get routes
    """
    handshake(ctx, ctx.obj.env)

    routes_api = create_vault_mgmt_api_routes(
        ctx, vault, ctx.obj.env, token_util.get_access_token()
    )
    dump = dump_all_routes(routes_api)
    click.echo(dump)
