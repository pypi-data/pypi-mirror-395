from typing import List
from keycloak import KeycloakAdmin
from ..dtos import UsersProfile, UsersProfileAttribute, UsersProfileGroup, OperationResult, KeycloakSDKException


class UsersProfileDAO:
    """DAO para operaciones CRUD de perfiles de usuario en Keycloak"""

    NAME = 'UsersProfile'

    def __init__(self, client: KeycloakAdmin):
        self.client = client
    
    def get(self) -> OperationResult[UsersProfile]:
        """Obtiene información del perfil de usuarios del realm"""
        try:
            users_profile_data = self.client.get_realm_users_profile()
            users_profile = UsersProfile(**users_profile_data)
            return OperationResult(
                success=True,
                message=f"Perfil de usuarios para el realm '{self.client.connection.realm_name}' encontrado",
                data=users_profile
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get", f"realm: '{self.client.connection.realm_name}'")

    def add_attribute(self, attribute: UsersProfileAttribute) -> OperationResult[None]:
        """Agrega un atributo al perfil de usuarios del realm"""
        try:
            users_profile = self.get()
            if not users_profile.success:
                return users_profile.error

            users_profile.data.attributes.append(attribute.model_dump(exclude_none=True))
            self.client.update_realm_users_profile(users_profile.data.model_dump())

            return OperationResult(
                success=True,
                message=f"Atributo '{attribute.name}' agregado exitosamente al perfil de usuarios"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.add_attribute", f"atributo: '{attribute.name}'")
