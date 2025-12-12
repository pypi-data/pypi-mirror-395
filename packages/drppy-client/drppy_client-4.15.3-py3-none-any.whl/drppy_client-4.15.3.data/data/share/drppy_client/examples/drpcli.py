import click

from common import Config

from machines import machines_cli
from params import params_cli
from subnets import subnets_cli
from profiles import profiles_cli
from content import contents_cli


@click.group()
@click.option('--endpoint', default=None, help='API host URL')
@click.option('--token', default=None, help='API token')
@click.option('--key', default=None, help='user:password  Used for basic auth')
@click.pass_context
def cli(ctx, endpoint, token, key):
    """Main entry point for the CLI."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(host=endpoint, token=token, key=key)
    pass


cli.add_command(machines_cli, name='machines')
cli.add_command(params_cli, name='params')
cli.add_command(subnets_cli, name="subnets")
cli.add_command(profiles_cli, name="profiles")
cli.add_command(contents_cli, name="contents")


if __name__ == '__main__':
    cli()
