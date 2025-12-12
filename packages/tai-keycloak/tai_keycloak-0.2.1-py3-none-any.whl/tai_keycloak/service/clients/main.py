from typing import Optional
from jwcrypto.jwk import JWK
from .admin import KeycloakAdminClient
from .app import KeycloakAppClient
from .api import KeycloakSyncAPIClient
from ..dtos import User, Role, Group, Client, Realm

from .config import (
    KeycloakConfig
)

__all__ = [
    "KeycloakAdminClient", "KeycloakAppClient", "KeycloakAPIClient",
    "KeycloakConfig", "User", "Role", "Group", "Client", "Realm"
]


class KeycloakClient:
    """
    Servicio principal para gestionar instancias de Keycloak.
    
    Proporciona una interfaz elegante y robusta para:
    - Gestión de realms
    - Gestión de usuarios
    - Gestión de grupos y roles
    - Gestión de clientes
    - Gestión de tokens
    """

    def __init__(self, config: Optional[KeycloakConfig] = None):
        self.config = config or KeycloakConfig()
        self._admin_client: Optional[KeycloakAdminClient] = None
        self._app_client: Optional[KeycloakAppClient] = None
        self._api_client: Optional[KeycloakSyncAPIClient] = None

    @property
    def admin(self) -> KeycloakAdminClient:
        """Cliente administrativo para Keycloak"""
        if not self._admin_client:
            self._admin_client = KeycloakAdminClient(self.config)
        return self._admin_client

    @property
    def app(self) -> KeycloakAppClient:
        """Cliente de aplicación para Keycloak"""
        if not self._app_client:
            self._app_client = KeycloakAppClient(self.config)
            self._app_client.get_public_key()
        return self._app_client
    
    @property
    def api(self) -> KeycloakSyncAPIClient:
        """Cliente API para Keycloak"""
        if not self._api_client:
            self._api_client = KeycloakSyncAPIClient(self.config)
            self._api_client.get_public_key()
        return self._api_client