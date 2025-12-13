#!/usr/bin/env python3
"""
SemBicho Scanner Module
Módulo principal para el análisis estático de seguridad
"""

import os
import json
import subprocess
import logging
import re
import requests
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import tempfile


@dataclass
class Vulnerability:
    """Clase para representar una vulnerabilidad encontrada"""
    file: str
    line: int
    rule_id: str
    severity: str
    message: str
    cwe: Optional[str] = None
    owasp_category: Optional[str] = None
    tool: str = ""
    confidence: Optional[str] = None
    category: str = "security"  # security, quality, performance, compliance
    impact: str = "medium"  # low, medium, high, critical
    likelihood: str = "medium"  # low, medium, high
    remediation_effort: str = "medium"  # low, medium, high
    code_snippet: Optional[str] = None


@dataclass
class ComplianceMetrics:
    """Métricas de compliance y estándares empresariales"""
    owasp_top_10_coverage: Dict[str, int]
    cwe_top_25_coverage: Dict[str, int]
    nist_framework_score: float
    pci_dss_relevant: int
    iso27001_relevant: int
    soc2_relevant: int
    gdpr_relevant: int
    hipaa_relevant: int
    compliance_score: float


@dataclass
class QualityMetrics:
    """Métricas avanzadas de calidad de código"""
    total_lines_scanned: int
    total_files_scanned: int
    complexity_score: float
    maintainability_index: float
    technical_debt_ratio: float
    code_coverage: Optional[float] = None
    cyclomatic_complexity: float = 0.0
    cognitive_complexity: float = 0.0
    duplicate_code_ratio: float = 0.0
    test_coverage_ratio: float = 0.0
    documentation_ratio: float = 0.0
    function_length_average: float = 0.0
    class_length_average: float = 0.0
    dependency_count: int = 0
    coupling_factor: float = 0.0
    cohesion_factor: float = 0.0


@dataclass
class SecurityMetrics:
    """Métricas avanzadas de seguridad empresarial"""
    total_vulnerabilities: int
    critical_vulnerabilities: int
    high_vulnerabilities: int
    medium_vulnerabilities: int
    low_vulnerabilities: int
    info_vulnerabilities: int
    false_positive_ratio: float
    remediation_priority_score: float
    risk_score: float
    security_score: float
    attack_surface_score: float
    encryption_usage_score: float
    authentication_score: float
    authorization_score: float
    input_validation_score: float
    output_encoding_score: float
    session_management_score: float
    error_handling_score: float


@dataclass
class ArchitectureMetrics:
    """Métricas de arquitectura y diseño"""
    design_patterns_used: List[str]
    anti_patterns_detected: List[str]
    solid_violations: Dict[str, int]
    architecture_smells: List[str]
    modularity_score: float
    reusability_score: float
    testability_score: float
    scalability_indicators: List[str]
    performance_concerns: List[str]
    security_patterns: List[str]


@dataclass
class PerformanceMetrics:
    """Métricas de rendimiento y eficiencia"""
    scan_duration: float
    files_per_second: float
    lines_per_second: float
    memory_usage_mb: float
    cpu_usage_percent: float
    cache_hit_ratio: float
    error_rate: float
    throughput_score: float


@dataclass
class ScanResult:
    """Resultado empresarial completo del escaneo"""
    # Información básica del proyecto
    project_name: str
    scan_date: str
    language: str
    framework: Optional[str]
    version: str
    environment: str  # development, staging, production
    
    # Resumen de vulnerabilidades
    total_vulnerabilities: int
    severity_counts: Dict[str, int]
    tools_used: List[str]
    vulnerabilities: List[Dict[str, Any]]
    
    # Métricas empresariales
    security_metrics: SecurityMetrics
    quality_metrics: QualityMetrics
    compliance_metrics: ComplianceMetrics
    architecture_metrics: ArchitectureMetrics
    performance_metrics: PerformanceMetrics
    
    # Metadatos del escaneo
    execution_time: float
    scan_coverage: float
    scan_id: str
    pipeline_id: Optional[str]
    commit_hash: Optional[str]
    branch_name: Optional[str]
    
    # Scores y calificaciones
    overall_security_grade: str  # A, B, C, D, F
    overall_quality_grade: str   # A, B, C, D, F
    overall_compliance_grade: str # A, B, C, D, F
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    
    # Tendencias y comparación
    security_trend: Optional[str] = None  # IMPROVING, STABLE, DEGRADING
    quality_trend: Optional[str] = None
    compliance_trend: Optional[str] = None
    
    # 🔥 NUEVOS CAMPOS CRÍTICOS (análisis SRE)
    scan_coverage_details: Optional[Dict[str, Any]] = None  # total_files, scanned, skipped
    risk_score: Optional[int] = None  # (critical*5 + high*3 + medium*1)
    category_counts: Optional[Dict[str, int]] = None  # security, quality, style, architecture, secrets
    owasp_distribution: Optional[Dict[str, int]] = None  # A01-A10
    cwe_distribution: Optional[Dict[str, int]] = None  # CWE counts
    scan_duration_seconds: Optional[float] = None  # tiempo exacto del escaneo
    dependencies: Optional[List[Dict[str, Any]]] = None  # SBOM dependencies
    sbom_cyclonedx: Optional[Dict[str, Any]] = None  # SBOM en formato CycloneDX
    sbom_spdx: Optional[Dict[str, Any]] = None  # 🔥 v2.6.0: SBOM en formato SPDX 2.3
    cve_report: Optional[List[Dict[str, Any]]] = None  # CVEs de dependencias
    dependency_tree: Optional[Dict[str, Any]] = None  # 🔥 v2.6.0: Árbol de dependencias transitivas
    nvd_enrichment: Optional[Dict[str, Any]] = None  # 🔥 v2.6.0: Datos enriquecidos de NVD API


