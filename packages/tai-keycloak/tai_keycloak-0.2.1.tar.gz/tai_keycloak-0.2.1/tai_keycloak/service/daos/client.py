from typing import List
from keycloak import KeycloakAdmin
from ..dtos import Client, ClientMapper, OperationResult, KeycloakSDKException


class ClientDAO:
    """DAO para operaciones CRUD de clientes en Keycloak"""

    NAME = 'Client'

    def __init__(self, client: KeycloakAdmin, client_name: str = None):
        self.client = client
        self.client_name = client_name
        self.client_id = None
        if client_name is not None:
            result = self._get_client_id(client_name)
            if result.success:
                self.client_id = result.data   
    
    def _get_client_id(self, client_name: str = None) -> OperationResult[str]:
        """Obtiene el client_id a partir del nombre del cliente"""
        try:

            if client_name:
                client_id = self.client.get_client_id(client_name)
            
            elif self.client_id:
                client_id = self.client_id
                client_name = self.client_name

            else:
                return OperationResult(
                    success=False,
                    message="No se proporcionó un client_name y no hay client_id almacenado",
                    data=None
                )
            return OperationResult(
                success=True,
                message=f"client_id para el cliente '{client_name}' obtenido exitosamente",
                data=client_id
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get_client_id", f"client_name '{client_name}'")

    def create(self, client: Client) -> OperationResult[Client]:
        """Crea un nuevo cliente"""
        try:
            client_data = client.model_dump(exclude_none=True)
            client_data.pop('id', None)
            client.id = self.client.create_client(client_data)
            
            return OperationResult(
                success=True,
                message=f"Cliente '{client.id}' creado exitosamente",
                data=client
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.create", f"client '{client.id}'")

    def get(self, client_name: str = None) -> OperationResult[Client]:
        """Obtiene información de un cliente"""
        try:
            client_id = self._get_client_id(client_name).data
            client_data = self.client.get_client(client_id)
            client = Client(**client_data)
            return OperationResult(
                success=True,
                message=f"Cliente '{client_id}' encontrado",
                data=client
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get", f"client: '{client_id}'")

    def list(self) -> OperationResult[List[Client]]:
        """Lista todos los clientes"""
        try:
            clients = []
            for client in self.client.get_clients():
                clients.append(Client(**client))

            return OperationResult(
                success=True,
                message=f"Encontrados {len(clients)} clientes",
                data=clients
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.list")

    def delete(self, client_name: str = None) -> OperationResult[None]:
        """Elimina un cliente"""
        try:
            client_id = self._get_client_id(client_name).data
            self.client.delete_client(client_id)
            return OperationResult(
                success=True,
                message=f"Cliente '{client_id}' eliminado exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.delete", f"client '{client_id}'")

    def get_secret(self, client_name: str = None) -> OperationResult[str]:
        """Obtiene el secreto de un cliente confidencial"""
        try:
            client_id = self._get_client_id(client_name).data
            client = self.get(client_id)  # Verifica que el cliente exista
            if client.data.publicClient:
                return OperationResult(
                    success=False,
                    message=f"El cliente '{client_id}' es público y no tiene un secreto",
                    data=None
                )
            secret_data = self.client.get_client_secrets(client_id)
            secret = secret_data.get('value')
            return OperationResult(
                success=True,
                message=f"Secreto del cliente '{client_id}' obtenido exitosamente",
                data=secret
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get_secret", f"client '{client_id}'")

    def regenerate_secret(self, client_name: str = None) -> OperationResult[str]:
        """Regenera el secreto de un cliente confidencial"""
        try:
            client_id = self._get_client_id(client_name).data
            client = self.get(client_id)  # Verifica que el cliente exista
            if client.data.publicClient:
                return OperationResult(
                    success=False,
                    message=f"El cliente '{client_id}' es público y no tiene un secreto",
                    data=None
                )
            secret = self.client.generate_client_secrets(client_id)
            return OperationResult(
                success=True,
                message=f"Secreto del cliente '{client_id}' regenerado exitosamente",
                data=secret
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.regenerate_secret", f"client '{client_id}'")

    def create_mapper(self, mapper: ClientMapper, client_name: str = None) -> OperationResult[dict]:
        """Crea un mapper para un cliente"""
        try:
            client_id = self._get_client_id(client_name).data
            self.client.add_mapper_to_client(client_id, mapper.model_dump(by_alias=True))
            return OperationResult(
                success=True,
                message=f"Mapper creado exitosamente para el cliente '{client_name}'",
                data=mapper
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.create_mapper", f"client '{client_name}'")

    def list_mappers(self, client_name: str = None) -> OperationResult[List[ClientMapper]]:
        """Lista los mappers de un cliente"""
        try:
            client_id = self._get_client_id(client_name).data
            mappers_data = self.client.get_mappers_from_client(client_id)
            mappers = [ClientMapper(**mapper) for mapper in mappers_data]
            return OperationResult(
                success=True,
                message=f"Encontrados {len(mappers)} mappers para el cliente '{client_id}'",
                data=mappers
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.list_mappers", f"client '{client_id}'")