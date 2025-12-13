# SemBicho CLI

🔒 **Static Application Security Testing + SBOM + CVE Tracking + Code Quality Analysis Tool**

Herramienta completa de línea de comandos para análisis estático de seguridad, gestión de dependencias y calidad de código.

## ✨ Características

- 🔐 **Security Scanning**: SAST para 12+ lenguajes
- 📦 **SBOM Generation**: Software Bill of Materials (CycloneDX, SPDX, Syft JSON) - **AUTOMÁTICO en cada scan**
- 🔍 **CVE Scanning**: Detección automática de vulnerabilidades conocidas con Grype
- 📝 **Code Linting**: Análisis de estilo y formato (Python, JavaScript/TypeScript)
- 🔢 **Complexity Analysis**: Métricas de complejidad ciclomática y cognitiva
- 📊 **Quality Reports**: Reportes unificados con scoring y grading
- 🔄 **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins
- 🏢 **Enterprise Backend**: Integración automática con backend SemBicho
- 📈 **Multi-format Output**: JSON, HTML, Console, Summary

## �🚀 Instalación

### Desde PyPI (Recomendado)

```bash
# Instalación básica (solo seguridad)
pip install sembicho-cli

# Con herramientas de calidad (recomendado)
pip install sembicho-cli[quality]

# Instalación completa
pip install sembicho-cli[all]
```

### Desde el código fuente

```bash
cd sembicho-cli
pip install -e .[all]
```

### Con Docker

```bash
docker build -t sembicho-cli .
docker run --rm -v $(pwd):/workspace sembicho-cli scan --path /workspace
```

## 🔧 Herramientas Adicionales

Para aprovechar todas las características:

### SBOM + CVE Scanning (Requerido para generación automática)
```bash
# Instalar Syft (SBOM Generator)
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Instalar Grype (CVE Scanner)
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Verificar instalación
syft version
grype version
```

### Code Quality Tools
```bash
# Python
pip install radon flake8 black pylint

# JavaScript/TypeScript
npm install -g eslint prettier escomplex
```

## 📖 Uso

### 🔐 Security Scanning (con SBOM Automático)

**NOTA**: A partir de v2.0, **SBOM + CVE scanning se genera AUTOMÁTICAMENTE** en cada escaneo (inspirado en Conviso AppSec Platform).

```bash
# Escaneo completo: SAST + SBOM + CVE (AUTOMÁTICO)
sembicho scan --path . --token TU_TOKEN --api-url https://sembichobackend.onrender.com

# Con reporte JSON
sembicho scan --path ./mi-proyecto --output security.json --format json --token TU_TOKEN

# Con reporte HTML
sembicho scan --path ./mi-proyecto --output security.html --format html --token TU_TOKEN

# Modo CI/CD (SBOM incluido automáticamente)
sembicho scan --path . --ci-mode --fail-on critical,high --token TU_TOKEN

# Deshabilitar SBOM (NO recomendado)
sembicho scan --path . --skip-sbom --token TU_TOKEN

# Cambiar formato SBOM (default: CycloneDX)
sembicho scan --path . --sbom-format spdx-json --token TU_TOKEN
```

**Qué hace automáticamente:**
1. ✅ Análisis SAST del código fuente
2. ✅ Generación SBOM de dependencias
3. ✅ Escaneo CVE con Grype
4. ✅ Envío a backend (reportes + SBOM + CVEs)
5. ✅ Visualización en dashboard

### 📝 Code Linting

```bash
# Linting de código Python
sembicho lint --path ./backend --language python

# Linting de código JavaScript
sembicho lint --path ./frontend/src --language javascript

# Con reporte JSON
sembicho lint --path ./src --output linting-report.json --format json
```

### 🔢 Complexity Analysis

```bash
# Análisis de complejidad
sembicho complexity --path ./src --language python

# Con umbral personalizado
sembicho complexity --path ./src --threshold 15

# Guardar reporte
sembicho complexity --path ./src --output complexity.json --format json
```

### 📊 Complete Quality Analysis

```bash
# Análisis completo de calidad (linting + complexity + more)
sembicho quality --path .

# Con grado mínimo para CI/CD
sembicho quality --path . --fail-on-grade B+

# Reporte completo JSON
sembicho quality --path . --output quality-report.json --format json
```

### Integración con Backend

```bash
# Enviar resultados al backend
sembicho scan --path . --api-url http://localhost:8000/api/results --token abc123

# Con configuración
sembicho config --init
# Editar .sembicho.json con tu configuración
sembicho scan --path .
```

