"""
Mostrar información del servicio iniciado
"""
import os
import click


def get_keycloak_config():
    """
    Obtener configuración de Keycloak desde variables de entorno.
    
    Returns:
        tuple: (admin_user, admin_password, host, port, from_env)
    """
    # Credenciales de admin
    admin_user = os.environ.get('KC_BOOTSTRAP_ADMIN_USERNAME', 'admin')
    admin_password = os.environ.get('KC_BOOTSTRAP_ADMIN_PASSWORD', 'admin')
    
    # HTTP Configuration
    port = os.environ.get('KC_HTTP_PORT', '8090')
    
    # Hostname (puede no estar definido en desarrollo)
    hostname = os.environ.get('KC_HOSTNAME', '')
    
    # Si hay hostname configurado, usarlo (para producción/onpremise)
    if hostname:
        # Limpiar el hostname si viene con protocolo
        if hostname.startswith('http://') or hostname.startswith('https://'):
            protocol = 'https' if hostname.startswith('https://') else 'http'
            host = hostname.replace('http://', '').replace('https://', '').rstrip('/')
        else:
            protocol = 'http'
            host = hostname
        
        from_env = True
    else:
        # Modo desarrollo: localhost
        protocol = 'http'
        host = 'localhost'
        from_env = 'KC_BOOTSTRAP_ADMIN_USERNAME' in os.environ
    
    return admin_user, admin_password, protocol, host, port, from_env


def show_service_info():
    """Mostrar información del servicio iniciado."""
    click.echo()
    click.echo("🎉 " + click.style("¡Keycloak iniciado exitosamente!", fg='green', bold=True))
    click.echo()
    
    # Obtener configuración de Keycloak
    admin_user, admin_password, protocol, host, port, from_env = get_keycloak_config()
    
    # Construir base_url
    if port in ['80', '443'] or (protocol == 'https' and port == '443') or (protocol == 'http' and port == '80'):
        base_url = f"{protocol}://{host}"
    else:
        base_url = f"{protocol}://{host}:{port}"
    
    # URLs útiles
    admin_url = f"{base_url}/admin"
    realms_url = f"{base_url}/realms/master"
    
    # Mostrar origen de la configuración
    if from_env:
        config_source = click.style("variables de entorno", fg='yellow', bold=True)
        config_icon = "🔧"
    else:
        config_source = click.style("valores por defecto", fg='cyan')
        config_icon = "⚙️"
    
    click.echo(f"{config_icon} " + click.style("Configuración:", fg='cyan', bold=True) + f" {config_source}")
    click.echo()
    
    click.echo("🔗 " + click.style("URLs del servicio:", fg='cyan', bold=True))
    click.echo(f"   🏠 Página principal: {click.style(base_url, fg='blue', underline=True)}")
    click.echo(f"   👨‍💼 Consola de admin: {click.style(admin_url, fg='blue', underline=True)}")
    click.echo(f"   🔐 Realm master:     {click.style(realms_url, fg='blue', underline=True)}")
    click.echo()
    
    click.echo("🔑 " + click.style("Credenciales de administrador:", fg='cyan', bold=True))
    click.echo(f"   👤 Usuario: {click.style(admin_user, fg='green')}")
    
    # Mejorar el mensaje de la contraseña según el origen
    if from_env and admin_password != 'admin':
        masked = '*' * len(admin_password)
        click.echo(f"   🔒 Password: {click.style(masked, fg='green')} (personalizado)")
    else:
        click.echo(f"   🔒 Password: {click.style(admin_password, fg='green')} (por defecto - desarrollo)")
    
    click.echo()
    
    # Información de base de datos
    db_type = os.environ.get('KC_DB', None)
    db_host = os.environ.get('KC_DB_URL_HOST', None)
    
    if db_type and db_host:
        db_name = os.environ.get('KC_DB_URL_DATABASE', 'keycloak')
        db_port = os.environ.get('KC_DB_URL_PORT', '5432')
        click.echo("💾 " + click.style("Base de datos:", fg='cyan', bold=True))
        click.echo(f"   Tipo: {click.style(db_type.upper(), fg='green')}")
        click.echo(f"   Host: {click.style(db_host, fg='green')}")
        click.echo(f"   Puerto: {click.style(db_port, fg='green')}")
        click.echo(f"   Database: {click.style(db_name, fg='green')}")
        click.echo()
    elif db_type == 'postgres' and not db_host:
        # Probablemente modo development-db con postgres en docker-compose
        db_name = os.environ.get('KC_DB_URL_DATABASE', 'keycloak')
        click.echo("💾 " + click.style("Base de datos:", fg='cyan', bold=True))
        click.echo(f"   Tipo: {click.style('PostgreSQL (Docker)', fg='green')}")
        click.echo(f"   Database: {click.style(db_name, fg='green')}")
        click.echo()
    
    # Comandos útiles
    click.echo("📋 " + click.style("Control del servidor:", fg='cyan', bold=True))
    click.echo("   ✋ Detener servidor: Presiona Ctrl+C (limpia automáticamente)")
    click.echo("   📝 Ver logs: docker-compose logs -f keycloak")
    click.echo()
    
    # Tips adicionales
    click.echo("💡 " + click.style("Tips:", fg='magenta', bold=True))
    click.echo("   🌐 El servidor puede tardar unos segundos en estar completamente listo")
    click.echo("   🔧 Este proceso mantendrá el servidor activo hasta que lo detengas")
    
    if from_env:
        click.echo("   📝 Configuración obtenida de variables de entorno (.env)")
    else:
        click.echo("   🚀 Usando configuración por defecto (desarrollo)")
        click.echo("   📝 Para personalizar, crea un archivo .env o usa tai-kc init")
    
    click.echo()