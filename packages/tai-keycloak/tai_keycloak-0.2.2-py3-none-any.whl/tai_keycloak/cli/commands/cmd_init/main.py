"""
Comando init: Inicializar recursos de Keycloak en el proyecto
"""
import os
import shutil
from pathlib import Path
import click


def get_package_resources_path() -> Path:
    """Obtener la ruta a los recursos de docker en el paquete instalado."""
    return Path(__file__).parent.parent.parent.parent / "docker"


def copy_docker_resources(target_dir: Path, deployment_mode: str):
    """Copiar recursos de docker al directorio objetivo."""
    source_dir = get_package_resources_path()
    
    if not source_dir.exists():
        raise FileNotFoundError(f"No se encontraron recursos en {source_dir}")
    
    # Archivos a copiar siempre
    essential_files = [
        "Dockerfile",
        "docker-compose.yml",
        "main-realm.json",
        ".gitignore",
        "README.md"
    ]
    
    # Archivo .env según el modo
    env_file_map = {
        "development": ".env.development",
        "azure": ".env.azure",
        "onpremise": ".env.onpremise"
    }
    
    click.echo("📁 " + click.style("Copiando recursos de Keycloak...", fg='yellow'))
    
    # Copiar archivos esenciales
    for filename in essential_files:
        source = source_dir / filename
        target = target_dir / filename
        
        if source.exists():
            shutil.copy2(source, target)
            click.echo(f"   ✅ {filename}")
        else:
            click.echo(f"   ⚠️  {filename} no encontrado")
    
    # Copiar archivo .env apropiado como .env
    env_source_file = env_file_map.get(deployment_mode)
    if env_source_file:
        source = source_dir / env_source_file
        target = target_dir / ".env"
        
        if source.exists():
            shutil.copy2(source, target)
            click.echo(f"   ✅ .env (desde {env_source_file})")
        else:
            click.echo(f"   ⚠️  {env_source_file} no encontrado")
    
    # Copiar también el .env.example
    source = source_dir / ".env.example"
    target = target_dir / ".env.example"
    if source.exists():
        shutil.copy2(source, target)
        click.echo(f"   ✅ .env.example")
    
    # Copiar carpeta traefik si es onpremise
    if deployment_mode == "onpremise":
        source_traefik = source_dir / "traefik"
        target_traefik = target_dir / "traefik"
        
        if source_traefik.exists():
            shutil.copytree(source_traefik, target_traefik, dirs_exist_ok=True)
            click.echo(f"   ✅ traefik/ (configuración para on-premise)")
    
    click.echo()


def copy_workflow(target_workflow_dir: Path, deployment_mode: str):
    """Copiar workflow de GitHub Actions si es deployment en cloud."""
    if deployment_mode != "azure":
        return
    
    source_dir = get_package_resources_path() / "workflows"
    workflow_file = "deploy-azure.yml"
    source = source_dir / workflow_file
    
    if not source.exists():
        click.echo(f"⚠️  " + click.style(f"Workflow {workflow_file} no encontrado", fg='yellow'))
        return
    
    # Crear directorio .github/workflows si no existe
    target_workflow_dir.mkdir(parents=True, exist_ok=True)
    
    target = target_workflow_dir / workflow_file
    shutil.copy2(source, target)
    
    click.echo("🔄 " + click.style("Workflow de CI/CD copiado:", fg='green'))
    click.echo(f"   ✅ .github/workflows/{workflow_file}")
    click.echo()


