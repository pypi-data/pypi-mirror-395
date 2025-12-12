import click
from .cmd_client import client
from .cmd_role import role
from .cmd_perm import perm
from .cmd_user import user
from .cmd_realm import realm


@click.group()
def api():
    "Grupo de comandos para gestionar la API de Keycloak."

api.add_command(client)
api.add_command(role)
api.add_command(perm)
api.add_command(user)
api.add_command(realm)