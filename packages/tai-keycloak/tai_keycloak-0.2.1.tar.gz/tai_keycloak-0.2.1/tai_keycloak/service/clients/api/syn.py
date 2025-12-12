"""
Servicio OIDC para autenticación y operaciones de usuario final
"""
from __future__ import annotations
from typing import Optional
from jwcrypto.jwk import JWK

from keycloak import KeycloakAdmin, KeycloakOpenID

from ..config import (
    KeycloakConfig
)

from ...daos import (
    UserDAO,
    GroupDAO
)

from ...token import TokenDAO


class KeycloakSyncAPIClient:
    """
    Cliente OIDC para operaciones service-account en Keycloak.
    """

    REALM_NAME = 'main'
    _instance: Optional[KeycloakSyncAPIClient] = None

    def __new__(cls, config: Optional[KeycloakConfig] = None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: Optional[KeycloakConfig] = None):
        if not self._initialized:
            self.config = config or KeycloakConfig()
            self._admin_service: Optional[KeycloakAdmin] = None
            self._openid_service: Optional[KeycloakOpenID] = None
            self._public_key: Optional[JWK] = None
            self._user_dao: Optional[UserDAO] = None
            self._token_dao: Optional[TokenDAO] = None
            self._group_dao: Optional[GroupDAO] = None
            self._initialized = True

            if not self.config.api_client_secret:
                raise ValueError("El secreto del cliente API no está configurado.")
            else:
                self.client_secret = self.config.api_client_secret
    
    def get_public_key(self) -> JWK:
        """Obtiene la clave pública del realm para validar tokens"""
        public_key_pem = self.openid_service.public_key()
        public_key_pem = f"-----BEGIN PUBLIC KEY-----\n{public_key_pem}\n-----END PUBLIC KEY-----"
        self._public_key = JWK.from_pem(public_key_pem.encode("utf-8"))
    
    @property
    def public_key(self) -> JWK:
        return self._public_key
    
    @property
    def admin_service(self) -> KeycloakAdmin:
        """Instancia autenticada de KeycloakAdmin con renovación automática de token"""
        if not self._admin_service:    
            # Crear KeycloakAdmin
            self._admin_service = KeycloakAdmin(
                server_url=self.config.url,
                realm_name=self.REALM_NAME,
                client_id='api',
                client_secret_key=self.client_secret,
                verify=self.config.verify_ssl
            )
        return self._admin_service
        
    @property
    def openid_service(self) -> KeycloakOpenID:
        """Instancia autenticada de KeycloakOpenID"""
        if not self._openid_service:
            # Crear KeycloakOpenID
            self._openid_service = KeycloakOpenID(
                server_url=self.config.url,
                realm_name=self.REALM_NAME,
                client_id='api',
                client_secret_key=self.client_secret,
                verify=self.config.verify_ssl
            )

        return self._openid_service
    
    @property
    def token(self) -> TokenDAO:
        """DAO para gestión de tokens"""
        if not self._token_dao:
            self._token_dao = TokenDAO(self.openid_service)
        return self._token_dao

    @property
    def user(self) -> UserDAO:
        """DAO para gestión de usuarios"""
        if not self._user_dao:
            self._user_dao = UserDAO(self.admin_service)
        return self._user_dao

    @property
    def group(self) -> GroupDAO:
        """DAO para gestión de grupos"""
        if not self._group_dao:
            self._group_dao = GroupDAO(self.admin_service)
        return self._group_dao

