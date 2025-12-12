import asyncio
from typing import List, Optional
from keycloak import KeycloakAdmin
from ...dtos import User, RLSAttribute, OperationResult, KeycloakSDKException


class AsyncUserDAO:
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
    
    async def create(self, user: User) -> OperationResult[User]:
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

            user_id = await self.client.a_create_user(user_data, exist_ok=False)

            created_user = User(id=user_id, **user_data)

            # Establecer contraseña si se proporciona
            if password:
                await self.client.a_set_user_password(user_id, password, temporary=False)

            return OperationResult(
                success=True,
                message=f"Usuario '{created_user.username}' creado exitosamente",
                data=created_user
            )

        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.create", f"usuario '{user.username}'")

    async def get(self, username: str) -> OperationResult[User]:
        """Obtiene un usuario por username"""
        try:
            user_id = await self.client.a_get_user_id(username)
            user_data, user_groups, api_roles, app_roles, realm_roles = await asyncio.gather(
                self.client.a_get_user(user_id),
                self.client.a_get_user_groups(user_id),
                self.client.a_get_client_roles_of_user(user_id, self.api_client_id),
                self.client.a_get_client_roles_of_user(user_id, self.app_client_id),
                self.client.a_get_realm_roles_of_user(user_id)
            )

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

    async def list(self, limit: Optional[int] = None, offset: Optional[int] = None) -> OperationResult[List[User]]:
        """Lista usuarios con filtros opcionales"""
        try:
            users: List[User] = []
            tasks = []
            query = {}
            
            if limit is not None:
                query['max'] = limit
            if offset is not None:
                query['first'] = offset

            for user_data in await self.client.a_get_users(query=query):
                user = User(**user_data)
                tasks.append(self.client.a_get_user_groups(user.id))
                tasks.append(self.client.a_get_client_roles_of_user(user.id, self.api_client_id))
                tasks.append(self.client.a_get_client_roles_of_user(user.id, self.app_client_id))
                tasks.append(self.client.a_get_realm_roles_of_user(user.id))
                users.append(user)

            # Ejecutar todas las tareas
            all_results = await asyncio.gather(*tasks)

            # Agrupar resultados por usuario (4 resultados por usuario)
            for i, user in enumerate(users):
                start_idx = i * 4
                groups = all_results[start_idx]
                api_roles = all_results[start_idx + 1]
                app_roles = all_results[start_idx + 2]
                realm_roles = all_results[start_idx + 3]
                
                user.groups = [group['name'] for group in groups]
                api_roles = [role['name'] for role in api_roles]
                app_roles = [role['name'] for role in app_roles]
                user.clientRoles = {
                    'api': api_roles,
                    'app': app_roles
                }
                user.realmRoles = [role['name'] for role in realm_roles]

            return OperationResult(
                success=True,
                message=f"Encontrados {len(users)} usuarios",
                data=users
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.list")

    async def count(self) -> OperationResult[int]:
        """Cuenta el número total de usuarios"""
        try:
            total_users = await self.client.a_users_count()
            return OperationResult(
                success=True,
                message=f"Total de usuarios: {total_users}",
                data=total_users
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.count")
    
    async def update(self, username: str, payload: User) -> OperationResult[User]:
        """Actualiza un usuario"""
        try:

            user = await self.get(username)

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

            await self.client.a_update_user(user_id, user)

            # Establecer contraseña si se proporciona
            if password:
                await self.client.a_set_user_password(user_id, password, temporary=False)

            return OperationResult(
                success=True,
                message=f'Usuario "{username}" actualizado exitosamente',
                data=user
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.update", f"usuario '{username}'")

    async def delete(self, username: str) -> OperationResult[None]:
        """Elimina un usuario"""
        try:
            user_id = await self.client.a_get_user_id(username)
            await self.client.a_delete_user(user_id)
            return OperationResult(
                success=True,
                message=f'Usuario "{username}" eliminado exitosamente'
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.delete", f"usuario '{username}'")

    async def add_to_group(self, username: str, group_name: str) -> OperationResult[None]:
        """Agrega un usuario a un grupo"""
        try:
            user_id = await self.client.a_get_user_id(username)
            result = await self.client.a_get_groups({"search": group_name})
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
            await self.client.a_group_user_add(user_id, group_id)
            return OperationResult(
                success=True,
                message=f'Usuario "{username}" agregado al grupo "{group_name}" exitosamente'
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.add_to_group", f"usuario '{username}' y grupo '{group_name}'")
    
    async def remove_from_group(self, username: str, group_name: str) -> OperationResult[None]:
        """Remueve un usuario de un grupo"""
        try:
            user_id = await self.client.a_get_user_id(username)
            result = await self.client.a_get_groups({"search": group_name})
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
            await self.client.a_group_user_remove(user_id, group_id)
            return OperationResult(
                success=True,
                message=f'Usuario "{username}" eliminado del grupo "{group_name}" exitosamente'
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.remove_from_group", f"usuario '{username}' y grupo '{group_name}'")

    async def switch_groups(self, username: str, from_group: str, to_group: str) -> OperationResult[None]:
        """Mueve un usuario de un grupo a otro"""
        try:
            await self.remove_from_group(username, from_group)
            await self.add_to_group(username, to_group)

            return OperationResult(
                success=True,
                message=f'Usuario "{username}" movido del grupo "{from_group}" al grupo "{to_group}" exitosamente'
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.switch_groups", f"usuario '{username}', desde grupo '{from_group}' a grupo '{to_group}'")

    async def set_attributes(self, username: str, attributes: List[RLSAttribute]) -> OperationResult[None]:
        try:
            if isinstance(attributes, RLSAttribute):
                attributes = [attributes]
                
            await self.update(
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