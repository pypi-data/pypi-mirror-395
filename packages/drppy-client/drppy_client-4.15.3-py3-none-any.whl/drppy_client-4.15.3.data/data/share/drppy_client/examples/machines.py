import json
import urllib3

import click

import drppy_client
from drppy_client.api_client import ApiClient
from drppy_client.api.machines_api import MachinesApi

from common import json_serialize

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _validate_machine(identifier):
    """Make sure the proper options are being passed in to function"""
    if not identifier:
        raise click.UsageError(
            'You must provide either the machine name or UUID.'
        )


@click.group()
@click.pass_context
def machines_cli(ctx):
    """Machine Specific Commands."""
    pass


@machines_cli.command()
@click.argument('params', nargs=-1)
@click.pass_context
def list(ctx, params=None):
    """List All Machines with optional filters"""
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    machines = MachinesApi(client)
    kwargs = {}
    if params:
        for param in params:
            if '=' not in param:
                raise click.BadParameter(
                    "Parameters must be in key=value format."
                )
            key, value = param.split('=', 1)
            key = key.to_lower()
            kwargs[key] = value
    machine_list = machines.list_machines(**kwargs)
    click.echo(json.dumps(machine_list, default=json_serialize))


@machines_cli.command()
@click.argument('identifier', required=False)
@click.pass_context
def show(ctx, identifier):
    """Show a machine by its name or its uuid.
    If using name use: Name:machineName"""
    _validate_machine(identifier)
    name = identifier
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    machines = MachinesApi(client)
    try:
        machine = machines.get_machine(name)
        click.echo(json.dumps(machine.to_dict(), default=json_serialize))
    except drppy_client.rest.ApiException as e:
        if e.status == 404:
            click.echo(f"Failed to locate machine: {name}")


@machines_cli.command()
@click.option("--payload",
              help="JSON Payload to pass to API with Machine info")
@click.pass_context
def create(ctx, payload):
    """Create a machine using the passed in json"""
    if not payload:
        click.echo(ctx.get_help())
        ctx.exit()
    try:
        payload = json.loads(payload)
    except json.JSONDecodeError:
        raise click.BadParameter("Payload must be valid JSON")
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    machines = MachinesApi(client)
    machine = machines.create_machine(payload)
    click.echo(json.dumps(machine.to_dict(), default=json_serialize))


@machines_cli.command()
@click.argument('identifier', required=False)
@click.pass_context
def destroy(ctx, identifier):
    """Delete a machine given its UUID or Name"""
    _validate_machine(identifier)
    name = identifier
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    machines = MachinesApi(client)
    try:
        click.echo(json.dumps(
            machines.delete_machine(name).to_dict(),
            default=json_serialize,
            indent=4)
        )
    except drppy_client.rest.ApiException as e:
        if e.status == 404:
            click.echo(f"Failed to locate machine: {name}")


@machines_cli.command()
@click.argument('identifier', required=False)
@click.pass_context
def params(ctx, identifier):
    """Get the params from a machine using name or uuid"""
    _validate_machine(identifier)
    name = identifier
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    machines = MachinesApi(client)
    try:
        mparams = machines.get_machine_params(name, decode='true')
        click.echo(json.dumps(mparams, indent=4, default=json_serialize))
    except drppy_client.rest.ApiException as e:
        if e.status == 404:
            click.echo(f"Failed to locate machine: {name}")


@machines_cli.command()
@click.argument('identifier', required=False)
@click.argument('param_name', required=False)
@click.option("--payload",
              help="JSON Payload to pass to API with Machine info")
@click.pass_context
def set_param(ctx, identifier, param_name, payload):
    """Set the value of a given param on the given machine"""
    _validate_machine(identifier)
    if not param_name:
        raise click.UsageError('You must provide param name')
    name = identifier
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    machines = MachinesApi(client)
    # This uses a monkey patched call. To see how it really works
    # see the custom_overrides.py file custom_post_machine_param()
    foo = machines.post_machine_param(machines, payload, name, param_name)
    click.echo(json.dumps(foo, default=json_serialize))


@machines_cli.command()
@click.argument('identifier', required=False)
@click.argument('param_name', required=False)
@click.pass_context
def get_param(ctx, identifier, param_name):
    """Get a single param from a machine"""
    _validate_machine(identifier)
    if not param_name:
        raise click.UsageError('You must provide param name')
    name = identifier
    config = ctx.obj['config']
    client = ApiClient(config.api_config)
    machines = MachinesApi(client)
    click.echo(
        json.dumps(
            machines.get_machine_param(name, param_name, decode='true'),
            default=json_serialize
        )
    )