### Filtros y opciones avanzadas

```bash
# Filtrar por severidad
sembicho scan --path . --severity high

# Modo verbose
sembicho scan --path . --verbose

# Herramientas específicas
sembicho scan --path . --tools bandit,semgrep

# Fallar en CI con vulnerabilidades críticas
sembicho scan --path . --ci-mode --fail-on critical
```

## 🛠️ Herramientas Integradas

- **Bandit**: Análisis de seguridad para Python
- **ESLint**: Análisis de JavaScript/TypeScript  
- **Semgrep**: Análisis multi-lenguaje con reglas OWASP

## 📊 Formatos de Salida

### JSON
```bash
sembicho scan --path . --format json --output results.json
```

Estructura del JSON:
```json
{
  "project_name": "mi-proyecto",
  "scan_date": "2024-01-15T10:30:00Z",
  "language": "python",
  "total_vulnerabilities": 5,
  "severity_counts": {
    "critical": 1,
    "high": 2,
    "medium": 2,
    "low": 0
  },
  "tools_used": ["bandit", "semgrep"],
  "vulnerabilities": [
    {
      "file": "app/auth.py",
      "line": 25,
      "rule_id": "B101",
      "severity": "high",
      "message": "Hardcoded password detected",
      "cwe": "CWE-798",
      "tool": "bandit"
    }
  ]
}
```

### HTML
```bash
sembicho scan --path . --format html --output report.html
```

Genera un reporte HTML completo con:
- Resumen ejecutivo con métricas
- Lista detallada de vulnerabilidades
- Filtros por severidad
- Información de herramientas utilizadas

### Console
```bash
sembicho scan --path .
```

Salida de consola con colores y formato legible.

## ⚙️ Configuración

### Crear configuración inicial
```bash
sembicho config --init
```

Esto crea un archivo `.sembicho.json`:
```json
{
  "api_url": "http://localhost:8000/api/results",
  "token": "",
  "default_format": "console",
  "fail_on": ["critical", "high"],
  "tools": ["bandit", "eslint", "semgrep"],
  "exclude_patterns": [
    "*.min.js",
    "node_modules/*",
    ".git/*",
    "__pycache__/*"
  ]
}
```

### Ver configuración actual
```bash
sembicho config --show
```

## 🔧 Integración CI/CD

### GitHub Actions
```yaml
- name: Security Scan
  run: |
    pip install -r sembicho-cli/requirements.txt
    python sembicho-cli/main.py scan --path . --ci-mode --fail-on critical,high
```

### GitLab CI
```yaml
security_scan:
  script:
    - cd sembicho-cli
    - pip install -r requirements.txt
    - python main.py scan --path .. --ci-mode --fail-on critical,high
```

### Jenkins
```groovy
stage('Security Scan') {
    steps {
        sh '''
            cd sembicho-cli
            pip install -r requirements.txt
            python main.py scan --path .. --ci-mode --fail-on critical,high
        '''
    }
}
```

## 🐳 Docker

### Dockerfile incluido
El proyecto incluye un Dockerfile optimizado para análisis de seguridad.

```bash
# Construir imagen
docker build -t sembicho-cli .

# Ejecutar escaneo
docker run --rm -v $(pwd):/workspace sembicho-cli scan --path /workspace

# Con configuración personalizada
docker run --rm -v $(pwd):/workspace -v $(pwd)/.sembicho.json:/app/.sembicho.json sembicho-cli scan --path /workspace
```

## 📝 Códigos de Salida

- `0`: Escaneo exitoso sin errores críticos
- `1`: Error en argumentos o ejecución  
- `1`: Vulnerabilidades encontradas (cuando se usa `--fail-on`)

## 🔍 Lenguajes Soportados

- **Python** (.py) - Bandit, Semgrep
- **JavaScript/TypeScript** (.js, .ts, .jsx, .tsx) - ESLint, Semgrep
- **Java** (.java) - Semgrep
- **PHP** (.php) - Semgrep
- **Go** (.go) - Semgrep
- **C/C++** (.c, .cpp) - Semgrep
- **Ruby** (.rb) - Semgrep
- **C#** (.cs) - Semgrep

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - ver [LICENSE](../LICENSE) para detalles.

## 🆘 Soporte

- 📧 Email: support@sembicho.com
- 🐛 Issues: [GitHub Issues](https://github.com/sembicho/sembicho-cli/issues)
- 📖 Documentación: [Docs](https://docs.sembicho.com)