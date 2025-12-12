"""
Modelos Pydantic para representar entidades de Keycloak de forma tipada y validada.
"""
import re
from typing import Optional
from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings

PROTOCOL = 'http'
HOSTNAME = 'localhost'
LOCAL_PORT = 8090
USERNAME = 'admin'
PASSWORD = 'admin'

class EnvironmentVariables(BaseSettings):
    """
    Variables de entorno para configuración de Keycloak.
    """
    MAIN_KEYCLOAK_URL: Optional[str] = None
    KEYCLOAK_API_CLIENT_SECRET: Optional[str] = None

class KeycloakConfig(BaseModel):
    """
    Configuración de conexión administrativa a Keycloak.
    """
    protocol: str = PROTOCOL
    hostname: str = HOSTNAME
    port: int = LOCAL_PORT
    username: str = USERNAME
    password: str = PASSWORD
    api_client_secret: Optional[str] = None
    verify_ssl: bool = True

    @model_validator(mode='before')
    @classmethod
    def parse_environment_variables(cls, values):
        """Parse MAIN_KEYCLOAK_URL si está presente"""
        env = EnvironmentVariables()
        if isinstance(values, dict):
            main_url = env.MAIN_KEYCLOAK_URL
            if main_url is not None:
                parsed = cls._parse_keycloak_url(main_url)
                # Solo sobrescribir valores que no hayan sido explícitamente configurados
                for key, value in parsed.items():
                    if key not in values:
                        values[key] = value

            if 'api_client_secret' not in values:
                api_client_secret = env.KEYCLOAK_API_CLIENT_SECRET
                if api_client_secret:
                    values['api_client_secret'] = api_client_secret
                    
        return values

    @property
    def url(self) -> str:
        """Construye la URL completa del servidor Keycloak"""
        return f"{self.protocol}://{self.hostname}:{self.port}"

    @staticmethod
    def _parse_keycloak_url(url_string: str) -> dict:
        """
        Parse diferentes formatos de MAIN_KEYCLOAK_URL
        y devuelve un dict con los componentes extraídos.
        """
        
        result = {}
        
        # Regex para parsear diferentes formatos
        # Patrón: [user[:password]@]host[:port]
        pattern = r'^(?:(?P<protocol>https?)://)?(?:(?P<user>[^:@]+)(?::(?P<password>[^@]+))?@)?(?P<host>[^:\/]+)(?::(?P<port>\d+))?$'
        
        match = re.match(pattern, url_string.strip())
        
        if not match:
            raise ValueError(f"Formato inválido para MAIN_KEYCLOAK_URL: {url_string}")
        
        groups = match.groupdict()
        
        # Extraer componentes
        host = groups.get('host')
        protocol = groups.get('protocol') or PROTOCOL
        username = groups.get('user') or USERNAME
        password = groups.get('password') or PASSWORD
        port = groups.get('port') or None

        if not host:
            raise ValueError("Host es requerido en MAIN_KEYCLOAK_URL")
        
        result.update({
            'username': username,
            'password': password,
            'hostname': host,
            'protocol': protocol,
            'port': int(port) if port else None
        })
        
        return result

