# =============================================================================
# Keycloak Dockerfile Unificado
# Soporta múltiples modos de despliegue: development, development-db, azure, onpremise
# =============================================================================
# Versión fija de Keycloak para evitar breaking changes
ARG KEYCLOAK_VERSION=26.4.5
ARG DEPLOYMENT_MODE=development

# =============================================================================
# Stage: Base - Configuración común para todos los modos
# =============================================================================
FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION} AS base

# Metadatos
LABEL maintainer="MateoSaezMata <msaez@triplealpha.in>"
LABEL description="Keycloak unified instance - supports development, development-db, azure, and on-premise deployments"
LABEL version="3.0.0"

# Copiar realm preconfigurado
COPY main-realm.json /opt/keycloak/data/import/

# Crear directorio para logs y configurar permisos
USER root
RUN mkdir -p /opt/keycloak/logs && \
    chown -R keycloak:keycloak /opt/keycloak/logs /opt/keycloak/data
USER keycloak

# =============================================================================
# Stage: Development - Modo desarrollo con H2 database (sin BD externa)
# =============================================================================
FROM base AS development

# Admin credentials (valores por defecto para desarrollo)
ARG KC_BOOTSTRAP_ADMIN_USERNAME=admin
ARG KC_BOOTSTRAP_ADMIN_PASSWORD=admin
ARG KEYCLOAK_API_CLIENT_SECRET=dev-secret

# HTTP Configuration
ARG KC_HTTP_PORT=8090
ARG KC_LOG_LEVEL=INFO

ENV KC_BOOTSTRAP_ADMIN_USERNAME=${KC_BOOTSTRAP_ADMIN_USERNAME}
ENV KC_BOOTSTRAP_ADMIN_PASSWORD=${KC_BOOTSTRAP_ADMIN_PASSWORD}
ENV KEYCLOAK_API_CLIENT_SECRET=${KEYCLOAK_API_CLIENT_SECRET}
ENV KC_HTTP_PORT=${KC_HTTP_PORT}
ENV KC_LOG_LEVEL=${KC_LOG_LEVEL}

# Configuración específica de desarrollo
ENV KC_HTTP_ENABLED=true
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# Exponer puerto HTTP
EXPOSE ${KC_HTTP_PORT}

# Healthcheck
HEALTHCHECK --interval=10s --timeout=10s --start-period=30s --retries=5 \
    CMD { printf 'GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n' >&3; cat <&3 | head -1 | grep '200'; } 3<>/dev/tcp/localhost/9000

# Comando para modo desarrollo con H2 e import de realm
CMD ["start-dev", "--import-realm"]

# =============================================================================
# Stage: DB - Configuración base de base de datos (reutilizable)
# =============================================================================
FROM base AS db

# Database configuration (valores por defecto)
ARG KC_DB=postgres
ARG KC_DRIVER=postgresql
ARG KC_DB_URL_HOST=postgres
ARG KC_DB_URL_PORT=5432
ARG KC_DB_URL_DATABASE=keycloak
ARG KC_DB_USERNAME=keycloak
ARG KC_DB_PASSWORD=keycloak

ENV KC_DB=${KC_DB}
ENV KC_DRIVER=${KC_DRIVER}
ENV KC_DB_URL_HOST=${KC_DB_URL_HOST}
ENV KC_DB_URL_PORT=${KC_DB_URL_PORT}
ENV KC_DB_URL_DATABASE=${KC_DB_URL_DATABASE}
ENV KC_DB_USERNAME=${KC_DB_USERNAME}
ENV KC_DB_PASSWORD=${KC_DB_PASSWORD}

# Construir la URL JDBC completa
ENV KC_DB_URL=jdbc:${KC_DRIVER}://${KC_DB_URL_HOST}:${KC_DB_URL_PORT}/${KC_DB_URL_DATABASE}

# Build de Keycloak con la configuración de BD
USER root
RUN /opt/keycloak/bin/kc.sh build --db=${KC_DB}
USER keycloak

# Configuración común para BD
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# =============================================================================
# Stage: Development-DB - Modo desarrollo con PostgreSQL (Docker o externa)
# =============================================================================
FROM db AS development-db

# Admin credentials (valores por defecto para desarrollo)
ARG KC_BOOTSTRAP_ADMIN_USERNAME=admin
ARG KC_BOOTSTRAP_ADMIN_PASSWORD=admin
ARG KEYCLOAK_API_CLIENT_SECRET=dev-secret

# HTTP Configuration
ARG KC_HTTP_PORT=8090
ARG KC_LOG_LEVEL=INFO

