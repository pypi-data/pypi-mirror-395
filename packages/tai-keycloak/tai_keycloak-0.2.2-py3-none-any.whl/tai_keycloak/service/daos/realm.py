from typing import List
from keycloak import KeycloakAdmin
from ..dtos import Realm, OperationResult, KeycloakSDKException


class RealmDAO:
    """DAO para operaciones CRUD de realms en Keycloak"""

    NAME = 'Realm'

    def __init__(self, client: KeycloakAdmin):
        self.client = client

    def create(self, realm: Realm) -> OperationResult[Realm]:
        """Crea un nuevo realm"""
        try:
            realm_data = realm.model_dump(by_alias=True, exclude_none=True)
            self.client.create_realm(realm_data, skip_exists=False)
            
            return OperationResult(
                success=True,
                message=f"Realm '{realm.realm}' creado exitosamente",
                data=realm
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.create", f"realm '{realm.realm}'")

    def get(self, realm_name: str) -> OperationResult[Realm]:
        """Obtiene información de un realm"""
        try:
            realm_data = self.client.get_realm(realm_name)
            realm = Realm(**realm_data)
            return OperationResult(
                success=True,
                message=f"Realm '{realm_name}' encontrado",
                data=realm
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.get", f"realm: '{realm_name}'")

    def list(self) -> OperationResult[List[Realm]]:
        """Lista todos los realms"""
        try:
            realms = []
            for realm in self.client.get_realms():
                realms.append(Realm(**realm))

            return OperationResult(
                success=True,
                message=f"Encontrados {len(realms)} realms",
                data=realms
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.list")
    
    def delete(self, realm_name: str) -> OperationResult[None]:
        """Elimina un realm"""
        try:
            self.client.delete_realm(realm_name)

            return OperationResult(
                success=True,
                message=f"Realm '{realm_name}' eliminado exitosamente"
            )
        except Exception as e:
            return KeycloakSDKException(e).handle(f"{self.NAME}.delete", f"realm '{realm_name}'")

