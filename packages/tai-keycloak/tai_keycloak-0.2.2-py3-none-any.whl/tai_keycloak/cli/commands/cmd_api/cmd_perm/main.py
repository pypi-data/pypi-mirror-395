import click
from tai_keycloak import Role, kc


@click.group()
def perm():
    "Grupo de comandos para gestionar permisos (roles) en Keycloak."

@perm.command()
def list_realm():
    """List all realm roles."""
    roles = kc.admin.realm_role.list()
    if roles.success:
        for role in roles.data:
            click.echo(f"{role}")
    else:
        click.echo(f"Error listing roles: {roles.error}")

@perm.command()
@click.argument('name')
@click.option('--description', help='Role description')
@click.option('--composite', is_flag=True, help='Make role composite')
def create_for_realm(name: str, description: str, composite: bool):
    """Create a new realm permission."""
    role = Role(name=name, description=description, composite=composite)
    result = kc.admin.realm_role.create(role)
    if result.success:
        click.echo(f"Role created: {result.data}")
    else:
        click.echo(f"Error creating role: {result.error}")

@perm.command()
@click.argument('name')
@click.option('--description', help='Role description')
def create_for_api(name: str, description: str):
    """Create a new api permission."""
    role = Role(name=name, description=description, client_role=True)
    result = kc.admin.api_role.create(role)
    if result.success:
        click.echo(f"API role created: {result.data}")
    else:
        click.echo(f"Error creating API role: {result.error}")

@perm.command()
@click.argument('name')
@click.option('--description', help='Role description')
def create_for_app(name: str, description: str):
    """Create a new application permission."""
    role = Role(name=name, description=description, client_role=True)
    result = kc.admin.app_role.create(role)
    if result.success:
        click.echo(f"Application role created: {result.data}")
    else:
        click.echo(f"Error creating application role: {result.error}")