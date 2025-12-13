#!/usr/bin/env python3
"""
SemBicho Linting Engine
Módulo para análisis de estilo y formato de código multi-lenguaje
"""

import os
import json
import subprocess
import logging
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

from .scanner import Vulnerability, SemBichoScanner


class LintSeverity(Enum):
    """Severidades estándar para reglas de linting"""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class LintCategory(Enum):
    """Categorías de reglas de linting"""
    STYLE = "style"                    # Formatting, naming conventions
    FORMAT = "format"                  # Code formatting, indentation
    BEST_PRACTICE = "best-practice"    # Code quality best practices
    PERFORMANCE = "performance"        # Performance anti-patterns
    MAINTAINABILITY = "maintainability"  # Code maintainability
    ACCESSIBILITY = "accessibility"    # Accessibility issues (frontend)
    SECURITY = "security"              # Security-related linting


@dataclass
class LintRule:
    """Representa una regla de linting"""
    rule_id: str
    tool: str
    severity: LintSeverity
    category: LintCategory
    message: str
    description: str
    file_pattern: Optional[str] = None
    language: Optional[str] = None
    remediation_effort: str = "low"  # low, medium, high
    auto_fixable: bool = False
    documentation_url: Optional[str] = None


@dataclass
class LintingMetrics:
    """Métricas específicas de linting"""
    total_lint_issues: int
    style_issues: int
    format_issues: int
    best_practice_issues: int
    performance_issues: int
    maintainability_issues: int
    auto_fixable_issues: int
    tools_executed: List[str]
    execution_time: float
    linting_score: float  # 0-100


