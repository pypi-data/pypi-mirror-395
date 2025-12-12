"""
Verificaciones del sistema para el comando run
"""
import os
import socket
import time
import subprocess

import click

from tai_keycloak import kc


def detect_database_mode() -> str:
    """Detectar el modo de base de datos basado en las variables de entorno.
    
    Returns:
        str: 'embedded' | 'docker' | 'external'
    """
    db_type = os.environ.get('KC_DB', None)
    db_host = os.environ.get('KC_DB_URL_HOST', None)
    db_username = os.environ.get('KC_DB_USERNAME', None)
    db_password = os.environ.get('KC_DB_PASSWORD', None)
    
    # Si no hay KC_DB definido, usar modo embedded (H2)
    if not db_type:
        return 'embedded'
    
    # Si hay KC_DB pero faltan las credenciales completas, usar docker
    if db_type and (not db_host or not db_username or not db_password):
        return 'docker'
    
    # Si están todas las variables, usar BD externa
    return 'external'


def validate_external_database(db_host: str, db_port: int, db_type: str) -> tuple[bool, str]:
    """Validar la conexión a una base de datos externa.
    
    Args:
        db_host: Hostname de la BD
        db_port: Puerto de la BD
        db_type: Tipo de BD (postgres, mysql, etc)
    
    Returns:
        tuple[bool, str]: (es_válida, mensaje)
    """
    # Validar que localhost no se use (problema con Docker)
    if db_host in ['localhost', '127.0.0.1']:
        return False, (
            f"No puedes usar '{db_host}' como host cuando Keycloak se ejecuta en Docker.\n"
            "   💡 Usa 'host.docker.internal' (Mac/Windows) o la IP del host (Linux).\n"
            "   💡 Alternativamente, usa la IP real de tu máquina."
        )
    
    # Intentar conexión TCP
    # Si es host.docker.internal, no podemos validar desde el host (solo funciona en Docker)
    if db_host == 'host.docker.internal':
        return True, f"Base de datos configurada con {db_host} (se validará desde el contenedor)"
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((db_host, db_port))
        sock.close()
        
        if result == 0:
            return True, f"Base de datos {db_type} accesible en {db_host}:{db_port}"
        else:
            return False, (
                f"No se puede conectar a {db_host}:{db_port}.\n"
                "   💡 Verifica que la base de datos esté corriendo y accesible.\n"
                "   💡 Verifica reglas de firewall y que el puerto esté abierto."
            )
    except socket.gaierror:
        return False, f"No se puede resolver el hostname '{db_host}'. Verifica el nombre del host."
    except Exception as e:
        return False, f"Error verificando conexión: {e}"


def setup_database_env_vars(mode: str) -> dict:
    """Configurar variables de entorno según el modo de base de datos.
    
    Args:
        mode: 'embedded' | 'docker' | 'external'
    
    Returns:
        dict: Variables de entorno a configurar
    """
    env_vars = {}
    
    if mode == 'embedded':
        # H2 embebida - sin configuración adicional
        click.echo("   ℹ️  " + click.style("Modo: Base de datos H2 embebida (memoria)", fg='cyan'))
        # Asegurar que no haya variables de BD externa
        for key in ['KC_DB', 'KC_DB_URL_HOST', 'KC_DB_URL_PORT', 
                    'KC_DB_URL_DATABASE', 'KC_DB_USERNAME', 'KC_DB_PASSWORD']:
            if key in os.environ:
                del os.environ[key]
    
    elif mode == 'docker':
        # PostgreSQL en Docker Compose
        click.echo("   ℹ️  " + click.style("Modo: PostgreSQL en Docker Compose", fg='cyan'))
        
        # Valores FIJOS para docker-compose (deben coincidir con docker-compose.yml)
        # En este modo SIEMPRE sobrescribimos las variables del usuario
        required_values = {
            'KC_DB': 'postgres',
            'KC_DRIVER': 'postgresql',
            'KC_DB_URL_HOST': 'postgres',  # Nombre del servicio en docker-compose
            'KC_DB_URL_PORT': '5432',
            'KC_DB_URL_DATABASE': 'keycloak',
            'KC_DB_USERNAME': 'keycloak',
            'KC_DB_PASSWORD': 'keycloak'
        }
        
        # También limpiar variables de PostgreSQL que podrían estar en el entorno
        postgres_vars_to_clean = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB']
        
        # Forzar todas las variables (ignorar las del usuario)
        for key, value in required_values.items():
            env_vars[key] = value
            os.environ[key] = value
        
        # Limpiar variables de PostgreSQL del entorno
        for var in postgres_vars_to_clean:
            if var in os.environ:
                del os.environ[var]
        
        click.echo("   ✓ Variables configuradas (modo Docker):")
        for key, value in required_values.items():
            # No mostrar contraseñas completas
            display_value = '***' if 'PASSWORD' in key else value
            click.echo(f"     - {key}={display_value}")
    
    elif mode == 'external':
        # Base de datos externa - validar variables existentes
        # NOTA: En tai-kc run, external también usa development-db (modo desarrollo)
        click.echo("   ℹ️  " + click.style("Modo: Base de datos externa (desarrollo)", fg='cyan'))
        
        required_vars = ['KC_DB', 'KC_DRIVER', 'KC_DB_URL_HOST', 'KC_DB_URL_PORT',
                        'KC_DB_URL_DATABASE', 'KC_DB_USERNAME', 'KC_DB_PASSWORD']
        
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            click.echo("   ❌ " + click.style("Faltan variables de entorno requeridas:", fg='red'))
            for var in missing_vars:
                click.echo(f"     - {var}")
            raise click.ClickException(
                "Para usar base de datos externa, define todas las variables requeridas."
            )
        
        click.echo("   ✓ Variables de BD externa detectadas:")
        for var in required_vars:
            value = os.environ[var]
            display_value = '***' if 'PASSWORD' in var else value
            click.echo(f"     - {var}={display_value}")
    
    return env_vars


