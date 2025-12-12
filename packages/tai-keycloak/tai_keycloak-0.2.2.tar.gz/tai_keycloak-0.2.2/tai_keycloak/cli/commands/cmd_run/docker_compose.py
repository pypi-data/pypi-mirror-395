"""
Gestión de Docker Compose para el comando run
"""
import os
import subprocess
from pathlib import Path
import click


def get_docker_compose_path() -> Path:
    """Encontrar el archivo docker-compose.yml."""
    # Buscar desde el directorio actual hacia arriba
    current_dir = Path.cwd()
    
    # Posibles ubicaciones del docker-compose
    possible_paths = [
        current_dir / "keycloak" / "docker-compose.yml",
        current_dir / "keycloak" / "docker" / "docker-compose.yml",
        current_dir / "docker-compose.yml",
        current_dir / "docker" / "docker-compose.yml",
        Path(__file__).parent.parent.parent.parent / "docker" / "docker-compose.yml"
    ]
    
    for path in possible_paths:
        if path.exists():
            return path.parent  # Retornar el directorio que contiene docker-compose.yml
    
    click.echo("❌ " + click.style("No se encontró docker-compose.yml", fg='red'))
    click.echo("💡 Primero ejecuta 'tai-kc init' para inicializar los recursos de Keycloak")
    return None


def run_docker_compose(compose_dir: Path, detach: bool, build: bool):
    """Ejecutar docker-compose."""
    click.echo("🐳 " + click.style("Iniciando contenedores...", fg='yellow'), nl=False)
    
    # Cambiar al directorio del docker-compose
    original_dir = os.getcwd()
    os.chdir(compose_dir)
    
    try:
        # Construir comando
        cmd = ['docker-compose', 'up']
        if detach:
            cmd.append('-d')
        if build:
            cmd.append('--build')
        
        # Ejecutar docker-compose
        if detach:
            # En modo detach, capturar salida
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                click.echo("\r   ✅ " + click.style("Contenedores iniciados en segundo plano", fg='green') + " " * 20)
                click.echo()
            else:
                click.echo("\r   ❌ " + click.style("Error iniciando contenedores:", fg='red') + " " * 20)
                click.echo(result.stderr)
                click.echo()
                return
        else:
            # En modo interactivo, mostrar salida en tiempo real
            click.echo("\r   📋 " + click.style("Logs del contenedor:", fg='cyan') + " " * 20)
            click.echo()
            subprocess.run(cmd)
    
    finally:
        # Volver al directorio original
        os.chdir(original_dir)


def run_docker_compose_detached(compose_dir: Path, build: bool, profile: str = "development", db: str = "embedded"):
    """Ejecutar docker-compose siempre en modo detach con el profile especificado.
    
    Args:
        compose_dir: Directorio donde está el docker-compose.yml
        build: Si se debe hacer rebuild
        profile: Profile de docker-compose (development, development-db, production, onpremise)
        db: Modo de base de datos para mostrar información (embedded, docker, external)
    """
    mode_labels = {
        'embedded': 'H2 embebida',
        'docker': 'PostgreSQL en Docker',
        'external': 'Base de datos externa'
    }
    
    profile_label = f" (profile: {profile}, modo: {mode_labels.get(db, db)})" if profile != "development" else f" (modo: {mode_labels.get(db, db)})"
    click.echo("🐳 " + click.style(f"Iniciando contenedores en segundo plano{profile_label}...", fg='yellow'), nl=False)
    
    # Cambiar al directorio del docker-compose
    original_dir = os.getcwd()
    os.chdir(compose_dir)
    
    try:
        # Configurar DEPLOYMENT_MODE según el perfil
        # tai-kc run solo usa development o development-db (siempre modo desarrollo)
        deployment_mode_map = {
            'development': 'development',
            'development-docker-db': 'development-db',
            'development-external-db': 'development-db'
        }
        deployment_mode = deployment_mode_map.get(profile, 'development')
        
        # Exportar DEPLOYMENT_MODE para docker-compose
        env = os.environ.copy()
        env['DEPLOYMENT_MODE'] = deployment_mode
        
        # Construir comando - siempre detach
        cmd = ['docker-compose', '--profile', profile, 'up', '-d']
        if build:
            cmd.append('--build')

        # Ejecutar docker-compose con el entorno configurado
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if result.returncode == 0:
            click.echo("\r   ✅ " + click.style("Contenedores iniciados exitosamente", fg='green') + " " * 20)
            click.echo()
        else:
            click.echo("\r   ❌ " + click.style("Error iniciando contenedores:", fg='red') + " " * 20)
            click.echo(result.stderr)
            click.echo()
            raise Exception("Error al iniciar contenedores")
    
    finally:
        # Volver al directorio original
        os.chdir(original_dir)


def cleanup_containers(compose_dir: Path, profile: str = "development"):
    """Limpiar contenedores del profile especificado."""
    if compose_dir:
        click.echo("\n🧹 " + click.style("Limpiando contenedores...", fg='yellow'), nl=False)
        original_dir = os.getcwd()
        try:
            os.chdir(compose_dir)
            # Usar --profile para asegurar que se detengan los contenedores correctos
            subprocess.run(['docker-compose', '--profile', profile, 'down', '-v'], 
                         capture_output=True, text=True)
            click.echo("\r   ✅ " + click.style("Limpieza completada", fg='green') + " " * 20)
            click.echo()
        except Exception as e:
            click.echo(f"\r   ❌ Error durante limpieza: {e}" + " " * 20)
            click.echo()
        finally:
            os.chdir(original_dir)