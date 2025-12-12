from datetime import datetime, timezone
from jwcrypto import jwt
from jwcrypto.jwk import JWK
from jwcrypto.common import json_decode
from typing import Optional, Union, List
from keycloak import KeycloakOpenID
from ..dtos import Token, OperationResult, KeycloakSDKException, AccessToken


class TokenDAO:
    """Interfaz base para DAOs de tokens"""

    NAME = 'Token'

    def __init__(self, client: KeycloakOpenID):
        self.client = client

    @staticmethod
    def decode(
        token: str,
        key: Optional[JWK] = None,
        expected_audience: Optional[Union[str, List[str]]] = None,
        expected_issuer: Optional[str] = None,
    ) -> OperationResult[AccessToken]:
        """
        Decodifica y valida un token JWT de Keycloak.

        - Verifica firma si se provee la clave pública.
        - Valida 'exp', 'iss' y 'aud' según los parámetros esperados.
        - Devuelve un objeto AccessToken con los claims.
        """
        try:
            # Decodificar sin validar todavía
            full_jwt = jwt.JWT(jwt=token)
            full_jwt.leeway = 60

            # Validar firma si hay clave
            if key is not None:
                full_jwt.validate(key)

            # Parsear claims
            raw_claims = json_decode(full_jwt.claims)
            
            access_token = AccessToken(**raw_claims)

            # --- Validaciones adicionales ---

            # 1️⃣ Expiración
            now = datetime.now(timezone.utc).timestamp()
            if now > access_token.exp:
                return OperationResult(
                    success=False,
                    message="Token expirado"
                )

            # 2️⃣ Issuer
            if expected_issuer and access_token.iss != expected_issuer:
                return OperationResult(
                    success=False,
                    message=f"Issuer inválido: {access_token.iss} (esperado: {expected_issuer})"
                )

            # 3️⃣ Audiencia
            audience = access_token.aud if isinstance(access_token.aud, list) else [access_token.aud]
            if expected_audience and not any(aud in audience for aud in expected_audience):
                return OperationResult(
                    success=False,
                    message=f"Audiencia inválida: {audience} (esperado: {expected_audience})"
                )

            return OperationResult(
                success=True,
                message="Token decodificado y validado exitosamente",
                data=access_token,
            )

        except Exception as e:
            # Manejo centralizado de errores
            return KeycloakSDKException(e).handle(
                "Token.decode", "decodificación/validación de token"
            )

    def request(self, username: Optional[str] = None, password: Optional[str] = None) -> OperationResult[Token]:
        """Obtiene un token de acceso para un usuario"""
        try:
            if username is None or password is None:
                tokens_data = self.client.token(grant_type='client_credentials')
                msg = "Tokens de servicio obtenido exitosamente"
            else:
                tokens_data = self.client.token(username, password)
                msg = f"Tokens obtenido exitosamente para el usuario '{username}'"

            token = Token(**tokens_data)
            return OperationResult(
                success=True,
                message=msg,
                data=token
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get", f"token para usuario '{username}'")

    def refresh(self, refresh_token: str) -> OperationResult[Token]:
        """Refresca un token de acceso usando un refresh token"""
        try:
            tokens_data = self.client.refresh_token(refresh_token)
            token = Token(**tokens_data)
            return OperationResult(
                success=True,
                message="Token refrescado exitosamente",
                data=token
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.refresh", "refresco de token")