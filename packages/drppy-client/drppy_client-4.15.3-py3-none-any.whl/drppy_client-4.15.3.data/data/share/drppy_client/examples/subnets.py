import json
import urllib3

import click

import drppy_client
from drppy_client.api_client import ApiClient
from drppy_client.api.subnets_api import SubnetsApi

from common import json_serialize

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@click.group()
@click.pass_context
def subnets_cli(ctx):
    """Subnets Specific Commands."""
    pass


@subnets_cli.command()
@click.pass_context
def list(ctx):
    """List All Subnets"""
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    subnets = SubnetsApi(client)
    subnet_list = subnets.list_subnets()
    click.echo(json.dumps(subnet_list, default=json_serialize))


@subnets_cli.command()
@click.argument('identifier', required=False)
@click.pass_context
def show(ctx, identifier):
    """Show a specific subnet given its name"""
    if not identifier:
        raise click.UsageError('You must provide the subnet name.')
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    subnets = SubnetsApi(client)
    try:
        subnet = subnets.get_subnet(identifier)
        click.echo(
            json.dumps(
                subnet.to_dict(),
                indent=4,
                default=json_serialize
            )
        )
    except drppy_client.rest.ApiException as e:
        if e.status == 404:
            click.echo(f"Failed to locate subnet: {identifier}")


@subnets_cli.command()
@click.argument('identifier', required=False)
@click.pass_context
def destroy(ctx, identifier):
    """Destroy a given subnet"""
    if not identifier:
        raise click.UsageError('You must provide the subnet name.')
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    subnets = SubnetsApi(client)
    try:
        subnet = subnets.delete_subnet(identifier)
        click.echo(
            json.dumps(
                subnet.to_dict(),
                indent=4,
                default=json_serialize
            )
        )
    except drppy_client.rest.ApiException as e:
        if e.status == 404:
            click.echo(f"Failed to locate subnet: {identifier}")


@subnets_cli.command()
@click.option("--payload", required=False,
              help="JSON payload containing the subnet to create.")
@click.argument('extra_args', nargs=-1, required=False)
@click.pass_context
def create(ctx, payload, extra_args):
    """Create a subnet using the passed in JSON"""
    if extra_args:
        click.echo("Try adding --payload with a json object.")
        click.echo(ctx.get_help())
        ctx.exit()
    try:
        payload = json.loads(payload)
    except json.JSONDecodeError:
        raise click.BadParameter("Payload must be valid JSON")

    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    subnets = SubnetsApi(client)
    subnet = subnets.create_subnet(payload)
    click.echo(
        json.dumps(
            subnet.to_dict(),
            indent=4,
            default=json_serialize
        )
    )
