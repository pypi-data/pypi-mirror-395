"""
Servicio principal para interactuar con Keycloak (Administración)
"""
from __future__ import annotations
from typing import Optional
from jwcrypto.jwk import JWK

from keycloak import KeycloakOpenID

from .config import (
    KeycloakConfig
)

from ..token import (
    TokenDAO
)

class KeycloakAppClient:
    """
    Cliente OIDC para operaciones human-like en Keycloak.
    """

    REALM_NAME = 'main'
    _instance: Optional[KeycloakAppClient] = None

    def __new__(cls, config: Optional[KeycloakConfig] = None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: Optional[KeycloakConfig] = None):
        if not self._initialized:
            self.config = config or KeycloakConfig()
            self._service: Optional[KeycloakOpenID] = None
            self._initialized = True

    def get_public_key(self) -> JWK:
        """Obtiene la clave pública del realm para validar tokens"""
        public_key_pem = self.service.public_key()
        public_key_pem = f"-----BEGIN PUBLIC KEY-----\n{public_key_pem}\n-----END PUBLIC KEY-----"
        self._public_key = JWK.from_pem(public_key_pem.encode("utf-8"))
    
    @property
    def public_key(self) -> JWK:
        return self._public_key
    
    @property
    def service(self) -> KeycloakOpenID:
        """Instancia autenticada de KeycloakOpenID"""
        if not self._service:
            self._service = KeycloakOpenID(
                server_url=self.config.url,
                realm_name=self.REALM_NAME,
                client_id='app',
                verify=self.config.verify_ssl
            )
        return self._service
    
    @property
    def token(self) -> TokenDAO:
        """DAO para gestión de tokens"""
        token = TokenDAO(self.service)
        return token
