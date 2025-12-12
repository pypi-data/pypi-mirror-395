import json
import urllib3

import click

import drppy_client
from drppy_client.api_client import ApiClient
from drppy_client.api.params_api import ParamsApi

from common import json_serialize

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@click.group()
@click.pass_context
def params_cli(ctx):
    """Parameter Specific Commands."""
    pass


@params_cli.command()
@click.pass_context
def list(ctx):
    """List All Parameters"""
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    params = ParamsApi(client)
    # Provides a list of Param objects
    params_list = params.list_params()
    click.echo(json.dumps(params_list, default=json_serialize))


@params_cli.command()
@click.argument('identifier', required=False)
@click.pass_context
def show(ctx, identifier):
    """Show a single param based on its id"""
    if not identifier:
        raise click.UsageError(
            'You must provide the param id. Ex: rs-debug-enable'
        )
    config = ctx.obj["config"]
    client = ApiClient(config.api_config)
    params = ParamsApi(client)
    try:
        param = params.get_param(identifier)
        click.echo(
            json.dumps(
                param.to_dict(),
                indent=4,
                default=json_serialize
            )
        )
    except drppy_client.rest.ApiException as e:
        if e.status == 404:
            click.echo(f"Failed to locate param: {identifier}")


@params_cli.command()
@click.option("--payload", help="JSON Payload to pass to API with Param def")
@click.pass_context
def create(ctx, payload):
    """Create a param using passed in JSON"""
    if not payload:
        click.echo("Missing JSON payload!")
        click.echo(ctx.get_help())
        ctx.exit()
    try:
        payload = json.loads(payload)
    except json.JSONDecodeError:
        raise click.BadParameter("Payload must be valid JSON")
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    params = ParamsApi(client)
    param = params.create_param(payload)
    click.echo(
        json.dumps(
            param.to_dict(),
            indent=4,
            default=json_serialize
        )
    )


@params_cli.command()
@click.argument('identifier', required=False)
@click.pass_context
def destroy(ctx, identifier):
    """Destroy a param using its id"""
    if not identifier:
        raise click.UsageError(
            'You must provide the param id. Ex: rs-debug-enable'
        )
    config = ctx.obj["config"]
    client = ApiClient(config.api_config)
    params = ParamsApi(client)
    try:
        param = params.delete_param(identifier)
        click.echo(
            json.dumps(
                param.to_dict(),
                indent=4,
                default=json_serialize
            )
        )
    except drppy_client.rest.ApiException as e:
        if e.status == 404:
            if e.body:
                msg = json.loads(e.body)
                errmsg = msg["Messages"]
                click.echo(errmsg[0])
            click.echo(f"Failed to locate param: {identifier}")