def check_docker_engine() -> bool:
    """Verificar que Docker Engine esté corriendo."""
    click.echo("🔍 " + click.style("Verificando Docker Engine...", fg='yellow'), nl=False)
    
    try:
        result = subprocess.run(
            ['docker', 'info'], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        if result.returncode == 0:
            click.echo("\r   ✅ " + click.style("Docker Engine está corriendo", fg='green') + " " * 40)
            click.echo()
            return True
        else:
            click.echo("\r   ❌ " + click.style("Docker Engine no responde", fg='red') + " " * 40)
            click.echo("   💡 Asegúrate de que Docker Desktop esté iniciado")
            click.echo()
            return False
    except subprocess.TimeoutExpired:
        click.echo("\r   ⏱️  " + click.style("Timeout verificando Docker", fg='red') + " " * 40)
        click.echo()
        return False
    except FileNotFoundError:
        click.echo("\r   ❌ " + click.style("Docker no está instalado", fg='red') + " " * 40)
        click.echo("   💡 Instala Docker desde https://docker.com")
        click.echo()
        return False
    except Exception as e:
        click.echo(f"\r   ❌ " + click.style(f"Error verificando Docker: {e}", fg='red') + " " * 40)
        click.echo()
        return False


def check_database_configuration(mode: str) -> tuple[bool, str]:
    """Verificar y configurar la base de datos según el modo detectado.
    
    Args:
        mode: 'embedded' | 'docker' | 'external'
    
    Returns:
        tuple[bool, str]: (éxito, profile de docker-compose)
    """
    click.echo("🔍 " + click.style("Configurando base de datos...", fg='yellow'))
    click.echo()
    
    try:
        # Configurar variables de entorno según el modo
        setup_database_env_vars(mode)
        click.echo()
        
        # Determinar el profile de docker-compose
        # tai-kc run es solo para desarrollo, todos los modos usan development o development-db
        if mode == 'embedded':
            profile = 'development'
        elif mode == 'docker':  # docker o external
            # Tanto BD en Docker como BD externa usan development-db (modo desarrollo)
            profile = 'development-docker-db'
        else:  # external
            profile = 'development-external-db'
            
            # Validar conexión a BD externa
            db_host = os.environ['KC_DB_URL_HOST']
            db_port = int(os.environ.get('KC_DB_URL_PORT', '5432'))
            db_type = os.environ['KC_DB']
            
            click.echo("🔍 " + click.style("Validando conexión a base de datos externa...", fg='yellow'), nl=False)
            is_valid, message = validate_external_database(db_host, db_port, db_type)
            
            if not is_valid:
                click.echo("\r   ❌ " + click.style("Error de validación", fg='red') + " " * 40)
                click.echo()
                click.echo("   " + message)
                click.echo()
                return False, profile
            
            click.echo("\r   ✅ " + click.style(message, fg='green') + " " * 40)
            click.echo()
        
        return True, profile
        
    except Exception as e:
        click.echo(f"   ❌ " + click.style(f"Error configurando base de datos: {e}", fg='red'))
        click.echo()
        return False, 'development'


def wait_for_keycloak_ready(timeout: int = 60) -> bool:
    """Esperar a que Keycloak esté completamente listo para recibir peticiones."""
    
    click.echo("⏱️  " + click.style("Esperando a que Keycloak esté listo...", fg='yellow'), nl=False)
    
    start_time = time.time()
    attempts = 0
    
    while time.time() - start_time < timeout:
        attempts += 1

        # Intentar conectar
        response = kc.admin.check_health(with_logs=False)
        if response.success:
            # Limpiar la línea y mostrar mensaje de éxito
            click.echo(f"\r   ✅ " + click.style("Keycloak está listo y funcionando correctamente!", fg='green') + " " * 40)
            click.echo()
            return True

        
        # Esperar antes del siguiente intento
        time.sleep(2)
    
    # Si llegamos aquí, se agotó el timeout
    click.echo("\r⏰ " + click.style(f"Timeout después de {timeout}s - el servidor puede que no esté listo", fg='yellow') + " " * 40)
    click.echo("   💡 " + click.style("Puedes verificar manualmente en el navegador", fg='cyan'))
    click.echo()
    
    # Aunque el health check falló, seguimos adelante por si es un problema con el endpoint
    return True


def monitor_containers(compose_dir):
    """Monitorear contenedores y mantener el proceso activo."""
    
    original_dir = os.getcwd()
    os.chdir(compose_dir)
    
    try:
        # Verificar que los contenedores estén ejecutándose
        while True:
            # Verificar estado de contenedores
            result = subprocess.run(['docker-compose', 'ps', '-q'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0 or not result.stdout.strip():
                click.echo("❌ " + click.style("Los contenedores se han detenido", fg='red'))
                break
            
            # Capturar logs internamente (sin mostrar)
            # Esto ayuda a mantener los logs disponibles pero no los muestra
            subprocess.run(['docker-compose', 'logs', '--tail=0'], 
                         capture_output=True, text=True)
            
            # Esperar antes de la siguiente verificación
            time.sleep(5)
            
    except KeyboardInterrupt:
        # El signal handler se encargará de la limpieza
        pass
    finally:
        os.chdir(original_dir)