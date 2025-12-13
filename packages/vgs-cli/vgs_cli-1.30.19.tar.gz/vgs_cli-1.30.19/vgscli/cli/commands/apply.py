import logging
import time
from typing import Optional

import click
from click_plugins import with_plugins
from vgscli.cli_utils import iter_entry_points
from simple_rest_client import exceptions
from simple_rest_client.exceptions import ClientError
from vgscli.auth import handshake, token_util
from vgscli.cli import create_account_mgmt_api, create_vault_mgmt_api
from vgscli.cli.types import ResourceId, ResourceIdParamType
from vgscli.cli_utils import dump_camelized_yaml, validate_multi_yaml, validate_yaml
from vgscli.errors import ServiceClientCreationError, VgsCliError, handle_errors

from vgs.sdk.errors import RouteNotValidError
from vgs.sdk.routes import dump_yaml, normalize, sync_all_routes
from vgs.sdk.serializers import Literal
from vgs.sdk.vaults_api import create_api as create_vaults_api

logger = logging.getLogger()


@with_plugins(iter_entry_points("vgs.apply.plugins"))
@click.group("apply")
def apply() -> None:
    """
    Create or update a VGS resource.
    """
    pass


@apply.command("service-account")
@click.option(
    "-O",
    "--organization",
    "org_id",
    type=ResourceIdParamType(prefix="AC"),
    help="ID of the organization to associate the vault with.",
)
@click.option(
    "--file",
    "-f",
    type=click.File(),
    help="Configuration to apply.",
    required=True,
)
@click.pass_context
@handle_errors()
def apply_service_account(ctx: click.Context, org_id: ResourceId, file) -> None:
    """
    Create a Service Account client.
    """
    data = validate_yaml(file, "validation-schemas/service-account-schema.yaml")["data"]

    account_mgmt = create_account_mgmt_api(ctx)
    try:
        # noinspection PyUnresolvedReferences
        response = account_mgmt.service_accounts.create(
            org_id.base58,
            body={
                "data": {
                    "attributes": {
                        "name": data["name"],
                        "annotations": data.pop("annotations", {}),
                        "vaults": data.get("vaults", []),
                        "scopes": data["scopes"],
                        "access_token_lifespan": data.get("accessTokenLifespan", None),
                    }
                }
            },
        )
    except ClientError as cause:
        raise ServiceClientCreationError(cause)

    attributes = response.body["data"]["attributes"]

    data["clientId"] = attributes["client_id"]
    data["clientSecret"] = attributes["client_secret"]

    # NOTE: Annotations are excluded from the output as they are undesirably camelized
    # (e.g., "vgs.io/vault-id" becomes "vgs.io/vaultId")

    click.echo(
        dump_camelized_yaml(
            {
                "apiVersion": "1.0.0",
                "kind": "ServiceAccount",
                "data": data,
            }
        )
    )


@apply.command("vault")
@click.option(
    "-O",
    "--organization",
    "org_id",
    type=ResourceIdParamType(prefix="AC"),
    help="ID of the organization to associate the vault with.",
)
@click.option(
    "--file",
    "-f",
    type=click.File(),
    help="Configuration to apply.",
    required=True,
)
@click.pass_context
@handle_errors()
def apply_vault(ctx: click.Context, org_id: Optional[ResourceId], file) -> None:
    """
    Create a new VGS vault.
    """
    data = validate_yaml(file, "validation-schemas/vault-schema.yaml")["data"]

    # kubectl behavior
    if "organizationId" in data:
        if org_id and org_id.base58 != data["organizationId"]:
            raise VgsCliError(
                f"Ambiguous organization ID. "
                f"Run the command with '--organization={data['organizationId']}' to resolve."
            )
    else:
        if not org_id:
            raise VgsCliError(
                "Missing organization ID. Pass the '--organization' option to resolve."
            )

        data["organizationId"] = org_id.base58

    account_mgmt = create_account_mgmt_api(ctx)

    # noinspection PyUnresolvedReferences
    response = account_mgmt.vaults.create_or_update(
        body={
            "data": {
                "attributes": {
                    "name": data["name"],
                    "environment": data["environment"],
                },
                "type": "vaults",
                "relationships": {
                    "organization": {
                        "data": {"type": "organizations", "id": data["organizationId"]}
                    }
                },
            }
        }
    )

    attributes = response.body["data"]["attributes"]

    data["id"] = attributes["identifier"]
    data["credentials"] = {
        "username": attributes["credentials"]["key"],
        "password": attributes["credentials"]["secret"],
    }

    vault_mgmt = create_vault_mgmt_api(
        ctx, response.body["data"]["links"]["vault_management_api"]
    )

    while True:
        # noinspection PyUnresolvedReferences
        response = vault_mgmt.vaults.retrieve(
            data["id"], headers={"VGS-Tenant": data["id"]}
        )
        if response.body["data"]["attributes"]["state"] == "PROVISIONED":
            break
        time.sleep(2)

    click.echo(
        dump_camelized_yaml(
            {
                "apiVersion": "1.0.0",
                "kind": "Vault",
                "data": data,
            }
        )
    )


