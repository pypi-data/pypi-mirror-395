import json
import urllib3

import click

import drppy_client
from drppy_client.api_client import ApiClient
from drppy_client.api.profiles_api import ProfilesApi

from common import json_serialize

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@click.group()
@click.pass_context
def profiles_cli(ctx):
    """Profiles Specific Commands."""
    pass


@profiles_cli.command()
@click.pass_context
def list(ctx):
    """List all profiles"""
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    profiles = ProfilesApi(client)
    profiles_list = profiles.list_profiles()
    click.echo(json.dumps(profiles_list, default=json_serialize))


@profiles_cli.command()
@click.argument('identifier', required=False)
@click.option("--aggregate", is_flag=True,
              help="Should return the aggregated view.")
@click.pass_context
def show(ctx, identifier, aggregate):
    """Show a specific profile given its name"""
    if not identifier:
        raise click.UsageError('You must provide the profile name.')
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    profiles = ProfilesApi(client)
    profile = profiles.get_profile(identifier)
    click.echo(
        json.dumps(
            profile.to_dict(),
            indent=4,
            default=json_serialize
        )
    )


@profiles_cli.command()
@click.argument('identifier', required=False)
@click.pass_context
def destroy(ctx, identifier):
    """Destroy a given profile based on its name"""
    if not identifier:
        raise click.UsageError('You must provide the profile name')
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    profiles = ProfilesApi(client)
    try:
        profile = profiles.delete_profile(identifier)
        click.echo(
            json.dumps(
                profile.to_dict(),
                indent=4,
                default=json_serialize
            )
        )
    except drppy_client.rest.ApiException as e:
        if e.status == 404:
            click.echo(f"Failed to locate profile: {identifier}")


@profiles_cli.command()
@click.option("--payload", required=False,
              help="JSON payload containing the profile to create.")
@click.argument('extra_args', nargs=-1, required=False)
@click.pass_context
def create(ctx, payload, extra_args):
    """Create a profile using the passed in JSON"""
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
    profiles = ProfilesApi(client)
    profile = profiles.create_profile(payload)
    click.echo(
        json.dumps(
            profile.to_dict(),
            indent=4,
            default=json_serialize
        )
    )