class LintingEngine:
    """Motor de análisis de linting multi-lenguaje"""
    
    # Configuración de herramientas por lenguaje
    LINTER_CONFIGS = {
        'python': {
            'flake8': {
                'cmd': ['flake8', '--format=json', '--output-file=-'],
                'output_format': 'flake8_json',
                'categories': ['style', 'best-practice'],
                'severity_mapping': {
                    'E': LintSeverity.MEDIUM,  # Error
                    'W': LintSeverity.LOW,     # Warning
                    'F': LintSeverity.HIGH,    # Flake8 error
                    'C': LintSeverity.LOW,     # Convention
                    'R': LintSeverity.MEDIUM,  # Refactor
                }
            },
            'black': {
                'cmd': ['black', '--check', '--diff'],
                'output_format': 'diff',
                'categories': ['format'],
                'severity_mapping': {
                    'format': LintSeverity.LOW
                }
            },
            'pylint': {
                'cmd': ['pylint', '--output-format=json'],
                'output_format': 'pylint_json',
                'categories': ['style', 'best-practice', 'performance'],
                'severity_mapping': {
                    'convention': LintSeverity.LOW,
                    'refactor': LintSeverity.MEDIUM,
                    'warning': LintSeverity.MEDIUM,
                    'error': LintSeverity.HIGH,
                    'fatal': LintSeverity.CRITICAL
                }
            }
        },
        
        'javascript': {
            'eslint': {
                'cmd': ['eslint', '--format=json'],
                'output_format': 'eslint_json',
                'categories': ['style', 'best-practice', 'security'],
                'severity_mapping': {
                    0: LintSeverity.INFO,
                    1: LintSeverity.LOW,
                    2: LintSeverity.MEDIUM
                }
            },
            'prettier': {
                'cmd': ['prettier', '--check'],
                'output_format': 'prettier_text',
                'categories': ['format'],
                'severity_mapping': {
                    'format': LintSeverity.LOW
                }
            }
        },
        
        'typescript': {
            'eslint': {
                'cmd': ['eslint', '--ext', '.ts,.tsx', '--format=json'],
                'output_format': 'eslint_json',
                'categories': ['style', 'best-practice', 'security'],
                'severity_mapping': {
                    0: LintSeverity.INFO,
                    1: LintSeverity.LOW,
                    2: LintSeverity.MEDIUM
                }
            },
            'tslint': {
                'cmd': ['tslint', '--format=json'],
                'output_format': 'tslint_json',
                'categories': ['style', 'best-practice'],
                'severity_mapping': {
                    'warning': LintSeverity.LOW,
                    'error': LintSeverity.MEDIUM
                }
            }
        },
        
        'java': {
            'checkstyle': {
                'cmd': ['checkstyle', '-f', 'xml'],
                'output_format': 'checkstyle_xml',
                'categories': ['style', 'best-practice'],
                'severity_mapping': {
                    'info': LintSeverity.INFO,
                    'warning': LintSeverity.LOW,
                    'error': LintSeverity.MEDIUM
                }
            },
            'spotbugs': {
                'cmd': ['spotbugs', '-xml:withMessages'],
                'output_format': 'spotbugs_xml',
                'categories': ['best-practice', 'performance', 'security'],
                'severity_mapping': {
                    'Low': LintSeverity.LOW,
                    'Medium': LintSeverity.MEDIUM,
                    'High': LintSeverity.HIGH
                }
            }
        },
        
        'php': {
            'phpcs': {
                'cmd': ['phpcs', '--report=json'],
                'output_format': 'phpcs_json',
                'categories': ['style', 'best-practice'],
                'severity_mapping': {
                    'WARNING': LintSeverity.LOW,
                    'ERROR': LintSeverity.MEDIUM
                }
            },
            'phpstan': {
                'cmd': ['phpstan', 'analyse', '--error-format=json'],
                'output_format': 'phpstan_json',
                'categories': ['best-practice', 'performance'],
                'severity_mapping': {
                    'tip': LintSeverity.INFO,
                    'warning': LintSeverity.LOW,
                    'error': LintSeverity.MEDIUM
                }
            }
        },
        
        'ruby': {
            'rubocop': {
                'cmd': ['rubocop', '--format=json'],
                'output_format': 'rubocop_json',
                'categories': ['style', 'best-practice', 'performance'],
                'severity_mapping': {
                    'info': LintSeverity.INFO,
                    'refactor': LintSeverity.LOW,
                    'convention': LintSeverity.LOW,
                    'warning': LintSeverity.MEDIUM,
                    'error': LintSeverity.HIGH,
                    'fatal': LintSeverity.CRITICAL
                }
            }
        },
        
        'go': {
            'golint': {
                'cmd': ['golint'],
                'output_format': 'golint_text',
                'categories': ['style', 'best-practice'],
                'severity_mapping': {
                    'suggestion': LintSeverity.LOW
                }
            },
            'gofmt': {
                'cmd': ['gofmt', '-l'],
                'output_format': 'gofmt_text',
                'categories': ['format'],
                'severity_mapping': {
                    'format': LintSeverity.LOW
                }
            }
        },
        
        'csharp': {
            'dotnet-format': {
                'cmd': ['dotnet', 'format', '--verify-no-changes', '--verbosity', 'diagnostic'],
                'output_format': 'dotnet_text',
                'categories': ['format', 'style'],
                'severity_mapping': {
                    'info': LintSeverity.INFO,
                    'warning': LintSeverity.LOW,
                    'error': LintSeverity.MEDIUM
                }
            }
        }
    }
    
    # Mapeo de reglas específicas a categorías mejoradas
    RULE_CATEGORY_MAPPING = {
        # Python - flake8
        'E1': LintCategory.STYLE,      # Indentation
        'E2': LintCategory.FORMAT,     # Whitespace
        'E3': LintCategory.FORMAT,     # Blank line
        'E4': LintCategory.FORMAT,     # Import
        'E5': LintCategory.FORMAT,     # Line length
        'E7': LintCategory.STYLE,      # Statement
        'E9': LintCategory.STYLE,      # Runtime
        'W1': LintCategory.STYLE,      # Indentation warning
        'W2': LintCategory.FORMAT,     # Whitespace warning
        'W3': LintCategory.FORMAT,     # Blank line warning
        'W5': LintCategory.STYLE,      # Line break warning
        'W6': LintCategory.STYLE,      # Deprecation warning
        'F4': LintCategory.BEST_PRACTICE,  # Import errors
        'F6': LintCategory.BEST_PRACTICE,  # Variables
        'F8': LintCategory.BEST_PRACTICE,  # Variables
        'C9': LintCategory.MAINTAINABILITY,  # Complexity
        
        # JavaScript - ESLint
        'no-unused-vars': LintCategory.BEST_PRACTICE,
        'no-undef': LintCategory.BEST_PRACTICE,
        'semi': LintCategory.STYLE,
        'quotes': LintCategory.STYLE,
        'indent': LintCategory.FORMAT,
        'eqeqeq': LintCategory.BEST_PRACTICE,
        'no-console': LintCategory.BEST_PRACTICE,
        'no-debugger': LintCategory.BEST_PRACTICE,
        'prefer-const': LintCategory.BEST_PRACTICE,
        'arrow-spacing': LintCategory.STYLE,
        'comma-dangle': LintCategory.STYLE,
        'no-trailing-spaces': LintCategory.FORMAT,
        
        # Java - Checkstyle
        'Indentation': LintCategory.FORMAT,
        'LineLength': LintCategory.FORMAT,
        'NeedBraces': LintCategory.STYLE,
        'EmptyBlock': LintCategory.STYLE,
        'MagicNumber': LintCategory.BEST_PRACTICE,
        'HiddenField': LintCategory.BEST_PRACTICE,
        'ParameterNumber': LintCategory.MAINTAINABILITY,
        'CyclomaticComplexity': LintCategory.MAINTAINABILITY,
        
        # PHP - PHPCS
        'Generic.WhiteSpace': LintCategory.FORMAT,
        'PEAR.Functions': LintCategory.STYLE,
        'PSR2.Classes': LintCategory.STYLE,
        'Squiz.PHP': LintCategory.BEST_PRACTICE,
        
        # Ruby - RuboCop
        'Layout': LintCategory.FORMAT,
        'Style': LintCategory.STYLE,
        'Naming': LintCategory.STYLE,
        'Metrics': LintCategory.MAINTAINABILITY,
        'Performance': LintCategory.PERFORMANCE,
        'Security': LintCategory.SECURITY,
        'Lint': LintCategory.BEST_PRACTICE,
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa el motor de linting
        
        Args:
            config: Configuración opcional
        """
        self.config = config or {}
        self.logger = logging.getLogger('sembicho.linting')
        self.enabled_tools = self.config.get('enabled_tools', {})
        self.thresholds = self.config.get('thresholds', {
            'max_issues': 1000,
            'fail_on_critical': True,
            'fail_on_high': False
        })
        
    def run_linting_analysis(self, path: str, language: str) -> tuple[List[Vulnerability], LintingMetrics]:
        """
        Ejecuta análisis de linting para un lenguaje específico
        
        Args:
            path: Ruta del proyecto o archivo
            language: Lenguaje detectado
            
        Returns:
            Tuple con lista de vulnerabilidades y métricas
        """
        start_time = time.time()
        vulnerabilities = []
        tools_executed = []
        
        if language not in self.LINTER_CONFIGS:
            self.logger.warning(f"No linters configured for language: {language}")
            return [], self._create_empty_metrics()
        
        linters = self.LINTER_CONFIGS[language]
        
        for tool_name, tool_config in linters.items():
            # Verificar si la herramienta está habilitada
            if not self._is_tool_enabled(tool_name, language):
                continue
                
            # Verificar si la herramienta está disponible
            if not self._is_tool_available(tool_name):
                self.logger.warning(f"Tool {tool_name} not available")
                continue
            
            try:
                tool_vulns = self._run_linter(path, tool_name, tool_config, language)
                vulnerabilities.extend(tool_vulns)
                tools_executed.append(tool_name)
                self.logger.info(f"✅ {tool_name}: {len(tool_vulns)} issues found")
                
            except Exception as e:
                self.logger.error(f"Error running {tool_name}: {e}")
                continue
        
        execution_time = time.time() - start_time
        metrics = self._calculate_metrics(vulnerabilities, tools_executed, execution_time)
        
        return vulnerabilities, metrics
    
    def _run_linter(self, path: str, tool_name: str, tool_config: Dict, language: str) -> List[Vulnerability]:
        """
        Ejecuta una herramienta de linting específica
        
        Args:
            path: Ruta a analizar
            tool_name: Nombre de la herramienta
            tool_config: Configuración de la herramienta
            language: Lenguaje de programación
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        cmd = tool_config['cmd'].copy()
        cmd.append(path)
        
        self.logger.debug(f"Running command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos timeout
                cwd=path if os.path.isdir(path) else os.path.dirname(path)
            )
            
            # Muchas herramientas de linting retornan código de salida != 0 cuando encuentran issues
            if result.returncode != 0 and result.returncode != 1:
                self.logger.warning(f"{tool_name} returned code {result.returncode}: {result.stderr}")
            
            output = result.stdout if result.stdout else result.stderr
            
            return self._parse_linter_output(
                output, 
                tool_name, 
                tool_config, 
                language, 
                path
            )
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"{tool_name} timed out")
            return []
        except FileNotFoundError:
            self.logger.error(f"{tool_name} not found in PATH")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error running {tool_name}: {e}")
            return []
    
    def _parse_linter_output(self, output: str, tool_name: str, tool_config: Dict, 
                           language: str, base_path: str) -> List[Vulnerability]:
        """
        Parsea la salida de una herramienta de linting
        
        Args:
            output: Salida de la herramienta
            tool_name: Nombre de la herramienta
            tool_config: Configuración de la herramienta
            language: Lenguaje de programación
            base_path: Ruta base del análisis
            
        Returns:
            Lista de vulnerabilidades parseadas
        """
        vulnerabilities = []
        output_format = tool_config['output_format']
        
        try:
            if output_format == 'flake8_json':
                vulnerabilities = self._parse_flake8_json(output, tool_name, tool_config, base_path)
            elif output_format == 'eslint_json':
                vulnerabilities = self._parse_eslint_json(output, tool_name, tool_config, base_path)
            elif output_format == 'pylint_json':
                vulnerabilities = self._parse_pylint_json(output, tool_name, tool_config, base_path)
            elif output_format.endswith('_text'):
                vulnerabilities = self._parse_text_output(output, tool_name, tool_config, base_path)
            else:
                self.logger.warning(f"Unknown output format: {output_format}")
                
        except Exception as e:
            self.logger.error(f"Error parsing {tool_name} output: {e}")
            
        return vulnerabilities
    
    def _parse_flake8_json(self, output: str, tool_name: str, tool_config: Dict, base_path: str) -> List[Vulnerability]:
        """Parsea salida JSON de flake8"""
        # Nota: flake8 no tiene salida JSON nativa, usaremos formato texto
        return self._parse_flake8_text(output, tool_name, tool_config, base_path)
    
    def _parse_flake8_text(self, output: str, tool_name: str, tool_config: Dict, base_path: str) -> List[Vulnerability]:
        """Parsea salida de texto de flake8"""
        vulnerabilities = []
        
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
                
            # Formato: file.py:line:col: code message
            parts = line.split(':', 3)
            if len(parts) < 4:
                continue
                
            file_path = parts[0]
            line_num = int(parts[1])
            col_num = int(parts[2])
            code_message = parts[3].strip()
            
            # Extraer código y mensaje
            code_parts = code_message.split(' ', 1)
            rule_id = code_parts[0]
            message = code_parts[1] if len(code_parts) > 1 else code_message
            
            severity = self._map_severity(rule_id, tool_config)
            category = self._map_category(rule_id)
            
            vulnerabilities.append(Vulnerability(
                file=file_path,
                line=line_num,
                rule_id=rule_id,
                severity=severity.value,
                message=message,
                tool=tool_name,
                category='quality',
                impact=self._severity_to_impact(severity),
                likelihood='high',
                remediation_effort='low'
            ))
            
        return vulnerabilities
    
    def _parse_eslint_json(self, output: str, tool_name: str, tool_config: Dict, base_path: str) -> List[Vulnerability]:
        """Parsea salida JSON de ESLint"""
        vulnerabilities = []
        
        try:
            data = json.loads(output)
            
            for file_result in data:
                file_path = file_result['filePath']
                
                for message in file_result.get('messages', []):
                    rule_id = message.get('ruleId', 'unknown')
                    severity_num = message.get('severity', 1)
                    
                    severity = tool_config['severity_mapping'].get(severity_num, LintSeverity.LOW)
                    category = self._map_category(rule_id)
                    
                    vulnerabilities.append(Vulnerability(
                        file=file_path,
                        line=message.get('line', 1),
                        rule_id=rule_id,
                        severity=severity.value,
                        message=message.get('message', ''),
                        tool=tool_name,
                        category='quality',
                        impact=self._severity_to_impact(severity),
                        likelihood='high',
                        remediation_effort='low'
                    ))
                    
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing ESLint JSON: {e}")
            
        return vulnerabilities
    
    def _parse_pylint_json(self, output: str, tool_name: str, tool_config: Dict, base_path: str) -> List[Vulnerability]:
        """Parsea salida JSON de Pylint"""
        vulnerabilities = []
        
        try:
            data = json.loads(output)
            
            for issue in data:
                rule_id = issue.get('message-id', issue.get('symbol', 'unknown'))
                type_name = issue.get('type', 'convention')
                
                severity = tool_config['severity_mapping'].get(type_name, LintSeverity.LOW)
                category = self._map_category(rule_id)
                
                vulnerabilities.append(Vulnerability(
                    file=issue.get('path', ''),
                    line=issue.get('line', 1),
                    rule_id=rule_id,
                    severity=severity.value,
                    message=issue.get('message', ''),
                    tool=tool_name,
                    category='quality',
                    impact=self._severity_to_impact(severity),
                    likelihood='high',
                    remediation_effort='medium'
                ))
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing Pylint JSON: {e}")
            
        return vulnerabilities
    
    def _parse_text_output(self, output: str, tool_name: str, tool_config: Dict, base_path: str) -> List[Vulnerability]:
        """Parsea salida de texto genérica"""
        vulnerabilities = []
        
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
                
            # Formato genérico básico
            vulnerability = Vulnerability(
                file=base_path,
                line=1,
                rule_id=f"{tool_name}-issue",
                severity=LintSeverity.LOW.value,
                message=line,
                tool=tool_name,
                category='quality',
                impact='low',
                likelihood='medium',
                remediation_effort='low'
            )
            
            vulnerabilities.append(vulnerability)
            
        return vulnerabilities
    
    def _map_severity(self, rule_id: str, tool_config: Dict) -> LintSeverity:
        """Mapea ID de regla a severidad"""
        severity_mapping = tool_config.get('severity_mapping', {})
        
        # Buscar por prefijo de regla (ej: E1 en E123)
        for prefix, severity in severity_mapping.items():
            if rule_id.startswith(str(prefix)):
                return severity
                
        return LintSeverity.LOW
    
    def _map_category(self, rule_id: str) -> LintCategory:
        """Mapea ID de regla a categoría"""
        for prefix, category in self.RULE_CATEGORY_MAPPING.items():
            if rule_id.startswith(prefix):
                return category
                
        return LintCategory.BEST_PRACTICE
    
    def _severity_to_impact(self, severity: LintSeverity) -> str:
        """Convierte severidad de linting a impact de vulnerabilidad"""
        mapping = {
            LintSeverity.INFO: 'low',
            LintSeverity.LOW: 'low',
            LintSeverity.MEDIUM: 'medium',
            LintSeverity.HIGH: 'high',
            LintSeverity.CRITICAL: 'critical'
        }
        return mapping.get(severity, 'low')
    
    def _is_tool_enabled(self, tool_name: str, language: str) -> bool:
        """Verifica si una herramienta está habilitada"""
        if not self.enabled_tools:
            return True  # Por defecto todas habilitadas
            
        lang_tools = self.enabled_tools.get(language, [])
        return tool_name in lang_tools or len(lang_tools) == 0
    
    def _is_tool_available(self, tool_name: str) -> bool:
        """Verifica si una herramienta está disponible en el sistema"""
        try:
            subprocess.run([tool_name, '--version'], 
                         capture_output=True, 
                         timeout=5)
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _calculate_metrics(self, vulnerabilities: List[Vulnerability], 
                         tools_executed: List[str], execution_time: float) -> LintingMetrics:
        """Calcula métricas de linting"""
        category_counts = {}
        auto_fixable = 0
        
        for vuln in vulnerabilities:
            # Contar por categoría (simplificado)
            if 'style' in vuln.message.lower():
                category_counts['style'] = category_counts.get('style', 0) + 1
            elif 'format' in vuln.message.lower():
                category_counts['format'] = category_counts.get('format', 0) + 1
            else:
                category_counts['best_practice'] = category_counts.get('best_practice', 0) + 1
        
        # Calcular score (100 - issues normalizados)
        total_issues = len(vulnerabilities)
        score = max(0, 100 - (total_issues * 2))  # 2 puntos por issue
        
        return LintingMetrics(
            total_lint_issues=total_issues,
            style_issues=category_counts.get('style', 0),
            format_issues=category_counts.get('format', 0),
            best_practice_issues=category_counts.get('best_practice', 0),
            performance_issues=category_counts.get('performance', 0),
            maintainability_issues=category_counts.get('maintainability', 0),
            auto_fixable_issues=auto_fixable,
            tools_executed=tools_executed,
            execution_time=execution_time,
            linting_score=score
        )
    
    def _create_empty_metrics(self) -> LintingMetrics:
        """Crea métricas vacías"""
        return LintingMetrics(
            total_lint_issues=0,
            style_issues=0,
            format_issues=0,
            best_practice_issues=0,
            performance_issues=0,
            maintainability_issues=0,
            auto_fixable_issues=0,
            tools_executed=[],
            execution_time=0.0,
            linting_score=100.0
        )


