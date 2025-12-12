import click
from tai_keycloak import Group, kc


@click.group()
def role():
    "Grupo de comandos para gestionar roles (grupos) en Keycloak."

@role.command()
def list():
    """List all roles."""
    groups = kc.admin.group.list()
    if groups.success:
        for group in groups.data:
            click.echo(f"{group}")
    else:
        click.echo(f"Error listing groups: {groups.error}")

@role.command()
@click.argument('name')
def create(name: str):
    """Create a new role."""
    group = Group(name=name)
    result = kc.admin.group.create(group)
    if result.success:
        click.echo(f"Group created: {result.data}")
    else:
        click.echo(f"Error creating group: {result.error}")