# SemBicho CLI - Integración con Backend

## 🚀 Mejoras Implementadas

### ✅ Autenticación JWT Completa
- **Nuevo comando `auth`** para manejo de sesiones
- **Almacenamiento seguro** de tokens en `~/.sembicho/auth.json`
- **Auto-carga** del token en comandos de scan

### ✅ Conexión Backend Corregida
- **URL actualizada** a `/reports` (era `/api/results`)
- **Formato de datos correcto** para el schema `ReporteCreate`
- **Manejo de errores** mejorado con códigos HTTP específicos

### ✅ Configuración Mejorada
- **URLs separadas** para API y autenticación
- **Configuración por defecto** actualizada para container
- **Seguridad** de tokens (ocultos en `config --show`)

## 📋 Comandos Principales

### 🔐 Autenticación

```bash
# Iniciar sesión
python main.py auth login --email tu@email.com

# Con URL personalizada del backend
python main.py auth login --email tu@email.com --backend-url http://localhost:8000

# Ver estado de autenticación
python main.py auth status

# Cerrar sesión
python main.py auth logout
```

### 🔍 Escaneo de Seguridad

```bash
# Scan local (sin backend)
python main.py scan --path ./mi-proyecto

# Scan con envío automático al backend (usa token guardado)
python main.py scan --path ./mi-proyecto --api-url http://localhost:8000/reports

# Scan con token específico
python main.py scan --path . --token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# Scan con múltiples opciones
python main.py scan --path . --format json --output reporte.json --api-url http://localhost:8000/reports
```

### ⚙️ Configuración

```bash
# Crear configuración inicial
python main.py config --init

# Ver configuración actual
python main.py config --show
```

## 🐳 Configuración para Backend en Container

### 1. **Configurar URL del Container**

Si tu backend está en Docker, actualiza la configuración:

```json
{
  "api_url": "http://localhost:8000/reports",
  "auth_url": "http://localhost:8000/auth/login"
}
```

### 2. **Para Docker Compose con red personalizada:**

```json
{
  "api_url": "http://backend:8000/reports",
  "auth_url": "http://backend:8000/auth/login"
}
```

### 3. **Para producción con dominio:**

```json
{
  "api_url": "https://tu-dominio.com/reports",
  "auth_url": "https://tu-dominio.com/auth/login"
}
```

## 🔄 Flujo de Trabajo Completo

### Paso 1: Preparar Backend
```bash
cd backend
docker-compose up -d
```

### Paso 2: Configurar CLI
```bash
cd sembicho-cli
python main.py config --init
```

### Paso 3: Autenticarse
```bash
python main.py auth login --email tu@email.com
```

### Paso 4: Ejecutar Scan
```bash
python main.py scan --path ./mi-proyecto --api-url http://localhost:8000/reports
```

## 📊 Formato de Datos Enviados

El CLI ahora envía los datos en el formato correcto para tu backend:

```json
{
  "pipelineId": "sembicho-cli-proyecto-2024-10-03T...",
  "data": {
    "project_name": "mi-proyecto",
    "scan_date": "2024-10-03T12:00:00Z",
    "language": "python",
    "total_vulnerabilities": 5,
    "severity_counts": {
      "critical": 1,
      "high": 2,
      "medium": 1,
      "low": 1
    },
    "vulnerabilities": [...],
    "tools_used": ["bandit", "semgrep"]
  },
  "fecha": "2024-10-03T12:00:00Z"
}
```

## 🔒 Seguridad

- **Tokens JWT** almacenados con permisos restrictivos (`600`)
- **Contraseñas** nunca almacenadas, solo solicitadas en runtime
- **Configuración** separada entre credenciales y configuración general
- **Headers de autorización** correctos (`Bearer token`)

## 🐛 Solución de Problemas

### Error 401: Token inválido
```bash
python main.py auth logout
python main.py auth login --email tu@email.com
```

### Error de conexión
```bash
# Verificar que el backend esté ejecutándose
curl http://localhost:8000/docs

# Probar con URL específica
python main.py scan --path . --api-url http://localhost:8000/reports --backend-url http://localhost:8000
```

### Error de formato de datos
El CLI ahora maneja automáticamente el formato correcto. Si persisten errores, verifica:
1. ✅ Backend ejecutándose en puerto correcto
2. ✅ Usuario autenticado con `auth login`
3. ✅ Token válido con `auth status`

## 📝 Ejemplos de Uso

### Ejemplo 1: Primer uso
```bash
# Configuración inicial
python main.py config --init
python main.py auth login --email admin@empresa.com
python main.py scan --path ./src
```

### Ejemplo 2: Uso en CI/CD
```bash
# Login programático
echo "password" | python main.py auth login --email ci@empresa.com --password -

# Scan con fail en vulnerabilidades críticas
python main.py scan --path . --fail-on critical,high --ci-mode --api-url http://backend:8000/reports
```

### Ejemplo 3: Desarrollo local
```bash
# Scan local sin backend
python main.py scan --path . --format html --output reporte.html

# Scan con backend de desarrollo
python main.py scan --path . --api-url http://localhost:8000/reports
```

## 🎯 Testing

Usa el script de pruebas incluido:

```bash
python test_integration.py
```

Este script:
- ✅ Verifica la instalación del CLI
- ✅ Crea configuración de prueba
- ✅ Genera archivos con vulnerabilidades de ejemplo
- ✅ Ejecuta scans locales
- ✅ Proporciona instrucciones para pruebas manuales

---

¡Tu CLI ahora está completamente integrado con el backend containerizado! 🎉