#!/usr/bin/env python3
"""
Quality Scanner Integrator for SemBicho
Integra linting, complexity, coverage y code smells en el scanner principal
"""

import os
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Importar módulos de linting
try:
    from .python_linting import PythonLintingEngine
    from .javascript_linting import JavaScriptLintingEngine
    LINTING_AVAILABLE = True
except ImportError:
    LINTING_AVAILABLE = False
    logging.warning("Linting engines not available")

# Importar módulo de complejidad
try:
    from .complexity_engine import ComplexityEngine, ComplexityMetric
    COMPLEXITY_AVAILABLE = True
except ImportError:
    COMPLEXITY_AVAILABLE = False
    logging.warning("Complexity engine not available")

from .scanner import (
    Vulnerability, 
    ScanResult, 
    QualityMetrics, 
    SecurityMetrics,
    ComplianceMetrics,
    ArchitectureMetrics,
    PerformanceMetrics,
    SemBichoScanner
)


@dataclass
class QualityAnalysisResult:
    """Resultado del análisis de calidad"""
    linting_issues: List[Vulnerability]
    linting_metrics: Dict
    complexity_issues: List[Vulnerability]
    complexity_metrics: Dict
    coverage_metrics: Dict
    code_smells: List[Vulnerability]
    total_quality_issues: int
    quality_score: float
    quality_grade: str
    execution_time: float


