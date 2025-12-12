from typing import List
from keycloak import KeycloakAdmin
from ...dtos import User, RLSAttribute, OperationResult, KeycloakSDKException


class UserDAO:
    """DAO para operaciones CRUD de usuarios en Keycloak"""

    NAME = 'User'

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

    def create(self, user: User) -> OperationResult[User]:
        """Crea un nuevo usuario"""
        try:
            if user.username is None:
                return OperationResult(
                    success=False,
                    message="El campo 'username' es obligatorio para crear un usuario",
                    data=None
                )
            
            user_data = user.model_dump(by_alias=True, exclude_none=True)

            # Remover campos que no se envían en la creación
            user_data.pop('id', None)
            password = user_data.pop('password', None)
            
            user_id = self.client.create_user(user_data, exist_ok=False)

            created_user = User(id=user_id, **user_data)

            # Establecer contraseña si se proporciona
            if password:
                self.client.set_user_password(user_id, password, temporary=False)

            return OperationResult(
                success=True,
                message=f"Usuario '{created_user.username}' creado exitosamente",
                data=created_user
            )

        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.create", f"usuario '{user.username}'")

    def get(self, username: str) -> OperationResult[User]:
        """Obtiene un usuario por username"""
        try:
            user_id = self.client.get_user_id(username)
            user_data = self.client.get_user(user_id)
            user_groups = self.client.get_user_groups(user_id)
            api_roles = self.client.get_client_roles_of_user(user_id, self.api_client_id)
            app_roles = self.client.get_client_roles_of_user(user_id, self.app_client_id)
            realm_roles = self.client.get_realm_roles_of_user(user_id)

            user = User(**user_data)
            user.groups = [group['name'] for group in user_groups]
            user.clientRoles = {
                'api': [role['name'] for role in api_roles],
                'app': [role['name'] for role in app_roles]
            }
            user.realmRoles = [role['name'] for role in realm_roles]

            return OperationResult(
                success=True,
                message=f"Usuario '{username}' encontrado",
                data=user
            )

        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get", f"usuario '{username}'")

    def list(self, limit: int = None, offset: int = 0) -> OperationResult[List[User]]:
        """Lista usuarios con filtros opcionales"""
        try:
            users = []
            query = {}
            
            if limit is not None:
                query['max'] = limit
            if offset:
                query['first'] = offset
                
            for user_data in self.client.get_users(query=query):
                user = User(**user_data)
                api_roles = self.client.get_client_roles_of_user(user.id, self.api_client_id)
                app_roles = self.client.get_client_roles_of_user(user.id, self.app_client_id)
                realm_roles = self.client.get_realm_roles_of_user(user.id)
                user.groups = [group['name'] for group in self.client.get_user_groups(user.id)]
                user.clientRoles = {
                    'api': [role['name'] for role in api_roles],
                    'app': [role['name'] for role in app_roles]
                }
                user.realmRoles = [role['name'] for role in realm_roles]
                users.append(user)

            return OperationResult(
                success=True,
                message=f"Encontrados {len(users)} usuarios",
                data=users
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.list")
    
    def update(self, username: str, payload: User) -> OperationResult[User]:
        """Actualiza un usuario"""
        try:
            user = self.get(username)

            if not user.success:
                return user.error

            user = user.data.model_dump()

            for k, v in payload.model_dump(exclude_unset=True).items():
                if isinstance(v, dict) and isinstance(user.get(k), dict):
                    user.get(k, {}).update(v)
                else:
                    user[k] = v

            user_id = user.pop('id')
            user.pop('username')
            password = user.pop('password', None)

            self.client.update_user(user_id, user)

            # Establecer contraseña si se proporciona
            if password:
                self.client.set_user_password(user_id, password, temporary=False)

            return OperationResult(
                success=True,
                message=f'Usuario "{username}" actualizado exitosamente',
                data=user
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.update", f"usuario '{username}'")

    def delete(self, username: str) -> OperationResult[None]:
        """Elimina un usuario"""
        try:
            user_id = self.client.get_user_id(username)
            self.client.delete_user(user_id)
            return OperationResult(
                success=True,
                message=f'Usuario "{username}" eliminado exitosamente'
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.delete", f"usuario '{username}'")

    def add_to_group(self, username: str, group_name: str) -> OperationResult[None]:
        """Agrega un usuario a un grupo"""
        try:
            user_id = self.client.get_user_id(username)
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
            self.client.group_user_add(user_id, group_id)
            return OperationResult(
                success=True,
                message=f'Usuario "{username}" agregado al grupo "{group_name}" exitosamente'
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.add_to_group", f"usuario '{username}' y grupo '{group_name}'")
    
    def remove_from_group(self, username: str, group_name: str) -> OperationResult[None]:
        """Remueve un usuario de un grupo"""
        try:
            user_id = self.client.get_user_id(username)
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
            self.client.group_user_remove(user_id, group_id)
            return OperationResult(
                success=True,
                message=f'Usuario "{username}" eliminado del grupo "{group_name}" exitosamente'
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.remove_from_group", f"usuario '{username}' y grupo '{group_name}'")
    
    def switch_groups(self, username: str, from_group: str, to_group: str) -> OperationResult[None]:
        """Mueve un usuario de un grupo a otro"""
        try:
            self.remove_from_group(username, from_group)
            self.add_to_group(username, to_group)

            return OperationResult(
                success=True,
                message=f'Usuario "{username}" movido del grupo "{from_group}" al grupo "{to_group}" exitosamente'
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.switch_groups", f"usuario '{username}', desde grupo '{from_group}' a grupo '{to_group}'")
    
    def set_attributes(self, username: str, attributes: List[RLSAttribute]) -> OperationResult[None]:
        try:
            if isinstance(attributes, RLSAttribute):
                attributes = [attributes]

            self.update(
                username,
                User(attributes={
                    f'rls.{attr.table}.{attr.field}': attr.values for attr in attributes
                })
            )

            return OperationResult(
                success=True,
                message=f'Atributos modificados para el usuario "{username}" exitosamente'
            )

        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.set_attributes", f"usuario '{username}', atributos '{attributes}'")
