import click
from click_plugins import with_plugins
from jinja2 import Environment, PackageLoader, StrictUndefined, UndefinedError
from vgscli.cli_utils import iter_entry_points
from vgscli.cli import create_account_mgmt_api, create_vault_mgmt_api
from vgscli.cli.types import Variable, VariableParamType
from vgscli.cli_utils import dump_camelized_yaml, read_file
from vgscli.errors import handle_errors


@with_plugins(iter_entry_points("vgs.generate.plugins"))
@click.group("generate")
def generate() -> None:
    """
    Output a VGS resource template. Edited templates can be applied with a
    corresponding command.
    """
    pass


@generate.command("vault")
@handle_errors()
def generate_vault() -> None:
    """
    Output a vault template.
    """
    click.echo(read_file("resource-templates/vault-template.yaml"), nl=False)


@generate.command("access-credentials")
@click.option("--vault", "-V", help="Vault ID", required=True)
@click.pass_context
@handle_errors()
def generate_access_credentials(ctx, vault):
    """
    Generate a VGS access-credential
    """
    account_mgmt = create_account_mgmt_api(ctx)

    response = account_mgmt.vaults.get_by_id(vault)

    vault_mgmt = create_vault_mgmt_api(
        ctx, response.body["data"][0]["links"]["vault_management_api"]
    )

    response = vault_mgmt.credentials.create(headers={"VGS-Tenant": vault})

    click.echo(
        dump_camelized_yaml(
            {
                "apiVersion": "1.0.0",
                "kind": "AccessCredentials",
                "data": response.body["data"],
            }
        )
    )


@generate.command("http-route")
@handle_errors()
def generate_route():
    """
    Generate a VGS HTTP Route
    """
    click.echo(read_file("resource-templates/http-route-template.yaml"), nl=False)


@generate.command("mft-route")
@handle_errors()
def generate_route():
    """
    Generate a VGS MFT Route
    """
    click.echo(read_file("resource-templates/mft-route-template.yaml"), nl=False)


@generate.command("service-account")
@click.option(
    "--template",
    "-t",
    type=click.Choice(
        ["vgs-cli", "calm", "checkout", "sub-account-checkout", "payments-admin"]
    ),
    help="Predefined service account template configuration",
    required=True,
)
@click.option(
    "--var",
    "variables",
    type=VariableParamType(),
    multiple=True,
    help="Template variables.",
)
@click.option(
    "--vault",
    "vaults",
    type=click.STRING,
    multiple=True,
    help="Service Account accessible vaults",
)
@click.pass_context
@handle_errors()
def generate_service_account(ctx, template, variables, vaults):
    """
    Output a Service Account template.
    """
    environment = Environment(
        loader=PackageLoader(
            package_name="vgscli", package_path="resource-templates/service-account"
        ),
        undefined=StrictUndefined,
    )

    def cli_warn(msg):
        click.echo(click.style("Warning!", fg="yellow") + " " + msg, err=True)

    def cli_fail(msg):
        click.echo(click.style("Error!", fg="red") + " " + msg, err=True)
        ctx.exit(1)

    environment.globals["cli_warn"] = cli_warn
    environment.globals["cli_fail"] = cli_fail

    variables = variables + (Variable("vaults", vaults),)
    try:
        template = environment.get_template(f"{template}.yaml")
        click.echo(template.render(**{var.name: var.value for var in variables}))
    except UndefinedError as error:
        click.echo(
            click.style("Error!", fg="red") + f" Could not render service "
            f"account template: {error}. "
            f"Please use '--var variable=value' to pass required variable."
        )
        ctx.exit(1)