class SemBichoScanner:
    """Scanner principal para análisis estático de seguridad"""
    
    SUPPORTED_LANGUAGES = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.php': 'php',
        '.rb': 'ruby',
        '.go': 'go',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp'
    }
    
    SEVERITY_LEVELS = ['low', 'medium', 'high', 'critical']
    
    # Mapeo CWE a categorías OWASP Top 10 2021
    OWASP_TOP_10_MAPPING = {
        'A01': ['CWE-79', 'CWE-89', 'CWE-94', 'CWE-95', 'CWE-96'],  # Injection
        'A02': ['CWE-259', 'CWE-798', 'CWE-522', 'CWE-256'],        # Cryptographic Failures
        'A03': ['CWE-22', 'CWE-23', 'CWE-35', 'CWE-59'],           # Injection
        'A04': ['CWE-601', 'CWE-611', 'CWE-918', 'CWE-93'],        # Insecure Design
        'A05': ['CWE-276', 'CWE-732', 'CWE-668', 'CWE-269'],       # Security Misconfiguration
        'A06': ['CWE-327', 'CWE-330', 'CWE-331', 'CWE-326'],       # Vulnerable Components
        'A07': ['CWE-287', 'CWE-384', 'CWE-613', 'CWE-620'],       # Identification and Authentication Failures
        'A08': ['CWE-352', 'CWE-434', 'CWE-829', 'CWE-829'],       # Software and Data Integrity Failures
        'A09': ['CWE-117', 'CWE-223', 'CWE-532', 'CWE-778'],       # Security Logging and Monitoring Failures
        'A10': ['CWE-918', 'CWE-444', 'CWE-942', 'CWE-1021']       # Server-Side Request Forgery
    }
    
    # Top 25 CWEs más peligrosos
    CWE_TOP_25 = [
        'CWE-79', 'CWE-89', 'CWE-20', 'CWE-125', 'CWE-119', 'CWE-22', 'CWE-352',
        'CWE-434', 'CWE-862', 'CWE-476', 'CWE-287', 'CWE-190', 'CWE-502', 'CWE-77',
        'CWE-798', 'CWE-269', 'CWE-400', 'CWE-94', 'CWE-522', 'CWE-611', 'CWE-918',
        'CWE-276', 'CWE-732', 'CWE-416', 'CWE-601'
    ]
    
    # Mapeo de herramientas a categorías de reglas
    RULE_CATEGORIES = {
        'bandit': {
            'B101': {'cwe': 'CWE-259', 'owasp': 'A02', 'category': 'hardcoded-password'},
            'B102': {'cwe': 'CWE-78', 'owasp': 'A01', 'category': 'shell-injection'},
            'B103': {'cwe': 'CWE-377', 'owasp': 'A05', 'category': 'insecure-temp'},
            'B104': {'cwe': 'CWE-319', 'owasp': 'A02', 'category': 'hardcoded-bind'},
            'B105': {'cwe': 'CWE-259', 'owasp': 'A02', 'category': 'hardcoded-password'},
            'B106': {'cwe': 'CWE-259', 'owasp': 'A02', 'category': 'hardcoded-password'},
            'B107': {'cwe': 'CWE-259', 'owasp': 'A02', 'category': 'hardcoded-password'},
            'B108': {'cwe': 'CWE-377', 'owasp': 'A05', 'category': 'insecure-temp'},
            'B110': {'cwe': 'CWE-703', 'owasp': 'A09', 'category': 'try-except-pass'},
            'B112': {'cwe': 'CWE-703', 'owasp': 'A09', 'category': 'try-except-continue'}
        }
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa el scanner
        
        Args:
            config: Configuración opcional para el scanner
        """
        self.config = config or {}
        self.results = []
        self.vulnerabilities: List[Vulnerability] = []
        self.tools_used = []
        self.logger = self._setup_logging()
        self.start_time = 0
        self.total_files_scanned = 0
        self.total_lines_scanned = 0
        
        # 🔥 NUEVO: Tracking de cobertura de escaneo (análisis SRE)
        self.total_files_in_repo = 0
        self.skipped_files = 0
        self.skipped_reasons = {"binary": 0, "too_large": 0, "unsupported": 0, "error": 0}
        
        # Configuración empresarial
        self.enterprise_mode = False
        self.backend_url = None
        self.auth_token = None
        self.environment = 'development'
        self.pipeline_id = None
        
    def configure_enterprise_mode(self, backend_url: str, token: str, environment: str = 'development', pipeline_id: Optional[str] = None):
        """
        Configura el scanner para modo empresarial backend-only
        
        Args:
            backend_url: URL del backend empresarial
            token: Token de autenticación
            environment: Entorno (development, staging, production)
            pipeline_id: ID del pipeline opcional
        """
        self.enterprise_mode = True
        self.backend_url = backend_url
        self.auth_token = token
        self.environment = environment
        self.pipeline_id = pipeline_id
        
        self.logger.info("🏢 Modo empresarial configurado")
        self.logger.debug(f"Backend: {backend_url}")
        self.logger.debug(f"Ambiente: {environment}")
        
    def _setup_logging(self) -> logging.Logger:
        """Configura el sistema de logging"""
        logger = logging.getLogger('sembicho')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _enrich_vulnerability(self, vuln: Vulnerability) -> Vulnerability:
        """
        Enriquece una vulnerabilidad con datos adicionales de CWE y OWASP
        
        Args:
            vuln: Vulnerabilidad a enriquecer
            
        Returns:
            Vulnerabilidad enriquecida
        """
        # Mapear regla a CWE y OWASP si es posible
        rule_info = self.RULE_CATEGORIES.get(vuln.tool, {}).get(vuln.rule_id, {})
        
        if not vuln.cwe and 'cwe' in rule_info:
            vuln.cwe = rule_info['cwe']
        
        if not vuln.owasp_category and 'owasp' in rule_info:
            vuln.owasp_category = rule_info['owasp']
        
        # Si tenemos CWE, mapear a OWASP Top 10
        if vuln.cwe and not vuln.owasp_category:
            for owasp_cat, cwe_list in self.OWASP_TOP_10_MAPPING.items():
                if vuln.cwe in cwe_list:
                    vuln.owasp_category = owasp_cat
                    break
        
        # Calcular impact y likelihood basado en severidad y CWE
        if vuln.cwe in self.CWE_TOP_25:
            vuln.impact = "high"
            vuln.likelihood = "high"
        
        return vuln
    
    def _count_files_and_lines(self, directory_path: str):
        """
        Cuenta archivos y líneas de código para métricas
        
        Args:
            directory_path: Directorio a analizar
        """
        self.total_files_scanned = 0
        self.total_lines_scanned = 0
        self.total_files_in_repo = 0
        self.skipped_files = 0
        self.skipped_reasons = {"binary": 0, "too_large": 0, "unsupported": 0, "error": 0}
        
        MAX_FILE_SIZE_MB = 10  # Límite de tamaño de archivo
        
        try:
            path_obj = Path(directory_path)
            
            # Contar TODOS los archivos del repo
            all_files = list(path_obj.rglob('*'))
            self.total_files_in_repo = sum(1 for f in all_files if f.is_file())
            
            # Escanear archivos soportados
            for ext in self.SUPPORTED_LANGUAGES.keys():
                files = list(path_obj.rglob(f'*{ext}'))
                
                for file_path in files:
                    try:
                        # Verificar tamaño
                        file_size_mb = file_path.stat().st_size / (1024 * 1024)
                        if file_size_mb > MAX_FILE_SIZE_MB:
                            self.skipped_files += 1
                            self.skipped_reasons["too_large"] += 1
                            continue
                        
                        # Intentar leer
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = sum(1 for _ in f)
                            self.total_lines_scanned += lines
                            self.total_files_scanned += 1
                    except UnicodeDecodeError:
                        self.skipped_files += 1
                        self.skipped_reasons["binary"] += 1
                    except Exception as e:
                        self.skipped_files += 1
                        self.skipped_reasons["error"] += 1
                        self.logger.debug(f"Error leyendo {file_path}: {e}")
                        
        except Exception as e:
            self.logger.debug(f"Error contando archivos: {e}")
    
    def _calculate_security_metrics(self) -> SecurityMetrics:
        """
        Calcula métricas avanzadas de seguridad
        
        Returns:
            Objeto SecurityMetrics con las métricas calculadas
        """
        total = len(self.vulnerabilities)
        critical = sum(1 for v in self.vulnerabilities if v.severity == 'critical')
        high = sum(1 for v in self.vulnerabilities if v.severity == 'high')
        medium = sum(1 for v in self.vulnerabilities if v.severity == 'medium')
        low = sum(1 for v in self.vulnerabilities if v.severity == 'low')
        
        # Calcular score de riesgo (0-100, donde 100 es el peor)
        risk_score = min(100, (critical * 10 + high * 5 + medium * 2 + low * 1))
        
        # Calcular score de seguridad (100 - risk_score)
        security_score = max(0, 100 - risk_score)
        
        # Estimar ratio de falsos positivos (basado en herramientas y confidence)
        high_confidence = sum(1 for v in self.vulnerabilities if v.confidence == 'high')
        false_positive_ratio = max(0, (total - high_confidence) / total) if total > 0 else 0
        
        # Score de prioridad de remediación
        remediation_priority = (critical * 0.4 + high * 0.3 + medium * 0.2 + low * 0.1)
        
        # Calcular scores adicionales basados en tipos de vulnerabilidades
        auth_vulns = sum(1 for v in self.vulnerabilities if 'auth' in v.message.lower() or 'login' in v.message.lower())
        crypto_vulns = sum(1 for v in self.vulnerabilities if 'crypto' in v.message.lower() or 'hash' in v.message.lower())
        input_vulns = sum(1 for v in self.vulnerabilities if 'injection' in v.message.lower() or 'input' in v.message.lower())
        
        return SecurityMetrics(
            total_vulnerabilities=total,
            critical_vulnerabilities=critical,
            high_vulnerabilities=high,
            medium_vulnerabilities=medium,
            low_vulnerabilities=low,
            info_vulnerabilities=0,  # No info level in current implementation
            false_positive_ratio=false_positive_ratio,
            remediation_priority_score=remediation_priority,
            risk_score=risk_score,
            security_score=security_score,
            attack_surface_score=max(0, 100 - (total * 2)),
            encryption_usage_score=max(0, 100 - (crypto_vulns * 10)),
            authentication_score=max(0, 100 - (auth_vulns * 15)),
            authorization_score=max(0, 100 - (auth_vulns * 12)),
            input_validation_score=max(0, 100 - (input_vulns * 8)),
            output_encoding_score=max(0, 100 - (input_vulns * 6)),
            session_management_score=max(0, 100 - (auth_vulns * 10)),
            error_handling_score=max(0, 100 - (sum(1 for v in self.vulnerabilities if 'except' in v.message.lower()) * 5))
        )
    
    def _calculate_compliance_metrics(self) -> ComplianceMetrics:
        """
        Calcula métricas de compliance
        
        Returns:
            Objeto ComplianceMetrics
        """
        owasp_coverage = {f'A{i:02d}': 0 for i in range(1, 11)}
        cwe_top25_coverage = {cwe: 0 for cwe in self.CWE_TOP_25}
        
        pci_dss_relevant = 0
        iso27001_relevant = 0
        soc2_relevant = 0
        
        for vuln in self.vulnerabilities:
            # Contar cobertura OWASP Top 10
            if vuln.owasp_category and vuln.owasp_category in owasp_coverage:
                owasp_coverage[vuln.owasp_category] += 1
            
            # Contar cobertura CWE Top 25
            if vuln.cwe and vuln.cwe in cwe_top25_coverage:
                cwe_top25_coverage[vuln.cwe] += 1
            
            # Determinar relevancia para estándares
            if vuln.cwe in ['CWE-79', 'CWE-89', 'CWE-287', 'CWE-522']:
                pci_dss_relevant += 1
            
            if vuln.severity in ['critical', 'high']:
                iso27001_relevant += 1
                soc2_relevant += 1
        
        # Calcular score NIST Framework (simplificado)
        total_vulns = len(self.vulnerabilities)
        nist_score = max(0, 100 - (total_vulns * 2)) if total_vulns > 0 else 100
        
        # Calcular score de compliance general
        compliance_score = (nist_score + max(0, 100 - pci_dss_relevant * 5) + max(0, 100 - iso27001_relevant * 3)) / 3
        
        return ComplianceMetrics(
            owasp_top_10_coverage=owasp_coverage,
            cwe_top_25_coverage=cwe_top25_coverage,
            nist_framework_score=nist_score,
            pci_dss_relevant=pci_dss_relevant,
            iso27001_relevant=iso27001_relevant,
            soc2_relevant=soc2_relevant,
            gdpr_relevant=sum(1 for v in self.vulnerabilities if 'data' in v.message.lower()),
            hipaa_relevant=sum(1 for v in self.vulnerabilities if 'health' in v.message.lower() or 'medical' in v.message.lower()),
            compliance_score=compliance_score
        )
    
    def _calculate_quality_metrics(self, target_path: str) -> QualityMetrics:
        """
        Calcula métricas de calidad de código
        
        Args:
            target_path: Ruta analizada
            
        Returns:
            Objeto QualityMetrics
        """
        # Calcular complejidad y métricas básicas
        complexity_score = min(100, len(self.vulnerabilities) * 2)
        maintainability_index = max(0, 100 - complexity_score)
        
        # Estimar technical debt (vulnerabilidades críticas y altas)
        critical_high = sum(1 for v in self.vulnerabilities if v.severity in ['critical', 'high'])
        total_vulns = len(self.vulnerabilities)
        technical_debt_ratio = (critical_high / total_vulns) if total_vulns > 0 else 0
        
        # Calcular métricas adicionales
        complexity_functions = sum(1 for v in self.vulnerabilities if 'complex' in v.message.lower())
        cyclomatic_complexity = max(1, complexity_functions * 2.5)
        
        return QualityMetrics(
            total_lines_scanned=self.total_lines_scanned,
            total_files_scanned=self.total_files_scanned,
            complexity_score=complexity_score,
            maintainability_index=maintainability_index,
            technical_debt_ratio=technical_debt_ratio,
            code_coverage=None,  # Require external tool
            cyclomatic_complexity=cyclomatic_complexity,
            cognitive_complexity=cyclomatic_complexity * 1.2,
            duplicate_code_ratio=0.05,  # Estimated
            test_coverage_ratio=0.0,   # Require external analysis
            documentation_ratio=max(0, 1.0 - (sum(1 for v in self.vulnerabilities if 'docstring' in v.message.lower()) / max(1, self.total_files_scanned))),
            function_length_average=self.total_lines_scanned / max(1, self.total_files_scanned),
            class_length_average=self.total_lines_scanned / max(1, self.total_files_scanned * 0.3),
            dependency_count=sum(1 for v in self.vulnerabilities if 'import' in v.message.lower()),
            coupling_factor=min(1.0, total_vulns * 0.01),
            cohesion_factor=max(0.5, 1.0 - (total_vulns * 0.005))
        )
    
    def _calculate_architecture_metrics(self) -> ArchitectureMetrics:
        """
        Calcula métricas de arquitectura y diseño
        
        Returns:
            Objeto ArchitectureMetrics con las métricas calculadas
        """
        design_patterns = []
        anti_patterns = []
        solid_violations = {'S': 0, 'O': 0, 'L': 0, 'I': 0, 'D': 0}
        architecture_smells = []
        security_patterns = []
        
        # Buscar patrones y anti-patrones en las vulnerabilidades
        for vuln in self.vulnerabilities:
            message = vuln.message.lower()
            
            # Anti-patrones comunes
            if 'god class' in message or 'large class' in message:
                anti_patterns.append('God Class')
            if 'long method' in message or 'complex method' in message:
                anti_patterns.append('Long Method')
            if 'hardcoded' in message:
                anti_patterns.append('Hardcoded Values')
                
            # Violaciones SOLID
            if 'single responsibility' in message:
                solid_violations['S'] += 1
            if 'open closed' in message:
                solid_violations['O'] += 1
            if 'liskov substitution' in message:
                solid_violations['L'] += 1
            if 'interface segregation' in message:
                solid_violations['I'] += 1
            if 'dependency inversion' in message:
                solid_violations['D'] += 1
                
            # Security patterns
            if 'authentication' in message:
                security_patterns.append('Authentication Pattern')
            if 'authorization' in message:
                security_patterns.append('Authorization Pattern')
            if 'encryption' in message or 'crypto' in message:
                security_patterns.append('Encryption Pattern')
        
        # Calcular scores
        modularity_score = max(0, 100 - len(anti_patterns) * 10)
        reusability_score = max(0, 100 - sum(solid_violations.values()) * 5)
        testability_score = max(0, 100 - len(architecture_smells) * 8)
        
        return ArchitectureMetrics(
            design_patterns_used=list(set(design_patterns)),
            anti_patterns_detected=list(set(anti_patterns)),
            solid_violations=solid_violations,
            architecture_smells=list(set(architecture_smells)),
            modularity_score=modularity_score,
            reusability_score=reusability_score,
            testability_score=testability_score,
            scalability_indicators=[],
            performance_concerns=[],
            security_patterns=list(set(security_patterns))
        )
    
    def _calculate_performance_metrics(self) -> PerformanceMetrics:
        """
        Calcula métricas de rendimiento y eficiencia
        
        Returns:
            Objeto PerformanceMetrics con las métricas calculadas
        """
        scan_duration = time.time() - self.start_time if hasattr(self, 'start_time') else 1.0
        files_per_second = self.total_files_scanned / scan_duration if scan_duration > 0 else 0
        lines_per_second = self.total_lines_scanned / scan_duration if scan_duration > 0 else 0
        
        # Estimar uso de memoria (simulado)
        memory_usage_mb = max(50, self.total_files_scanned * 0.5 + len(self.vulnerabilities) * 0.1)
        
        # Calcular throughput score basado en eficiencia
        throughput_score = min(100, (files_per_second * 10) + (lines_per_second / 100))
        
        return PerformanceMetrics(
            scan_duration=scan_duration,
            files_per_second=files_per_second,
            lines_per_second=lines_per_second,
            memory_usage_mb=memory_usage_mb,
            cpu_usage_percent=0.0,  # No podemos medir sin librerías adicionales
            cache_hit_ratio=0.8,    # Estimado
            error_rate=0.0,         # Por ahora sin errores
            throughput_score=throughput_score
        )
    
    def _calculate_owasp_distribution(self) -> Dict[str, int]:
        """
        🔥 NUEVO: Calcula distribución de vulnerabilidades por OWASP Top 10
        
        Returns:
            Diccionario con conteo por categoría OWASP (A01-A10)
        """
        owasp_dist = {f'A{i:02d}': 0 for i in range(1, 11)}
        
        for vuln in self.vulnerabilities:
            if vuln.owasp_category and vuln.owasp_category in owasp_dist:
                owasp_dist[vuln.owasp_category] += 1
        
        return owasp_dist
    
    def _calculate_cwe_distribution(self) -> Dict[str, int]:
        """
        🔥 NUEVO: Calcula distribución de vulnerabilidades por CWE
        
        Returns:
            Diccionario con conteo por CWE
        """
        cwe_dist = {}
        
        for vuln in self.vulnerabilities:
            if vuln.cwe:
                cwe_dist[vuln.cwe] = cwe_dist.get(vuln.cwe, 0) + 1
        
        return dict(sorted(cwe_dist.items(), key=lambda x: x[1], reverse=True)[:25])  # Top 25
    
    def _calculate_category_counts(self) -> Dict[str, int]:
        """
        🔥 NUEVO: Calcula distribución por tipo de issue
        
        Returns:
            Diccionario con conteo por categoría
        """
        category_counts = {
            "security": 0,
            "quality": 0,
            "style": 0,
            "architecture": 0,
            "secrets": 0,
            "performance": 0,
            "supply-chain": 0
        }
        
        for vuln in self.vulnerabilities:
            category = vuln.category if vuln.category in category_counts else "security"
            category_counts[category] += 1
        
        return category_counts
    
    def _calculate_risk_score(self) -> int:
        """
        🔥 NUEVO: Calcula score de riesgo según fórmula estándar
        Formula: (critical*5) + (high*3) + (medium*1)
        
        Returns:
            Score de riesgo (0-infinito, típicamente 0-500)
        """
        critical = sum(1 for v in self.vulnerabilities if v.severity == 'critical')
        high = sum(1 for v in self.vulnerabilities if v.severity == 'high')
        medium = sum(1 for v in self.vulnerabilities if v.severity == 'medium')
        
        return (critical * 5) + (high * 3) + (medium * 1)
    
    def _get_scan_coverage_details(self) -> Dict[str, Any]:
        """
        🔥 NUEVO: Retorna detalles de cobertura del escaneo
        
        Returns:
            Diccionario con métricas de cobertura
        """
        total_files_in_repo = getattr(self, 'total_files_in_repo', self.total_files_scanned)
        skipped_files = getattr(self, 'skipped_files', 0)
        skipped_reasons = getattr(self, 'skipped_reasons', {})
        
        return {
            "total_files": total_files_in_repo,
            "scanned_files": self.total_files_scanned,
            "skipped_files": skipped_files,
            "skipped_reasons": skipped_reasons,
            "coverage_percentage": round((self.total_files_scanned / max(1, total_files_in_repo)) * 100, 2)
        }
    
    def _extract_dependencies(self, scan_path: str) -> List[Dict[str, Any]]:
        """
        🔥 NUEVO v2.5.0: Extrae dependencias del proyecto
        
        Soporta:
        - Python: requirements.txt, setup.py, Pipfile, pyproject.toml
        - Node.js: package.json, package-lock.json
        - Java: pom.xml, build.gradle
        - PHP: composer.json
        - Ruby: Gemfile
        - .NET: *.csproj, packages.config
        
        Args:
            scan_path: Ruta del proyecto a escanear
            
        Returns:
            Lista de dependencias con nombre, versión, tipo
        """
        dependencies = []
        scan_path = Path(scan_path)
        
        # Python dependencies
        requirements_files = [
            'requirements.txt', 'requirements-dev.txt', 'requirements-test.txt',
            'requirements-prod.txt', 'dev-requirements.txt'
        ]
        
        for req_file in requirements_files:
            req_path = scan_path / req_file
            if req_path.exists():
                try:
                    with open(req_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Parse "package==version" or "package>=version"
                                match = re.match(r'^([a-zA-Z0-9_-]+)([=<>!]+)(.+)$', line)
                                if match:
                                    name, operator, version = match.groups()
                                    dependencies.append({
                                        'name': name.strip(),
                                        'version': version.strip(),
                                        'type': 'python',
                                        'source': req_file,
                                        'operator': operator
                                    })
                                elif '==' not in line and '>=' not in line:
                                    # Package sin version especificada
                                    dependencies.append({
                                        'name': line.split()[0],
                                        'version': 'latest',
                                        'type': 'python',
                                        'source': req_file,
                                        'operator': ''
                                    })
                except Exception as e:
                    logging.warning(f"Error parsing {req_file}: {e}")
        
        # Node.js package.json
        package_json = scan_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    pkg_data = json.load(f)
                    for dep_type in ['dependencies', 'devDependencies']:
                        if dep_type in pkg_data:
                            for name, version in pkg_data[dep_type].items():
                                dependencies.append({
                                    'name': name,
                                    'version': version.lstrip('^~'),
                                    'type': 'npm',
                                    'source': 'package.json',
                                    'dev': dep_type == 'devDependencies'
                                })
            except Exception as e:
                logging.warning(f"Error parsing package.json: {e}")
        
        # Java pom.xml
        pom_xml = scan_path / 'pom.xml'
        if pom_xml.exists():
            try:
                with open(pom_xml, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple regex parse (no XML parser para mantener dependencias mínimas)
                    deps = re.findall(r'<dependency>.*?<groupId>(.*?)</groupId>.*?<artifactId>(.*?)</artifactId>.*?<version>(.*?)</version>.*?</dependency>', content, re.DOTALL)
                    for group, artifact, version in deps:
                        dependencies.append({
                            'name': f"{group.strip()}:{artifact.strip()}",
                            'version': version.strip(),
                            'type': 'maven',
                            'source': 'pom.xml'
                        })
            except Exception as e:
                logging.warning(f"Error parsing pom.xml: {e}")
        
        # PHP composer.json
        composer_json = scan_path / 'composer.json'
        if composer_json.exists():
            try:
                with open(composer_json, 'r', encoding='utf-8') as f:
                    composer_data = json.load(f)
                    for dep_type in ['require', 'require-dev']:
                        if dep_type in composer_data:
                            for name, version in composer_data[dep_type].items():
                                if name != 'php':  # Skip PHP itself
                                    dependencies.append({
                                        'name': name,
                                        'version': version.lstrip('^~'),
                                        'type': 'composer',
                                        'source': 'composer.json',
                                        'dev': dep_type == 'require-dev'
                                    })
            except Exception as e:
                logging.warning(f"Error parsing composer.json: {e}")
        
        # Ruby Gemfile
        gemfile = scan_path / 'Gemfile'
        if gemfile.exists():
            try:
                with open(gemfile, 'r', encoding='utf-8') as f:
                    for line in f:
                        match = re.match(r"^\s*gem\s+['\"]([^'\"]+)['\"](?:\s*,\s*['\"]([^'\"]+)['\"])?", line)
                        if match:
                            name = match.group(1)
                            version = match.group(2) if match.group(2) else 'latest'
                            dependencies.append({
                                'name': name,
                                'version': version,
                                'type': 'gem',
                                'source': 'Gemfile'
                            })
            except Exception as e:
                logging.warning(f"Error parsing Gemfile: {e}")
        
        logging.info(f"📦 Extracted {len(dependencies)} dependencies from project")
        return dependencies
    
    def _generate_sbom_cyclonedx(self, scan_path: str) -> Optional[Dict[str, Any]]:
        """
        🔥 NUEVO v2.5.0: Genera SBOM en formato CycloneDX 1.4 JSON
        
        CycloneDX es un estándar OWASP para Software Bill of Materials
        https://cyclonedx.org/
        
        Args:
            scan_path: Ruta del proyecto a escanear
            
        Returns:
            Dict con SBOM en formato CycloneDX, o None si no hay dependencias
        """
        dependencies = self._extract_dependencies(scan_path)
        if not dependencies:
            logging.warning("No dependencies found, SBOM will be empty")
            return None
        
        # Generar componentes CycloneDX
        components = []
        for idx, dep in enumerate(dependencies, start=1):
            file_path = dep.get('path')
            file_hash = None
            if file_path and os.path.isfile(file_path):
                import hashlib
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
            component = {
                "type": "library",
                "name": dep['name'],
                "version": dep['version'],
                "purl": self._generate_purl(dep),
                "properties": [
                    {"name": "source", "value": dep.get('source', 'unknown')},
                    {"name": "type", "value": dep['type']},
                    {"name": "file_hash", "value": file_hash or "N/A"},
                    {"name": "spdx_ref", "value": f"SPDXRef-Package-{idx}"}
                ]
            }
            if dep.get('dev'):
                component['scope'] = 'optional'
            components.append(component)
        
        # Generar metadata
        metadata = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tools": [{
                "vendor": "SemBicho Security",
                "name": "sembicho-cli",
                "version": "2.5.0"
            }],
            "component": {
                "type": "application",
                "name": os.path.basename(scan_path),
                "version": "1.0.0"
            }
        }
        
        sbom = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "serialNumber": f"urn:uuid:{self._generate_uuid()}",
            "version": 1,
            "metadata": metadata,
            "components": components
        }
        
        logging.info(f"✅ Generated CycloneDX SBOM with {len(components)} components")
        return sbom
    
    def _generate_purl(self, dep: Dict[str, Any]) -> str:
        """
        Genera Package URL (purl) según spec https://github.com/package-url/purl-spec
        
        Args:
            dep: Diccionario con info de dependencia
            
        Returns:
            String purl (ej: pkg:npm/express@4.17.1)
        """
        dep_type = dep['type']
        name = dep['name']
        version = dep['version']
        
        # Mapeo de tipos a namespaces purl
        type_mapping = {
            'python': 'pypi',
            'npm': 'npm',
            'maven': 'maven',
            'composer': 'composer',
            'gem': 'gem',
            'nuget': 'nuget'
        }
        
        purl_type = type_mapping.get(dep_type, dep_type)
        
        # Maven usa namespace diferente (group:artifact)
        if dep_type == 'maven' and ':' in name:
            group, artifact = name.split(':', 1)
            return f"pkg:maven/{group}/{artifact}@{version}"
        
        return f"pkg:{purl_type}/{name}@{version}"
    
    def _generate_uuid(self) -> str:
        """Genera UUID v4 simple sin dependencia externa"""
        import random
        return ''.join(random.choice('0123456789abcdef') for _ in range(32))
    
    def _scan_dependencies_for_cves(self, scan_path: str) -> Optional[List[Dict[str, Any]]]:
        """
        🔥 NUEVO v2.6.0: Escanea dependencias en busca de CVEs conocidos
        
        Utiliza:
        1. Safety DB (Python dependencies)
        2. OSV (Open Source Vulnerabilities) - multi-lenguaje
        3. NVD API como fallback
        
        Args:
            scan_path: Ruta del proyecto a escanear
            
        Returns:
            Lista de CVEs encontrados con detalles, o None si no hay
        """
        dependencies = self._extract_dependencies(scan_path)
        if not dependencies:
            logging.warning("No dependencies to scan for CVEs")
            return None
        
        cve_findings = []
        
        # Escanear Python dependencies con Safety
        python_deps = [d for d in dependencies if d['type'] == 'python']
        if python_deps:
            cve_findings.extend(self._scan_python_with_safety(python_deps))
        
        # Escanear con OSV API (multi-lenguaje)
        npm_deps = [d for d in dependencies if d['type'] == 'npm']
        maven_deps = [d for d in dependencies if d['type'] == 'maven']
        
        if npm_deps:
            cve_findings.extend(self._scan_with_osv(npm_deps, 'npm'))
        
        if maven_deps:
            cve_findings.extend(self._scan_with_osv(maven_deps, 'Maven'))
        
        logging.info(f"🔍 Found {len(cve_findings)} CVEs in dependencies")
        return cve_findings if cve_findings else None
    
    def _scan_python_with_safety(self, python_deps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Escanea dependencias Python usando Safety CLI (si está disponible)
        o usando Safety DB API directamente
        
        Args:
            python_deps: Lista de dependencias Python
            
        Returns:
            Lista de CVEs encontrados
        """
        cves = []
        
        # Intentar con Safety CLI primero
        try:
            # Crear temp requirements.txt
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
                for dep in python_deps:
                    if dep['version'] != 'latest':
                        tmp.write(f"{dep['name']}=={dep['version']}\n")
                tmp_path = tmp.name
            
            # Ejecutar safety check con --continue-on-error para evitar exit codes != 0
            result = subprocess.run(
                ['safety', 'check', '--json', '-r', tmp_path, '--continue-on-error'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.unlink(tmp_path)
            
            # Verificar que stdout sea JSON válido antes de parsear
            if result.stdout and result.stdout.strip():
                try:
                    # Intentar parsear como JSON
                    safety_data = json.loads(result.stdout)
                    
                    # Safety puede devolver dict con 'vulnerabilities' key o lista directa
                    vulns = safety_data if isinstance(safety_data, list) else safety_data.get('vulnerabilities', [])
                    
                    for vuln in vulns:
                        cves.append({
                            'cve_id': vuln.get('cve', vuln.get('id', 'PYSEC-UNKNOWN')),
                            'package': vuln.get('package_name', vuln.get('package', 'unknown')),
                            'version': vuln.get('vulnerable_spec', vuln.get('version', 'unknown')),
                            'severity': vuln.get('severity', 'UNKNOWN').upper(),
                            'title': vuln.get('advisory', vuln.get('title', 'Security vulnerability')),
                            'description': vuln.get('advisory', vuln.get('description', '')),
                            'fixed_version': vuln.get('fixed_in', []),
                            'source': 'safety',
                            'cvss_score': vuln.get('cvss', None)
                        })
                    
                    if cves:
                        logging.info(f"✅ Safety scan completed: {len(cves)} CVEs found")
                    else:
                        logging.info("✅ Safety scan completed: No vulnerabilities found")
                        
                except json.JSONDecodeError as json_err:
                    # Safety devolvió texto en lugar de JSON (probablemente error de auth o config)
                    logging.warning(f"Safety output is not valid JSON, skipping. Output: {result.stdout[:100]}")
                    # Intentar extraer info del stderr si existe
                    if result.stderr and 'authentication' in result.stderr.lower():
                        logging.info("💡 Tip: Safety requires authentication. Set SAFETY_API_KEY env var or use --continue-on-error")
            else:
                # No hay output, probablemente no hay vulnerabilidades o error
                if result.returncode == 0:
                    logging.info("✅ Safety scan completed: No vulnerabilities found")
                else:
                    logging.warning(f"Safety scan returned no output (exit code {result.returncode})")
                    
        except FileNotFoundError:
            logging.warning("Safety CLI not installed, skipping Python CVE scan")
        except subprocess.TimeoutExpired:
            logging.warning("Safety scan timed out")
        except Exception as e:
            logging.warning(f"Safety scan error: {e}")
        
        return cves
    
    def _scan_with_osv(self, deps: List[Dict[str, Any]], ecosystem: str) -> List[Dict[str, Any]]:
        """
        Escanea dependencias usando OSV API (https://osv.dev)
        
        Args:
            deps: Lista de dependencias
            ecosystem: Ecosistema (npm, Maven, PyPI, etc)
            
        Returns:
            Lista de CVEs encontrados
        """
        cves = []
        osv_api = "https://api.osv.dev/v1/query"
        
        for dep in deps[:20]:  # Limit to 20 deps to avoid rate limiting
            try:
                payload = {
                    "package": {"name": dep['name'], "ecosystem": ecosystem},
                    "version": dep['version']
                }
                
                response = requests.post(osv_api, json=payload, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    vulns = data.get('vulns', [])
                    
                    for vuln in vulns:
                        cves.append({
                            'cve_id': vuln.get('id', 'OSV-UNKNOWN'),
                            'package': dep['name'],
                            'version': dep['version'],
                            'severity': self._parse_osv_severity(vuln),
                            'title': vuln.get('summary', 'Security vulnerability'),
                            'description': vuln.get('details', ''),
                            'fixed_version': self._extract_fixed_versions(vuln),
                            'source': 'osv',
                            'cvss_score': self._extract_cvss_from_osv(vuln)
                        })
                
                time.sleep(0.2)  # Rate limiting
                
            except requests.Timeout:
                logging.warning(f"OSV API timeout for {dep['name']}")
            except Exception as e:
                logging.warning(f"OSV scan error for {dep['name']}: {e}")
        
        return cves
    
    def _parse_osv_severity(self, vuln: Dict) -> str:
        """Extrae severidad de vulnerability OSV"""
        severity_data = vuln.get('severity', [])
        if severity_data and len(severity_data) > 0:
            sev = severity_data[0].get('score', 'UNKNOWN')
            if isinstance(sev, str):
                return sev.upper()
        return 'MEDIUM'
    
    def _extract_fixed_versions(self, vuln: Dict) -> List[str]:
        """Extrae versiones que solucionan la vulnerabilidad"""
        fixed = []
        affected = vuln.get('affected', [])
        for aff in affected:
            ranges = aff.get('ranges', [])
            for r in ranges:
                events = r.get('events', [])
                for event in events:
                    if 'fixed' in event:
                        fixed.append(event['fixed'])
        return fixed
    
    def _extract_cvss_from_osv(self, vuln: Dict) -> Optional[float]:
        """Extrae CVSS score de vulnerability OSV"""
        severity_data = vuln.get('severity', [])
        for sev in severity_data:
            if sev.get('type') == 'CVSS_V3':
                score_str = sev.get('score', '')
                # Parse "CVSS:3.1/AV:N/AC:L/..."
                if '/' in score_str:
                    return None  # Vector, no score
                try:
                    return float(score_str)
                except:
                    pass
        return None
    
    def _generate_sbom_spdx(self, scan_path: str) -> Optional[Dict[str, Any]]:
        """
        🔥 NUEVO v2.6.0: Genera SBOM en formato SPDX 2.3 JSON
        
        SPDX (Software Package Data Exchange) es un estándar ISO/IEC para SBOM
        https://spdx.dev/
        
        Args:
            scan_path: Ruta del proyecto a escanear
            
        Returns:
            Dict con SBOM en formato SPDX 2.3, o None si no hay dependencias
        """
        dependencies = self._extract_dependencies(scan_path)
        if not dependencies:
            logging.warning("No dependencies found, SPDX SBOM will be empty")
            return None
        
        # Generar packages SPDX
        packages = []
        
        # Package principal (aplicación)
        main_package = {
            "SPDXID": "SPDXRef-Package-Application",
            "name": os.path.basename(scan_path),
            "versionInfo": "1.0.0",
            "supplier": "Organization: Unknown",
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION"
        }
        packages.append(main_package)
        
        # Dependencias como packages
        for idx, dep in enumerate(dependencies, start=1):
            file_path = dep.get('path')
            file_hash = None
            if file_path and os.path.isfile(file_path):
                import hashlib
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
            package = {
                "SPDXID": f"SPDXRef-Package-{idx}",
                "name": dep['name'],
                "versionInfo": dep['version'],
                "supplier": f"Organization: {dep['type']}",
                "downloadLocation": self._generate_download_location(dep),
                "filesAnalyzed": False,
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "copyrightText": "NOASSERTION",
                "externalRefs": [
                    {
                        "referenceCategory": "PACKAGE-MANAGER",
                        "referenceType": "purl",
                        "referenceLocator": self._generate_purl(dep)
                    },
                    {
                        "referenceCategory": "FILE-HASH",
                        "referenceType": "sha256",
                        "referenceLocator": file_hash or "N/A"
                    },
                    {
                        "referenceCategory": "CYCLONEDX",
                        "referenceType": "component-ref",
                        "referenceLocator": f"component:{idx}"
                    }
                ]
            }
            packages.append(package)
        
        # Generar relaciones (dependencias del package principal)
        relationships = []
        for idx in range(1, len(dependencies) + 1):
            relationships.append({
                "spdxElementId": "SPDXRef-Package-Application",
                "relationshipType": "DEPENDS_ON",
                "relatedSpdxElement": f"SPDXRef-Package-{idx}"
            })
        
        sbom_spdx = {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": f"SBOM-{os.path.basename(scan_path)}",
            "documentNamespace": f"https://sembicho.com/spdx/{self._generate_uuid()}",
            "creationInfo": {
                "created": datetime.utcnow().isoformat() + "Z",
                "creators": ["Tool: sembicho-cli-2.6.0"],
                "licenseListVersion": "3.21"
            },
            "packages": packages,
            "relationships": relationships
        }
        
        logging.info(f"✅ Generated SPDX 2.3 SBOM with {len(packages)} packages")
        return sbom_spdx
    
    def _generate_download_location(self, dep: Dict[str, Any]) -> str:
        """
        Genera download location según tipo de dependencia
        
        Args:
            dep: Diccionario con info de dependencia
            
        Returns:
            URL de descarga o NOASSERTION
        """
        dep_type = dep['type']
        name = dep['name']
        version = dep['version']
        
        if dep_type == 'python':
            return f"https://pypi.org/project/{name}/{version}/"
        elif dep_type == 'npm':
            return f"https://registry.npmjs.org/{name}/-/{name}-{version}.tgz"
        elif dep_type == 'maven':
            if ':' in name:
                group, artifact = name.split(':', 1)
                group_path = group.replace('.', '/')
                return f"https://repo1.maven.org/maven2/{group_path}/{artifact}/{version}/{artifact}-{version}.jar"
        elif dep_type == 'composer':
            return f"https://packagist.org/packages/{name}"
        elif dep_type == 'gem':
            return f"https://rubygems.org/gems/{name}/versions/{version}"
        
        return "NOASSERTION"
    
    def _build_dependency_tree(self, scan_path: str) -> Optional[Dict[str, Any]]:
        """
        🔥 NUEVO v2.6.0: Construye árbol de dependencias transitivas
        
        Analiza dependencias directas e indirectas (si están disponibles)
        para detectar vulnerabilidades en toda la cadena.
        
        Args:
            scan_path: Ruta del proyecto a escanear
            
        Returns:
            Árbol de dependencias con niveles, o None si no disponible
        """
        dependencies = self._extract_dependencies(scan_path)
        if not dependencies:
            return None
        
        # Por ahora solo retornamos dependencias directas
        # TODO: Implementar análisis transitivo con pip-tree, npm ls, etc.
        tree = {
            "root": os.path.basename(scan_path),
            "direct_dependencies": len(dependencies),
            "transitive_dependencies": 0,  # Requiere análisis profundo
            "total_dependencies": len(dependencies),
            "dependencies": [
                {
                    "name": dep['name'],
                    "version": dep['version'],
                    "type": dep['type'],
                    "level": 1,  # Direct dependency
                    "children": []  # TODO: Analizar subdependencias
                }
                for dep in dependencies
            ],
            "depth": 1,
            "notes": "Full transitive analysis requires pip-tree or npm ls integration"
        }
        
        logging.info(f"📊 Dependency tree: {len(dependencies)} direct dependencies")
        return tree
    
    def _enrich_with_nvd(self, cve_findings: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        🔥 NUEVO v2.6.0: Enriquece CVEs con datos de NVD (National Vulnerability Database)
        
        Añade información adicional de NIST NVD:
        - CVSS v3.1 scores detallados
        - EPSS (Exploit Prediction Scoring System)
        - CISA KEV (Known Exploited Vulnerabilities)
        - Referencias CWE
        - Descripción detallada
        
        Args:
            cve_findings: Lista de CVEs encontrados
            
        Returns:
            Diccionario con datos enriquecidos de NVD, o None si API no disponible
        """
        if not cve_findings:
            return None
        
        nvd_data = {
            "total_cves": len(cve_findings),
            "nvd_enriched": 0,
            "epss_available": 0,
            "kev_flagged": 0,
            "enrichment_details": []
        }
        
        nvd_api_base = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        
        for cve in cve_findings[:10]:  # Limit to 10 to avoid rate limiting
            cve_id = cve.get('cve_id', '')
            if not cve_id or not cve_id.startswith('CVE-'):
                continue
            
            try:
                # Query NVD API v2.0
                response = requests.get(
                    f"{nvd_api_base}?cveId={cve_id}",
                    headers={"apiKey": ""},  # Public API, no key needed for basic
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    vulns = data.get('vulnerabilities', [])
                    
                    if vulns:
                        vuln_data = vulns[0].get('cve', {})
                        
                        enriched = {
                            "cve_id": cve_id,
                            "nvd_published": vuln_data.get('published', ''),
                            "nvd_modified": vuln_data.get('lastModified', ''),
                            "description": self._extract_nvd_description(vuln_data),
                            "cvss_v3": self._extract_nvd_cvss_v3(vuln_data),
                            "cwe_ids": self._extract_nvd_cwes(vuln_data),
                            "references": len(vuln_data.get('references', []))
                        }
                        
                        nvd_data["enrichment_details"].append(enriched)
                        nvd_data["nvd_enriched"] += 1
                
                time.sleep(0.6)  # NVD rate limit: max 5 requests/30s without API key
                
            except requests.Timeout:
                logging.warning(f"NVD API timeout for {cve_id}")
            except Exception as e:
                logging.warning(f"NVD enrichment error for {cve_id}: {e}")
        
        if nvd_data["nvd_enriched"] > 0:
            logging.info(f"✅ Enriched {nvd_data['nvd_enriched']}/{len(cve_findings)} CVEs with NVD data")
            return nvd_data
        
        return None
    
    def _extract_nvd_description(self, cve_data: Dict) -> str:
        """Extrae descripción de CVE desde NVD"""
        descriptions = cve_data.get('descriptions', [])
        for desc in descriptions:
            if desc.get('lang') == 'en':
                return desc.get('value', '')
        return ''
    
    def _extract_nvd_cvss_v3(self, cve_data: Dict) -> Optional[Dict[str, Any]]:
        """Extrae CVSS v3 detallado desde NVD"""
        metrics = cve_data.get('metrics', {})
        cvss_v3_list = metrics.get('cvssMetricV31', []) or metrics.get('cvssMetricV30', [])
        
        if cvss_v3_list:
            cvss = cvss_v3_list[0].get('cvssData', {})
            return {
                "baseScore": cvss.get('baseScore'),
                "baseSeverity": cvss.get('baseSeverity'),
                "vectorString": cvss.get('vectorString'),
                "attackVector": cvss.get('attackVector'),
                "attackComplexity": cvss.get('attackComplexity'),
                "privilegesRequired": cvss.get('privilegesRequired'),
                "userInteraction": cvss.get('userInteraction'),
                "scope": cvss.get('scope'),
                "confidentialityImpact": cvss.get('confidentialityImpact'),
                "integrityImpact": cvss.get('integrityImpact'),
                "availabilityImpact": cvss.get('availabilityImpact')
            }
        return None
    
    def _extract_nvd_cwes(self, cve_data: Dict) -> List[str]:
        """Extrae CWE IDs desde NVD"""
        weaknesses = cve_data.get('weaknesses', [])
        cwe_ids = []
        for weakness in weaknesses:
            descriptions = weakness.get('description', [])
            for desc in descriptions:
                value = desc.get('value', '')
                if value.startswith('CWE-'):
                    cwe_ids.append(value)
        return cwe_ids
    
    def detect_languages(self, path: str) -> List[str]:
        """
        Detecta automáticamente los lenguajes en el directorio/archivo
        
        Args:
            path: Ruta a analizar
            
        Returns:
            Lista de lenguajes detectados
        """
        languages = set()
        target_path = Path(path)
        
        if target_path.is_file():
            ext = target_path.suffix.lower()
            if ext in self.SUPPORTED_LANGUAGES:
                languages.add(self.SUPPORTED_LANGUAGES[ext])
        else:
            for file_path in target_path.rglob('*'):
                if file_path.is_file():
                    ext = file_path.suffix.lower()
                    if ext in self.SUPPORTED_LANGUAGES:
                        languages.add(self.SUPPORTED_LANGUAGES[ext])
        
        return list(languages)
    
    def _run_bandit(self, path: str) -> List[Vulnerability]:
        """
        Ejecuta Bandit para análisis de Python
        
        Args:
            path: Ruta a analizar
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        try:
            # Verificar si bandit está disponible
            result = subprocess.run(['bandit', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                raise FileNotFoundError("Bandit no está disponible")
                
            # Ejecutar bandit con formato JSON
            cmd = ['bandit', '-r', path, '-f', 'json']
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            if result.returncode in [0, 1]:  # 0 = sin issues, 1 = issues encontrados
                data = json.loads(result.stdout)
                
                for issue in data.get('results', []):
                    vuln = Vulnerability(
                        file=issue.get('filename', ''),
                        line=issue.get('line_number', 0),
                        rule_id=issue.get('test_id', ''),
                        severity=issue.get('issue_severity', 'medium').lower(),
                        message=issue.get('issue_text', ''),
                        cwe=issue.get('issue_cwe', {}).get('id') if issue.get('issue_cwe') else None,
                        tool='bandit',
                        confidence=issue.get('issue_confidence', '').lower()
                    )
                    vulnerabilities.append(vuln)
                    
                self.tools_used.append('bandit')
                self.logger.info(f"Bandit encontró {len(vulnerabilities)} vulnerabilidades")
                
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            self.logger.warning(f"Bandit no disponible o error: {e}")
        except FileNotFoundError:
            self.logger.debug("Bandit no está instalado, generando análisis básico de Python")
            vulnerabilities.extend(self._basic_python_security_analysis(path))
        except json.JSONDecodeError:
            self.logger.error("Error parseando salida de Bandit")
        except Exception as e:
            self.logger.warning(f"Bandit no disponible: {e}")
            vulnerabilities.extend(self._basic_python_security_analysis(path))
            
        return vulnerabilities
    
    def _run_eslint(self, path: str) -> List[Vulnerability]:
        """
        Ejecuta ESLint para análisis de JavaScript/TypeScript
        
        Args:
            path: Ruta a analizar
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        try:
            # Ejecutar eslint con formato JSON
            cmd = ['npx', 'eslint', path, '--format', 'json', '--ext', '.js,.ts,.jsx,.tsx']
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            if result.returncode in [0, 1]:  # 0 = sin issues, 1 = issues encontrados
                data = json.loads(result.stdout)
                
                for file_result in data:
                    for message in file_result.get('messages', []):
                        severity = self._map_eslint_severity(message.get('severity', 1))
                        
                        vuln = Vulnerability(
                            file=file_result.get('filePath', ''),
                            line=message.get('line', 0),
                            rule_id=message.get('ruleId', ''),
                            severity=severity,
                            message=message.get('message', ''),
                            tool='eslint'
                        )
                        vulnerabilities.append(vuln)
                        
                self.tools_used.append('eslint')
                self.logger.info(f"ESLint encontró {len(vulnerabilities)} vulnerabilidades")
                
        except subprocess.TimeoutExpired:
            self.logger.error("ESLint timeout")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error ejecutando ESLint: {e}")
        except json.JSONDecodeError:
            self.logger.error("Error parseando salida de ESLint")
        except Exception as e:
            self.logger.error(f"Error inesperado en ESLint: {e}")
            
        return vulnerabilities
    
    def _run_semgrep(self, path: str) -> List[Vulnerability]:
        """
        Ejecuta Semgrep para análisis multi-lenguaje
        
        Args:
            path: Ruta a analizar
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        try:
            # Ejecutar semgrep con reglas automáticas
            cmd = ['semgrep', '--config=auto', '--json', path]
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            if result.returncode in [0, 1]:  # 0 = sin issues, 1 = issues encontrados
                data = json.loads(result.stdout)
                
                for finding in data.get('results', []):
                    severity = self._map_semgrep_severity(finding.get('extra', {}).get('severity', 'INFO'))
                    
                    vuln = Vulnerability(
                        file=finding.get('path', ''),
                        line=finding.get('start', {}).get('line', 0),
                        rule_id=finding.get('check_id', ''),
                        severity=severity,
                        message=finding.get('extra', {}).get('message', ''),
                        cwe=self._extract_cwe_from_semgrep(finding),
                        tool='semgrep'
                    )
                    vulnerabilities.append(vuln)
                    
                self.tools_used.append('semgrep')
                self.logger.info(f"Semgrep encontró {len(vulnerabilities)} vulnerabilidades")
                
        except subprocess.TimeoutExpired:
            self.logger.warning("Semgrep timeout")
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Semgrep no disponible o error: {e}")
        except FileNotFoundError:
            self.logger.debug("Semgrep no está instalado, generando análisis básico")
            vulnerabilities.extend(self._basic_multi_language_analysis(path))
        except json.JSONDecodeError:
            self.logger.error("Error parseando salida de Semgrep")
        except Exception as e:
            self.logger.warning(f"Semgrep no disponible: {e}")
            vulnerabilities.extend(self._basic_multi_language_analysis(path))
            
        return vulnerabilities
    
    def _run_secrets_scanner(self, path: str) -> List[Vulnerability]:
        """
        Ejecuta escaneo de secretos y credenciales hardcodeadas
        
        Args:
            path: Ruta a analizar
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        # Patrones de secretos comunes
        secret_patterns = {
            'aws_access_key': r'AKIA[0-9A-Z]{16}',
            'aws_secret_key': r'[0-9a-zA-Z/+]{40}',
            'github_token': r'ghp_[A-Za-z0-9]{36}',
            'github_oauth': r'gho_[A-Za-z0-9]{36}',
            'slack_token': r'xox[baprs]-[0-9]{12}-[0-9]{12}-[0-9a-zA-Z]{24}',
            'discord_token': r'[MNO][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}',
            'telegram_bot': r'[0-9]{9}:[A-Za-z0-9_-]{35}',
            'generic_api_key': r'(?i)(api[_-]?key|apikey|access[_-]?token)["\']?\s*[:=]\s*["\']([a-zA-Z0-9_-]{20,})["\']',
            'password': r'(?i)(password|passwd|pwd)["\']?\s*[:=]\s*["\']([^"\']{8,})["\']',
            'database_url': r'(?i)(database_url|db_url)["\']?\s*[:=]\s*["\']([^"\']{10,})["\']',
            'jwt_secret': r'(?i)(jwt[_-]?secret|secret[_-]?key)["\']?\s*[:=]\s*["\']([a-zA-Z0-9_-]{20,})["\']',
            'private_key': r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----',
            'credit_card': r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b'
        }
        
        try:
            path_obj = Path(path)
            
            if path_obj.is_file():
                files_to_scan = [path_obj]
            else:
                files_to_scan = []
                for ext in ['.py', '.js', '.ts', '.json', '.yml', '.yaml', '.env', '.config']:
                    files_to_scan.extend(path_obj.rglob(f'*{ext}'))
            
            for file_path in files_to_scan:
                if not file_path.is_file():
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        for secret_type, pattern in secret_patterns.items():
                            matches = re.finditer(pattern, line)
                            
                            for match in matches:
                                # Validaciones adicionales para reducir falsos positivos
                                if self._is_likely_secret(line, match.group(0), secret_type):
                                    severity = self._get_secret_severity(secret_type)
                                    
                                    vuln = Vulnerability(
                                        file=str(file_path),
                                        line=line_num,
                                        rule_id=f'SECRETS-{secret_type.upper()}',
                                        severity=severity,
                                        message=f'Possible {secret_type.replace("_", " ")} detected: {match.group(0)[:20]}...',
                                        cwe='CWE-798',
                                        owasp_category='A02',
                                        tool='secrets',
                                        confidence='medium',
                                        category='security',
                                        impact='high',
                                        likelihood='medium',
                                        code_snippet=line.strip()
                                    )
                                    vulnerabilities.append(vuln)
                
                except Exception as e:
                    self.logger.debug(f"Error escaneando {file_path}: {e}")
                    continue
            
            self.tools_used.append('secrets')
            self.logger.info(f"Secrets scanner encontró {len(vulnerabilities)} posibles secretos")
            
        except Exception as e:
            self.logger.error(f"Error en secrets scanner: {e}")
        
        return vulnerabilities
    
    def _is_likely_secret(self, line: str, match: str, secret_type: str) -> bool:
        """
        Determina si un match es probablemente un secreto real
        
        Args:
            line: Línea de código completa
            match: Texto que coincide con el patrón
            secret_type: Tipo de secreto detectado
            
        Returns:
            True si es probable que sea un secreto real
        """
        line_lower = line.lower()
        
        # Filtrar comentarios y documentación
        if any(marker in line for marker in ['#', '//', '/*', '*/', '"""', "'''"]):
            return False
        
        # Filtrar ejemplos y placeholders
        if any(word in line_lower for word in ['example', 'placeholder', 'your_', 'put_your', 'insert_', 'replace_']):
            return False
        
        # Filtrar valores obvios de prueba
        if any(test_val in match.lower() for test_val in ['test', 'demo', 'sample', '123456', 'password', 'secret']):
            return False
        
        # Filtrar secretos demasiado cortos (excepto algunos tipos específicos)
        if secret_type not in ['credit_card', 'private_key'] and len(match) < 15:
            return False
        
        return True
    
    def _get_secret_severity(self, secret_type: str) -> str:
        """
        Determina la severidad basada en el tipo de secreto
        
        Args:
            secret_type: Tipo de secreto
            
        Returns:
            Nivel de severidad
        """
        critical_secrets = ['aws_access_key', 'aws_secret_key', 'private_key', 'database_url']
        high_secrets = ['github_token', 'github_oauth', 'slack_token', 'jwt_secret']
        medium_secrets = ['discord_token', 'telegram_bot', 'generic_api_key']
        
        if secret_type in critical_secrets:
            return 'critical'
        elif secret_type in high_secrets:
            return 'high'
        elif secret_type in medium_secrets:
            return 'medium'
        else:
            return 'low'
    
    def _run_dependency_scanner(self, path: str) -> List[Vulnerability]:
        """
        Ejecuta escaneo de vulnerabilidades en dependencias
        
        Args:
            path: Ruta a analizar
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        try:
            path_obj = Path(path)
            
            # Buscar archivos de dependencias
            dependency_files = {
                'package.json': self._scan_npm_dependencies,
                'requirements.txt': self._scan_python_dependencies,
                'Pipfile': self._scan_pipenv_dependencies,
                'pom.xml': self._scan_maven_dependencies,
                'build.gradle': self._scan_gradle_dependencies,
                'composer.json': self._scan_composer_dependencies
            }
            
            for dep_file, scanner_func in dependency_files.items():
                if path_obj.is_file() and path_obj.name == dep_file:
                    vulnerabilities.extend(scanner_func(path_obj))
                elif path_obj.is_dir():
                    found_files = list(path_obj.rglob(dep_file))
                    for found_file in found_files:
                        vulnerabilities.extend(scanner_func(found_file))
            
            if vulnerabilities:
                self.tools_used.append('dependency-check')
                self.logger.info(f"Dependency scanner encontró {len(vulnerabilities)} vulnerabilidades")
            
        except Exception as e:
            self.logger.error(f"Error en dependency scanner: {e}")
        
        return vulnerabilities
    
    def _scan_npm_dependencies(self, package_file: Path) -> List[Vulnerability]:
        """Escanea dependencias de NPM"""
        vulnerabilities = []
        
        try:
            # Intentar usar npm audit si está disponible
            result = subprocess.run(
                ['npm', 'audit', '--json'],
                cwd=package_file.parent,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 or result.stdout:
                audit_data = json.loads(result.stdout)
                
                for advisory_id, advisory in audit_data.get('advisories', {}).items():
                    vuln = Vulnerability(
                        file=str(package_file),
                        line=1,
                        rule_id=f'NPM-{advisory_id}',
                        severity=self._map_npm_severity(advisory.get('severity', 'moderate')),
                        message=f"Vulnerable npm package: {advisory.get('module_name')} - {advisory.get('title')}",
                        cwe=advisory.get('cwe'),
                        tool='npm-audit',
                        confidence='high',
                        category='dependency',
                        impact='medium',
                        likelihood='high'
                    )
                    vulnerabilities.append(vuln)
                    
        except (subprocess.CalledProcessError, json.JSONDecodeError, subprocess.TimeoutExpired):
            # Fallback: análisis básico del package.json
            vulnerabilities.extend(self._basic_npm_analysis(package_file))
        
        return vulnerabilities
    
    def _scan_python_dependencies(self, req_file: Path) -> List[Vulnerability]:
        """Escanea dependencias de Python"""
        vulnerabilities = []
        
        try:
            # Intentar usar safety check si está disponible
            result = subprocess.run(
                ['safety', 'check', '--json', '-r', str(req_file)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and result.stdout:
                safety_data = json.loads(result.stdout)
                
                for vuln_data in safety_data:
                    vuln = Vulnerability(
                        file=str(req_file),
                        line=1,
                        rule_id=f'PY-{vuln_data.get("id")}',
                        severity='high',
                        message=f"Vulnerable Python package: {vuln_data.get('package')} - {vuln_data.get('advisory')}",
                        tool='safety',
                        confidence='high',
                        category='dependency',
                        impact='high',
                        likelihood='medium'
                    )
                    vulnerabilities.append(vuln)
                    
        except (subprocess.CalledProcessError, json.JSONDecodeError, subprocess.TimeoutExpired):
            # Fallback: análisis básico
            vulnerabilities.extend(self._basic_python_analysis(req_file))
        
        return vulnerabilities
    
    def _basic_npm_analysis(self, package_file: Path) -> List[Vulnerability]:
        """Análisis básico de package.json sin herramientas externas"""
        vulnerabilities = []
        
        # Paquetes conocidos con vulnerabilidades comunes
        vulnerable_packages = {
            'lodash': {'versions': ['<4.17.21'], 'severity': 'high'},
            'axios': {'versions': ['<0.21.1'], 'severity': 'medium'},
            'minimist': {'versions': ['<1.2.6'], 'severity': 'high'},
            'yargs-parser': {'versions': ['<13.1.2'], 'severity': 'medium'},
            'serialize-javascript': {'versions': ['<6.0.0'], 'severity': 'high'}
        }
        
        try:
            with open(package_file, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            dependencies = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
            
            for package, version in dependencies.items():
                if package in vulnerable_packages:
                    vuln_info = vulnerable_packages[package]
                    vuln = Vulnerability(
                        file=str(package_file),
                        line=1,
                        rule_id=f'NPM-BASIC-{package.upper()}',
                        severity=vuln_info['severity'],
                        message=f"Potentially vulnerable npm package: {package}@{version}",
                        tool='basic-npm-check',
                        confidence='medium',
                        category='dependency',
                        impact='medium',
                        likelihood='medium'
                    )
                    vulnerabilities.append(vuln)
                    
        except Exception as e:
            self.logger.debug(f"Error en análisis básico NPM: {e}")
        
        return vulnerabilities
    
    def _basic_python_analysis(self, req_file: Path) -> List[Vulnerability]:
        """Análisis básico de requirements.txt"""
        vulnerabilities = []
        
        # Paquetes conocidos con vulnerabilidades
        vulnerable_packages = {
            'django': {'versions': ['<3.2.13'], 'severity': 'high'},
            'flask': {'versions': ['<2.0.0'], 'severity': 'medium'},
            'requests': {'versions': ['<2.25.0'], 'severity': 'medium'},
            'pillow': {'versions': ['<8.3.2'], 'severity': 'high'},
            'pyyaml': {'versions': ['<5.4.0'], 'severity': 'medium'}
        }
        
        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].strip()
                    
                    if package_name in vulnerable_packages:
                        vuln_info = vulnerable_packages[package_name]
                        vuln = Vulnerability(
                            file=str(req_file),
                            line=line_num,
                            rule_id=f'PY-BASIC-{package_name.upper()}',
                            severity=vuln_info['severity'],
                            message=f"Potentially vulnerable Python package: {line}",
                            tool='basic-python-check',
                            confidence='medium',
                            category='dependency',
                            impact='medium',
                            likelihood='medium'
                        )
                        vulnerabilities.append(vuln)
                        
        except Exception as e:
            self.logger.debug(f"Error en análisis básico Python: {e}")
        
        return vulnerabilities
    
    def _scan_pipenv_dependencies(self, pipfile: Path) -> List[Vulnerability]:
        """Placeholder para escaneo de Pipenv"""
        return []
    
    def _scan_maven_dependencies(self, pom_file: Path) -> List[Vulnerability]:
        """Placeholder para escaneo de Maven"""
        return []
    
    def _scan_gradle_dependencies(self, gradle_file: Path) -> List[Vulnerability]:
        """Placeholder para escaneo de Gradle"""
        return []
    
    def _scan_composer_dependencies(self, composer_file: Path) -> List[Vulnerability]:
        """Placeholder para escaneo de Composer"""
        return []
    
    def _analyze_python_internal(self, path: str) -> List[Vulnerability]:
        """
        Análisis empresarial completo de seguridad para Python
        
        Args:
            path: Ruta a analizar (archivo o directorio)
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        # Patrones de seguridad para Python (nivel empresarial) - 80+ patrones
        security_patterns = {
            # === INJECTION VULNERABILITIES (OWASP A03) ===
            'hardcoded_password': {
                'pattern': r'(?i)(password|passwd|pwd|secret|key|token|api_key)\s*=\s*["\'][^"\']{3,}["\']',
                'severity': 'critical',
                'message': 'Hardcoded password or secret detected',
                'cwe': 'CWE-798',
                'owasp': 'A07',
                'rule_id': 'PY-HARDCODED-SECRET'
            },
            'sql_injection_format': {
                'pattern': r'(?i)(execute|query|cursor)\s*\(\s*["\'][^"\']*%[sd][^"\']*["\']',
                'severity': 'critical',
                'message': 'SQL injection via string formatting',
                'cwe': 'CWE-89',
                'owasp': 'A03',
                'rule_id': 'PY-SQL-INJECTION-FORMAT'
            },
            'sql_injection_concat': {
                'pattern': r'(?i)(execute|query|cursor)\s*\([^)]*\+.*["\']',
                'severity': 'critical',
                'message': 'SQL injection via string concatenation',
                'cwe': 'CWE-89',
                'owasp': 'A03',
                'rule_id': 'PY-SQL-INJECTION-CONCAT'
            },
            'sql_injection_fstring': {
                'pattern': r'(?i)(execute|query|cursor)\s*\(\s*f["\'][^"\']*\{[^}]*\}[^"\']*["\']',
                'severity': 'critical',
                'message': 'SQL injection via f-string',
                'cwe': 'CWE-89',
                'owasp': 'A03',
                'rule_id': 'PY-SQL-INJECTION-FSTRING'
            },
            'django_raw_sql': {
                'pattern': r'(?i)\.raw\s*\([^)]*\+',
                'severity': 'high',
                'message': 'Django raw SQL with concatenation',
                'cwe': 'CWE-89',
                'owasp': 'A03',
                'rule_id': 'PY-DJANGO-RAW-SQL'
            },
            'command_injection_os': {
                'pattern': r'os\.(system|popen|exec|spawn)',
                'severity': 'high',
                'message': 'Command injection vulnerability via os module',
                'cwe': 'CWE-78',
                'owasp': 'A03',
                'rule_id': 'PY-COMMAND-INJECTION-OS'
            },
            'command_injection_subprocess': {
                'pattern': r'subprocess\.(call|run|Popen).*shell\s*=\s*True',
                'severity': 'high',
                'message': 'Command injection via subprocess with shell=True',
                'cwe': 'CWE-78',
                'owasp': 'A03',
                'rule_id': 'PY-COMMAND-INJECTION-SUBPROCESS'
            },
            'eval_usage': {
                'pattern': r'\beval\s*\(',
                'severity': 'critical',
                'message': 'Code injection via eval()',
                'cwe': 'CWE-95',
                'owasp': 'A03',
                'rule_id': 'PY-EVAL-USAGE'
            },
            'exec_usage': {
                'pattern': r'\bexec\s*\(',
                'severity': 'critical', 
                'message': 'Code injection via exec()',
                'cwe': 'CWE-95',
                'owasp': 'A03',
                'rule_id': 'PY-EXEC-USAGE'
            },
            'compile_usage': {
                'pattern': r'\bcompile\s*\(',
                'severity': 'high',
                'message': 'Dynamic code compilation detected',
                'cwe': 'CWE-95',
                'owasp': 'A03',
                'rule_id': 'PY-COMPILE-USAGE'
            },
            'path_traversal_open': {
                'pattern': r'open\s*\([^)]*\.\./.*["\']',
                'severity': 'high',
                'message': 'Potential path traversal vulnerability',
                'cwe': 'CWE-22',
                'owasp': 'A01',
                'rule_id': 'PY-PATH-TRAVERSAL-OPEN'
            },
            'path_traversal_user_input': {
                'pattern': r'open\s*\([^)]*request\.|open\s*\([^)]*input\(',
                'severity': 'high',
                'message': 'File access with user input',
                'cwe': 'CWE-22',
                'owasp': 'A01',
                'rule_id': 'PY-PATH-TRAVERSAL-INPUT'
            },
            'ldap_injection': {
                'pattern': r'ldap.*search.*\+',
                'severity': 'high',
                'message': 'LDAP injection vulnerability',
                'cwe': 'CWE-90',
                'owasp': 'A03',
                'rule_id': 'PY-LDAP-INJECTION'
            },
            'xml_external_entity': {
                'pattern': r'XMLParser.*resolve_entities\s*=\s*True',
                'severity': 'high',
                'message': 'XML External Entity (XXE) vulnerability',
                'cwe': 'CWE-611',
                'owasp': 'A05',
                'rule_id': 'PY-XXE-VULNERABILITY'
            },
            
            # === DESERIALIZATION VULNERABILITIES (OWASP A08) ===
            'pickle_loads': {
                'pattern': r'pickle\.loads?\s*\(',
                'severity': 'critical',
                'message': 'Insecure deserialization via pickle',
                'cwe': 'CWE-502',
                'owasp': 'A08',
                'rule_id': 'PY-UNSAFE-PICKLE'
            },
            'cpickle_loads': {
                'pattern': r'cPickle\.loads?\s*\(',
                'severity': 'critical',
                'message': 'Insecure deserialization via cPickle',
                'cwe': 'CWE-502',
                'owasp': 'A08',
                'rule_id': 'PY-UNSAFE-CPICKLE'
            },
            'yaml_unsafe_load': {
                'pattern': r'yaml\.load\s*\([^)]*\)',
                'severity': 'high',
                'message': 'Unsafe YAML deserialization',
                'cwe': 'CWE-502',
                'owasp': 'A08',
                'rule_id': 'PY-YAML-UNSAFE'
            },
            'marshal_loads': {
                'pattern': r'marshal\.loads?\s*\(',
                'severity': 'high',
                'message': 'Unsafe marshal deserialization',
                'cwe': 'CWE-502',
                'owasp': 'A08',
                'rule_id': 'PY-MARSHAL-UNSAFE'
            },
            'shelve_open': {
                'pattern': r'shelve\.open\s*\(',
                'severity': 'medium',
                'message': 'Potentially unsafe shelve usage',
                'cwe': 'CWE-502',
                'owasp': 'A08',
                'rule_id': 'PY-SHELVE-USAGE'
            },
            
            # === CRYPTOGRAPHIC FAILURES (OWASP A02) ===
            'weak_random': {
                'pattern': r'random\.(random|randint|choice|uniform|seed)',
                'severity': 'medium',
                'message': 'Cryptographically weak random number generation',
                'cwe': 'CWE-338',
                'owasp': 'A02',
                'rule_id': 'PY-WEAK-RANDOM'
            },
            'md5_usage': {
                'pattern': r'hashlib\.md5\s*\(',
                'severity': 'high',
                'message': 'MD5 is cryptographically broken',
                'cwe': 'CWE-327',
                'owasp': 'A02',
                'rule_id': 'PY-MD5-USAGE'
            },
            'sha1_usage': {
                'pattern': r'hashlib\.sha1\s*\(',
                'severity': 'medium',
                'message': 'SHA1 is cryptographically weak',
                'cwe': 'CWE-327',
                'owasp': 'A02',
                'rule_id': 'PY-SHA1-USAGE'
            },
            'no_ssl_verification': {
                'pattern': r'verify\s*=\s*False|ssl._create_unverified_context',
                'severity': 'high',
                'message': 'SSL certificate verification disabled',
                'cwe': 'CWE-295',
                'owasp': 'A02',
                'rule_id': 'PY-SSL-VERIFICATION-DISABLED'
            },
            'weak_ssl_protocol': {
                'pattern': r'PROTOCOL_SSLv[23]|PROTOCOL_TLSv1\b',
                'severity': 'high',
                'message': 'Weak SSL/TLS protocol version',
                'cwe': 'CWE-326',
                'owasp': 'A02',
                'rule_id': 'PY-WEAK-SSL-PROTOCOL'
            },
            'des_cipher': {
                'pattern': r'DES\.new|TripleDES\.new',
                'severity': 'high',
                'message': 'Weak encryption algorithm (DES/3DES)',
                'cwe': 'CWE-327',
                'owasp': 'A02',
                'rule_id': 'PY-WEAK-CIPHER-DES'
            },
            'rc4_cipher': {
                'pattern': r'ARC4\.new|RC4\.new',
                'severity': 'high',
                'message': 'Weak encryption algorithm (RC4)',
                'cwe': 'CWE-327',
                'owasp': 'A02',
                'rule_id': 'PY-WEAK-CIPHER-RC4'
            },
            'hardcoded_encryption_key': {
                'pattern': r'(?i)(key|secret)\s*=\s*["\'][a-zA-Z0-9+/=]{16,}["\']',
                'severity': 'critical',
                'message': 'Hardcoded encryption key detected',
                'cwe': 'CWE-798',
                'owasp': 'A02',
                'rule_id': 'PY-HARDCODED-CRYPTO-KEY'
            },
            
            # === SECURITY MISCONFIGURATION (OWASP A05) ===
            'debug_mode_django': {
                'pattern': r'(?i)DEBUG\s*=\s*True',
                'severity': 'medium',
                'message': 'Debug mode enabled in Django',
                'cwe': 'CWE-489',
                'owasp': 'A05',
                'rule_id': 'PY-DJANGO-DEBUG'
            },
            'debug_mode_flask': {
                'pattern': r'app\.run\([^)]*debug\s*=\s*True',
                'severity': 'medium',
                'message': 'Debug mode enabled in Flask',
                'cwe': 'CWE-489',
                'owasp': 'A05',
                'rule_id': 'PY-FLASK-DEBUG'
            },
            'flask_secret_key': {
                'pattern': r'SECRET_KEY\s*=\s*["\'][^"\']*["\']',
                'severity': 'medium',
                'message': 'Flask secret key may be hardcoded',
                'cwe': 'CWE-798',
                'owasp': 'A05',
                'rule_id': 'PY-FLASK-SECRET-KEY'
            },
            'insecure_temp_file': {
                'pattern': r'tempfile\.mktemp\s*\(',
                'severity': 'medium',
                'message': 'Insecure temporary file creation',
                'cwe': 'CWE-377',
                'owasp': 'A05',
                'rule_id': 'PY-INSECURE-TEMP-FILE'
            },
            'world_writable_file': {
                'pattern': r'chmod.*777|os\.chmod.*0o777',
                'severity': 'medium',
                'message': 'World-writable file permissions',
                'cwe': 'CWE-732',
                'owasp': 'A05',
                'rule_id': 'PY-WORLD-WRITABLE'
            },
            'django_csrf_exempt': {
                'pattern': r'@csrf_exempt',
                'severity': 'medium',
                'message': 'CSRF protection disabled',
                'cwe': 'CWE-352',
                'owasp': 'A05',
                'rule_id': 'PY-CSRF-EXEMPT'
            },
            'django_middleware_missing': {
                'pattern': r'MIDDLEWARE.*=.*\[.*\]',
                'severity': 'low',
                'message': 'Review Django middleware configuration',
                'cwe': 'CWE-693',
                'owasp': 'A05',
                'rule_id': 'PY-DJANGO-MIDDLEWARE'
            },
            
            # === BROKEN ACCESS CONTROL (OWASP A01) ===
            'unvalidated_redirect': {
                'pattern': r'redirect\s*\([^)]*request\.',
                'severity': 'medium',
                'message': 'Unvalidated redirect vulnerability',
                'cwe': 'CWE-601',
                'owasp': 'A01',
                'rule_id': 'PY-UNVALIDATED-REDIRECT'
            },
            'django_user_input_redirect': {
                'pattern': r'HttpResponseRedirect\s*\([^)]*request\.',
                'severity': 'medium',
                'message': 'Redirect with user input',
                'cwe': 'CWE-601',
                'owasp': 'A01',
                'rule_id': 'PY-DJANGO-USER-REDIRECT'
            },
            'flask_send_file_user_input': {
                'pattern': r'send_file\s*\([^)]*request\.',
                'severity': 'high',
                'message': 'File access with user input',
                'cwe': 'CWE-22',
                'owasp': 'A01',
                'rule_id': 'PY-FLASK-SEND-FILE'
            },
            'authorization_bypass': {
                'pattern': r'@login_required.*#.*skip|if.*is_authenticated.*#.*bypass',
                'severity': 'high',
                'message': 'Potential authorization bypass',
                'cwe': 'CWE-862',
                'owasp': 'A01',
                'rule_id': 'PY-AUTH-BYPASS'
            },
            
            # === IDENTIFICATION AND AUTHENTICATION FAILURES (OWASP A07) ===
            'weak_session_config': {
                'pattern': r'SESSION_COOKIE_SECURE\s*=\s*False|SESSION_COOKIE_HTTPONLY\s*=\s*False',
                'severity': 'medium',
                'message': 'Insecure session cookie configuration',
                'cwe': 'CWE-614',
                'owasp': 'A07',
                'rule_id': 'PY-WEAK-SESSION-CONFIG'
            },
            'session_fixation': {
                'pattern': r'session\[["\'].*["\']]\s*=.*request\.',
                'severity': 'medium',
                'message': 'Potential session fixation vulnerability',
                'cwe': 'CWE-384',
                'owasp': 'A07',
                'rule_id': 'PY-SESSION-FIXATION'
            },
            'password_in_get': {
                'pattern': r'password.*=.*request\.GET',
                'severity': 'medium',
                'message': 'Password transmitted in GET request',
                'cwe': 'CWE-598',
                'owasp': 'A07',
                'rule_id': 'PY-PASSWORD-IN-GET'
            },
            'weak_jwt_secret': {
                'pattern': r'jwt\.encode.*["\']secret["\']',
                'severity': 'high',
                'message': 'Weak JWT secret key',
                'cwe': 'CWE-798',
                'owasp': 'A07',
                'rule_id': 'PY-WEAK-JWT-SECRET'
            },
            
            # === SECURITY LOGGING AND MONITORING FAILURES (OWASP A09) ===
            'empty_except_block': {
                'pattern': r'except.*:\s*pass\s*$',
                'severity': 'low',
                'message': 'Empty exception handler may hide errors',
                'cwe': 'CWE-703',
                'owasp': 'A09',
                'rule_id': 'PY-EMPTY-EXCEPT'
            },
            'broad_exception_handler': {
                'pattern': r'except\s*:\s*|except\s+Exception\s*:\s*',
                'severity': 'low',
                'message': 'Overly broad exception handler',
                'cwe': 'CWE-703',
                'owasp': 'A09',
                'rule_id': 'PY-BROAD-EXCEPT'
            },
            'assert_usage_security': {
                'pattern': r'assert\s+.*security|assert\s+.*auth',
                'severity': 'medium',
                'message': 'Security assertion may be disabled in production',
                'cwe': 'CWE-617',
                'owasp': 'A09',
                'rule_id': 'PY-SECURITY-ASSERT'
            },
            'print_sensitive_data': {
                'pattern': r'print\s*\([^)]*(?:password|token|key|secret)',
                'severity': 'medium',
                'message': 'Sensitive data in print statement',
                'cwe': 'CWE-532',
                'owasp': 'A09',
                'rule_id': 'PY-PRINT-SENSITIVE'
            },
            'logging_sensitive_data': {
                'pattern': r'log.*\([^)]*(?:password|token|key|secret)',
                'severity': 'medium',
                'message': 'Sensitive data in log statement',
                'cwe': 'CWE-532',
                'owasp': 'A09',
                'rule_id': 'PY-LOG-SENSITIVE'
            },
            
            # === VULNERABLE AND OUTDATED COMPONENTS (OWASP A06) ===
            'flask_wtf_old': {
                'pattern': r'from flask_wtf import.*WTF',
                'severity': 'low',
                'message': 'Check Flask-WTF version for known vulnerabilities',
                'cwe': 'CWE-1035',
                'owasp': 'A06',
                'rule_id': 'PY-FLASK-WTF-VERSION'
            },
            'requests_version': {
                'pattern': r'import requests',
                'severity': 'low',
                'message': 'Check requests library version for vulnerabilities',
                'cwe': 'CWE-1035',
                'owasp': 'A06',
                'rule_id': 'PY-REQUESTS-VERSION'
            },
            
            # === ADDITIONAL SECURITY PATTERNS ===
            'file_inclusion': {
                'pattern': r'include\s*\([^)]*\$|require\s*\([^)]*\$',
                'severity': 'high',
                'message': 'Potential file inclusion vulnerability',
                'cwe': 'CWE-98',
                'owasp': 'A03',
                'rule_id': 'PY-FILE-INCLUSION'
            },
            'dangerous_defaults': {
                'pattern': r'def\s+\w+\s*\([^)]*=\s*\[\]|def\s+\w+\s*\([^)]*=\s*\{\}',
                'severity': 'low',
                'message': 'Mutable default argument',
                'cwe': 'CWE-1188',
                'owasp': 'A04',
                'rule_id': 'PY-MUTABLE-DEFAULT'
            },
            'type_confusion': {
                'pattern': r'isinstance\s*\([^)]*,\s*str\).*int\(',
                'severity': 'medium',
                'message': 'Potential type confusion vulnerability',
                'cwe': 'CWE-843',
                'owasp': 'A04',
                'rule_id': 'PY-TYPE-CONFUSION'
            },
            'race_condition_file': {
                'pattern': r'os\.path\.exists\s*\([^)]*\).*open\s*\(',
                'severity': 'medium',
                'message': 'Potential race condition (TOCTOU)',
                'cwe': 'CWE-367',
                'owasp': 'A04',
                'rule_id': 'PY-RACE-CONDITION'
            },
            'integer_overflow': {
                'pattern': r'range\s*\([^)]*\*.*[^)]*\)|for.*in.*\*.*:',
                'severity': 'low',
                'message': 'Potential integer overflow in range',
                'cwe': 'CWE-190',
                'owasp': 'A04',
                'rule_id': 'PY-INTEGER-OVERFLOW'
            }
        }
        
        # Patrones de calidad de código y arquitectura (30+ patrones)
        quality_patterns = {
            # === COMPLEJIDAD Y TAMAÑO ===
            'long_function': {
                'pattern': r'def\s+\w+\s*\([^)]*\):',
                'severity': 'low',
                'message': 'Function may be too long (check line count)',
                'cwe': 'CWE-1114',
                'owasp': 'A04',
                'rule_id': 'PY-LONG-FUNCTION'
            },
            'god_class': {
                'pattern': r'class\s+\w+.*:',
                'severity': 'low',
                'message': 'Class may be too large (God Object antipattern)',
                'cwe': 'CWE-1120',
                'owasp': 'A04',
                'rule_id': 'PY-GOD-CLASS'
            },
            'too_many_parameters': {
                'pattern': r'def\s+\w+\s*\([^)]*,.*,.*,.*,.*,.*,.*\):',
                'severity': 'low',
                'message': 'Function has too many parameters (>6)',
                'cwe': 'CWE-1093',
                'owasp': 'A04',
                'rule_id': 'PY-TOO-MANY-PARAMS'
            },
            'deep_nesting': {
                'pattern': r'\s{16,}if\s|    \s{12,}for\s|    \s{12,}while\s',
                'severity': 'low',
                'message': 'Deep nesting detected (>4 levels)',
                'cwe': 'CWE-1121',
                'owasp': 'A04',
                'rule_id': 'PY-DEEP-NESTING'
            },
            'complex_conditional': {
                'pattern': r'if\s+[^:]*and.*and.*and.*:',
                'severity': 'low',
                'message': 'Complex conditional expression',
                'cwe': 'CWE-1122',
                'owasp': 'A04',
                'rule_id': 'PY-COMPLEX-CONDITIONAL'
            },
            
            # === MAGIC NUMBERS Y CONSTANTS ===
            'magic_numbers': {
                'pattern': r'[^a-zA-Z_\[](?:100|200|404|500|1000|9999)\b(?!\])',
                'severity': 'low',
                'message': 'Magic number detected, consider using constants',
                'cwe': 'CWE-1108',
                'owasp': 'A04',
                'rule_id': 'PY-MAGIC-NUMBERS'
            },
            'hardcoded_ip': {
                'pattern': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                'severity': 'low',
                'message': 'Hardcoded IP address',
                'cwe': 'CWE-1188',
                'owasp': 'A04',
                'rule_id': 'PY-HARDCODED-IP'
            },
            'hardcoded_url': {
                'pattern': r'["\']https?://[^"\']*["\']',
                'severity': 'low',
                'message': 'Hardcoded URL, consider configuration',
                'cwe': 'CWE-1188',
                'owasp': 'A04',
                'rule_id': 'PY-HARDCODED-URL'
            },
            
            # === ERROR HANDLING ===
            'broad_except': {
                'pattern': r'except\s*:\s*$|except\s+Exception\s*:\s*$',
                'severity': 'low',
                'message': 'Overly broad exception handler',
                'cwe': 'CWE-703',
                'owasp': 'A09',
                'rule_id': 'PY-BROAD-EXCEPT'
            },
            'empty_except': {
                'pattern': r'except.*:\s*pass\s*$',
                'severity': 'medium',
                'message': 'Empty exception handler silences errors',
                'cwe': 'CWE-703',
                'owasp': 'A09',
                'rule_id': 'PY-EMPTY-EXCEPT'
            },
            'multiple_except_same': {
                'pattern': r'except\s+(\w+)\s*:.*except\s+\1\s*:',
                'severity': 'low',
                'message': 'Duplicate exception handlers',
                'cwe': 'CWE-561',
                'owasp': 'A04',
                'rule_id': 'PY-DUPLICATE-EXCEPT'
            },
            'bare_raise': {
                'pattern': r'^\s*raise\s*$',
                'severity': 'low',
                'message': 'Bare raise without exception context',
                'cwe': 'CWE-755',
                'owasp': 'A04',
                'rule_id': 'PY-BARE-RAISE'
            },
            
            # === MUTABLE DEFAULTS Y SIDE EFFECTS ===
            'mutable_default_list': {
                'pattern': r'def\s+\w+\s*\([^)]*=\s*\[\]',
                'severity': 'medium',
                'message': 'Mutable default argument (list)',
                'cwe': 'CWE-1188',
                'owasp': 'A04',
                'rule_id': 'PY-MUTABLE-DEFAULT-LIST'
            },
            'mutable_default_dict': {
                'pattern': r'def\s+\w+\s*\([^)]*=\s*\{\}',
                'severity': 'medium',
                'message': 'Mutable default argument (dict)',
                'cwe': 'CWE-1188',
                'owasp': 'A04',
                'rule_id': 'PY-MUTABLE-DEFAULT-DICT'
            },
            'global_variable_modification': {
                'pattern': r'global\s+\w+.*=',
                'severity': 'low',
                'message': 'Global variable modification',
                'cwe': 'CWE-1188',
                'owasp': 'A04',
                'rule_id': 'PY-GLOBAL-MODIFICATION'
            },
            
            # === NAMING Y CODING STANDARDS ===
            'single_letter_variable': {
                'pattern': r'\b[a-z]\s*=\s*(?!range|len|int|str|float)',
                'severity': 'low',
                'message': 'Single letter variable name (except common patterns)',
                'cwe': 'CWE-1114',
                'owasp': 'A04',
                'rule_id': 'PY-SINGLE-LETTER-VAR'
            },
            'unused_import': {
                'pattern': r'import\s+(\w+)(?!.*\1)',
                'severity': 'low',
                'message': 'Potentially unused import',
                'cwe': 'CWE-561',
                'owasp': 'A04',
                'rule_id': 'PY-UNUSED-IMPORT'
            },
            'wildcard_import': {
                'pattern': r'from\s+\w+\s+import\s+\*',
                'severity': 'low',
                'message': 'Wildcard import pollutes namespace',
                'cwe': 'CWE-1188',
                'owasp': 'A04',
                'rule_id': 'PY-WILDCARD-IMPORT'
            },
            
            # === PERFORMANCE Y EFFICIENCY ===
            'string_concatenation_loop': {
                'pattern': r'for.*:\s*.*\+=.*["\']',
                'severity': 'low',
                'message': 'String concatenation in loop (use join())',
                'cwe': 'CWE-1046',
                'owasp': 'A04',
                'rule_id': 'PY-STRING-CONCAT-LOOP'
            },
            'inefficient_membership_test': {
                'pattern': r'if\s+\w+\s+in\s+\[.*\]',
                'severity': 'low',
                'message': 'Inefficient membership test (use set)',
                'cwe': 'CWE-1046',
                'owasp': 'A04',
                'rule_id': 'PY-INEFFICIENT-MEMBERSHIP'
            },
            'nested_loop_same_var': {
                'pattern': r'for\s+(\w+)\s+in.*for\s+\1\s+in',
                'severity': 'medium',
                'message': 'Nested loops with same variable name',
                'cwe': 'CWE-1164',
                'owasp': 'A04',
                'rule_id': 'PY-NESTED-LOOP-SAME-VAR'
            },
            
            # === SOLID VIOLATIONS ===
            'srp_violation': {
                'pattern': r'class\s+\w*(?:Manager|Handler|Service).*and.*(?:Manager|Handler|Service)',
                'severity': 'low',
                'message': 'Potential Single Responsibility Principle violation',
                'cwe': 'CWE-1120',
                'owasp': 'A04',
                'rule_id': 'PY-SRP-VIOLATION'
            },
            'large_interface': {
                'pattern': r'def\s+\w+.*def\s+\w+.*def\s+\w+.*def\s+\w+.*def\s+\w+.*def\s+\w+',
                'severity': 'low',
                'message': 'Interface may be too large',
                'cwe': 'CWE-1093',
                'owasp': 'A04',
                'rule_id': 'PY-LARGE-INTERFACE'
            },
            
            # === TESTING Y DEBUGGING ===
            'debug_print_leftover': {
                'pattern': r'print\s*\(["\']debug|DEBUG.*print',
                'severity': 'low',
                'message': 'Debug print statement left in code',
                'cwe': 'CWE-489',
                'owasp': 'A05',
                'rule_id': 'PY-DEBUG-PRINT'
            },
            'todo_fixme_comments': {
                'pattern': r'#.*(?:TODO|FIXME|XXX|HACK)',
                'severity': 'low',
                'message': 'TODO/FIXME comment indicates incomplete code',
                'cwe': 'CWE-1164',
                'owasp': 'A04',
                'rule_id': 'PY-TODO-COMMENT'
            },
            'test_method_no_assert': {
                'pattern': r'def\s+test_\w+.*:\s*(?!.*assert)',
                'severity': 'medium',
                'message': 'Test method without assertions',
                'cwe': 'CWE-1164',
                'owasp': 'A04',
                'rule_id': 'PY-TEST-NO-ASSERT'
            },
            
            # === DOCUMENTATION ===
            'missing_docstring_class': {
                'pattern': r'class\s+\w+.*:\s*(?!.*["\'\'"]{3})',
                'severity': 'low',
                'message': 'Class missing docstring',
                'cwe': 'CWE-1164',
                'owasp': 'A04',
                'rule_id': 'PY-MISSING-CLASS-DOCSTRING'
            },
            'missing_docstring_function': {
                'pattern': r'def\s+\w+.*:\s*(?!.*["\'\'"]{3})',
                'severity': 'low',
                'message': 'Function missing docstring',
                'cwe': 'CWE-1164',
                'owasp': 'A04',
                'rule_id': 'PY-MISSING-FUNC-DOCSTRING'
            }
        }
        
        # Combinar todos los patrones
        all_patterns = {**security_patterns, **quality_patterns}
        
        vulnerabilities.extend(self._scan_files_with_patterns(path, all_patterns, ['.py'], 'sembicho-python-enterprise'))
        
        # Análisis adicional de arquitectura Python
        vulnerabilities.extend(self._analyze_python_architecture(path))
        
        return vulnerabilities
    
    def _analyze_python_architecture(self, path: str) -> List[Vulnerability]:
        """
        Análisis arquitectural específico para Python
        """
        vulnerabilities = []
        
        try:
            path_obj = Path(path)
            python_files = []
            
            if path_obj.is_file() and path_obj.suffix == '.py':
                python_files = [path_obj]
            else:
                python_files = list(path_obj.rglob('*.py'))
            
            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines = content.split('\n')
                    
                    # Análisis de complejidad
                    function_count = len(re.findall(r'def\s+\w+', content))
                    class_count = len(re.findall(r'class\s+\w+', content))
                    
                    # Detectar violaciones SOLID
                    import_count = len([line for line in lines if line.strip().startswith('import ') or line.strip().startswith('from ')])
                    
                    if import_count > 20:
                        vuln = Vulnerability(
                            file=str(file_path),
                            line=1,
                            rule_id='PY-TOO-MANY-IMPORTS',
                            severity='medium',
                            message=f'Too many imports ({import_count}), indicates tight coupling',
                            cwe='CWE-1120',
                            owasp_category='A04',
                            tool='sembicho-python-architecture',
                            confidence='medium',
                            code_snippet=f'File has {import_count} imports'
                        )
                        vulnerabilities.append(vuln)
                    
                    # Detectar funciones muy largas
                    current_function = None
                    function_start = 0
                    for line_num, line in enumerate(lines, 1):
                        if re.match(r'\s*def\s+\w+', line):
                            if current_function and line_num - function_start > 50:
                                vuln = Vulnerability(
                                    file=str(file_path),
                                    line=function_start,
                                    rule_id='PY-LONG-FUNCTION',
                                    severity='medium',
                                    message=f'Function {current_function} is too long ({line_num - function_start} lines)',
                                    cwe='CWE-1114',
                                    owasp_category='A04',
                                    tool='sembicho-python-architecture',
                                    confidence='high',
                                    code_snippet=line.strip()
                                )
                                vulnerabilities.append(vuln)
                            
                            current_function = re.search(r'def\s+(\w+)', line).group(1)
                            function_start = line_num
                    
                    # Verificar última función
                    if current_function and len(lines) - function_start > 50:
                        vuln = Vulnerability(
                            file=str(file_path),
                            line=function_start,
                            rule_id='PY-LONG-FUNCTION',
                            severity='medium',
                            message=f'Function {current_function} is too long ({len(lines) - function_start} lines)',
                            cwe='CWE-1114',
                            owasp_category='A04',
                            tool='sembicho-python-architecture',
                            confidence='high',
                            code_snippet=f'def {current_function}(...)'
                        )
                        vulnerabilities.append(vuln)
                
                except Exception as e:
                    self.logger.debug(f"Error en análisis arquitectural de {file_path}: {e}")
                    continue
            
            if vulnerabilities:
                self.tools_used.append('sembicho-python-architecture')
                self.logger.info(f"Análisis arquitectural Python encontró {len(vulnerabilities)} issues")
                        
        except Exception as e:
            self.logger.debug(f"Error en análisis arquitectural Python: {e}")
        
        return vulnerabilities
    
    def _analyze_javascript_internal(self, path: str) -> List[Vulnerability]:
        """
        Análisis empresarial completo de seguridad para JavaScript/TypeScript
        
        Args:
            path: Ruta a analizar
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        # Patrones de seguridad avanzados para JavaScript
        security_patterns = {
            'eval_usage': {
                'pattern': r'\beval\s*\(',
                'severity': 'critical',
                'message': 'Code injection via eval()',
                'cwe': 'CWE-95',
                'owasp': 'A03',
                'rule_id': 'JS-EVAL-INJECTION'
            },
            'function_constructor': {
                'pattern': r'new\s+Function\s*\(',
                'severity': 'high',
                'message': 'Code injection via Function constructor',
                'cwe': 'CWE-95',
                'owasp': 'A03',
                'rule_id': 'JS-FUNCTION-CONSTRUCTOR'
            },
            'document_write': {
                'pattern': r'document\.write\s*\(',
                'severity': 'high',
                'message': 'XSS vulnerability via document.write',
                'cwe': 'CWE-79',
                'owasp': 'A03',
                'rule_id': 'JS-DOCUMENT-WRITE-XSS'
            },
            'innerhtml_usage': {
                'pattern': r'\.innerHTML\s*=\s*[^;]*\+',
                'severity': 'high',
                'message': 'XSS vulnerability via innerHTML concatenation',
                'cwe': 'CWE-79',
                'owasp': 'A03',
                'rule_id': 'JS-INNERHTML-XSS'
            },
            'outerhtml_usage': {
                'pattern': r'\.outerHTML\s*=\s*[^;]*\+',
                'severity': 'high',
                'message': 'XSS vulnerability via outerHTML concatenation',
                'cwe': 'CWE-79',
                'owasp': 'A03',
                'rule_id': 'JS-OUTERHTML-XSS'
            },
            'insertadjacenthtml': {
                'pattern': r'\.insertAdjacentHTML\s*\(',
                'severity': 'medium',
                'message': 'Potential XSS via insertAdjacentHTML',
                'cwe': 'CWE-79',
                'owasp': 'A03',
                'rule_id': 'JS-INSERT-ADJACENT-HTML'
            },
            'console_log_production': {
                'pattern': r'console\.(log|info|warn|error|debug)\s*\(',
                'severity': 'low',
                'message': 'Console output in production code',
                'cwe': 'CWE-532',
                'owasp': 'A09',
                'rule_id': 'JS-CONSOLE-PRODUCTION'
            },
            'hardcoded_credentials': {
                'pattern': r'(?i)(password|token|secret|key|api[_-]?key)\s*[:=]\s*["\'][^"\']{8,}["\']',
                'severity': 'critical',
                'message': 'Hardcoded credentials detected',
                'cwe': 'CWE-798',
                'owasp': 'A07',
                'rule_id': 'JS-HARDCODED-CREDS'
            },
            'sql_injection_template': {
                'pattern': r'(?i)(query|execute)\s*\([^)]*`[^`]*\$\{[^}]*\}',
                'severity': 'critical',
                'message': 'SQL injection via template literals',
                'cwe': 'CWE-89',
                'owasp': 'A03',
                'rule_id': 'JS-SQL-TEMPLATE-INJECTION'
            },
            'sql_injection_concat': {
                'pattern': r'(?i)(query|execute)\s*\([^)]*\+.*["\']',
                'severity': 'critical',
                'message': 'SQL injection via string concatenation',
                'cwe': 'CWE-89',
                'owasp': 'A03',
                'rule_id': 'JS-SQL-CONCAT-INJECTION'
            },
            'weak_random': {
                'pattern': r'Math\.random\s*\(',
                'severity': 'medium',
                'message': 'Cryptographically insecure random number generation',
                'cwe': 'CWE-338',
                'owasp': 'A02',
                'rule_id': 'JS-WEAK-RANDOM'
            },
            'unsafe_regexp': {
                'pattern': r'new RegExp\s*\([^)]*\+',
                'severity': 'medium',
                'message': 'ReDoS vulnerability via dynamic RegExp',
                'cwe': 'CWE-1333',
                'owasp': 'A06',
                'rule_id': 'JS-UNSAFE-REGEXP'
            },
            'postmessage_origin': {
                'pattern': r'postMessage\s*\([^)]*,\s*["\'][*]["\']',
                'severity': 'high',
                'message': 'Unsafe postMessage with wildcard origin',
                'cwe': 'CWE-346',
                'owasp': 'A07',
                'rule_id': 'JS-POSTMESSAGE-WILDCARD'
            },
            'prototype_pollution': {
                'pattern': r'__proto__|\[.*constructor.*\]|\[.*prototype.*\]',
                'severity': 'high',
                'message': 'Potential prototype pollution',
                'cwe': 'CWE-1321',
                'owasp': 'A08',
                'rule_id': 'JS-PROTOTYPE-POLLUTION'
            },
            'dangerous_innerhtml': {
                'pattern': r'dangerouslySetInnerHTML',
                'severity': 'medium',
                'message': 'Dangerous React HTML injection',
                'cwe': 'CWE-79',
                'owasp': 'A03',
                'rule_id': 'JS-REACT-DANGEROUS-HTML'
            },
            'localstorage_sensitive': {
                'pattern': r'localStorage\.setItem\s*\([^)]*(?i)(password|token|key)',
                'severity': 'medium',
                'message': 'Sensitive data stored in localStorage',
                'cwe': 'CWE-922',
                'owasp': 'A02',
                'rule_id': 'JS-LOCALSTORAGE-SENSITIVE'
            },
            'websocket_insecure': {
                'pattern': r'new WebSocket\s*\(\s*["\']ws://',
                'severity': 'medium',
                'message': 'Insecure WebSocket connection (ws://)',
                'cwe': 'CWE-319',
                'owasp': 'A02',
                'rule_id': 'JS-WEBSOCKET-INSECURE'
            }
        }
        
        # Patrones de calidad de código JavaScript
        quality_patterns = {
            'var_usage': {
                'pattern': r'\bvar\s+\w+',
                'severity': 'low',
                'message': 'Use let/const instead of var',
                'cwe': 'CWE-1109',
                'owasp': 'A04',
                'rule_id': 'JS-VAR-USAGE'
            },
            'equal_comparison': {
                'pattern': r'[^!=]==[^=]',
                'severity': 'low',
                'message': 'Use strict equality (===) instead of ==',
                'cwe': 'CWE-1108',
                'owasp': 'A04',
                'rule_id': 'JS-LOOSE-EQUALITY'
            },
            'global_variables': {
                'pattern': r'window\.\w+\s*=',
                'severity': 'low',
                'message': 'Global variable pollution',
                'cwe': 'CWE-1109',
                'owasp': 'A04',
                'rule_id': 'JS-GLOBAL-POLLUTION'
            },
            'callback_hell': {
                'pattern': r'function\s*\([^)]*\)\s*\{[^}]*function\s*\([^)]*\)\s*\{[^}]*function',
                'severity': 'medium',
                'message': 'Callback hell detected, consider async/await',
                'cwe': 'CWE-1114',
                'owasp': 'A04',
                'rule_id': 'JS-CALLBACK-HELL'
            },
            'magic_numbers': {
                'pattern': r'[^a-zA-Z_]\d{3,}[^a-zA-Z_]',
                'severity': 'low',
                'message': 'Magic number detected',
                'cwe': 'CWE-1108',
                'owasp': 'A04',
                'rule_id': 'JS-MAGIC-NUMBERS'
            },
            'empty_catch': {
                'pattern': r'catch\s*\([^)]*\)\s*\{\s*\}',
                'severity': 'medium',
                'message': 'Empty catch block',
                'cwe': 'CWE-396',
                'owasp': 'A09',
                'rule_id': 'JS-EMPTY-CATCH'
            },
            'unused_variables': {
                'pattern': r'var\s+(\w+)\s*=.*(?!\1)',
                'severity': 'low',
                'message': 'Potentially unused variable',
                'cwe': 'CWE-1164',
                'owasp': 'A04',
                'rule_id': 'JS-UNUSED-VAR'
            }
        }
        
        # Combinar patrones
        all_patterns = {**security_patterns, **quality_patterns}
        
        vulnerabilities.extend(self._scan_files_with_patterns(path, all_patterns, ['.js', '.ts', '.jsx', '.tsx'], 'sembicho-javascript-enterprise'))
        
        # Análisis específico de frameworks
        vulnerabilities.extend(self._analyze_javascript_frameworks(path))
        
        return vulnerabilities
    
    def _analyze_javascript_frameworks(self, path: str) -> List[Vulnerability]:
        """
        Análisis específico de frameworks JavaScript (React, Vue, Angular, etc.)
        """
        vulnerabilities = []
        
        try:
            path_obj = Path(path)
            js_files = []
            
            if path_obj.is_file() and path_obj.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                js_files = [path_obj]
            else:
                for ext in ['.js', '.ts', '.jsx', '.tsx']:
                    js_files.extend(path_obj.rglob(f'*{ext}'))
            
            for file_path in js_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines = content.split('\n')
                    
                    # Detectar React específico
                    if 'react' in content.lower() or 'jsx' in str(file_path):
                        # Detectar ref usage inseguro
                        if re.search(r'ref\s*=\s*["\'][^"\']*["\']', content):
                            vuln = Vulnerability(
                                file=str(file_path),
                                line=1,
                                rule_id='REACT-STRING-REF',
                                severity='medium',
                                message='String refs are deprecated and unsafe',
                                cwe='CWE-477',
                                owasp_category='A04',
                                tool='sembicho-react',
                                confidence='high',
                                code_snippet='String ref usage detected'
                            )
                            vulnerabilities.append(vuln)
                    
                    # Detectar Vue específico
                    if 'vue' in content.lower():
                        if re.search(r'v-html\s*=', content):
                            vuln = Vulnerability(
                                file=str(file_path),
                                line=1,
                                rule_id='VUE-HTML-DIRECTIVE',
                                severity='medium',
                                message='v-html directive can lead to XSS',
                                cwe='CWE-79',
                                owasp_category='A03',
                                tool='sembicho-vue',
                                confidence='medium',
                                code_snippet='v-html directive usage'
                            )
                            vulnerabilities.append(vuln)
                    
                    # Análisis de complejidad
                    function_count = len(re.findall(r'function\s+\w+|=>\s*\{', content))
                    if function_count > 20:
                        vuln = Vulnerability(
                            file=str(file_path),
                            line=1,
                            rule_id='JS-TOO-MANY-FUNCTIONS',
                            severity='medium',
                            message=f'File has too many functions ({function_count})',
                            cwe='CWE-1120',
                            owasp_category='A04',
                            tool='sembicho-javascript-complexity',
                            confidence='high',
                            code_snippet=f'{function_count} functions in file'
                        )
                        vulnerabilities.append(vuln)
                
                except Exception as e:
                    self.logger.debug(f"Error analizando frameworks JS en {file_path}: {e}")
                    continue
            
            if vulnerabilities:
                self.tools_used.append('sembicho-javascript-frameworks')
                self.logger.info(f"Análisis de frameworks JavaScript encontró {len(vulnerabilities)} issues")
                        
        except Exception as e:
            self.logger.debug(f"Error en análisis de frameworks JavaScript: {e}")
        
        return vulnerabilities
    
    def _analyze_java_internal(self, path: str) -> List[Vulnerability]:
        """
        Análisis de seguridad para Java
        """
        patterns = {
            'sql_injection': {
                'pattern': r'Statement.*execute.*\+',
                'severity': 'high',
                'message': 'Possible SQL injection via string concatenation',
                'cwe': 'CWE-89',
                'owasp': 'A03',
                'rule_id': 'JAVA-SQL-INJECTION'
            },
            'command_injection': {
                'pattern': r'Runtime\.getRuntime\(\)\.exec\s*\(',
                'severity': 'high',
                'message': 'Command injection vulnerability',
                'cwe': 'CWE-78',
                'owasp': 'A03',
                'rule_id': 'JAVA-COMMAND-INJECTION'
            },
            'hardcoded_password': {
                'pattern': r'(?i)(password|passwd)\s*=\s*"[^"]{3,}"',
                'severity': 'high',
                'message': 'Hardcoded password detected',
                'cwe': 'CWE-798',
                'owasp': 'A07',
                'rule_id': 'JAVA-HARDCODED-PASSWORD'
            }
        }
        
        return self._scan_files_with_patterns(path, patterns, ['.java'], 'sembicho-java')
    
    def _analyze_php_internal(self, path: str) -> List[Vulnerability]:
        """
        Análisis de seguridad para PHP
        """
        patterns = {
            'sql_injection': {
                'pattern': r'mysql_query\s*\([^)]*\$',
                'severity': 'high',
                'message': 'Possible SQL injection vulnerability',
                'cwe': 'CWE-89',
                'owasp': 'A03',
                'rule_id': 'PHP-SQL-INJECTION'
            },
            'file_inclusion': {
                'pattern': r'(include|require)(_once)?\s*\([^)]*\$',
                'severity': 'high',
                'message': 'Possible file inclusion vulnerability',
                'cwe': 'CWE-98',
                'owasp': 'A03',
                'rule_id': 'PHP-FILE-INCLUSION'
            },
            'eval_usage': {
                'pattern': r'\beval\s*\(',
                'severity': 'high',
                'message': 'Use of eval() is dangerous',
                'cwe': 'CWE-95',
                'owasp': 'A03',
                'rule_id': 'PHP-EVAL-USAGE'
            }
        }
        
        return self._scan_files_with_patterns(path, patterns, ['.php'], 'sembicho-php')
    
    def _analyze_go_internal(self, path: str) -> List[Vulnerability]:
        """
        Análisis de seguridad para Go
        """
        patterns = {
            'command_injection': {
                'pattern': r'exec\.Command\s*\([^)]*\+',
                'severity': 'high',
                'message': 'Possible command injection',
                'cwe': 'CWE-78',
                'owasp': 'A03',
                'rule_id': 'GO-COMMAND-INJECTION'
            },
            'weak_random': {
                'pattern': r'rand\.(Int|Float)',
                'severity': 'medium',
                'message': 'Use crypto/rand for security-sensitive randomness',
                'cwe': 'CWE-338',
                'owasp': 'A02',
                'rule_id': 'GO-WEAK-RANDOM'
            }
        }
        
        return self._scan_files_with_patterns(path, patterns, ['.go'], 'sembicho-go')
    
    def _analyze_csharp_internal(self, path: str) -> List[Vulnerability]:
        """
        Análisis de seguridad para C#
        """
        patterns = {
            'sql_injection': {
                'pattern': r'SqlCommand\s*\([^)]*\+',
                'severity': 'high',
                'message': 'Possible SQL injection via string concatenation',
                'cwe': 'CWE-89',
                'owasp': 'A03',
                'rule_id': 'CS-SQL-INJECTION'
            },
            'weak_random': {
                'pattern': r'new Random\s*\(',
                'severity': 'medium',
                'message': 'Use RNGCryptoServiceProvider for cryptographic randomness',
                'cwe': 'CWE-338',
                'owasp': 'A02',
                'rule_id': 'CS-WEAK-RANDOM'
            }
        }
        
        return self._scan_files_with_patterns(path, patterns, ['.cs'], 'sembicho-csharp')
    
    def _analyze_multi_language_internal(self, path: str) -> List[Vulnerability]:
        """
        Análisis multi-lenguaje para patrones generales de seguridad
        """
        patterns = {
            'hardcoded_api_key': {
                'pattern': r'(?i)(api[_-]?key|apikey|access[_-]?token)\s*[:=]\s*["\'][a-zA-Z0-9_-]{20,}["\']',
                'severity': 'critical',
                'message': 'Hardcoded API key detected',
                'cwe': 'CWE-798',
                'owasp': 'A07',
                'rule_id': 'MULTI-HARDCODED-API-KEY'
            },
            'weak_crypto_md5': {
                'pattern': r'(?i)md5\s*\(',
                'severity': 'medium',
                'message': 'MD5 is cryptographically broken',
                'cwe': 'CWE-327',
                'owasp': 'A02',
                'rule_id': 'MULTI-WEAK-CRYPTO-MD5'
            },
            'weak_crypto_sha1': {
                'pattern': r'(?i)sha1\s*\(',
                'severity': 'medium',
                'message': 'SHA1 is cryptographically weak',
                'cwe': 'CWE-327',
                'owasp': 'A02',
                'rule_id': 'MULTI-WEAK-CRYPTO-SHA1'
            },
            'http_usage': {
                'pattern': r'http://[^"\'\s]+',
                'severity': 'low',
                'message': 'Unencrypted HTTP URL detected',
                'cwe': 'CWE-319',
                'owasp': 'A02',
                'rule_id': 'MULTI-HTTP-USAGE'
            },
            'todo_fixme': {
                'pattern': r'(?i)(TODO|FIXME|HACK|XXX).*(?i)(security|vuln|auth|password)',
                'severity': 'low',
                'message': 'Security-related TODO/FIXME comment',
                'cwe': 'CWE-546',
                'owasp': 'A05',
                'rule_id': 'MULTI-SECURITY-TODO'
            },
            'private_key': {
                'pattern': r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
                'severity': 'critical',
                'message': 'Private key found in source code',
                'cwe': 'CWE-798',
                'owasp': 'A07',
                'rule_id': 'MULTI-PRIVATE-KEY'
            }
        }
        
        # Escanear todos los archivos de texto
        extensions = ['.py', '.js', '.ts', '.java', '.php', '.go', '.cs', '.cpp', '.c', '.h', 
                     '.rb', '.swift', '.kt', '.scala', '.rs', '.vue', '.jsx', '.tsx', '.yaml', '.yml', '.json', '.xml', '.config']
        
        return self._scan_files_with_patterns(path, patterns, extensions, 'sembicho-multi')
    
    def _analyze_dependencies_internal(self, path: str) -> List[Vulnerability]:
        """
        Análisis de dependencias basado en archivos de configuración (sin herramientas externas)
        """
        vulnerabilities = []
        
        # Patrones para archivos de dependencias conocidos vulnerables
        vulnerable_packages = {
            'python': {
                'django<2.2.28': 'Known vulnerabilities in Django < 2.2.28',
                'flask<1.1.4': 'Known vulnerabilities in Flask < 1.1.4',
                'requests<2.25.1': 'Known vulnerabilities in requests < 2.25.1',
                'pyyaml<5.4': 'Known vulnerabilities in PyYAML < 5.4',
                'pillow<8.1.1': 'Known vulnerabilities in Pillow < 8.1.1'
            },
            'javascript': {
                'lodash<4.17.21': 'Known vulnerabilities in lodash < 4.17.21',
                'jquery<3.5.0': 'Known XSS vulnerabilities in jQuery < 3.5.0',
                'express<4.17.1': 'Known vulnerabilities in Express < 4.17.1',
                'axios<0.21.1': 'Known vulnerabilities in axios < 0.21.1'
            }
        }
        
        # Buscar archivos de dependencias
        try:
            path_obj = Path(path)
            
            # Python - requirements.txt, Pipfile, pyproject.toml
            for req_file in ['requirements.txt', 'Pipfile', 'pyproject.toml']:
                if path_obj.is_file() and path_obj.name == req_file:
                    files_to_check = [path_obj]
                else:
                    files_to_check = list(path_obj.rglob(req_file))
                
                for file_path in files_to_check:
                    vulnerabilities.extend(self._check_python_dependencies(file_path))
            
            # JavaScript - package.json
            pkg_files = list(path_obj.rglob('package.json')) if path_obj.is_dir() else ([path_obj] if path_obj.name == 'package.json' else [])
            for file_path in pkg_files:
                vulnerabilities.extend(self._check_javascript_dependencies(file_path))
                
        except Exception as e:
            self.logger.debug(f"Error analizando dependencias: {e}")
        
        if vulnerabilities:
            self.tools_used.append('sembicho-dependencies')
            
        return vulnerabilities
    
    def _scan_files_with_patterns(self, path: str, patterns: Dict, extensions: List[str], tool_name: str) -> List[Vulnerability]:
        """
        Escanea archivos con patrones específicos
        
        Args:
            path: Ruta a escanear
            patterns: Diccionario de patrones a buscar
            extensions: Extensiones de archivo a incluir
            tool_name: Nombre de la herramienta para reportes
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        try:
            path_obj = Path(path)
            files_to_scan = []
            
            if path_obj.is_file():
                if path_obj.suffix in extensions:
                    files_to_scan = [path_obj]
            else:
                for ext in extensions:
                    files_to_scan.extend(path_obj.rglob(f'*{ext}'))
            
            for file_path in files_to_scan:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        for pattern_name, pattern_info in patterns.items():
                            matches = re.finditer(pattern_info['pattern'], line)
                            
                            for match in matches:
                                vuln = Vulnerability(
                                    file=str(file_path),
                                    line=line_num,
                                    rule_id=pattern_info['rule_id'],
                                    severity=pattern_info['severity'],
                                    message=pattern_info['message'],
                                    cwe=pattern_info['cwe'],
                                    owasp_category=pattern_info.get('owasp'),
                                    tool=tool_name,
                                    confidence='medium',
                                    code_snippet=line.strip()
                                )
                                vulnerabilities.append(vuln)
                
                except Exception as e:
                    self.logger.debug(f"Error analizando {file_path}: {e}")
                    continue
            
            if vulnerabilities:
                self.tools_used.append(tool_name)
                self.logger.info(f"{tool_name} encontró {len(vulnerabilities)} vulnerabilidades")
                        
        except Exception as e:
            self.logger.debug(f"Error en {tool_name}: {e}")
        
        return vulnerabilities
    
    def _check_python_dependencies(self, file_path: Path) -> List[Vulnerability]:
        """
        Verifica dependencias de Python por vulnerabilidades conocidas
        """
        vulnerabilities = []
        
        # Patrones conocidos de dependencias vulnerables
        vulnerable_patterns = {
            r'django\s*[<>=]*\s*[12]\.[01]\.': {
                'message': 'Django version may have known vulnerabilities',
                'severity': 'medium',
                'cwe': 'CWE-1104'
            },
            r'flask\s*[<>=]*\s*0\.': {
                'message': 'Flask version may have known vulnerabilities',
                'severity': 'medium', 
                'cwe': 'CWE-1104'
            },
            r'requests\s*[<>=]*\s*2\.(1[0-9]|2[0-4])\.': {
                'message': 'Requests version may have known vulnerabilities',
                'severity': 'low',
                'cwe': 'CWE-1104'
            }
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern, info in vulnerable_patterns.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        vuln = Vulnerability(
                            file=str(file_path),
                            line=line_num,
                            rule_id='PY-VULNERABLE-DEPENDENCY',
                            severity=info['severity'],
                            message=info['message'],
                            cwe=info['cwe'],
                            tool='sembicho-dependencies',
                            confidence='low',
                            code_snippet=line.strip()
                        )
                        vulnerabilities.append(vuln)
        
        except Exception as e:
            self.logger.debug(f"Error verificando dependencias Python: {e}")
        
        return vulnerabilities
    
    def _check_javascript_dependencies(self, file_path: Path) -> List[Vulnerability]:
        """
        Verifica dependencias de JavaScript por vulnerabilidades conocidas
        """
        vulnerabilities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.loads(f.read())
            
            dependencies = {}
            dependencies.update(content.get('dependencies', {}))
            dependencies.update(content.get('devDependencies', {}))
            
            # Patrones de dependencias vulnerables conocidas
            vulnerable_deps = {
                'lodash': {
                    'versions': ['4.17.15', '4.17.16', '4.17.17', '4.17.18', '4.17.19', '4.17.20'],
                    'message': 'Lodash version has known prototype pollution vulnerabilities',
                    'severity': 'medium'
                },
                'jquery': {
                    'versions': ['3.4.1', '3.4.0', '3.3.1'],
                    'message': 'jQuery version has known XSS vulnerabilities', 
                    'severity': 'medium'
                },
                'axios': {
                    'versions': ['0.18.0', '0.18.1', '0.19.0', '0.19.1', '0.19.2', '0.20.0', '0.21.0'],
                    'message': 'Axios version may have known vulnerabilities',
                    'severity': 'low'
                }
            }
            
            for dep_name, version in dependencies.items():
                if dep_name in vulnerable_deps:
                    # Extraer versión numérica simple
                    version_clean = re.sub(r'[^0-9.]', '', version)
                    if version_clean in vulnerable_deps[dep_name]['versions']:
                        vuln = Vulnerability(
                            file=str(file_path),
                            line=1,
                            rule_id='JS-VULNERABLE-DEPENDENCY',
                            severity=vulnerable_deps[dep_name]['severity'],
                            message=f"{dep_name}@{version}: {vulnerable_deps[dep_name]['message']}",
                            cwe='CWE-1104',
                            tool='sembicho-dependencies',
                            confidence='medium',
                            code_snippet=f'"{dep_name}": "{version}"'
                        )
                        vulnerabilities.append(vuln)
        
        except Exception as e:
            self.logger.debug(f"Error verificando dependencias JavaScript: {e}")
        
        return vulnerabilities
    
    def _map_npm_severity(self, npm_severity: str) -> str:
        """Mapea severidad de NPM audit a formato estándar"""
        mapping = {
            'info': 'low',
            'low': 'low',
            'moderate': 'medium',
            'high': 'high',
            'critical': 'critical'
        }
        return mapping.get(npm_severity.lower(), 'medium')
    
    def _map_eslint_severity(self, eslint_severity: int) -> str:
        """Mapea severidad de ESLint a formato estándar"""
        mapping = {1: 'medium', 2: 'high'}
        return mapping.get(eslint_severity, 'medium')
    
    def _map_semgrep_severity(self, semgrep_severity: str) -> str:
        """Mapea severidad de Semgrep a formato estándar"""
        mapping = {
            'INFO': 'low',
            'WARNING': 'medium', 
            'ERROR': 'high',
            'CRITICAL': 'critical'
        }
        return mapping.get(semgrep_severity.upper(), 'medium')
    
    def _extract_cwe_from_semgrep(self, finding: Dict) -> Optional[str]:
        """Extrae CWE ID de un finding de Semgrep"""
        metadata = finding.get('extra', {}).get('metadata', {})
        cwe = metadata.get('cwe') or metadata.get('cwe-id')
        
        if cwe:
            if isinstance(cwe, list) and cwe:
                return f"CWE-{cwe[0]}"
            elif isinstance(cwe, str):
                return f"CWE-{cwe}" if not cwe.startswith('CWE-') else cwe
                
        return None
    
    def scan_file(self, file_path: str) -> ScanResult:
        """
        Analiza un archivo específico usando solo análisis interno
        
        Args:
            file_path: Ruta del archivo a analizar
            
        Returns:
            Resultados del análisis
        """
        self.logger.info(f"Analizando archivo: {file_path}")
        self.vulnerabilities.clear()
        self.tools_used.clear()
        
        path_obj = Path(file_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        # Detectar lenguaje
        languages = self.detect_languages(file_path)
        primary_language = languages[0] if languages else 'unknown'
        
        # Ejecutar análisis interno según el lenguaje
        if 'python' in languages:
            self.vulnerabilities.extend(self._analyze_python_internal(file_path))
        
        if any(lang in ['javascript', 'typescript'] for lang in languages):
            self.vulnerabilities.extend(self._analyze_javascript_internal(file_path))
        
        if 'java' in languages:
            self.vulnerabilities.extend(self._analyze_java_internal(file_path))
        
        if 'php' in languages:
            self.vulnerabilities.extend(self._analyze_php_internal(file_path))
        
        if 'go' in languages:
            self.vulnerabilities.extend(self._analyze_go_internal(file_path))
        
        if 'csharp' in languages:
            self.vulnerabilities.extend(self._analyze_csharp_internal(file_path))
        
        # Análisis multi-lenguaje (secretos, configuraciones, etc.)
        self.vulnerabilities.extend(self._analyze_multi_language_internal(file_path))
        
        return self._build_scan_result(path_obj.name, primary_language, file_path)
    
    def scan_directory(self, directory_path: str) -> ScanResult:
        """
        Analiza un directorio completo usando solo análisis interno
        
        Args:
            directory_path: Ruta del directorio a analizar
            
        Returns:
            Resultados del análisis
        """
        self.logger.info(f"Analizando directorio: {directory_path}")
        self.start_time = time.time()
        self.vulnerabilities.clear()
        self.tools_used.clear()
        
        path_obj = Path(directory_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Directorio no encontrado: {directory_path}")
        
        # Contar archivos y líneas para métricas
        self._count_files_and_lines(directory_path)
        
        # Detectar lenguajes
        languages = self.detect_languages(directory_path)
        primary_language = languages[0] if languages else 'unknown'
        
        # Ejecutar análisis interno por lenguaje
        if 'python' in languages:
            self.vulnerabilities.extend(self._analyze_python_internal(directory_path))
        
        if any(lang in ['javascript', 'typescript'] for lang in languages):
            self.vulnerabilities.extend(self._analyze_javascript_internal(directory_path))
        
        if 'java' in languages:
            self.vulnerabilities.extend(self._analyze_java_internal(directory_path))
        
        if 'php' in languages:
            self.vulnerabilities.extend(self._analyze_php_internal(directory_path))
        
        if 'go' in languages:
            self.vulnerabilities.extend(self._analyze_go_internal(directory_path))
        
        if 'csharp' in languages:
            self.vulnerabilities.extend(self._analyze_csharp_internal(directory_path))
        
        # Análisis multi-lenguaje (secretos, configuraciones inseguras, etc.)
        self.vulnerabilities.extend(self._analyze_multi_language_internal(directory_path))
        
        # Escaneo de secretos (siempre ejecutar)
        self.vulnerabilities.extend(self._run_secrets_scanner(directory_path))
        
        # Análisis de dependencias (solo archivos de configuración)
        self.vulnerabilities.extend(self._analyze_dependencies_internal(directory_path))
        
        # Enriquecer vulnerabilidades con datos adicionales
        enriched_vulns = []
        for vuln in self.vulnerabilities:
            enriched_vulns.append(self._enrich_vulnerability(vuln))
        self.vulnerabilities = enriched_vulns
        
        return self._build_scan_result(path_obj.name, primary_language, directory_path)
    
    def _build_scan_result(self, project_name: str, language: str, scan_path: str) -> ScanResult:
        """
        Construye el resultado final del escaneo
        
        Args:
            project_name: Nombre del proyecto
            language: Lenguaje principal detectado
            
        Returns:
            Resultado estructurado del escaneo
        """
        # Calcular tiempo de ejecución
        execution_time = time.time() - self.start_time if hasattr(self, 'start_time') else 0
        
        # Contar vulnerabilidades por severidad
        severity_counts = {level: 0 for level in self.SEVERITY_LEVELS}
        for vuln in self.vulnerabilities:
            if vuln.severity in severity_counts:
                severity_counts[vuln.severity] += 1
        
        # Convertir vulnerabilidades a diccionarios
        vuln_dicts = []
        for vuln in self.vulnerabilities:
            vuln_dict = asdict(vuln)
            # Remover campos None o vacíos
            vuln_dict = {k: v for k, v in vuln_dict.items() if v is not None and v != ''}
            vuln_dicts.append(vuln_dict)
        
        # Calcular métricas empresariales completas
        security_metrics = self._calculate_security_metrics()
        quality_metrics = self._calculate_quality_metrics(project_name)
        compliance_metrics = self._calculate_compliance_metrics()
        architecture_metrics = self._calculate_architecture_metrics()
        performance_metrics = self._calculate_performance_metrics()
        
        # Calcular cobertura de escaneo
        scan_coverage = min(100.0, (self.total_files_scanned / max(1, self.total_files_scanned)) * 100)
        
        # Generar ID único del escaneo
        scan_id = f"scan_{project_name}_{int(time.time())}"
        
        # Calcular calificaciones empresariales (A-F)
        security_grade = self._calculate_grade(security_metrics.security_score)
        quality_grade = self._calculate_grade(quality_metrics.maintainability_index)
        compliance_grade = self._calculate_grade(compliance_metrics.compliance_score)
        architecture_grade = self._calculate_grade(architecture_metrics.modularity_score)
        
        # Determinar nivel de riesgo
        risk_level = self._calculate_risk_level(security_metrics.risk_score, len(self.vulnerabilities))
        
        # Detectar framework si es posible
        framework = self._detect_framework(project_name)
        
        scan_result = ScanResult(
            # Información básica del proyecto
            project_name=project_name,
            scan_date=datetime.utcnow().isoformat() + 'Z',
            language=language,
            framework=framework,
            version="1.0.0",
            environment=self.environment if hasattr(self, 'environment') else 'development',
            
            # Resumen de vulnerabilidades
            total_vulnerabilities=len(self.vulnerabilities),
            severity_counts=severity_counts,
            tools_used=list(set(self.tools_used)),
            vulnerabilities=vuln_dicts,
            
            # Métricas empresariales
            security_metrics=security_metrics,
            quality_metrics=quality_metrics,
            compliance_metrics=compliance_metrics,
            architecture_metrics=architecture_metrics,
            performance_metrics=performance_metrics,
            
            # Metadatos del escaneo
            execution_time=execution_time,
            scan_coverage=scan_coverage,
            scan_id=scan_id,
            pipeline_id=self.pipeline_id if hasattr(self, 'pipeline_id') else None,
            commit_hash=None,  # TODO: Obtener de git si está disponible
            branch_name=None,  # TODO: Obtener de git si está disponible
            
            # Scores y calificaciones
            overall_security_grade=security_grade,
            overall_quality_grade=quality_grade,
            overall_compliance_grade=self._calculate_grade(compliance_metrics.compliance_score),
            risk_level=risk_level,
            
            # Tendencias (por ahora None, requiere histórico)
            security_trend=None,
            quality_trend=None,
            compliance_trend=None,
            
            # 🔥 NUEVOS CAMPOS CRÍTICOS (análisis SRE)
            scan_coverage_details=self._get_scan_coverage_details(),
            risk_score=self._calculate_risk_score(),
            category_counts=self._calculate_category_counts(),
            owasp_distribution=self._calculate_owasp_distribution(),
            cwe_distribution=self._calculate_cwe_distribution(),
            scan_duration_seconds=performance_metrics.scan_duration if performance_metrics else execution_time,
            dependencies=self._extract_dependencies(scan_path),  # ✅ v2.5.0: Extrae dependencias reales
            sbom_cyclonedx=self._generate_sbom_cyclonedx(scan_path),  # ✅ v2.5.0: Genera SBOM CycloneDX
            sbom_spdx=self._generate_sbom_spdx(scan_path),  # ✅ v2.6.0: Genera SBOM SPDX 2.3
            cve_report=self._scan_dependencies_for_cves(scan_path),  # ✅ v2.5.0: Escanea CVEs en dependencias
            dependency_tree=self._build_dependency_tree(scan_path),  # ✅ v2.6.0: Árbol de dependencias
            nvd_enrichment=self._enrich_with_nvd(self._scan_dependencies_for_cves(scan_path) or [])  # ✅ v2.6.0: Enriquecimiento NVD
        )
        
        # Guardar para posibles reportes
        self._last_result = scan_result
        
        # En modo empresarial, enviar automáticamente al backend
        if self.enterprise_mode and self.backend_url and self.auth_token:
            self.logger.info("📤 Enviando resultados al backend empresarial...")
            success = self.send_to_api(
                self.backend_url,
                self.auth_token,
                asdict(scan_result),
                self.pipeline_id
            )
            if not success:
                self.logger.warning("⚠️  No se pudo enviar al backend, continuando...")
        
        return scan_result
    
    def _calculate_grade(self, score: float) -> str:
        """Convierte un score (0-100) a una calificación (A-F)"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _calculate_risk_level(self, risk_score: float, total_vulns: int) -> str:
        """Calcula el nivel de riesgo basado en score y cantidad de vulnerabilidades"""
        if risk_score >= 80 or total_vulns >= 20:
            return 'CRITICAL'
        elif risk_score >= 60 or total_vulns >= 10:
            return 'HIGH'
        elif risk_score >= 30 or total_vulns >= 5:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _detect_framework(self, project_name: str) -> Optional[str]:
        """Detecta el framework basado en archivos y dependencias"""
        # Esta es una implementación básica, se puede expandir
        if any('react' in vuln.message.lower() for vuln in self.vulnerabilities):
            return 'React'
        elif any('angular' in vuln.message.lower() for vuln in self.vulnerabilities):
            return 'Angular'
        elif any('vue' in vuln.message.lower() for vuln in self.vulnerabilities):
            return 'Vue.js'
        elif any('django' in vuln.message.lower() for vuln in self.vulnerabilities):
            return 'Django'
        elif any('flask' in vuln.message.lower() for vuln in self.vulnerabilities):
            return 'Flask'
        elif any('spring' in vuln.message.lower() for vuln in self.vulnerabilities):
            return 'Spring'
        return None
    
    def generate_report(self, format_type: str = "json") -> str:
        """
        Genera un reporte de los resultados
        
        Args:
            format_type: Formato del reporte (json, html, console, sarif, xml, summary)
            
        Returns:
            Reporte formateado
        """
        if not hasattr(self, '_last_result'):
            self._last_result = self._build_scan_result("unknown", "unknown")
        
        format_type = format_type.lower()
        
        if format_type == "json":
            return self._generate_json_report()
        elif format_type == "html":
            return self._generate_html_report()
        elif format_type == "console":
            return self._generate_console_report()
        elif format_type == "sarif":
            return self._generate_sarif_report()
        elif format_type == "xml":
            return self._generate_xml_report()
        elif format_type == "summary":
            return self._generate_summary_report()
        else:
            raise ValueError(f"Formato no soportado: {format_type}. Formatos disponibles: json, html, console, sarif, xml, summary")
    
    def _generate_json_report(self) -> str:
        """Genera reporte en formato JSON estructurado"""
        return json.dumps(asdict(self._last_result), indent=2, ensure_ascii=False, default=str)
    
    def _generate_sarif_report(self) -> str:
        """
        Genera reporte en formato SARIF 2.1.0 (Static Analysis Results Interchange Format)
        Estándar de la industria para reportes de análisis estático
        """
        sarif_report = {
            "version": "2.1.0",
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "SemBicho",
                            "version": "1.0.0",
                            "informationUri": "https://github.com/your-org/sembicho",
                            "rules": self._generate_sarif_rules()
                        }
                    },
                    "results": self._generate_sarif_results(),
                    "properties": {
                        "scanDate": self._last_result.scan_date,
                        "projectName": self._last_result.project_name,
                        "language": self._last_result.language,
                        "totalVulnerabilities": self._last_result.total_vulnerabilities,
                        "severityCounts": self._last_result.severity_counts,
                        "securityMetrics": asdict(self._last_result.security_metrics),
                        "qualityMetrics": asdict(self._last_result.quality_metrics),
                        "complianceMetrics": asdict(self._last_result.compliance_metrics)
                    }
                }
            ]
        }
        
        return json.dumps(sarif_report, indent=2, ensure_ascii=False)
    
    def _generate_sarif_rules(self) -> List[Dict]:
        """Genera reglas SARIF basadas en las vulnerabilidades encontradas"""
        rules = {}
        
        for vuln in self._last_result.vulnerabilities:
            rule_id = vuln.get('rule_id', 'unknown')
            
            if rule_id not in rules:
                rules[rule_id] = {
                    "id": rule_id,
                    "name": rule_id,
                    "shortDescription": {"text": vuln.get('message', 'Security vulnerability detected')},
                    "helpUri": f"https://cwe.mitre.org/data/definitions/{vuln.get('cwe', '').replace('CWE-', '')}.html" if vuln.get('cwe') else None,
                    "properties": {
                        "category": vuln.get('category', 'security'),
                        "impact": vuln.get('impact', 'medium'),
                        "likelihood": vuln.get('likelihood', 'medium'),
                        "cwe": vuln.get('cwe'),
                        "owasp": vuln.get('owasp_category')
                    }
                }
        
        return list(rules.values())
    
    def _generate_sarif_results(self) -> List[Dict]:
        """Genera resultados SARIF"""
        results = []
        
        for vuln in self._last_result.vulnerabilities:
            result = {
                "ruleId": vuln.get('rule_id', 'unknown'),
                "level": self._map_severity_to_sarif_level(vuln.get('severity', 'medium')),
                "message": {"text": vuln.get('message', 'Security vulnerability detected')},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": vuln.get('file', 'unknown')},
                            "region": {"startLine": vuln.get('line', 1)}
                        }
                    }
                ],
                "properties": {
                    "tool": vuln.get('tool', 'unknown'),
                    "confidence": vuln.get('confidence', 'medium'),
                    "category": vuln.get('category', 'security'),
                    "impact": vuln.get('impact', 'medium'),
                    "likelihood": vuln.get('likelihood', 'medium'),
                    "cwe": vuln.get('cwe'),
                    "owasp": vuln.get('owasp_category')
                }
            }
            
            if vuln.get('code_snippet'):
                result["locations"][0]["physicalLocation"]["contextRegion"] = {
                    "snippet": {"text": vuln.get('code_snippet')}
                }
            
            results.append(result)
        
        return results
    
    def _map_severity_to_sarif_level(self, severity: str) -> str:
        """Mapea severidades a niveles SARIF"""
        mapping = {
            'low': 'note',
            'medium': 'warning',
            'high': 'error',
            'critical': 'error'
        }
        return mapping.get(severity.lower(), 'warning')
    
    def _generate_xml_report(self) -> str:
        """Genera reporte en formato XML"""
        from xml.etree.ElementTree import Element, SubElement, tostring
        from xml.dom import minidom
        
        root = Element('SemBichoReport')
        root.set('version', '1.0')
        root.set('generated', self._last_result.scan_date)
        
        # Metadata
        metadata = SubElement(root, 'Metadata')
        SubElement(metadata, 'ProjectName').text = self._last_result.project_name
        SubElement(metadata, 'Language').text = self._last_result.language
        SubElement(metadata, 'ScanDate').text = self._last_result.scan_date
        SubElement(metadata, 'ExecutionTime').text = str(self._last_result.execution_time)
        
        # Summary
        summary = SubElement(root, 'Summary')
        SubElement(summary, 'TotalVulnerabilities').text = str(self._last_result.total_vulnerabilities)
        SubElement(summary, 'SecurityScore').text = str(self._last_result.security_metrics.security_score)
        SubElement(summary, 'RiskScore').text = str(self._last_result.security_metrics.risk_score)
        
        severity_counts = SubElement(summary, 'SeverityCounts')
        for severity, count in self._last_result.severity_counts.items():
            sev_elem = SubElement(severity_counts, 'Severity')
            sev_elem.set('level', severity)
            sev_elem.text = str(count)
        
        # Tools
        tools = SubElement(root, 'ToolsUsed')
        for tool in self._last_result.tools_used:
            SubElement(tools, 'Tool').text = tool
        
        # Compliance
        compliance = SubElement(root, 'Compliance')
        SubElement(compliance, 'NISTFrameworkScore').text = str(self._last_result.compliance_metrics.nist_framework_score)
        SubElement(compliance, 'PCIDSSRelevant').text = str(self._last_result.compliance_metrics.pci_dss_relevant)
        SubElement(compliance, 'ISO27001Relevant').text = str(self._last_result.compliance_metrics.iso27001_relevant)
        
        # Vulnerabilities
        vulnerabilities = SubElement(root, 'Vulnerabilities')
        for vuln in self._last_result.vulnerabilities:
            vuln_elem = SubElement(vulnerabilities, 'Vulnerability')
            vuln_elem.set('id', vuln.get('rule_id', 'unknown'))
            vuln_elem.set('severity', vuln.get('severity', 'medium'))
            
            SubElement(vuln_elem, 'File').text = vuln.get('file', 'unknown')
            SubElement(vuln_elem, 'Line').text = str(vuln.get('line', 1))
            SubElement(vuln_elem, 'Message').text = vuln.get('message', '')
            SubElement(vuln_elem, 'Tool').text = vuln.get('tool', 'unknown')
            
            if vuln.get('cwe'):
                SubElement(vuln_elem, 'CWE').text = vuln.get('cwe')
            if vuln.get('owasp_category'):
                SubElement(vuln_elem, 'OWASP').text = vuln.get('owasp_category')
        
        # Formatear XML con indentación
        rough_string = tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def _generate_summary_report(self) -> str:
        """Genera reporte de resumen ejecutivo"""
        result = self._last_result
        
        # Calcular scores y métricas clave
        security_score = result.security_metrics.security_score
        risk_score = result.security_metrics.risk_score
        total_vulns = result.total_vulnerabilities
        critical_vulns = result.security_metrics.critical_vulnerabilities
        high_vulns = result.security_metrics.high_vulnerabilities
        
        # Determinar calificación general
        if security_score >= 90:
            grade = "A"
            grade_desc = "Excelente"
        elif security_score >= 80:
            grade = "B"
            grade_desc = "Bueno"
        elif security_score >= 70:
            grade = "C"
            grade_desc = "Aceptable"
        elif security_score >= 60:
            grade = "D"
            grade_desc = "Necesita mejoras"
        else:
            grade = "F"
            grade_desc = "Crítico"
        
        # Top 5 vulnerabilidades más críticas
        top_vulns = sorted(
            result.vulnerabilities,
            key=lambda x: self._get_vulnerability_priority(x),
            reverse=True
        )[:5]
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                SEMBICHO SECURITY REPORT                              ║
║                                   RESUMEN EJECUTIVO                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

📊 INFORMACIÓN DEL PROYECTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Proyecto: {result.project_name}
  Lenguaje: {result.language}
  Fecha: {result.scan_date}
  Tiempo de ejecución: {result.execution_time:.2f}s
  Archivos analizados: {result.quality_metrics.total_files_scanned}
  Líneas de código: {result.quality_metrics.total_lines_scanned:,}

🎯 CALIFICACIÓN GENERAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Calificación: {grade} ({grade_desc})
  Security Score: {security_score:.1f}/100
  Risk Score: {risk_score:.1f}/100

🚨 RESUMEN DE VULNERABILIDADES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total: {total_vulns}
  🔴 Críticas: {critical_vulns}
  🟠 Altas: {high_vulns}
  🟡 Medias: {result.security_metrics.medium_vulnerabilities}
  🟢 Bajas: {result.security_metrics.low_vulnerabilities}

📋 CUMPLIMIENTO Y ESTÁNDARES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NIST Framework: {result.compliance_metrics.nist_framework_score:.1f}/100
  PCI-DSS Relevantes: {result.compliance_metrics.pci_dss_relevant}
  ISO 27001 Relevantes: {result.compliance_metrics.iso27001_relevant}
  SOC 2 Relevantes: {result.compliance_metrics.soc2_relevant}

🔥 TOP 5 VULNERABILIDADES CRÍTICAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for i, vuln in enumerate(top_vulns, 1):
            severity_icon = self._get_severity_icon(vuln.get('severity', 'medium'))
            report += f"""
  {i}. {severity_icon} {vuln.get('severity', 'medium').upper()} - {vuln.get('rule_id', 'Unknown')}
     📁 {vuln.get('file', 'unknown')}:{vuln.get('line', 1)}
     💬 {vuln.get('message', 'No description')[:80]}...
     🔧 Tool: {vuln.get('tool', 'unknown')} | CWE: {vuln.get('cwe', 'N/A')} | OWASP: {vuln.get('owasp_category', 'N/A')}
"""
        
        report += f"""
🛠️ HERRAMIENTAS UTILIZADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {', '.join(result.tools_used)}

📈 MÉTRICAS DE CALIDAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Índice de mantenibilidad: {result.quality_metrics.maintainability_index:.1f}/100
  Ratio de deuda técnica: {result.quality_metrics.technical_debt_ratio:.2%}
  Score de complejidad: {result.quality_metrics.complexity_score:.1f}

💡 RECOMENDACIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if critical_vulns > 0:
            report += f"  🔴 URGENTE: Corregir {critical_vulns} vulnerabilidades críticas inmediatamente\n"
        if high_vulns > 0:
            report += f"  🟠 ALTA PRIORIDAD: Resolver {high_vulns} vulnerabilidades altas\n"
        if security_score < 70:
            report += "  📚 Implementar revisiones de seguridad en el proceso de desarrollo\n"
        if result.quality_metrics.technical_debt_ratio > 0.3:
            report += "  🔧 Refactorizar código para reducir deuda técnica\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generado por SemBicho v1.0.0 - {result.scan_date}
"""
        
        return report
    
    def _get_vulnerability_priority(self, vuln: Dict) -> int:
        """Calcula prioridad de vulnerabilidad para ordenamiento"""
        severity_weights = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        impact_weights = {'high': 3, 'medium': 2, 'low': 1}
        likelihood_weights = {'high': 3, 'medium': 2, 'low': 1}
        
        severity_score = severity_weights.get(vuln.get('severity', 'medium'), 2)
        impact_score = impact_weights.get(vuln.get('impact', 'medium'), 2)
        likelihood_score = likelihood_weights.get(vuln.get('likelihood', 'medium'), 2)
        
        return severity_score * 10 + impact_score * 3 + likelihood_score
    
    def _get_severity_icon(self, severity: str) -> str:
        """Retorna emoji para severidad"""
        icons = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }
        return icons.get(severity.lower(), '⚪')
    
    def _generate_html_report(self) -> str:
        """Genera reporte en formato HTML"""
        result = self._last_result
        
        html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SemBicho Security Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .summary-card { background: #f8f9fa; padding: 15px; border-radius: 6px; text-align: center; }
        .severity-critical { background-color: #dc3545; color: white; }
        .severity-high { background-color: #fd7e14; color: white; }
        .severity-medium { background-color: #ffc107; color: black; }
        .severity-low { background-color: #28a745; color: white; }
        .vulnerabilities { margin-top: 20px; }
        .vuln-item { border: 1px solid #ddd; margin-bottom: 10px; padding: 15px; border-radius: 6px; }
        .vuln-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .vuln-severity { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .vuln-details { color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 SemBicho Security Report</h1>
            <p><strong>Proyecto:</strong> {project_name} | <strong>Fecha:</strong> {scan_date} | <strong>Lenguaje:</strong> {language}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Vulnerabilidades</h3>
                <h2>{total_vulnerabilities}</h2>
            </div>
            <div class="summary-card severity-critical">
                <h3>Críticas</h3>
                <h2>{critical_count}</h2>
            </div>
            <div class="summary-card severity-high">
                <h3>Altas</h3>
                <h2>{high_count}</h2>
            </div>
            <div class="summary-card severity-medium">
                <h3>Medias</h3>
                <h2>{medium_count}</h2>
            </div>
            <div class="summary-card severity-low">
                <h3>Bajas</h3>
                <h2>{low_count}</h2>
            </div>
        </div>
        
        <div class="vulnerabilities">
            <h2>Detalles de Vulnerabilidades</h2>
            {vulnerabilities_html}
        </div>
        
        <div style="margin-top: 30px; text-align: center; color: #666;">
            <p>Herramientas utilizadas: {tools_used}</p>
            <p>Generado por SemBicho CLI</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Generar HTML de vulnerabilidades
        vulnerabilities_html = ""
        for vuln in result['vulnerabilities']:
            severity_class = f"severity-{vuln['severity']}"
            vulnerabilities_html += f"""
            <div class="vuln-item">
                <div class="vuln-header">
                    <strong>{vuln['file']}:{vuln['line']}</strong>
                    <span class="vuln-severity {severity_class}">{vuln['severity'].upper()}</span>
                </div>
                <div class="vuln-details">
                    <p><strong>Regla:</strong> {vuln['rule_id']} ({vuln['tool']})</p>
                    <p><strong>Mensaje:</strong> {vuln['message']}</p>
                    {f"<p><strong>CWE:</strong> {vuln['cwe']}</p>" if vuln.get('cwe') else ""}
                </div>
            </div>
            """
        
        return html_template.format(
            project_name=result['project_name'],
            scan_date=result['scan_date'],
            language=result['language'],
            total_vulnerabilities=result['total_vulnerabilities'],
            critical_count=result['severity_counts']['critical'],
            high_count=result['severity_counts']['high'],
            medium_count=result['severity_counts']['medium'],
            low_count=result['severity_counts']['low'],
            vulnerabilities_html=vulnerabilities_html,
            tools_used=", ".join(result['tools_used'])
        )
    
    def _generate_console_report(self) -> str:
        """Genera reporte para consola"""
        result = self._last_result
        
        report = f"""
🔒 SemBicho Security Report
=====================================
Proyecto: {result['project_name']}
Fecha: {result['scan_date']}
Lenguaje: {result['language']}
Herramientas: {', '.join(result['tools_used'])}

📊 Resumen:
Total vulnerabilidades: {result['total_vulnerabilities']}
- Críticas: {result['severity_counts']['critical']}
- Altas: {result['severity_counts']['high']}
- Medias: {result['severity_counts']['medium']}
- Bajas: {result['severity_counts']['low']}

🔍 Detalles:
"""
        
        for vuln in result['vulnerabilities']:
            severity_icon = {
                'critical': '🔴',
                'high': '🟠', 
                'medium': '🟡',
                'low': '🟢'
            }.get(vuln['severity'], '⚪')
            
            report += f"""
{severity_icon} {vuln['severity'].upper()} - {vuln['file']}:{vuln['line']}
   Regla: {vuln['rule_id']} ({vuln['tool']})
   Mensaje: {vuln['message']}
"""
            if vuln.get('cwe'):
                report += f"   CWE: {vuln['cwe']}\n"
        
        return report
    
    def send_to_api(self, api_url: str, token: Optional[str] = None, data: Optional[Dict] = None, pipeline_id: Optional[str] = None) -> bool:
        """
        Envía resultados al backend vía POST
        
        Args:
            api_url: URL del endpoint API
            token: Token de autenticación
            data: Datos a enviar (si no se proporciona, usa los últimos resultados)
            pipeline_id: ID del pipeline personalizado
            
        Returns:
            True si el envío fue exitoso, False en caso contrario
        """
        try:
            # Obtener datos a enviar
            if data:
                scan_results = data
            elif hasattr(self, '_last_result') and self._last_result:
                # Conversión a dict
                try:
                    # Intentar convertir a dict si es un dataclass
                    from dataclasses import is_dataclass
                    if is_dataclass(self._last_result):
                        scan_results = asdict(self._last_result)
                    else:
                        scan_results = self._manual_dataclass_to_dict(self._last_result)
                except (TypeError, AttributeError):
                    # Conversión manual si asdict falla
                    scan_results = self._manual_dataclass_to_dict(self._last_result)
            else:
                self.logger.error("No hay datos de escaneo para enviar")
                return False
            
            # Verificar que scan_results es un dict
            if not isinstance(scan_results, dict):
                # Último intento de conversión manual
                scan_results = self._manual_dataclass_to_dict(scan_results)
                if not isinstance(scan_results, dict):
                    self.logger.error(f"No se pudo convertir los datos a diccionario")
                    return False
            
            # Generar pipeline_id si no se proporciona
            if not pipeline_id:
                project_name = scan_results.get('project_name', 'unknown')
                scan_date = scan_results.get('scan_date', 'unknown')
                pipeline_id = f"sembicho-cli-{project_name}-{scan_date}"
            
            # Formatear datos según el schema del backend
            payload = {
                "pipelineId": pipeline_id,
                "data": scan_results,
                "fecha": scan_results.get('scan_date')
            }
            
            headers = {'Content-Type': 'application/json'}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            else:
                self.logger.warning("No se proporcionó token de autenticación")
                return False
            
            self.logger.info(f"Enviando reporte a {api_url} con pipeline ID: {pipeline_id}")
            
            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                self.logger.info(f"Resultados enviados exitosamente a {api_url}")
                return True
            elif response.status_code == 401:
                self.logger.error("Error de autenticación: Token inválido o expirado")
                self.logger.info("Verifica que el token sea válido")
                return False
            else:
                self.logger.error(f"Error del servidor: {response.status_code} - {response.text}")
                return False
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error de conexión enviando resultados a API: {e}")
            self.logger.info("Verifica que el backend esté ejecutándose y sea accesible")
            return False
        except Exception as e:
            self.logger.error(f"Error inesperado enviando a API: {e}")
            return False
    
    def _manual_dataclass_to_dict(self, obj) -> Dict:
        """
        Conversión manual de ScanResult a diccionario
        """
        try:
            if hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    if hasattr(value, '__dict__') and not isinstance(value, (str, int, float, bool, list, dict)):
                        # Si es otro dataclass, convertirlo recursivamente
                        result[key] = self._manual_dataclass_to_dict(value)
                    else:
                        result[key] = value
                return result
            else:
                return obj
        except Exception as e:
            self.logger.error(f"Error en conversión manual: {e}")
            return {}