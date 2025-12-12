# Keycloak Docker Configuration

Esta carpeta contiene todos los recursos necesarios para ejecutar Keycloak en diferentes modos de despliegue.

## 🎯 Modos de Despliegue

### 1. Development (H2 Database)
Modo más simple para desarrollo local con base de datos en memoria.

**Características:**
- Base de datos H2 en memoria
- No requiere PostgreSQL
- Datos se pierden al reiniciar
- Ideal para pruebas rápidas

**Uso:**
```bash
tai-kc run
# o explícitamente:
tai-kc run --db embedded
```

**Archivo de configuración:** `.env.development`

---

### 2. Development-DB (PostgreSQL en Docker)
Modo desarrollo con PostgreSQL para persistencia de datos.

**Características:**
- PostgreSQL 16 en Docker
- Datos persistentes en volumen Docker
- Útil para desarrollo que requiere persistencia
- Puede usar PostgreSQL externa también

**Uso:**
```bash
tai-kc run --db docker
```

**Archivo de configuración:** `.env.development` (con variables de BD descomentadas)

---

### 3. Azure (Azure Web Apps)
Modo optimizado para despliegue en Azure Web Apps.

**Características:**
- Puerto 80 (requerido por Azure)
- PostgreSQL externa (Azure Database for PostgreSQL)
- Modo optimizado con `start --optimized`
- Proxy edge habilitado

**Uso local:**
```bash
# Configurar DEPLOYMENT_MODE=azure en .env
tai-kc run --db external
```

**Archivo de configuración:** `.env.azure`

**Requisitos:**
- Azure Database for PostgreSQL configurado
- Variables de entorno configuradas en Azure Web App
- CI/CD configurado con GitHub Actions

---

### 4. OnPremise (Traefik + HTTPS)
Modo para despliegue on-premise con reverse proxy y HTTPS.

**Características:**
- Traefik como reverse proxy
- HTTPS con certificados SSL
- PostgreSQL externa
- Variables de HOSTNAME y PROXY configurables

**Uso:**
```bash
# Configurar DEPLOYMENT_MODE=onpremise en .env
tai-kc run --db external
```

**Archivo de configuración:** `.env.onpremise`

**Requisitos:**
- Certificados SSL en `traefik/certs/`
- PostgreSQL externa configurada
- Puertos 80 y 443 abiertos
- DNS apuntando al servidor

---

## 📁 Estructura de Archivos

```
docker/
├── Dockerfile              # Dockerfile multi-stage
├── docker-compose.yml      # Docker Compose con profiles
├── main-realm.json         # Realm preconfigurado
├── .env.development        # Config para development
├── .env.azure             # Config para Azure
├── .env.onpremise         # Config para on-premise
├── .env.example           # Plantilla de variables
├── .gitignore             # Archivos a ignorar
├── README.md              # Esta documentación
├── traefik/               # Configuración de Traefik
│   ├── certs/            # Certificados SSL
│   └── dynamic/          # Configuración dinámica
└── workflows/             # GitHub Actions workflows
    └── deploy-azure.yml  # Workflow para Azure
```

---

## 🔧 Variables de Entorno

### Variables Comunes

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `KEYCLOAK_VERSION` | Versión de Keycloak | Sí |
| `DEPLOYMENT_MODE` | Modo de despliegue | Sí |
| `KC_BOOTSTRAP_ADMIN_USERNAME` | Usuario admin | Sí |
| `KC_BOOTSTRAP_ADMIN_PASSWORD` | Password admin | Sí |
| `KEYCLOAK_API_CLIENT_SECRET` | Secret del cliente API | Sí |
| `KC_HTTP_PORT` | Puerto HTTP | Sí |
| `KC_LOG_LEVEL` | Nivel de logs | No |

