"""tai-keycloak package"""

from .service import (
    KeycloakClient,
    KeycloakAsyncAPIClient,
    KeycloakSyncAPIClient,
    User,
    RLSAttribute,
    Role,
    Group,
    Client,
    Realm,
    UsersProfile,
    UsersProfileAttribute,
    ClientMapper,
    ClientMapperConfig,
    AccessToken,
    UserInfo,
    faked_token
)

__all__ = [
    "KeycloakClient",
    "KeycloakAsyncAPIClient",
    "KeycloakSyncAPIClient",
    "User",
    "RLSAttribute",
    "Role",
    "Group",
    "Client",
    "Realm",
    "UsersProfile",
    "UsersProfileAttribute",
    "ClientMapper",
    "ClientMapperConfig",
    "AccessToken",
    "UserInfo",
    "faked_token"
]

kc = KeycloakClient()