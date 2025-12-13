import click

from vgs.sdk.account_mgmt import AccountMgmtAPI
from vgs.sdk.vault_mgmt import VaultMgmtAPI
from vgscli.auth import handshake, token_util


def create_account_mgmt_api(ctx: click.Context) -> AccountMgmtAPI:
    environment = ctx.obj.env

    handshake(ctx, environment)
    access_token = token_util.get_access_token()

    return AccountMgmtAPI(access_token, environment)


def create_vault_mgmt_api(ctx: click.Context, root_url: str) -> VaultMgmtAPI:
    environment = ctx.obj.env

    handshake(ctx, environment)
    access_token = token_util.get_access_token()

    return VaultMgmtAPI(access_token, root_url)
