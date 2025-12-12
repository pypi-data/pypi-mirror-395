import click
from tai_keycloak import User, kc

@click.group()
def user():
    "Grupo de comandos para gestionar usuarios en Keycloak."

@user.command()
def list():
    """List all users."""
    users = kc.admin.user.list()
    if users.success:
        for user in users.data:
            click.echo(f"{user}")
    else:
        click.echo(f"Error listing users: {users.error}")

@user.command()
def create():
    """Create a new user."""
    username = click.prompt("Username")
    email = click.prompt("Email")
    first_name = click.prompt("First name")
    last_name = click.prompt("Last name")
    password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    result = kc.admin.user.create(user, password=password)
    if result.success:
        click.echo(f"User created: {result.data}")
    else:
        click.echo(f"Error creating user: {result.error}")

@user.command()
@click.argument('username')
def delete(username: str):
    """Delete a user by ID."""
    result = kc.admin.user.delete(username)
    if result.success:
        click.echo(f"User deleted: {username}")
    else:
        click.echo(f"Error deleting user: {result.error}")
