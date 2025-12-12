"""
Modelos Pydantic para representar entidades de Keycloak de forma tipada y validada.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Any
from pydantic import Field, model_validator, field_serializer
from enum import Enum

from .base import PrettyModel


class ClientProtocol(str, Enum):
    """Protocolo del cliente Keycloak"""
    OPENID_CONNECT = "openid-connect"
    SAML = "saml"


class AccessType(str, Enum):
    """Tipo de acceso del cliente"""
    PUBLIC = "public"
    CONFIDENTIAL = "confidential"
    BEARER_ONLY = "bearer-only"


class Role(PrettyModel):
    """Modelo para roles de Keycloak"""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    composite: bool = False
    clientRole: bool = False
    containerId: Optional[str] = None
    attributes: Optional[Dict[str, List[str]]] = None


class Group(PrettyModel):
    """Modelo para grupos de Keycloak"""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=255)
    path: Optional[str] = None
    attributes: Optional[Dict[str, List[str]]] = None
    realmRoles: Optional[List[str]] = None
    clientRoles: Optional[Dict[str, List[str]]] = None
    subGroups: Optional[List['Group']] = None


class RLSAttribute(PrettyModel):
    table: str
    field: str
    values: str | List[str]


class User(PrettyModel):
    """Modelo para usuarios de Keycloak"""
    id: Optional[str] = None
    username: str = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None)
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    firstName: Optional[str] = Field(None)
    lastName: Optional[str] = Field(None)
    enabled: bool = True
    createdTimestamp: Optional[int] = None
    access: Optional[Dict[str, bool]] = None
    emailVerified: bool = Field(True)
    attributes: Optional[Dict[str, str | List[str]]] = Field(default_factory=dict)
    groups: Optional[List[str]] = None
    realmRoles: Optional[List[str]] = None
    clientRoles: Optional[Dict[str, List[str]]] = None
    credentials: Optional[List[Dict[str, Any]]] = None
    totp: bool = Field(False)
    disableableCredentialTypes: Optional[List[str]] = None
    notBefore: Optional[int] = None
    requiredActions: Optional[List[str]] = None


class UsersProfile(PrettyModel):
    """Modelo para perfiles de usuario de Keycloak"""
    attributes: Optional[List[UsersProfileAttribute]] = Field(default_factory=list)
    groups: Optional[List[UsersProfileGroup]] = Field(default_factory=list)


class UsersProfileGroup(PrettyModel):
    """Modelo para grupos en perfiles de usuario de Keycloak"""
    name: Optional[str] = None
    displayHeader: Optional[str] = None
    displayDescription: Optional[str] = None
    annotations: Optional[Dict[str, str]] = None


class UsersProfileAttribute(PrettyModel):
    """Modelo para atributos de usuario de Keycloak"""
    name: Optional[str] = None
    displayName: Optional[str] = None
    validations: Optional[Dict[str, Any]] = None
    annotations: Optional[Dict[str, str]] = None
    required: Optional[Dict[str, list]] = None
    permissions: Optional[Dict[str, list]] = {'edit': ['admin']}
    selector: Optional[Dict[str, list]] = None
    group: Optional[str] = None
    multivalued: bool = True


class Client(PrettyModel):
    """Modelo para clientes de Keycloak"""
    id: Optional[str] = None
    clientId: str = Field(..., serialization_alias='clientId')
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: bool = True
    alwaysDisplayInConsole: bool = Field(False)
    clientAuthenticatorType: str = Field('client-secret')
    redirectUris: List[str] = Field(default_factory=list, serialization_alias='redirectUris')
    webOrigins: List[str] = Field(default_factory=list)
    protocol: ClientProtocol = ClientProtocol.OPENID_CONNECT
    accessType: AccessType = Field(AccessType.PUBLIC, exclude=True)
    publicClient: bool = Field(True)
    bearerOnly: bool = Field(False)
    standardFlowEnabled: bool = Field(True)
    implicitFlowEnabled: bool = Field(False)
    directAccessGrantsEnabled: bool = Field(True)
    serviceAccountsEnabled: bool = Field(False)
    publicClient: bool = Field(True)
    attributes: Optional[Dict[str, Any]] = None

    def model_post_init(self, context):
        if self.accessType == AccessType.PUBLIC:
            self.publicClient = True
            self.bearerOnly = False
        elif self.accessType == AccessType.CONFIDENTIAL:
            self.publicClient = False
            self.bearerOnly = False
        elif self.accessType == AccessType.BEARER_ONLY:
            self.publicClient = False
            self.bearerOnly = True


class ClientMapper(PrettyModel):
    """Modelo para mappers de clientes de Keycloak"""
    name: str = Field(..., min_length=1, max_length=255)
    protocol: ClientProtocol = ClientProtocol.OPENID_CONNECT
    protocolMapper: str = Field("oidc-usermodel-attribute-mapper", min_length=1, max_length=255)
    config: ClientMapperConfig = Field(...)


class ClientMapperConfig(PrettyModel):
    """Modelo para configuración de mappers de clientes de Keycloak"""
    claim_name: str = Field(..., alias='claim.name')
    user_attribute: str = Field(..., alias='user.attribute')
    json_type_label: str = Field("String", alias='jsonType.label')
    id_token_claim: str = Field(True, alias='id.token.claim')
    access_token_claim: str = Field(True, alias='access.token.claim')
    lightweight_claim: str = Field(False, alias='lightweight.claim')
    userinfo_token_claim: str = Field(True, alias='userinfo.token.claim')
    introspection_token_claim: str = Field(True, alias='introspection.token.claim')
    multivalued: str = Field(True, alias='multivalued')

    model_config = {
        'populate_by_name': True
    }


class Realm(PrettyModel):
    """Modelo para realm de Keycloak"""
    id: Optional[str] = None
    realm: str = Field(..., min_length=1, max_length=255)
    displayName: Optional[str] = Field(None)
    displayNameHtml: Optional[str] = Field(None)
    enabled: bool = True
    sslRequired: str = Field('external')
    registrationAllowed: bool = Field(False)
    registrationEmailAsUsername: bool = Field(False)
    rememberMe: bool = Field(False)
    verifyEmail: bool = Field(False)
    loginWithEmailAllowed: bool = Field(True)
    duplicateEmailsAllowed: bool = Field(False)
    resetPasswordAllowed: bool = Field(False)
    editUsernameAllowed: bool = Field(False)
    bruteForceProtected: bool = Field(False)
    passwordPolicy: Optional[str] = Field(None)
    attributes: Optional[Dict[str, Any]] = None
    users: Optional[List[User]] = None
    groups: Optional[List[Group]] = None
    roles: Optional[Dict[str, List[Role]]] = None
    clients: Optional[List[Client]] = None

# Permitir referencias circulares
Group.model_rebuild()