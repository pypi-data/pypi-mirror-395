# SemBicho CLI - Herramienta Autocontenida de Análisis de Seguridad

**SemBicho CLI v2.0** es una herramienta profesional de análisis estático de seguridad (SAST) completamente autocontenida, diseñada para integrarse fácilmente en pipelines de CI/CD sin dependencias externas.

## 🚀 Características Principales

### ✅ **Autocontenida - Sin Dependencias Externas**
- **No requiere** Bandit, Semgrep, ESLint, o cualquier otra herramienta externa
- **Instalación simple**: `pip install sembicho-cli`
- **Funciona inmediatamente** después de la instalación

### 🌐 **Soporte Multi-Lenguaje**
- **Python**: Análisis completo de vulnerabilidades de seguridad
- **JavaScript/TypeScript**: Detección de XSS, inyecciones, eval(), etc.
- **Java**: SQL injection, command injection, hardcoded passwords
- **PHP**: File inclusion, SQL injection, eval()
- **Go**: Command injection, weak random, unsafe patterns
- **C#**: SQL injection, weak cryptography
- **Multi-lenguaje**: Secretos, API keys, configuraciones inseguras

### 📊 **Reportes Profesionales**
- **Múltiples formatos**: JSON, HTML, XML, SARIF, Console, Summary
- **Métricas avanzadas**: OWASP Top 10, CWE Top 25, NIST Framework
- **Compliance**: PCI-DSS, ISO 27001, SOC 2 scoring
- **Integración con APIs**: Envío automático de resultados

### 🔧 **Optimizado para CI/CD**
- **Modo CI**: Salida optimizada para pipelines
- **Exit codes**: Falla en vulnerabilidades críticas/altas
- **Multiple formats**: Un comando, múltiples reportes
- **Token authentication**: Integración segura con backends

## 📦 Instalación

### Instalación Rápida (Recomendada)
```bash
pip install sembicho-cli
```

### Desde Código Fuente
```bash
git clone https://github.com/sembicho/sembicho-cli.git
cd sembicho-cli
pip install -e .
```

### Verificar Instalación
```bash
sembicho version
# o
sembicho-cli version
```

## 🎯 Uso Básico

### Escaneo Local Simple
```bash
# Escanear directorio actual
sembicho scan

# Escanear directorio específico
sembicho scan --path /ruta/a/mi/proyecto

# Escanear con formato específico
sembicho scan --path ./mi-app --format json --output reporte.json
```

### Integración con Backend API
```bash
# Enviar resultados a backend
sembicho scan \
  --path ./mi-proyecto \
  --api-url http://localhost:8000/api/reports \
  --token abc123 \
  --pipeline-id "mi-pipeline-$(date +%Y%m%d)"
```

### Modo CI/CD
```bash
# Modo CI con fallo en vulnerabilidades críticas/altas
sembicho scan \
  --path . \
  --ci-mode \
  --fail-on critical,high \
  --format json \
  --output security-report.json
```

### Múltiples Formatos
```bash
# Generar múltiples reportes
sembicho scan \
  --path ./src \
  --multiple-formats json,html,sarif \
  --output security-report
```

## 📋 Ejemplos de Uso por Lenguaje

### Python
```bash
# Detecta automáticamente y analiza Python
sembicho scan --path ./mi-app-python --format summary

# Vulnerabilidades detectadas:
# - SQL injection via string concatenation
# - Hardcoded passwords/secrets
# - Use of eval()/exec()
# - Pickle deserialization
# - Debug mode enabled
# - Weak random number generation
```

### JavaScript/TypeScript
```bash
# Análisis de aplicación web
sembicho scan --path ./mi-app-web --format html --output web-security.html

# Vulnerabilidades detectadas:
# - XSS via innerHTML/document.write
# - eval() usage
# - Console.log in production
# - Hardcoded API keys
# - Math.random() weakness
```

### Proyecto Multi-Lenguaje
```bash
# Análisis completo de aplicación fullstack
sembicho scan \
  --path ./mi-aplicacion \
  --format summary \
  --severity medium \
  --exclude "*/node_modules/*,*/venv/*"
```

## 🔧 Configuración

### Archivo de Configuración (.sembicho.json)
```json
{
  "api_url": "http://localhost:8000/api/reports",
  "token": "tu-token-aqui",
  "excluded_patterns": [
    "*/node_modules/*",
    "*/venv/*",
    "*/vendor/*",
    "*.min.js"
  ],
  "severity_threshold": "medium",
  "fail_on_severity": ["critical", "high"],
  "output_formats": ["json", "html"]
}
```

### Variables de Entorno
```bash
export SEMBICHO_API_URL="http://localhost:8000/api/reports"
export SEMBICHO_TOKEN="tu-token-secreto"
export SEMBICHO_SEVERITY="high"
```

## 🚀 Integración en CI/CD

### GitHub Actions
```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install SemBicho CLI
      run: pip install sembicho-cli
    
    - name: Run Security Scan
      run: |
        sembicho scan \
          --path . \
          --ci-mode \
          --fail-on critical,high \
          --format sarif \
          --output security-results.sarif
    
    - name: Upload SARIF
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: security-results.sarif
```