ENV KC_BOOTSTRAP_ADMIN_USERNAME=${KC_BOOTSTRAP_ADMIN_USERNAME}
ENV KC_BOOTSTRAP_ADMIN_PASSWORD=${KC_BOOTSTRAP_ADMIN_PASSWORD}
ENV KEYCLOAK_API_CLIENT_SECRET=${KEYCLOAK_API_CLIENT_SECRET}
ENV KC_HTTP_PORT=${KC_HTTP_PORT}
ENV KC_LOG_LEVEL=${KC_LOG_LEVEL}

# Configuración de desarrollo
ENV KC_HTTP_ENABLED=true

# Exponer puerto HTTP
EXPOSE ${KC_HTTP_PORT}

# Healthcheck
HEALTHCHECK --interval=10s --timeout=10s --start-period=30s --retries=5 \
    CMD { printf 'GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n' >&3; cat <&3 | head -1 | grep '200'; } 3<>/dev/tcp/localhost/9000

# Comando para modo desarrollo con BD e import de realm
CMD ["start-dev", "--import-realm"]

# =============================================================================
# Stage: Azure - Modo Azure Web Apps con puerto 80 y BD externa
# =============================================================================
FROM db AS azure

# Admin credentials (DEBEN proveerse en runtime)
ARG KC_BOOTSTRAP_ADMIN_USERNAME
ARG KC_BOOTSTRAP_ADMIN_PASSWORD
ARG KEYCLOAK_API_CLIENT_SECRET

# Azure Web Apps requiere puerto 80
ARG KC_HTTP_PORT=80
ARG KC_LOG_LEVEL=INFO

ENV KC_BOOTSTRAP_ADMIN_USERNAME=${KC_BOOTSTRAP_ADMIN_USERNAME}
ENV KC_BOOTSTRAP_ADMIN_PASSWORD=${KC_BOOTSTRAP_ADMIN_PASSWORD}
ENV KEYCLOAK_API_CLIENT_SECRET=${KEYCLOAK_API_CLIENT_SECRET}
ENV KC_HTTP_PORT=${KC_HTTP_PORT}
ENV KC_LOG_LEVEL=${KC_LOG_LEVEL}

# Configuración para Azure
ENV KC_HTTP_ENABLED=true
ENV KC_PROXY=edge

# Exponer puerto 80 para Azure
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=5 \
    CMD { printf 'GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n' >&3; cat <&3 | head -1 | grep '200'; } 3<>/dev/tcp/localhost/9000

# Comando para modo producción optimizado con import de realm
CMD ["start", "--optimized", "--import-realm"]

# =============================================================================
# Stage: OnPremise - Modo on-premise con HOSTNAME, PROXY y BD externa
# =============================================================================
FROM db AS onpremise

# Admin credentials (DEBEN proveerse en runtime)
ARG KC_BOOTSTRAP_ADMIN_USERNAME
ARG KC_BOOTSTRAP_ADMIN_PASSWORD
ARG KEYCLOAK_API_CLIENT_SECRET

# HTTP Configuration
ARG KC_HTTP_PORT=8090
ARG KC_LOG_LEVEL=INFO

# Hostname y Proxy configuration (DEBEN proveerse en runtime)
ARG KC_HOSTNAME
ARG KC_HOSTNAME_PATH=/
ARG KC_PROXY_HEADERS=xforwarded

ENV KC_BOOTSTRAP_ADMIN_USERNAME=${KC_BOOTSTRAP_ADMIN_USERNAME}
ENV KC_BOOTSTRAP_ADMIN_PASSWORD=${KC_BOOTSTRAP_ADMIN_PASSWORD}
ENV KEYCLOAK_API_CLIENT_SECRET=${KEYCLOAK_API_CLIENT_SECRET}
ENV KC_HTTP_PORT=${KC_HTTP_PORT}
ENV KC_LOG_LEVEL=${KC_LOG_LEVEL}
ENV KC_HOSTNAME=${KC_HOSTNAME}
ENV KC_HOSTNAME_PATH=${KC_HOSTNAME_PATH}
ENV KC_PROXY_HEADERS=${KC_PROXY_HEADERS}

# Configuración específica de on-premise
ENV KC_HTTP_ENABLED=true
ENV KC_PROXY=edge

# Exponer puerto HTTP
EXPOSE ${KC_HTTP_PORT}

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=5 \
    CMD { printf 'GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n' >&3; cat <&3 | head -1 | grep '200'; } 3<>/dev/tcp/localhost/9000

# Comando para modo producción optimizado con import de realm
CMD ["start", "--optimized", "--import-realm"]

# =============================================================================
# Stage: Final - Selecciona el stage apropiado basado en DEPLOYMENT_MODE
# =============================================================================
FROM ${DEPLOYMENT_MODE} AS final

# Labels adicionales para tracking
LABEL deployment.mode=${DEPLOYMENT_MODE}
LABEL keycloak.version=${KEYCLOAK_VERSION}