# Integración con SemBichoScanner
class SemBichoScannerWithLinting(SemBichoScanner):
    """Extensión del scanner principal con capacidades de linting"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(config)
        self.linting_engine = LintingEngine(
            config.get('linting', {}) if config else {}
        )
        
    def _run_quality_analysis(self, path: str) -> List[Vulnerability]:
        """
        Ejecuta análisis de calidad (linting) en el proyecto
        
        Args:
            path: Ruta del proyecto
            
        Returns:
            Lista de vulnerabilidades de calidad
        """
        quality_vulnerabilities = []
        
        # Detectar lenguajes en el proyecto
        languages = self._detect_project_languages(path)
        
        for language in languages:
            try:
                vulns, metrics = self.linting_engine.run_linting_analysis(path, language)
                quality_vulnerabilities.extend(vulns)
                
                self.logger.info(f"🔍 {language}: {len(vulns)} quality issues, score: {metrics.linting_score:.1f}")
                
            except Exception as e:
                self.logger.error(f"Error in quality analysis for {language}: {e}")
                
        return quality_vulnerabilities
    
    def _detect_project_languages(self, path: str) -> List[str]:
        """Detecta los lenguajes presentes en el proyecto"""
        languages = set()
        
        if os.path.isfile(path):
            ext = Path(path).suffix
            lang = self.SUPPORTED_LANGUAGES.get(ext)
            if lang:
                languages.add(lang)
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    ext = Path(file).suffix
                    lang = self.SUPPORTED_LANGUAGES.get(ext)
                    if lang:
                        languages.add(lang)
                        
        return list(languages)