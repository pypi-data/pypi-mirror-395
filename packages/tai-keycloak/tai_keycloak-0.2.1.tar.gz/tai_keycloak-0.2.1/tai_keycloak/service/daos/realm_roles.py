from typing import List
from keycloak import KeycloakAdmin
from ..dtos import Role, OperationResult, KeycloakSDKException


class RealmRoleDAO:
    """DAO para operaciones CRUD de roles de realm en Keycloak"""

    NAME = 'RealmRole'

    def __init__(self, client: KeycloakAdmin):
        self.client = client

    def create(self, role: Role) -> OperationResult[None]:
        """Crea un nuevo rol (realm o cliente)"""
        try:
            role_data = role.model_dump(by_alias=True, exclude_none=True)
            role_data.pop('id', None)
            
            self.client.create_realm_role(role_data, skip_exists=False)
            
            return OperationResult(
                success=True,
                message=f"Rol de realm '{role.name}' creado exitosamente"
            )

        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.create", f"rol de realm '{role.name}'")
    
    def get(self, role_name: str) -> OperationResult[Role]:
        """Obtiene un rol de realm por nombre"""
        try:
            role_data = self.client.get_realm_role(role_name)
            role = Role(**role_data)

            return OperationResult(
                success=True,
                message=f"Rol de realm '{role_name}' encontrado",
                data=role
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get", f"rol de realm '{role_name}'")
    
    def list(self) -> OperationResult[List[Role]]:
        """Lista todos los roles del realm"""
        try:
            roles = [Role(**role) for role in self.client.get_realm_roles()]

            return OperationResult(
                success=True,
                message=f"Encontrados {len(roles)} roles de realm",
                data=roles
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.list")
    
    def delete(self, role_name: str) -> OperationResult[None]:
        """Elimina un rol de realm"""
        try:
            self.client.delete_realm_role(role_name)
            return OperationResult(
                success=True,
                message=f"Rol de realm '{role_name}' eliminado exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.delete", f"rol de realm '{role_name}'")
    
    def add_to_group(self, group_name: str, role_name: str) -> OperationResult[None]:
        """Asigna un rol de realm a un grupo"""
        try:
            role = self.client.get_realm_role(role_name)
            result = self.client.get_groups({"search": group_name})
            if not result:
                return OperationResult(
                    success=False,
                    message=f"Grupo '{group_name}' no encontrado",
                    data=None
                )
            if len(result) > 1:
                return OperationResult(
                    success=False,
                    message=f"Se encontraron múltiples grupos con el nombre '{group_name}'",
                    data=None
                )
            group_id = result[0]['id']
            self.client.assign_group_realm_roles(group_id, role)

            return OperationResult(
                success=True,
                message=f"Rol de realm '{role_name}' asignado al grupo '{group_name}' exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.add_to_group", f"rol de realm '{role_name}' al grupo '{group_name}'")
    
    def remove_from_group(self, group_name: str, role_name: str) -> OperationResult[None]:
        """Remueve un rol de realm de un grupo"""
        try:
            role = self.client.get_realm_role(role_name)
            result = self.client.get_groups({"search": group_name})
            if not result:
                return OperationResult(
                    success=False,
                    message=f"Grupo '{group_name}' no encontrado",
                    data=None
                )
            if len(result) > 1:
                return OperationResult(
                    success=False,
                    message=f"Se encontraron múltiples grupos con el nombre '{group_name}'",
                    data=None
                )
            group_id = result[0]['id']
            self.client.delete_group_realm_roles(group_id, [role])

            return OperationResult(
                success=True,
                message=f"Rol de realm '{role_name}' eliminado del grupo '{group_name}' exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.remove_from_group", f"rol de realm '{role_name}' del grupo '{group_name}'")
    
    def add_to_user(self, username: str, role_name: str) -> OperationResult[None]:
        """Asigna un rol de realm a un usuario"""
        try:
            user_id = self.client.get_user_id(username)
            role = self.client.get_realm_role(role_name)

            self.client.assign_realm_roles(user_id, role)
            return OperationResult(
                success=True,
                message=f"Rol de realm '{role_name}' asignado al usuario '{username}' exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.add_to_user", f"rol de realm '{role_name}' al usuario '{username}'")
    
    def remove_from_user(self, username: str, role_name: str) -> OperationResult[None]:
        """Remueve un rol de realm de un usuario"""
        try:
            user_id = self.client.get_user_id(username)
            role = self.client.get_realm_role(role_name)

            self.client.delete_realm_roles_of_user(user_id, role)
            return OperationResult(
                success=True,
                message=f"Rol de realm '{role_name}' eliminado del usuario '{username}' exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.remove_from_user", f"rol de realm '{role_name}' del usuario '{username}'")
