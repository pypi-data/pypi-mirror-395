import click
from tai_keycloak import Realm, kc


@click.group()
def realm():
    "Grupo de comandos para gestionar realms en Keycloak."

@realm.command()
def list():
    """List all realms."""
    realms = kc.admin.realm.list()
    if realms.success:
        for realm in realms.data:
            click.echo(f"{realm}")
    else:
        click.echo(f"Error listing realms: {realms.error}")

@realm.command()
@click.argument('name')
@click.option('--display-name', help='Display name for the realm')
@click.option('--enabled/--disabled', default=True, help='Enable or disable the realm')
def create(name: str, display_name: str, enabled: bool):
    """Create a new realm."""
    realm = Realm(realm=name, display_name=display_name, enabled=enabled)
    result = kc.admin.realm.create(realm)
    if result.success:
        click.echo(f"Realm created: {result.data}")
    else:
        click.echo(f"Error creating realm: {result.error}")

@realm.command()
@click.argument('name')
def get(name: str):
    """Get realm information."""
    result = kc.admin.realm.get(name)
    if result.success:
        click.echo(f"Realm info: {result.data}")
    else:
        click.echo(f"Error getting realm: {result.error}")

@realm.command()
@click.argument('name')
@click.confirmation_option(prompt='Are you sure you want to delete this realm?')
def delete(name: str):
    """Delete a realm."""
    result = kc.admin.realm.delete(name)
    if result.success:
        click.echo(f"Realm deleted: {name}")
    else:
        click.echo(f"Error deleting realm: {result.error}")