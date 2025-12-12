import click
from tai_keycloak import Client, kc
from tai_keycloak.service.dtos import ClientProtocol, AccessType


@click.group()
def client():
    "Grupo de comandos para gestionar clientes en Keycloak."

@client.command()
def list():
    """List all clients."""
    clients = kc.admin.client.list()
    if clients.success:
        for client in clients.data:
            click.echo(f"{client}")
    else:
        click.echo(f"Error listing clients: {clients.error}")

@client.command()
@click.argument('client_id')
@click.option('--name', help='Client name')
@click.option('--description', help='Client description')
@click.option('--protocol', type=click.Choice(['openid-connect', 'saml']), default='openid-connect', help='Client protocol')
@click.option('--access-type', type=click.Choice(['public', 'confidential', 'bearer-only']), default='public', help='Access type')
@click.option('--enabled/--disabled', default=True, help='Enable or disable the client')
def create(client_id: str, name: str, description: str, protocol: str, access_type: str, enabled: bool):
    """Create a new client."""
    client = Client(
        client_id=client_id,
        name=name or client_id,
        description=description,
        protocol=ClientProtocol(protocol),
        access_type=AccessType(access_type.replace('-', '_')),  # Convert kebab-case to snake_case
        enabled=enabled
    )
    result = kc.admin.client.create(client)
    if result.success:
        click.echo(f"Client created: {result.data}")
    else:
        click.echo(f"Error creating client: {result.error}")

@client.command()
@click.argument('client_id')
def get_secret(client_id: str):
    """Get the secret for a confidential client."""
    try:
        secret = kc.admin.client.get_secret(client_id)
        click.echo(f"Client secret for '{client_id}': {secret.data}")
    except Exception as e:
        click.echo(f"Error getting client secret: {e}")

@client.command()
@click.argument('client_id')
def regenerate_secret(client_id: str):
    """Regenerate the secret for a confidential client."""
    try:
        new_secret = kc.admin.client.regenerate_secret(client_id)
        click.echo(f"New secret for '{client_id}': {new_secret.data}")
        click.echo("⚠️  Make sure to update your applications with the new secret!")
        
    except Exception as e:
        click.echo(f"Error regenerating client secret: {e}")