class QualityScannerIntegrator:
    """
    Integrador que conecta análisis de calidad con el scanner de seguridad
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa el integrador de calidad
        
        Args:
            config: Configuración opcional (puede venir de sembicho-quality.yml)
        """
        self.config = config or {}
        self.logger = logging.getLogger('sembicho.quality')
        
        # Configuración de módulos
        self.linting_config = self.config.get('linting', {})
        self.complexity_config = self.config.get('complexity', {})
        self.coverage_config = self.config.get('coverage', {})
        self.code_smells_config = self.config.get('code_smells', {})
        
        # Inicializar engines de linting
        if LINTING_AVAILABLE:
            self.python_linting = PythonLintingEngine(
                self.linting_config.get('rules', {}).get('python', {})
            )
            self.javascript_linting = JavaScriptLintingEngine(
                self.linting_config.get('rules', {}).get('javascript', {})
            )
        else:
            self.python_linting = None
            self.javascript_linting = None
        
        # Inicializar engine de complejidad
        if COMPLEXITY_AVAILABLE:
            self.complexity_engine = ComplexityEngine(self.complexity_config)
        else:
            self.complexity_engine = None
            
        # Flags de features habilitadas
        self.linting_enabled = self.linting_config.get('enabled', True)
        self.complexity_enabled = self.complexity_config.get('enabled', True)  # Habilitado por defecto
        self.coverage_enabled = self.coverage_config.get('enabled', False)
        self.code_smells_enabled = self.code_smells_config.get('enabled', False)
        
    def analyze_quality(self, path: str, language: str = None) -> QualityAnalysisResult:
        """
        Ejecuta análisis de calidad completo
        
        Args:
            path: Ruta del proyecto o archivo
            language: Lenguaje detectado (opcional)
            
        Returns:
            QualityAnalysisResult con todos los resultados
        """
        start_time = time.time()
        
        self.logger.info(f"Starting quality analysis for: {path}")
        
        # Detectar lenguaje si no se proporciona
        if not language:
            language = self._detect_language(path)
        
        # Inicializar resultados
        linting_issues = []
        linting_metrics = {}
        complexity_issues = []
        complexity_metrics = {}
        coverage_metrics = {}
        code_smells = []
        
        # 1. Análisis de Linting
        if self.linting_enabled and LINTING_AVAILABLE:
            try:
                linting_issues, linting_metrics = self._run_linting_analysis(path, language)
                self.logger.info(f"Linting: {len(linting_issues)} issues found")
            except Exception as e:
                self.logger.error(f"Linting failed: {e}")
        
        # 2. Análisis de Complejidad (TODO: Fase 2)
        if self.complexity_enabled:
            try:
                complexity_issues, complexity_metrics = self._run_complexity_analysis(path, language)
                self.logger.info(f"Complexity: {len(complexity_issues)} issues found")
            except Exception as e:
                self.logger.error(f"X Complexity analysis failed: {e}")
        
        # 3. Análisis de Cobertura (TODO: Fase 2)
        if self.coverage_enabled:
            try:
                coverage_metrics = self._run_coverage_analysis(path, language)
                self.logger.info(f"Coverage: {coverage_metrics.get('total_coverage', 0):.1f}%")
            except Exception as e:
                self.logger.error(f"X Coverage analysis failed: {e}")
        
        # 4. Detección de Code Smells (TODO: Fase 3)
        if self.code_smells_enabled:
            try:
                code_smells = self._run_code_smell_detection(path, language)
                self.logger.info(f"Code Smells: {len(code_smells)} detected")
            except Exception as e:
                self.logger.error(f"X Code smell detection failed: {e}")
        
        # Calcular métricas totales
        total_issues = len(linting_issues) + len(complexity_issues) + len(code_smells)
        quality_score = self._calculate_quality_score(
            linting_metrics,
            complexity_metrics,
            coverage_metrics,
            len(code_smells)
        )
        quality_grade = self._score_to_grade(quality_score)
        
        execution_time = time.time() - start_time
        
        self.logger.info("Quality Analysis Complete:")
        self.logger.info(f"   Total Issues: {total_issues}")
        self.logger.info(f"   Quality Score: {quality_score:.1f}/100")
        self.logger.info(f"   Grade: {quality_grade}")
        self.logger.info(f"   Time: {execution_time:.2f}s")
        
        return QualityAnalysisResult(
            linting_issues=linting_issues,
            linting_metrics=linting_metrics,
            complexity_issues=complexity_issues,
            complexity_metrics=complexity_metrics,
            coverage_metrics=coverage_metrics,
            code_smells=code_smells,
            total_quality_issues=total_issues,
            quality_score=quality_score,
            quality_grade=quality_grade,
            execution_time=execution_time
        )
    
    def _run_linting_analysis(self, path: str, language: str) -> Tuple[List[Vulnerability], Dict]:
        """Ejecuta análisis de linting según el lenguaje"""
        
        if language == 'python' and self.python_linting:
            vulnerabilities, metrics = self.python_linting.run_full_analysis(path)
            return vulnerabilities, metrics
            
        elif language in ['javascript', 'typescript'] and self.javascript_linting:
            is_typescript = language == 'typescript'
            vulnerabilities, metrics = self.javascript_linting.run_full_analysis(path, is_typescript)
            return vulnerabilities, metrics
            
        else:
            self.logger.warning(f"Linting not available for language: {language}")
            return [], {}
    
    def _run_complexity_analysis(self, path: str, language: str) -> Tuple[List[Vulnerability], Dict]:
        """Ejecuta análisis de complejidad"""
        if not COMPLEXITY_AVAILABLE or not self.complexity_engine:
            return [], {}
        
        try:
            result = self.complexity_engine.analyze_complexity(path, language)
            
            # Convertir métricas de complejidad a Vulnerabilities para reporte unificado
            vulnerabilities = []
            for metric in result.complexity_metrics:
                # Solo reportar como vulnerability si complejidad es alta
                if metric.cyclomatic_complexity > 10:
                    vuln = Vulnerability(
                        type='COMPLEXITY',
                        severity='high' if metric.cyclomatic_complexity > 20 else 'medium',
                        confidence='high',
                        file_path=metric.file_path,
                        line_number=metric.line_number,
                        code_snippet=f"Function: {metric.name}",
                        description=metric.description,
                        recommendation=f"Refactorizar {metric.name} para reducir complejidad de {metric.cyclomatic_complexity} a menos de 10",
                        cwe_id='CWE-1093',  # Excessive complexity
                        owasp_category='A04:2021 - Insecure Design',
                        tool='complexity_engine'
                    )
                    vulnerabilities.append(vuln)
            
            # Crear dict de métricas
            metrics = {
                'total_functions': result.total_functions,
                'average_complexity': result.average_complexity,
                'max_complexity': result.max_complexity,
                'high_complexity_count': result.high_complexity_count,
                'critical_complexity_count': result.critical_complexity_count,
                'quality_score': result.complexity_score,
                'grade': result.complexity_grade,
                'tools_executed': result.tools_executed
            }
            
            return vulnerabilities, metrics
            
        except Exception as e:
            self.logger.error(f"Complexity analysis error: {e}")
            return [], {}
    
    def _run_coverage_analysis(self, path: str, language: str) -> Dict:
        """Ejecuta análisis de cobertura (TODO: Fase 2)"""
        # Placeholder para Fase 2
        return {}
    
    def _run_code_smell_detection(self, path: str, language: str) -> List[Vulnerability]:
        """Detecta code smells (TODO: Fase 3)"""
        # Placeholder para Fase 3
        return []
    
    def _detect_language(self, path: str) -> str:
        """Detecta el lenguaje principal del proyecto"""
        if os.path.isfile(path):
            ext = Path(path).suffix
            lang_mapping = {
                '.py': 'python',
                '.js': 'javascript',
                '.jsx': 'javascript',
                '.ts': 'typescript',
                '.tsx': 'typescript',
                '.java': 'java',
                '.php': 'php',
                '.rb': 'ruby',
                '.go': 'go',
                '.cs': 'csharp'
            }
            return lang_mapping.get(ext, 'unknown')
        
        # Para directorios, buscar archivos predominantes
        extensions = {}
        for root, dirs, files in os.walk(path):
            # Ignorar directorios comunes
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.git', '__pycache__']]
            
            for file in files:
                ext = Path(file).suffix
                if ext:
                    extensions[ext] = extensions.get(ext, 0) + 1
        
        if not extensions:
            return 'unknown'
        
        # Obtener extensión más común
        most_common_ext = max(extensions.items(), key=lambda x: x[1])[0]
        
        lang_mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.cs': 'csharp'
        }
        
        return lang_mapping.get(most_common_ext, 'unknown')
    
    def _calculate_quality_score(self, linting_metrics: Dict, complexity_metrics: Dict,
                                 coverage_metrics: Dict, code_smells_count: int) -> float:
        """
        Calcula score de calidad ponderado
        
        Fórmula: (linting * 0.3) + (complexity * 0.25) + (coverage * 0.25) + (smells * 0.2)
        """
        score = 0.0
        
        # Linting score (30% del total)
        linting_score = linting_metrics.get('metrics', {}).get('quality_score', 100.0)
        score += linting_score * 0.3
        
        # Complexity score (25% del total)
        if complexity_metrics and 'quality_score' in complexity_metrics:
            complexity_score = complexity_metrics.get('quality_score', 100.0)
            score += complexity_score * 0.25
        else:
            score += 100.0 * 0.25  # Score perfecto si no se analizó
        
        # Coverage score (25% del total)
        if coverage_metrics:
            coverage_score = coverage_metrics.get('total_coverage', 0.0)
            score += coverage_score * 0.25
        else:
            score += 100.0 * 0.25  # Score perfecto si no se analizó
        
        # Code smells score (20% del total)
        smells_score = max(0, 100.0 - (code_smells_count * 5))  # -5 puntos por smell
        score += smells_score * 0.2
        
        return round(min(100.0, score), 1)
    
    def _score_to_grade(self, score: float) -> str:
        """Convierte score numérico a grado A-F"""
        if score >= 95:
            return 'A+'
        elif score >= 90:
            return 'A'
        elif score >= 85:
            return 'B+'
        elif score >= 80:
            return 'B'
        elif score >= 75:
            return 'C+'
        elif score >= 70:
            return 'C'
        elif score >= 65:
            return 'D+'
        elif score >= 60:
            return 'D'
        else:
            return 'F'


