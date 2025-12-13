# 🔒 SemBicho CLI - Enterprise Security Scanner

> **Herramienta profesional de análisis estático de seguridad para múltiples lenguajes de programación**

[![Security Rating](https://img.shields.io/badge/Security-Enterprise%20Grade-brightgreen.svg)]()
[![OWASP](https://img.shields.io/badge/OWASP-Top%2010%20Coverage-blue.svg)]()
[![CWE](https://img.shields.io/badge/CWE-Top%2025%20Coverage-orange.svg)]()
[![SARIF](https://img.shields.io/badge/SARIF-2.1.0%20Compatible-purple.svg)]()

## 🚀 **Características Enterprise**

### 🎯 **Análisis Integral de Seguridad**
- **Vulnerabilidades de código**: Detección automática con Bandit, ESLint, Semgrep
- **Secretos hardcodeados**: API keys, passwords, tokens, certificados
- **Análisis de dependencias**: NPM, PyPI, Maven, Gradle vulnerabilities
- **Compliance scoring**: OWASP Top 10, CWE Top 25, NIST, PCI-DSS, ISO 27001, SOC 2

### 📊 **Métricas Avanzadas**
- **Security Score**: Calificación de seguridad (0-100)
- **Risk Score**: Evaluación de riesgo empresarial
- **Quality Metrics**: Índice de mantenibilidad, deuda técnica
- **Compliance Metrics**: Cumplimiento de estándares industriales

### 📋 **Reportes Profesionales**
- **SARIF 2.1.0**: Estándar de la industria para herramientas CI/CD
- **XML Estructurado**: Para integración con sistemas enterprise
- **JSON Detallado**: API-ready con métricas completas
- **HTML Interactivo**: Dashboards visuales para stakeholders
- **Summary Ejecutivo**: Resumen para management y decisiones
- **Console**: Output optimizado para DevOps

### 🔗 **Integración Enterprise**
- **API Backend**: Integración directa con sistemas de gestión
- **Token-based Auth**: Autenticación segura sin credenciales almacenadas
- **CI/CD Ready**: Exit codes y outputs optimizados para pipelines
- **Multiple Formats**: Generación simultánea de múltiples reportes

---

## 📦 **Instalación Rápida**

```bash
# Clonar el repositorio
git clone https://github.com/your-org/sembicho-cli
cd sembicho-cli

# Instalar dependencias
pip install -r requirements.txt

# Configuración inicial
python main.py config --init
```

---

## 🎮 **Uso Básico**

### **1. Escaneo Local Simple**
```bash
# Análisis básico con reporte ejecutivo
python main.py scan --path ./mi-proyecto

# Análisis completo con múltiples formatos
python main.py scan --path . --multiple-formats json,html,sarif
```

### **2. Integración con Backend**
```bash
# Escaneo con envío automático al backend
python main.py scan --path . \
  --api-url https://security.empresa.com/reports \
  --token "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### **3. CI/CD Pipeline**
```bash
# Modo CI con exit codes para pipeline
python main.py scan --path . \
  --ci-mode \
  --fail-on critical,high \
  --format sarif \
  --output security-report.sarif
```

---

## 🛠️ **Comandos Avanzados**

### **Formatos de Reporte**
```bash
# Reporte ejecutivo (recomendado para management)
python main.py scan --path . --format summary

# SARIF para herramientas CI/CD (GitHub, Azure DevOps, etc.)
python main.py scan --path . --format sarif --output report.sarif

# JSON estructurado para APIs
python main.py scan --path . --format json --output report.json

# HTML interactivo para equipos
python main.py scan --path . --format html --output dashboard.html

# XML para sistemas enterprise
python main.py scan --path . --format xml --output compliance.xml
```

### **Múltiples Formatos Simultáneos**
```bash
# Generar todos los formatos automáticamente
python main.py scan --path . \
  --multiple-formats json,html,sarif,xml,summary \
  --output security_audit
```

### **Filtros y Configuración**
```bash
# Solo vulnerabilidades críticas y altas
python main.py scan --path . --severity high

# Herramientas específicas
python main.py scan --path . --tools bandit,secrets

# Pipeline específico
python main.py scan --path . \
  --pipeline-id "release-v2.1.0" \
  --api-url https://api.empresa.com/security/reports \
  --token $SECURITY_TOKEN
```

---

## 📊 **Métricas y Scoring**

### **Security Score (0-100)**
- **90-100**: 🟢 **Grade A** - Excelente
- **80-89**: 🔵 **Grade B** - Bueno  
- **70-79**: 🟡 **Grade C** - Aceptable
- **60-69**: 🟠 **Grade D** - Necesita mejoras
- **0-59**: 🔴 **Grade F** - Crítico

### **Compliance Coverage**
- **OWASP Top 10 2021**: Mapeo automático de vulnerabilidades
- **CWE Top 25**: Cobertura de debilidades más peligrosas
- **NIST Framework**: Scoring de ciberseguridad
- **PCI-DSS**: Relevancia para datos de tarjetas
- **ISO 27001**: Gestión de seguridad de información
- **SOC 2**: Controles de seguridad y disponibilidad

### **Quality Metrics**
- **Maintainability Index**: Facilidad de mantenimiento
- **Technical Debt Ratio**: Porcentaje de deuda técnica
- **Complexity Score**: Complejidad del código

---

## 🔧 **Configuración Avanzada**

### **Archivo .sembicho.json**
```json
{
  "api_url": "https://security.empresa.com/reports",
  "token": "your-jwt-token-here",
  "pipeline_id": "custom-pipeline-id",
  "default_format": "summary",
  "fail_on": ["critical", "high"],
  "tools": ["bandit", "eslint", "semgrep", "secrets", "dependency-check"],
  "compliance": {
    "owasp_top_10": true,
    "cwe_mapping": true,
    "nist_framework": true,
    "pci_dss": true,
    "iso27001": true
  },
  "exclude_patterns": [
    "node_modules/*",
    ".git/*",
    "*.min.js",
    "coverage/*"
  ]
}
```

---

## 🏢 **Integración Enterprise**

### **GitHub Actions**
```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: SemBicho Security Scan
        run: |
          python main.py scan --path . \
            --ci-mode \
            --format sarif \
            --output security.sarif \
            --fail-on critical,high
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: security.sarif
```

### **Azure DevOps**
```yaml
- task: PythonScript@0
  displayName: 'SemBicho Security Scan'
  inputs:
    scriptSource: 'filePath'
    scriptPath: 'sembicho-cli/main.py'
    arguments: 'scan --path $(Build.SourcesDirectory) --format sarif --output $(Agent.TempDirectory)/security.sarif'
```

### **Jenkins Pipeline**
```groovy
stage('Security Scan') {
    steps {
        sh '''
            python sembicho-cli/main.py scan --path . \
              --format json \
              --output security-report.json \
              --api-url $SECURITY_API_URL \
              --token $SECURITY_TOKEN
        '''
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
```

---

## 🔍 **Detección de Vulnerabilidades**

### **Categorías de Vulnerabilidades**
- **🔴 Críticas**: SQL Injection, RCE, Authentication Bypass
- **🟠 Altas**: XSS, CSRF, Insecure Crypto, Hardcoded Secrets  
- **🟡 Medias**: Information Disclosure, Weak Validation
- **🟢 Bajas**: Code Quality, Best Practices

### **Tipos de Análisis**
1. **Static Analysis**: Bandit (Python), ESLint (JS/TS), Semgrep (Multi-language)
2. **Secret Detection**: API Keys, Passwords, Tokens, Certificates
3. **Dependency Analysis**: Known vulnerabilities in packages
4. **Compliance Check**: OWASP, CWE, NIST alignment

### **Lenguajes Soportados**
- **Python** (.py) - Bandit + Semgrep + Secrets
- **JavaScript/TypeScript** (.js, .ts, .jsx, .tsx) - ESLint + Semgrep + Secrets  
- **Java** (.java) - Semgrep + Dependency Check
- **PHP** (.php) - Semgrep + Secrets
- **Go** (.go) - Semgrep + Secrets
- **C/C++** (.c, .cpp) - Semgrep
- **C#** (.cs) - Semgrep

---

## 📈 **Reportes Ejemplos**

### **Summary Report (Ejecutivo)**
```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                SEMBICHO SECURITY REPORT                              ║
║                                   RESUMEN EJECUTIVO                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

🎯 CALIFICACIÓN GENERAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Calificación: B (Bueno)
  Security Score: 78.5/100
  Risk Score: 21.5/100

🚨 RESUMEN DE VULNERABILIDADES  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total: 12
  🔴 Críticas: 0
  🟠 Altas: 3  
  🟡 Medias: 6
  🟢 Bajas: 3
```

### **SARIF Output (CI/CD)**
```json
{
  "version": "2.1.0",
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "runs": [{
    "tool": {
      "driver": {
        "name": "SemBicho",
        "version": "1.0.0",
        "rules": [...]
      }
    },
    "results": [...]
  }]
}
```

---

## 💼 **Casos de Uso Enterprise**

### **Para DevSecOps Teams**
```bash
# Scan completo con métricas de calidad
python main.py scan --path . \
  --format json \
  --api-url https://devsecops.empresa.com/api \
  --token $DEVSECOPS_TOKEN \
  --pipeline-id "sprint-42"
```

### **Para Compliance Officers**
```bash
# Reporte de cumplimiento regulatorio
python main.py scan --path . \
  --format xml \
  --output compliance-audit.xml
```

### **Para Security Managers**
```bash
# Dashboard ejecutivo
python main.py scan --path . \
  --format summary \
  --output executive-summary.txt
```

### **Para CI/CD Pipelines**
```bash
# Integración automática con fail conditions
python main.py scan --path . \
  --ci-mode \
  --fail-on critical \
  --format sarif \
  --api-url $CI_SECURITY_API \
  --token $CI_TOKEN
```

---

## 🔒 **Seguridad y Best Practices**

### **Token Management**
- ✅ **Nunca hardcodear tokens** en código
- ✅ Usar **variables de entorno** en CI/CD
- ✅ **Rotar tokens** regularmente
- ✅ Usar **scopes mínimos** necesarios

### **Configuración Segura**
```bash
# Variables de entorno recomendadas
export SEMBICHO_API_URL="https://security.empresa.com/api"
export SEMBICHO_TOKEN="jwt-token-here"
export SEMBICHO_PIPELINE_ID="release-v1.0"

# Uso seguro
python main.py scan --path . \
  --api-url $SEMBICHO_API_URL \
  --token $SEMBICHO_TOKEN \
  --pipeline-id $SEMBICHO_PIPELINE_ID
```

---

## 📚 **Documentación Técnica**

### **Exit Codes**
- `0` - Scan completado exitosamente, sin vulnerabilidades críticas
- `1` - Vulnerabilidades encontradas que cumplen fail conditions
- `2` - Error de configuración o argumentos
- `3` - Error de conexión con backend
- `4` - Error interno de la herramienta

### **API Integration**
```bash
# Headers requeridos
Authorization: Bearer <jwt-token>
Content-Type: application/json

# Payload structure  
{
  "pipelineId": "custom-pipeline-id",
  "data": { /* scan results */ },
  "fecha": "2024-10-03T12:00:00Z"
}
```

---

## 🏆 **Enterprise Ready Features**

✅ **SARIF 2.1.0 Compatible** - GitHub, Azure DevOps, SonarQube  
✅ **Multi-format Reports** - JSON, HTML, XML, Summary  
✅ **Compliance Scoring** - OWASP, CWE, NIST, PCI-DSS, ISO 27001  
✅ **Secret Detection** - API Keys, Passwords, Certificates  
✅ **Dependency Analysis** - NPM, PyPI, Maven vulnerabilities  
✅ **CI/CD Integration** - Jenkins, GitHub Actions, Azure DevOps  
✅ **Enterprise Auth** - JWT token-based, no stored credentials  
✅ **Quality Metrics** - Technical debt, maintainability scoring  
✅ **Executive Reporting** - Management-friendly summaries  
✅ **Scalable Architecture** - Multi-language, multi-tool support  

---

## 🤝 **Soporte Enterprise**

Para soporte empresarial, integraciones personalizadas, y licencias corporativas:

📧 **Email**: enterprise@sembicho.com  
🌐 **Web**: https://sembicho.com/enterprise  
📞 **Teléfono**: +1-555-SEMBICHO  

---

**© 2024 SemBicho Security. Enterprise Grade Static Analysis.**