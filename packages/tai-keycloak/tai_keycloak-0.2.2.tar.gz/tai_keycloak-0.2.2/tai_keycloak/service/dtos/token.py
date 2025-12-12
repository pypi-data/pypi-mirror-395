from __future__ import annotations
from typing import Optional, List, Dict, Any
from pydantic import Field

from .base import PrettyModel

class Token(PrettyModel):
    """Información de token OIDC"""
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str = Field(None)
    token_type: str
    id_token: Optional[str] = None
    session_state: Optional[str] = None
    scope: Optional[str] = None

class AccessToken(PrettyModel):
    """Payload del access token OIDC"""
    exp: int
    iat: int
    jti: str
    iss: str
    aud: str | List[str]
    typ: str
    azp: str
    sub: Optional[str] = Field(None)
    sid: Optional[str] = Field(None)
    session_state: Optional[str] = Field(None)
    acr: Optional[str] = Field(None)
    realm_access: Optional[Dict[str, List[str]]] = None
    resource_access: Optional[Dict[str, Dict[str, List[str]]]] = None
    scope: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    preferred_username: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    rls: Dict[str, Dict[str, List[str | Any]]] = Field(default_factory=dict)


    @property
    def api_roles(self) -> List[str]:
        """Roles asignados al cliente 'api'"""
        if self.resource_access and 'api' in self.resource_access:
            return self.resource_access['api'].get('roles', [])
        return []
    
    @property
    def realm_roles(self) -> List[str]:
        """Roles asignados a nivel de realm"""
        if self.realm_access:
            return self.realm_access.get('roles', [])
        return []


# Token fake permisivo para testing/desarrollo
faked_token = AccessToken(
    exp=9999999999,  # Expira muy lejos en el futuro
    iat=0,
    jti="fake-jti",
    iss="fake-issuer",
    aud="fake-audience",
    sub="fake-user",
    sid="fake-user",
    typ="Bearer",
    azp="fake-client",
    session_state="fake-session",
    acr="1",
    realm_access={"roles": ["admin", "user", "superuser"]},
    resource_access={"api": {"roles": ["admin", "read", "write", "delete"]}},
    scope="openid profile email",
    email_verified=True,
    name="Fake User",
    preferred_username="fake_user",
    given_name="Fake",
    family_name="User",
    email="fake@example.com"
)


class UserInfo(PrettyModel):
    """Información de usuario desde OIDC"""
    sub: str
    preferred_username: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    groups: Optional[list] = None
    roles: Optional[list] = None

