import json
import urllib3

import click

import drppy_client
from drppy_client.api_client import ApiClient
from drppy_client.api.contents_api import ContentsApi

from common import json_serialize

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@click.group()
@click.pass_context
def contents_cli(ctx):
    """Contents Specific Commands."""
    pass


@contents_cli.command()
@click.pass_context
def list(ctx):
    """List all contents"""
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    contents = ContentsApi(client)
    contents_list = contents.list_contents()
    click.echo(json.dumps(contents_list, default=json_serialize))


@contents_cli.command()
@click.argument('identifier', required=False)
@click.option("--aggregate", is_flag=True,
              help="Should return the aggregated view.")
@click.pass_context
def show(ctx, identifier, aggregate):
    """Show a specific content given its name"""
    if not identifier:
        raise click.UsageError('You must provide the content name.')
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    contents = ContentsApi(client)
    content = contents.get_content(identifier)
    click.echo(
        json.dumps(
            content.to_dict(),
            indent=4,
            default=json_serialize
        )
    )


@contents_cli.command()
@click.argument('identifier', required=False)
@click.pass_context
def destroy(ctx, identifier):
    """Destroy a given content based on its name"""
    if not identifier:
        raise click.UsageError('You must provide the content name')
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    contents = ContentsApi(client)
    try:
        content = contents.delete_content(identifier)
        click.echo(
            json.dumps(
                content.to_dict(),
                indent=4,
                default=json_serialize
            )
        )
    except drppy_client.rest.ApiException as e:
        if e.status == 404:
            click.echo(f"Failed to locate content: {identifier}")


@contents_cli.command()
@click.option("--payload", required=False,
              help="JSON payload containing the content to create.")
@click.argument('extra_args', nargs=-1, required=False)
@click.pass_context
def create(ctx, payload, extra_args):
    """Create a content using the passed in JSON"""
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
    contents = ContentsApi(client)
    content = contents.create_content(body=payload)
    click.echo(
        json.dumps(
            content.to_dict(),
            indent=4,
            default=json_serialize
        )
    )
