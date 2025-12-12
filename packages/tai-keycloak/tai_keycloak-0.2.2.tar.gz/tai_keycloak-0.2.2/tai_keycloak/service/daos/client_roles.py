from typing import List
from keycloak import KeycloakAdmin
from ..dtos import Role, OperationResult, KeycloakSDKException


class ClientRoleDAO:
    """DAO para operaciones CRUD de roles de cliente en Keycloak"""

    NAME = 'ClientRole'

    def __init__(self, client: KeycloakAdmin, client_id: str):
        self.client = client
        try:
            self.client_id = self.client.get_client_id(client_id)
        except Exception as e:
            KeycloakSDKException(e).handle(f"{self.NAME}.get_client_id", f"client_id '{client_id}'")
            self.client_id = None

    def create(self, role: Role) -> OperationResult[Role]:
        """Crea un nuevo rol (realm o cliente)"""
        if not self.client_id:
            return OperationResult(
                success=False,
                message="No se pudo determinar el client_id para crear el rol",
                data=None
            )
        try:
            role.clientRole = True
            role_data = role.model_dump(by_alias=True, exclude_none=True)
            role_data.pop('id', None)

            self.client.create_client_role(self.client_id, role_data, skip_exists=False)

            return OperationResult(
                success=True,
                message=f"Rol de cliente '{role.name}' creado exitosamente",
                data=role
            )

        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.create", f"rol de cliente '{role.name}'")
    
    def get(self, role_name: str) -> OperationResult[Role]:
        """Obtiene un rol de cliente por nombre"""
        if not self.client_id:
            return OperationResult(
                success=False,
                message="No se pudo determinar el client_id para obtener el rol",
                data=None
            )
        try:
            role_data = self.client.get_client_role(self.client_id, role_name)
            role = Role(**role_data)

            return OperationResult(
                success=True,
                message=f"Rol de cliente '{role_name}' encontrado",
                data=role
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get", f"rol de realm '{role_name}'")
    
    def list(self) -> OperationResult[List[Role]]:
        """Lista todos los roles del cliente"""
        if not self.client_id:
            return OperationResult(
                success=False,
                message="No se pudo determinar el client_id para listar los roles",
                data=None
            )
        try:
            roles = [Role(**role) for role in self.client.get_client_roles(self.client_id)]

            return OperationResult(
                success=True,
                message=f"Encontrados {len(roles)} roles de cliente",
                data=roles
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.list")
    
    def delete(self, role_name: str) -> OperationResult[None]:
        """Elimina un rol de cliente"""
        if not self.client_id:
            return OperationResult(
                success=False,
                message="No se pudo determinar el client_id para eliminar el rol",
                data=None
            )
        try:
            self.client.delete_client_role(self.client_id, role_name)
            return OperationResult(
                success=True,
                message=f"Rol de cliente '{role_name}' eliminado exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.delete", f"rol de cliente '{role_name}'")
    
    def add_to_group(self, group_name: str, role_name: str) -> OperationResult[None]:
        """Asigna un rol de cliente a un grupo"""
        if not self.client_id:
            return OperationResult(
                success=False,
                message="No se pudo determinar el client_id para asignar el rol al grupo",
                data=None
            )
        try:
            role = self.client.get_client_role(self.client_id, role_name)
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
            self.client.assign_group_client_roles(group_id, self.client_id, role)

            return OperationResult(
                success=True,
                message=f"Rol de cliente '{role_name}' asignado al grupo '{group_name}' exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.add_to_group", f"rol de cliente '{role_name}' al grupo '{group_name}'")
    
    def remove_from_group(self, group_name: str, role_name: str) -> OperationResult[None]:
        """Remueve un rol de cliente de un grupo"""
        if not self.client_id:
            return OperationResult(
                success=False,
                message="No se pudo determinar el client_id para eliminar el rol del grupo",
                data=None
            )
        try:
            role = self.client.get_client_role(self.client_id, role_name)
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
            self.client.delete_group_client_roles(group_id, self.client_id, role)

            return OperationResult(
                success=True,
                message=f"Rol de cliente '{role_name}' eliminado del grupo '{group_name}' exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.remove_from_group", f"rol de cliente '{role_name}' del grupo '{group_name}'")
    
    def add_to_user(self, username: str, role_name: str) -> OperationResult[None]:
        """Asigna un rol de cliente a un usuario"""
        if not self.client_id:
            return OperationResult(
                success=False,
                message="No se pudo determinar el client_id para asignar el rol al usuario",
                data=None
            )
        try:
            user_id = self.client.get_user_id(username)
            role = self.client.get_client_role(self.client_id, role_name)

            self.client.assign_client_role(user_id, self.client_id, role)
            return OperationResult(
                success=True,
                message=f"Rol de cliente '{role_name}' asignado al usuario '{username}' exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.add_to_user", f"rol de realm '{role_name}' al usuario '{username}'")
    
    def remove_from_user(self, username: str, role_name: str) -> OperationResult[None]:
        """Remueve un rol de cliente de un usuario"""
        if not self.client_id:
            return OperationResult(
                success=False,
                message="No se pudo determinar el client_id para eliminar el rol del usuario",
                data=None
            )
        try:
            user_id = self.client.get_user_id(username)
            role = self.client.get_client_role(self.client_id, role_name)

            self.client.delete_client_roles_of_user(user_id, self.client_id, role)
            return OperationResult(
                success=True,
                message=f"Rol de cliente '{role_name}' eliminado del usuario '{username}' exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.remove_from_user", f"rol de cliente '{role_name}' del usuario '{username}'")
