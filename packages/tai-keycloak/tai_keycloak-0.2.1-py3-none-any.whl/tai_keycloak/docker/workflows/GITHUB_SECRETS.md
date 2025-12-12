# GitHub Secrets Configuration for Azure Deployment

Este documento describe cómo configurar los secretos necesarios en GitHub para el deployment automático a Azure Web Apps.

## 📋 Secretos Requeridos

Navega a tu repositorio → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### 1. Azure Credentials

**`AZURE_CREDENTIALS`**
```json
{
  "clientId": "<service-principal-client-id>",
  "clientSecret": "<service-principal-client-secret>",
  "subscriptionId": "<azure-subscription-id>",
  "tenantId": "<azure-tenant-id>"
}
```

**Cómo obtenerlo:**
```bash
# Crear Service Principal con permisos de Contributor
az ad sp create-for-rbac \
  --name "keycloak-deployment" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group> \
  --sdk-auth
```

---

### 2. Azure Container Registry (ACR)

**`ACR_LOGIN_SERVER`**
- Ejemplo: `myregistry.azurecr.io`
- Obtener: Azure Portal → Container Registry → Login server

**`ACR_USERNAME`**
- Usuario del ACR
- Obtener: Azure Portal → Container Registry → Access keys → Username

**`ACR_PASSWORD`**
- Contraseña del ACR
- Obtener: Azure Portal → Container Registry → Access keys → Password

---

### 3. Azure Web App

**`AZURE_WEBAPP_NAME`**
- Nombre de tu Azure Web App
- Ejemplo: `my-keycloak-app`

---

### 4. Keycloak Admin Credentials

**`KC_BOOTSTRAP_ADMIN_USERNAME`**
- Usuario administrador de Keycloak
- Ejemplo: `admin`

**`KC_BOOTSTRAP_ADMIN_PASSWORD`**
- Contraseña del administrador
- ⚠️ **Usar contraseña segura en producción**

**`KEYCLOAK_API_CLIENT_SECRET`**
- Secret para el cliente API de Keycloak
- Generar: `openssl rand -base64 32`

---

### 5. PostgreSQL Database

**`KC_DB_URL_HOST`**
- Host del Azure Database for PostgreSQL
- Ejemplo: `mypostgres.postgres.database.azure.com`

**`KC_DB_USERNAME`**
- Usuario de PostgreSQL
- Formato Azure: `username@servername`
- Ejemplo: `keycloak@mypostgres`

**`KC_DB_PASSWORD`**
- Contraseña de PostgreSQL

---

### 6. Public Hostname

**`KC_HOSTNAME`**
- URL pública de tu aplicación
- Ejemplo: `https://my-keycloak-app.azurewebsites.net`

---

## 🚀 Verificar Configuración

Una vez configurados todos los secretos:

1. Ve a **Actions** en tu repositorio
2. Verifica que no haya errores de configuración
3. Haz un push a `main` o `production` para trigger el workflow

```bash
git add .
git commit -m "Configure Keycloak deployment"
git push origin main
```

---

## 📊 Checklist de Secretos

- [ ] `AZURE_CREDENTIALS`
- [ ] `ACR_LOGIN_SERVER`
- [ ] `ACR_USERNAME`
- [ ] `ACR_PASSWORD`
- [ ] `AZURE_WEBAPP_NAME`
- [ ] `KC_BOOTSTRAP_ADMIN_USERNAME`
- [ ] `KC_BOOTSTRAP_ADMIN_PASSWORD`
- [ ] `KEYCLOAK_API_CLIENT_SECRET`
- [ ] `KC_DB_URL_HOST`
- [ ] `KC_DB_USERNAME`
- [ ] `KC_DB_PASSWORD`
- [ ] `KC_HOSTNAME`

---

## 🔒 Mejores Prácticas

1. **Nunca commitear secretos** en el código
2. Usar **Azure Key Vault** para secretos en producción
3. **Rotar credenciales** periódicamente
4. Usar **contraseñas seguras** (mínimo 16 caracteres)
5. Limitar **permisos del Service Principal** al mínimo necesario

---

## 🆘 Troubleshooting

### Error: "Invalid service principal"
- Verificar que el JSON de `AZURE_CREDENTIALS` esté bien formado
- Confirmar que el Service Principal tenga permisos de Contributor

### Error: "Cannot connect to ACR"
- Verificar `ACR_LOGIN_SERVER`, `ACR_USERNAME`, `ACR_PASSWORD`
- Confirmar que el ACR exista y esté accesible

### Error: "Database connection failed"
- Verificar credenciales de PostgreSQL
- Confirmar que Azure Web App esté en la whitelist del firewall de PostgreSQL

---

## 📚 Referencias

- [Azure Service Principal](https://learn.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/)
- [Azure Web Apps](https://learn.microsoft.com/en-us/azure/app-service/)
