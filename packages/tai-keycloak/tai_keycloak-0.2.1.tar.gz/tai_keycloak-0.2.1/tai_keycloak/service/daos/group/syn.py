from typing import List
from keycloak import KeycloakAdmin
from ...dtos import Group, OperationResult, KeycloakSDKException


class GroupDAO:
    """DAO para operaciones CRUD de grupos en Keycloak"""

    NAME = 'Group'

    def __init__(self, client: KeycloakAdmin):
        self.client = client
        self._api_client_id = None
        self._app_client_id = None
    
    @property
    def api_client_id(self):
        if not self._api_client_id:
            self._api_client_id = self.client.get_client_id('api')
        return self._api_client_id

    @property
    def app_client_id(self):
        if not self._app_client_id:
            self._app_client_id = self.client.get_client_id('app')
        return self._app_client_id
    
    def create(self, group: Group) -> OperationResult[Group]:
        """Crea un nuevo grupo"""
        try:
            group_data = group.model_dump(exclude_unset=True)
            group_data.pop('id', None)
            group_data.pop('subGroups', None)  # Los subgrupos se manejan por separado
            group.id = self.client.create_group(group_data, skip_exists=False)

            return OperationResult(
                success=True,
                message=f"Grupo '{group.name}' creado exitosamente",
                data=group
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.create_group", f"grupo '{group.name}'")

    def get(self, group_name: str) -> OperationResult[Group]:
        """Obtiene información de un grupo"""
        try:
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
            group_data = self.client.get_group(group_id)
            group_client_roles = self.client.get_group_client_roles(group_id, self.api_client_id)
            group_app_roles = self.client.get_group_client_roles(group_id, self.app_client_id)
            group_realm_roles = self.client.get_group_realm_roles(group_id)

            group = Group(**group_data)
            group.clientRoles = {
                'api': [role['name'] for role in group_client_roles],
                'app': [role['name'] for role in group_app_roles]
            }
            group.realmRoles = [role['name'] for role in group_realm_roles]

            return OperationResult(
                success=True,
                message=f"Grupo '{group_name}' encontrado",
                data=group
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get", f"grupo: '{group_name}'")

    def list(self) -> OperationResult[List[Group]]:
        """Lista todos los grupos"""
        try:
            groups = []
            for group_data in self.client.get_groups():
                group = Group(**group_data)
                group_client_roles = self.client.get_group_client_roles(group.id, self.api_client_id)
                group_app_roles = self.client.get_group_client_roles(group.id, self.app_client_id)
                group_realm_roles = self.client.get_group_realm_roles(group.id)

                group.clientRoles = {
                    'api': [role['name'] for role in group_client_roles],
                    'app': [role['name'] for role in group_app_roles]
                }
                group.realmRoles = [role['name'] for role in group_realm_roles]
                groups.append(group)

            return OperationResult(
                success=True,
                message=f"Encontrados {len(groups)} grupos",
                data=groups
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.list")

    def delete(self, group_name: str) -> OperationResult[None]:
        """Elimina un grupo"""
        try:
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
            self.client.delete_group(group_id)
            return OperationResult(
                success=True,
                message=f"Grupo '{group_name}' eliminado exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.delete", f"grupo '{group_name}'")

    def add_user(self, username: str, group_name: str) -> OperationResult[None]:
        """Añade un usuario a un grupo"""
        try:
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
            user_id = self.client.get_user_id(username)
            self.client.group_user_add(user_id, group_id)
            return OperationResult(
                success=True,
                message=f"Usuario '{username}' añadido al grupo '{group_name}' exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.add_user", f"usuario '{username}' y grupo '{group_name}'")
    
    def remove_user(self, username: str, group_name: str) -> OperationResult[None]:
        """Remueve un usuario de un grupo"""
        try:
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
            user_id = self.client.get_user_id(username)
            self.client.group_user_remove(user_id, group_id)
            return OperationResult(
                success=True,
                message="Usuario eliminado del grupo exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.remove_user", f"usuario '{username}' y grupo '{group_name}'")