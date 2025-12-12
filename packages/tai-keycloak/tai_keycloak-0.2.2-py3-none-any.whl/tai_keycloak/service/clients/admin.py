"""
Servicio principal para interactuar con Keycloak (Administración)
"""
from __future__ import annotations
from typing import Dict, Optional, Any

from keycloak import KeycloakAdmin

from .config import (
    KeycloakConfig
)

from ..dtos import (
    OperationResult, KeycloakSDKException
)

from ..daos import (
    UserDAO, GroupDAO, ClientDAO, RealmDAO,
    ClientRoleDAO, RealmRoleDAO, UsersProfileDAO
)


class KeycloakAdminClient:
    """
    Servicio principal para gestionar instancias de Keycloak (Administración).
    
    Proporciona una interfaz elegante y robusta para:
    - Gestión de realms
    - Gestión de usuarios
    - Gestión de grupos y roles
    - Gestión de clientes
    """

    REALM_NAME = 'main'
    _instance: Optional[KeycloakAdminClient] = None

    def __new__(cls, config: Optional[KeycloakConfig] = None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: Optional[KeycloakConfig] = None):
        if not self._initialized:
            self.config = config or KeycloakConfig()
            self._service: Optional[KeycloakAdmin] = None
            self._user_dao: Optional[UserDAO] = None
            self._group_dao: Optional[GroupDAO] = None
            self._client_dao: Optional[ClientDAO] = None
            self._app_client_dao: Optional[ClientDAO] = None
            self._api_client_dao: Optional[ClientDAO] = None
            self._realm_dao: Optional[RealmDAO] = None
            self._app_role_dao: Optional[ClientRoleDAO] = None
            self._api_role_dao: Optional[ClientRoleDAO] = None
            self._realm_role_dao: Optional[RealmRoleDAO] = None
            self._users_profile_dao: Optional[UsersProfileDAO] = None
            self._initialized = True

    @property
    def service(self) -> KeycloakAdmin:
        """Instancia autenticada de KeycloakAdmin"""
        if not self._service:
            self._service = KeycloakAdmin(
                server_url=self.config.url,
                username=self.config.username,
                password=self.config.password,
                verify=self.config.verify_ssl
            )
            self._service.connection.get_token()
            self._service.change_current_realm(self.REALM_NAME)
        return self._service
    
    @property
    def user(self) -> UserDAO:
        """DAO para gestión de usuarios"""
        if not self._user_dao:
            self._user_dao = UserDAO(self.service)
        return self._user_dao

    @property
    def group(self) -> GroupDAO:
        """DAO para gestión de grupos"""
        if not self._group_dao:
            self._group_dao = GroupDAO(self.service)
        return self._group_dao

    @property
    def client(self) -> ClientDAO:
        """DAO para gestión de clientes"""
        if not self._client_dao:
            self._client_dao = ClientDAO(self.service)
        return self._client_dao

    @property
    def app_client(self) -> ClientDAO:
        """DAO para gestión de clientes"""
        if not self._app_client_dao:
            self._app_client_dao = ClientDAO(self.service, 'app')
        return self._app_client_dao

    @property
    def api_client(self) -> ClientDAO:
        """DAO para gestión de clientes"""
        if not self._api_client_dao:
            self._api_client_dao = ClientDAO(self.service, 'api')
        return self._api_client_dao

    @property
    def realm(self) -> RealmDAO:
        """DAO para gestión de realms"""
        if not self._realm_dao:
            self._realm_dao = RealmDAO(self.service)
        return self._realm_dao

    @property
    def api_role(self) -> ClientRoleDAO:
        """DAO para gestión de roles de cliente"""
        if not self._api_role_dao:
            self._api_role_dao = ClientRoleDAO(self.service, 'api')
        return self._api_role_dao
    
    @property
    def app_role(self) -> ClientRoleDAO:
        """DAO para gestión de roles de cliente"""
        if not self._app_role_dao:
            self._app_role_dao = ClientRoleDAO(self.service, 'app')
        return self._app_role_dao

    @property
    def realm_role(self) -> RealmRoleDAO:
        """DAO para gestión de roles de realm"""
        if not self._realm_role_dao:
            self._realm_role_dao = RealmRoleDAO(self.service)
        return self._realm_role_dao
    
    @property
    def profile(self) -> UsersProfileDAO:
        """DAO para gestión de perfiles de usuario"""
        if not self._users_profile_dao:
            self._users_profile_dao = UsersProfileDAO(self.service)
        return self._users_profile_dao

    # === INFORMACIÓN DEL SERVIDOR ===
    
    def get_server_info(self, with_logs: bool=True) -> OperationResult[Dict[str, Any]]:
        """Obtiene información detallada del servidor Keycloak (admin)"""
        try:
            server_info = self.service.get_server_info()
            return OperationResult(
                success=True,
                message="Información del servidor obtenida",
                data=server_info,
                with_logs=with_logs
            )
        except Exception as e:
            return KeycloakSDKException(e).handle("KeycloakAdminClient.get_server_info", "/admin/serverinfo", with_logs=with_logs)
    
    def check_health(self, with_logs: bool=True) -> OperationResult[Dict[str, Any]]:
        """Verifica el estado de salud del servidor Keycloak (admin)"""
        try:
            health_info = self.service.connection.raw_get(path='/health/ready')

            if health_info.status_code == 200:
                return OperationResult(
                    success=True,
                    message="Estado de salud del servidor obtenido",
                    data=health_info.json(),
                    with_logs=with_logs
                )
            else:
                return OperationResult(
                    success=False,
                    message="El servidor no está saludable",
                    data=health_info.json(),
                    with_logs=with_logs
                )
        except Exception as e:
            return KeycloakSDKException(e).handle("KeycloakAdminClient.check_health", "Error verificando estado de salud del servidor", with_logs=with_logs)