### GitLab CI
```yaml
security_scan:
  stage: test
  image: python:3.9
  before_script:
    - pip install sembicho-cli
  script:
    - sembicho scan --path . --ci-mode --fail-on critical,high --format json --output security-report.json
  artifacts:
    reports:
      junit: security-report.json
    when: always
  only:
    - branches
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    stages {
        stage('Security Scan') {
            steps {
                sh 'pip install sembicho-cli'
                sh '''
                    sembicho scan \
                      --path . \
                      --ci-mode \
                      --fail-on critical,high \
                      --multiple-formats json,html \
                      --output security-report
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'security-report.*', fingerprint: true
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'security-report.html',
                        reportName: 'Security Report'
                    ])
                }
            }
        }
    }
}
```

### Azure DevOps
```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.9'

- script: |
    pip install sembicho-cli
    sembicho scan --path . --ci-mode --fail-on critical,high --format json --output $(Build.ArtifactStagingDirectory)/security-report.json
  displayName: 'Run Security Scan'

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)/security-report.json'
    artifactName: 'security-report'
```

## 📊 Formatos de Reporte

### Summary (Por Defecto)
Reporte visual con colores y métricas resumidas - ideal para desarrolladores.

### JSON
```json
{
  "project_name": "mi-proyecto",
  "scan_date": "2025-10-03T20:30:00Z",
  "total_vulnerabilities": 5,
  "severity_counts": {
    "critical": 1,
    "high": 2,
    "medium": 2,
    "low": 0
  },
  "security_metrics": {
    "security_score": 75.0,
    "risk_score": 25.0
  },
  "vulnerabilities": [...]
}
```

### SARIF (Para GitHub/Tools)
Formato estándar para integración con herramientas de análisis estático.

### HTML
Reporte visual navegable con gráficos y filtros.

## 🛡️ Vulnerabilidades Detectadas

### OWASP Top 10 2021
- **A01: Broken Access Control**
- **A02: Cryptographic Failures**
- **A03: Injection**
- **A04: Insecure Design**
- **A05: Security Misconfiguration**
- **A06: Vulnerable Components**
- **A07: Identification/Authentication Failures**
- **A08: Software/Data Integrity Failures**
- **A09: Security Logging/Monitoring Failures**
- **A10: Server-Side Request Forgery (SSRF)**

### CWE Top 25
Detección de las 25 debilidades más peligrosas según MITRE.

### Específicas por Lenguaje
- **Python**: SQL injection, eval(), pickle, debug mode, weak random
- **JavaScript**: XSS, eval(), prototype pollution, unsafe RegExp
- **Java**: SQL injection, command injection, hardcoded secrets
- **PHP**: File inclusion, SQL injection, eval()
- **Go**: Command injection, weak random
- **C#**: SQL injection, weak cryptography

## 🎛️ Opciones Avanzadas

### Filtrado por Severidad
```bash
# Solo vulnerabilidades críticas y altas
sembicho scan --severity high --path ./src

# Fallar build solo en críticas
sembicho scan --fail-on critical --ci-mode
```

### Exclusión de Archivos
```bash
# Excluir patrones específicos
sembicho scan --exclude "*/tests/*,*.min.js,*/node_modules/*"
```

### Herramientas Específicas
```bash
# Solo análisis de Python y multi-lenguaje
sembicho scan --tools sembicho-python,sembicho-multi

# Ver herramientas disponibles
sembicho scan --help
```

## 📈 Métricas y Scoring

### Security Score (0-100)
- **90-100**: Excelente (A)
- **80-89**: Bueno (B)  
- **70-79**: Aceptable (C)
- **60-69**: Necesita mejoras (D)
- **<60**: Crítico (F)

### Risk Score (0-100)
Basado en número y severidad de vulnerabilidades:
- Críticas: 10 puntos cada una
- Altas: 5 puntos cada una
- Medias: 2 puntos cada una
- Bajas: 1 punto cada una

### Compliance Metrics
- **NIST Framework Score**
- **PCI-DSS Relevant Issues**
- **ISO 27001 Relevant Issues**
- **SOC 2 Relevant Issues**

## 🔗 Integración con Backend

SemBicho CLI se integra perfectamente con APIs backend para centralizar resultados:

```bash
# Configuración de API
sembicho scan \
  --api-url https://security-dashboard.empresa.com/api/reports \
  --token $SECURITY_API_TOKEN \
  --pipeline-id "${CI_PIPELINE_ID:-local-$(date +%s)}"
```

El payload enviado incluye:
- Resultados completos del escaneo
- Métricas de seguridad y calidad
- Metadatos del pipeline
- Timestamp y identificadores únicos

## 🆘 Solución de Problemas

### Error: "No vulnerabilities found but expected some"
```bash
# Verificar que el directorio tiene archivos de código
sembicho scan --path ./src --verbose

# Verificar detección de lenguajes
sembicho scan --path ./src --format summary
```

### Error: "API connection failed"
```bash
# Verificar conectividad
curl -H "Authorization: Bearer $TOKEN" $API_URL

# Probar sin API primero
sembicho scan --path ./src --format json --output local-report.json
```

### Performance en Proyectos Grandes
```bash
# Excluir directorios innecesarios
sembicho scan \
  --path ./huge-project \
  --exclude "*/node_modules/*,*/vendor/*,*/dist/*,*.min.js" \
  --format summary
```

## 📞 Soporte y Contribución

- **Issues**: [GitHub Issues](https://github.com/sembicho/sembicho-cli/issues)
- **Documentation**: [docs.sembicho.com](https://docs.sembicho.com)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security**: Para reportar vulnerabilidades de seguridad, contacta security@sembicho.com

## 📜 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

---

**SemBicho CLI v2.0** - Análisis de seguridad autocontenido, profesional y listo para producción. 🛡️✨