class EnhancedSemBichoScanner(SemBichoScanner):
    """
    Scanner mejorado que integra análisis de seguridad + calidad
    Extiende el scanner original sin breaking changes
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa el scanner mejorado
        
        Args:
            config: Configuración que puede incluir security + quality settings
        """
        super().__init__(config)
        
        # Inicializar integrador de calidad
        self.quality_integrator = QualityScannerIntegrator(config)
        
        # Flag para habilitar análisis de calidad
        self.quality_analysis_enabled = config.get('quality_analysis_enabled', True) if config else True
        
    def scan_directory(self, directory_path: str) -> ScanResult:
        """
        Escanea un directorio con análisis de seguridad + calidad
        
        Override del método original para agregar análisis de calidad
        
        Args:
            directory_path: Ruta del directorio a escanear
            
        Returns:
            ScanResult con métricas de seguridad y calidad
        """
        self.logger.info(f"Starting enhanced scan: {directory_path}")
        
        # 1. Ejecutar scan de seguridad original
        security_result = super().scan_directory(directory_path)
        
        # 2. Ejecutar análisis de calidad si está habilitado
        if self.quality_analysis_enabled:
            try:
                language = self._detect_primary_language(directory_path)
                quality_result = self.quality_integrator.analyze_quality(directory_path, language)
                
                # 3. Integrar resultados de calidad en el ScanResult
                security_result = self._merge_quality_results(security_result, quality_result)
                
            except Exception as e:
                self.logger.error(f"X Quality analysis failed: {e}")
                # Continuar con resultados de seguridad incluso si calidad falla
        
        return security_result
    
    def scan_file(self, file_path: str) -> ScanResult:
        """
        Escanea un archivo con análisis de seguridad + calidad
        
        Override del método original
        
        Args:
            file_path: Ruta del archivo a escanear
            
        Returns:
            ScanResult con métricas de seguridad y calidad
        """
        self.logger.info(f"Starting enhanced file scan: {file_path}")
        
        # 1. Ejecutar scan de seguridad original
        security_result = super().scan_file(file_path)
        
        # 2. Ejecutar análisis de calidad si está habilitado
        if self.quality_analysis_enabled:
            try:
                ext = Path(file_path).suffix
                language = self.SUPPORTED_LANGUAGES.get(ext, 'unknown')
                quality_result = self.quality_integrator.analyze_quality(file_path, language)
                
                # 3. Integrar resultados
                security_result = self._merge_quality_results(security_result, quality_result)
                
            except Exception as e:
                self.logger.error(f"X Quality analysis failed: {e}")
        
        return security_result
    
    def _merge_quality_results(self, security_result: ScanResult, 
                               quality_result: QualityAnalysisResult) -> ScanResult:
        """
        Fusiona resultados de seguridad y calidad en un ScanResult unificado
        
        Args:
            security_result: Resultado del scan de seguridad
            quality_result: Resultado del análisis de calidad
            
        Returns:
            ScanResult actualizado con métricas de calidad
        """
        # Agregar vulnerabilidades de calidad
        quality_vulns = (
            quality_result.linting_issues +
            quality_result.complexity_issues +
            quality_result.code_smells
        )
        
        # Actualizar lista de vulnerabilidades
        security_result.vulnerabilities.extend([asdict(v) for v in quality_vulns])
        security_result.total_vulnerabilities += len(quality_vulns)
        
        # Actualizar QualityMetrics con datos reales
        linting_metrics = quality_result.linting_metrics.get('metrics', {})
        
        # Actualizar complejidad si está disponible
        if quality_result.complexity_metrics:
            security_result.quality_metrics.cyclomatic_complexity = (
                quality_result.complexity_metrics.get('average_complexity', 0.0)
            )
        else:
            security_result.quality_metrics.cyclomatic_complexity = 0.0
        security_result.quality_metrics.duplicate_code_ratio = (
            quality_result.complexity_metrics.get('duplication_ratio', 0.0)
        )
        security_result.quality_metrics.test_coverage_ratio = (
            quality_result.coverage_metrics.get('total_coverage', 0.0) / 100.0
        )
        
        # Actualizar grade de calidad
        security_result.overall_quality_grade = quality_result.quality_grade
        
        # Actualizar tools used
        tools_executed = linting_metrics.get('tools_executed', [])
        security_result.tools_used.extend(tools_executed)
        
        self.logger.info(f"Merged results: {len(quality_vulns)} quality issues added")
        
        return security_result
    
    def _detect_primary_language(self, directory_path: str) -> str:
        """Detecta el lenguaje principal del proyecto"""
        return self.quality_integrator._detect_language(directory_path)