### Variables de Base de Datos (development-db, azure, onpremise)

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `KC_DB` | Tipo de BD (postgres, mysql) | Sí |
| `KC_DRIVER` | Driver JDBC | Sí |
| `KC_DB_URL_HOST` | Host de la BD | Sí |
| `KC_DB_URL_PORT` | Puerto de la BD | Sí |
| `KC_DB_URL_DATABASE` | Nombre de la BD | Sí |
| `KC_DB_USERNAME` | Usuario de la BD | Sí |
| `KC_DB_PASSWORD` | Password de la BD | Sí |

### Variables de Proxy (azure, onpremise)

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `KC_HOSTNAME` | Hostname público | Sí (prod) |
| `KC_HOSTNAME_PATH` | Path base | No |
| `KC_PROXY_HEADERS` | Headers del proxy | No |

---

## 🚀 Guía de Inicio Rápido

### Desarrollo Local (H2)
```bash
# 1. Copiar configuración
cp .env.development .env

# 2. Iniciar Keycloak
tai-kc run

# 3. Acceder a:
#    http://localhost:8090
#    Usuario: admin
#    Password: admin
```

### Desarrollo con PostgreSQL
```bash
# 1. Copiar configuración
cp .env.development .env

# 2. Iniciar con PostgreSQL
tai-kc run --db docker

# 3. Acceder a:
#    http://localhost:8090
#    PostgreSQL: localhost:5432
```

### Azure Web Apps
```bash
# 1. Configurar Azure Database for PostgreSQL
# 2. Copiar y editar configuración
cp .env.azure .env
# Editar .env con los valores de Azure

# 3. Configurar GitHub Secrets
# 4. Push a main/production para desplegar
git push origin main
```

### On-Premise
```bash
# 1. Configurar PostgreSQL externa
# 2. Copiar y editar configuración
cp .env.onpremise .env
# Editar .env con tus valores

# 3. Colocar certificados SSL
cp cert.pem traefik/certs/
cp key.pem traefik/certs/

# 4. Iniciar con Traefik
tai-kc run --db external

# 5. Acceder a:
#    https://tu-dominio.com
```

---

## 🔍 Troubleshooting

### Keycloak no inicia
1. Verificar logs: `docker logs keycloak`
2. Verificar que Docker esté corriendo: `docker info`
3. Verificar que el puerto no esté ocupado: `netstat -an | grep 8090`

### Error de conexión a BD
1. Verificar que PostgreSQL esté corriendo
2. Verificar credenciales en `.env`
3. Verificar que la BD `keycloak` exista
4. En Docker, usar `host.docker.internal` (no `localhost`)

### Traefik no arranca
1. Verificar que los certificados existan en `traefik/certs/`
2. Verificar configuración en `traefik/dynamic/tls.yml`
3. Verificar que los puertos 80 y 443 estén disponibles

### Health check falla
1. Esperar más tiempo (puede tardar 60-90s en producción)
2. Verificar logs del contenedor
3. Verificar conexión a la BD

---

## 📚 Documentación Adicional

- [Dockerfile Multi-Stage](../../keycloak/DOCKER_STAGES.md)
- [Keycloak Official Docs](https://www.keycloak.org/documentation)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Traefik Docs](https://doc.traefik.io/traefik/)

---

## 🔐 Seguridad

### Desarrollo
- ✅ Credenciales por defecto están bien para desarrollo
- ✅ H2 en memoria es seguro para pruebas locales

### Producción (Azure/OnPremise)
- ⚠️ **CAMBIAR** todas las contraseñas por defecto
- ⚠️ **USAR** secretos seguros (Azure Key Vault, etc.)
- ⚠️ **HABILITAR** HTTPS siempre
- ⚠️ **CONFIGURAR** firewall y reglas de red
- ⚠️ **AUDITAR** logs regularmente

---

## 🤝 Contribuir

Si encuentras algún problema o tienes sugerencias:
1. Reporta el issue en GitHub
2. Propón mejoras vía Pull Request
3. Actualiza la documentación si es necesario