def show_next_steps(deployment_mode: str, keycloak_dir: Path):
    """Mostrar instrucciones de los siguientes pasos."""
    click.echo()
    click.echo("🎉 " + click.style("¡Inicialización completada exitosamente!", fg='green', bold=True))
    click.echo()
    click.echo("📝 " + click.style("Siguientes pasos:", fg='cyan', bold=True))
    click.echo()
    
    if deployment_mode == "development":
        click.echo("1️⃣  Revisa y ajusta las variables en keycloak/.env")
        click.echo("2️⃣  Inicia Keycloak con:")
        click.echo("   " + click.style('tai-kc run', fg='green', bold=True))
        click.echo()
        click.echo("💡 Para desarrollo con PostgreSQL:")
        click.echo("   " + click.style('tai-kc run --db docker', fg='green', bold=True))
        
    elif deployment_mode == "azure":
        click.echo("1️⃣  Configura los secretos en GitHub:")
        click.echo("   - Ve a Settings → Secrets and variables → Actions")
        click.echo("   - Agrega los secretos listados en .github/workflows/deploy-azure.yml")
        click.echo()
        click.echo("2️⃣  Configura tu Azure Database for PostgreSQL")
        click.echo()
        click.echo("3️⃣  Edita keycloak/.env con tus valores de Azure")
        click.echo()
        click.echo("4️⃣  Haz commit y push a la rama main/production:")
        click.echo("   " + click.style('git add .', fg='green'))
        click.echo("   " + click.style('git commit -m "Add Keycloak deployment"', fg='green'))
        click.echo("   " + click.style('git push origin main', fg='green'))
        click.echo()
        click.echo("5️⃣  El workflow se ejecutará automáticamente y desplegará a Azure")
        click.echo()
        click.echo("💡 Para pruebas locales antes de Azure:")
        click.echo("   " + click.style('tai-kc run --db external', fg='green', bold=True))
        click.echo("   (Asegúrate de configurar DEPLOYMENT_MODE=azure en .env)")
        
    elif deployment_mode == "onpremise":
        click.echo("1️⃣  Coloca tus certificados SSL en:")
        click.echo("   keycloak/traefik/certs/cert.pem")
        click.echo("   keycloak/traefik/certs/key.pem")
        click.echo()
        click.echo("2️⃣  Configura tu servidor PostgreSQL externo")
        click.echo()
        click.echo("3️⃣  Edita keycloak/.env con tus valores:")
        click.echo("   - KC_HOSTNAME (tu dominio)")
        click.echo("   - Credenciales de PostgreSQL")
        click.echo("   - Credenciales de admin de Keycloak")
        click.echo()
        click.echo("4️⃣  Inicia Keycloak con Traefik:")
        click.echo("   " + click.style('tai-kc run --db external', fg='green', bold=True))
        click.echo("   (DEPLOYMENT_MODE=onpremise debe estar configurado en .env)")
        click.echo()
        click.echo("💡 Asegúrate de que los puertos 80 y 443 estén abiertos")
    
    click.echo()
    click.echo("📚 " + click.style("Documentación completa:", fg='cyan'))
    click.echo(f"   {keycloak_dir / 'README.md'}")
    click.echo()


@click.command()
@click.option(
    '--mode',
    type=click.Choice(['development', 'azure', 'onpremise'], case_sensitive=False),
    prompt='Selecciona el modo de deployment',
    help='Modo de deployment: development (local), azure (Azure Web Apps), onpremise (con Traefik)'
)
@click.option(
    '--force',
    is_flag=True,
    help='Sobrescribir archivos existentes sin preguntar'
)
def init(mode: str, force: bool):
    """
    Inicializar recursos de Keycloak en el proyecto actual.
    
    Crea una carpeta 'keycloak/' con todos los recursos necesarios para
    ejecutar Keycloak según el modo de deployment seleccionado.
    """
    
    click.echo("🔐 " + click.style("Inicializando recursos de Keycloak", fg='cyan', bold=True))
    click.echo()
    
    # Directorios objetivo
    cwd = Path.cwd()
    keycloak_dir = cwd / "keycloak"
    workflow_dir = cwd / ".github" / "workflows"
    
    # Verificar si ya existe la carpeta keycloak
    if keycloak_dir.exists() and not force:
        click.echo(f"⚠️  " + click.style("La carpeta 'keycloak/' ya existe", fg='yellow'))
        
        if not click.confirm("¿Deseas sobrescribir los archivos?", default=False):
            click.echo("❌ Operación cancelada")
            return
    
    # Crear directorio keycloak
    keycloak_dir.mkdir(exist_ok=True)
    
    # Modo seleccionado
    mode_labels = {
        "development": "🛠️  Desarrollo Local (H2 database)",
        "azure": "☁️  Azure Web Apps (PostgreSQL + CI/CD)",
        "onpremise": "🏢 On-Premise (Traefik + PostgreSQL + HTTPS)"
    }
    
    click.echo(f"📦 Modo seleccionado: {click.style(mode_labels[mode], fg='green', bold=True)}")
    click.echo()
    
    try:
        # Copiar recursos de docker
        copy_docker_resources(keycloak_dir, mode)
        
        # Copiar workflow si es Azure
        if mode == "azure":
            copy_workflow(workflow_dir, mode)
        
        # Mostrar siguientes pasos
        show_next_steps(mode, keycloak_dir)
        
    except Exception as e:
        click.echo()
        click.echo("❌ " + click.style(f"Error durante la inicialización: {e}", fg='red'))
        click.echo()
        
        # Limpiar si hubo error
        if click.confirm("¿Deseas limpiar los archivos creados?", default=True):
            if keycloak_dir.exists():
                shutil.rmtree(keycloak_dir)
                click.echo("🧹 Carpeta keycloak/ eliminada")
            
            if mode == "azure" and workflow_dir.exists():
                workflow_file = workflow_dir / "deploy-azure.yml"
                if workflow_file.exists():
                    workflow_file.unlink()
                    click.echo("🧹 Workflow eliminado")
        
        raise