def sync_http_route(payload, ctx, vault_id):
    handshake(ctx, ctx.obj.env)

    vault_management_api = create_vaults_api(
        ctx, vault_id, ctx.obj.env, token_util.get_access_token()
    )
    route_id = payload["spec"]["id"]
    try:
        # api expects it to be wrapped in data attribute
        response = vault_management_api.routes.update(
            route_id, body={"data": payload["spec"]}
        )
    except exceptions.ClientError as e:
        error_msg = "\n".join([error["detail"] for error in e.response.body["errors"]])
        raise RouteNotValidError(error_msg)
    if ctx.obj.debug:
        click.echo(f"Received raw response {response}")
    logger.debug(response)
    # TODO: this flilth can be removed after the normalize_one function is exposed.
    payload = normalize([response.body["data"]])[0]
    if ctx.obj.debug:
        click.echo(f"Normalized body {payload}")
    payload = wrap_in_http_envelope(payload)
    if ctx.obj.debug:
        click.echo(f"Wrapped body {payload}")
    click.echo(f"Route {route_id} processed")
    return payload


def wrap_in_http_envelope(payload):
    # TODO: this either needs to come from the API or we should add support for versioning in the client (yuk)
    envelope = {
        "apiVersion": "vault.vgs.io/v1",
        "kind": "HttpRoute",
        "metadata": {"name": payload["id"]},
        "spec": payload,
    }
    return envelope


def sync_mft_route(payload, ctx, vault_id):
    print("Sync MFT Route")
    print(payload, ctx, vault_id)


def no_op(*_):
    print("No Op")


HANDLERS = {
    ("vault.vgs.io/v1", "HttpRoute"): sync_http_route,
    ("mft.vgs.io/v1beta", "MftRoute"): sync_mft_route,
}


@apply.command("vault-resources")
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.option(
    "--file",
    "-f",
    type=click.File(),
    help="Configuration to apply.",
    required=True,
)
@click.option("--dry-run", default=False)
@click.pass_context
@handle_errors()
def all_vault_resources(
    ctx: click.Context, vault: Optional[ResourceId], file, dry_run
) -> None:
    """
    Apply all vault resources (routes, preferences, certificates) to a single vault.
    """
    parsed_resources = validate_multi_yaml(
        file, "validation-schemas/vault-resources.yaml"
    )
    for resource in parsed_resources:
        if dry_run:
            print(
                f"Pretending to send {resource['apiVersion']} {resource['kind']} {resource['metadata']['name']} to server"
            )
        else:
            # for each resource find handler.
            logger.info(
                f"Processing {resource['apiVersion']} {resource['kind']} {resource['metadata']['name']} to server"
            )
            response_payload = HANDLERS.get((resource["apiVersion"], resource["kind"]), no_op)(
                resource, ctx, vault
            )
            if response_payload:
                print(dump_yaml(response_payload))


@apply.command("routes")
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.option(
    "--filename",
    "-f",
    help="Filename for the input data",
    type=click.File("r"),
    required=True,
)
@click.pass_context
@handle_errors()
def apply_routes(ctx, vault, filename):
    """
    Create or update VGS routes.
    """
    handshake(ctx, ctx.obj.env)

    route_data = filename.read()
    vault_management_api = create_vaults_api(
        ctx, vault, ctx.obj.env, token_util.get_access_token()
    )
    sync_all_routes(
        vault_management_api,
        route_data,
        lambda route_id: click.echo(f"Route {route_id} processed"),
    )
    click.echo(f"Routes updated successfully for vault {vault}")
