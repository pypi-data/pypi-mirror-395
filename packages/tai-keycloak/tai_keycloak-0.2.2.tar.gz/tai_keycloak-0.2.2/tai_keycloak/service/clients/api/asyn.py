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
    AsyncUserDAO,
    AsyncGroupDAO
)

from ...token import AsyncTokenDAO


class KeycloakAsyncAPIClient:
    """
    Cliente OIDC para operaciones service-account en Keycloak.
    """

    REALM_NAME = 'main'
    _instance: Optional[KeycloakAsyncAPIClient] = None

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
            self._user_dao: Optional[AsyncUserDAO] = None
            self._token_dao: Optional[AsyncTokenDAO] = None
            self._group_dao: Optional[AsyncGroupDAO] = None
            self._initialized = True

            if not self.config.api_client_secret:
                raise ValueError("El secreto del cliente API no está configurado.")
            else:
                self.client_secret = self.config.api_client_secret

    async def get_public_key(self) -> JWK:
        """Obtiene la clave pública del realm para validar tokens"""
        public_key_pem = await self.openid_service.a_public_key()
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
    def token(self) -> AsyncTokenDAO:
        """DAO para gestión de tokens"""
        if not self._token_dao:
            self._token_dao = AsyncTokenDAO(self.openid_service)
        return self._token_dao

    @property
    def user(self) -> AsyncUserDAO:
        """DAO para gestión de usuarios"""
        if not self._user_dao:
            self._user_dao = AsyncUserDAO(self.admin_service)
        return self._user_dao

    @property
    def group(self) -> AsyncGroupDAO:
        """DAO para gestión de grupos"""
        if not self._group_dao:
            self._group_dao = AsyncGroupDAO(self.admin_service)
        return self._group_dao

