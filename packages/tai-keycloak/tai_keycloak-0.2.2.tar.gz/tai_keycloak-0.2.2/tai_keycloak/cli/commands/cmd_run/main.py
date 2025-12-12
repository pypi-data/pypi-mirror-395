import click
import signal
import sys
from .checks import (
    check_docker_engine, 
    detect_database_mode,
    check_database_configuration,
    wait_for_keycloak_ready, 
    monitor_containers
)
from .docker_compose import get_docker_compose_path, run_docker_compose_detached, cleanup_containers
from .display import show_service_info


@click.command()
@click.option('--build', is_flag=True, help='Forzar rebuild de la imagen')
@click.option('--db', 
              type=click.Choice(['embedded', 'docker', 'external', 'auto'], case_sensitive=False),
              default='auto',
              help='Modo de base de datos: embedded (H2), docker (PostgreSQL en Docker), external (BD externa), auto (detectar automáticamente)')
def run(build: bool, db: str):
    """Comando para iniciar el servidor Keycloak en modo DESARROLLO.
    
    Modos de base de datos:
    
    - embedded: Base de datos H2 en memoria (desarrollo rápido)
    - docker: PostgreSQL en Docker Compose (desarrollo con persistencia)
    - external: Base de datos PostgreSQL externa (desarrollo con BD existente)
    - auto: Detectar automáticamente basado en variables de entorno (por defecto)
    
    NOTA: Este comando es solo para desarrollo. Para producción (Azure/OnPremise),
    usa docker-compose directamente con los profiles 'azure' u 'onpremise'.
    """
    
    click.echo("🚀 " + click.style("Iniciando keycloak...", fg='cyan', bold=True))
    click.echo()
    
    # Variable global para el path del docker-compose (para cleanup)
    compose_dir = None
    profile = None
    
    def signal_handler(signum, frame):
        """Manejar Ctrl+C para limpiar contenedores."""
        if compose_dir and profile:
            cleanup_containers(compose_dir, profile)
        sys.exit(0)
    
    # Configurar manejo de señales
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Paso 1: Verificar Docker Engine
        if not check_docker_engine():
            return
        
        # Paso 2: Detectar o configurar modo de base de datos
        if db == 'auto':
            detected_mode = detect_database_mode()
            click.echo("🔎 " + click.style(f"Modo detectado automáticamente: {detected_mode}", fg='cyan'))
            click.echo()
        else:
            detected_mode = db
            click.echo("🔧 " + click.style(f"Modo especificado manualmente: {detected_mode}", fg='cyan'))
            click.echo()
        
        # Paso 3: Configurar y validar base de datos
        success, profile = check_database_configuration(detected_mode)
        if not success:
            click.echo("❌ " + click.style("No se pudo configurar la base de datos", fg='red'))
            return
        
        # Paso 4: Ejecutar Docker Compose en modo detach
        compose_dir = get_docker_compose_path()
        if not compose_dir:
            return
        
        # Ejecutar docker-compose siempre en modo detach con el profile determinado
        run_docker_compose_detached(compose_dir, build, profile, detected_mode)
        
        # Paso 5: Esperar a que Keycloak esté completamente listo
        if wait_for_keycloak_ready():
            # Paso 6: Mostrar información del servicio
            show_service_info()
            
            # Paso 7: Mantener el proceso activo y monitorear contenedores
            click.echo("⏳ " + click.style("Servidor ejecutándose... Presiona Ctrl+C para detener", fg='cyan'))
            click.echo()
            
            monitor_containers(compose_dir)
        else:
            click.echo("❌ " + click.style("El servidor no se inició correctamente", fg='red'))
            cleanup_containers(compose_dir, profile)
        
    except KeyboardInterrupt:
        if compose_dir and profile:
            cleanup_containers(compose_dir, profile)
    except Exception as e:
        import logging
        logging.exception(e)
        click.echo(f"❌ Error inesperado: {e}")
        if compose_dir and profile:
            cleanup_containers(compose_dir, profile)


