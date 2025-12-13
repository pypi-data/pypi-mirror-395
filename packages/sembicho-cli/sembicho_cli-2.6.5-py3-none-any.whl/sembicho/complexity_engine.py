#!/usr/bin/env python3
"""
Complexity Analysis Engine for SemBicho
Analiza complejidad ciclomática, cognitiva y otras métricas de complejidad
"""

import os
import json
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ComplexityLevel(Enum):
    """Niveles de complejidad"""
    LOW = "low"           # 1-5: Simple
    MODERATE = "moderate" # 6-10: Aceptable
    HIGH = "high"         # 11-20: Complejo
    VERY_HIGH = "very_high" # 21-50: Muy complejo
    CRITICAL = "critical" # 50+: Crítico


@dataclass
class ComplexityMetric:
    """Métrica de complejidad para una función/método/clase"""
    name: str                    # Nombre de la función/método
    type: str                    # function, method, class
    file_path: str               # Ruta del archivo
    line_number: int             # Línea donde inicia
    cyclomatic_complexity: int   # Complejidad ciclomática
    cognitive_complexity: int    # Complejidad cognitiva (si disponible)
    lines_of_code: int          # Líneas de código
    parameters: int             # Número de parámetros
    nesting_depth: int          # Profundidad de anidamiento
    complexity_level: ComplexityLevel
    description: str            # Descripción del issue


@dataclass
class ComplexityAnalysisResult:
    """Resultado del análisis de complejidad"""
    total_functions: int
    average_complexity: float
    max_complexity: int
    high_complexity_count: int  # Funciones con complejidad > 10
    critical_complexity_count: int  # Funciones con complejidad > 20
    complexity_metrics: List[ComplexityMetric]
    complexity_score: float  # 0-100
    complexity_grade: str    # A+ a F
    tools_executed: List[str]


class ComplexityEngine:
    """
    Motor de análisis de complejidad multi-lenguaje
    """
    
    # Configuración de herramientas por lenguaje
    COMPLEXITY_TOOLS = {
        'python': ['radon'],
        'javascript': ['escomplex'],
        'typescript': ['escomplex'],
        'java': ['pmd', 'checkstyle'],
        'php': ['phpmd'],
        'ruby': ['flog'],
        'go': ['gocyclo'],
        'csharp': ['ndepend']
    }
    
    # Umbrales de complejidad
    THRESHOLDS = {
        'cyclomatic': {
            'function': {'low': 5, 'moderate': 10, 'high': 20, 'critical': 50},
            'class': {'low': 20, 'moderate': 50, 'high': 100, 'critical': 200}
        },
        'cognitive': {
            'function': {'low': 5, 'moderate': 15, 'high': 25, 'critical': 50}
        },
        'nesting': {
            'max_depth': 4
        }
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa el motor de complejidad
        
        Args:
            config: Configuración opcional
        """
        self.config = config or {}
        self.logger = logging.getLogger('sembicho.complexity')
        
        # Configuración de umbrales
        self.thresholds = self.config.get('thresholds', self.THRESHOLDS)
        
    def analyze_complexity(self, path: str, language: str) -> ComplexityAnalysisResult:
        """
        Analiza la complejidad del código
        
        Args:
            path: Ruta del archivo o directorio
            language: Lenguaje del código
            
        Returns:
            ComplexityAnalysisResult con métricas
        """
        self.logger.info(f"🔍 Analyzing complexity for: {path} ({language})")
        
        complexity_metrics = []
        tools_executed = []
        
        if language == 'python':
            complexity_metrics, tools = self._analyze_python_complexity(path)
            tools_executed.extend(tools)
        elif language in ['javascript', 'typescript']:
            complexity_metrics, tools = self._analyze_javascript_complexity(path, language == 'typescript')
            tools_executed.extend(tools)
        else:
            self.logger.warning(f"Complexity analysis not available for: {language}")
        
        # Calcular métricas agregadas
        result = self._calculate_aggregate_metrics(complexity_metrics, tools_executed)
        
        return result
    
    def _analyze_python_complexity(self, path: str) -> Tuple[List[ComplexityMetric], List[str]]:
        """Analiza complejidad de código Python usando radon"""
        metrics = []
        tools = []
        
        try:
            # Usar radon cc (cyclomatic complexity)
            result = self._run_radon_cc(path)
            if result:
                metrics.extend(result)
                tools.append('radon')
        except Exception as e:
            self.logger.warning(f"Radon not available: {e}")
        
        return metrics, tools
    
    def _analyze_javascript_complexity(self, path: str, is_typescript: bool) -> Tuple[List[ComplexityMetric], List[str]]:
        """Analiza complejidad de código JavaScript/TypeScript"""
        metrics = []
        tools = []
        
        try:
            # Usar escomplex o complexity-report
            result = self._run_escomplex(path, is_typescript)
            if result:
                metrics.extend(result)
                tools.append('escomplex')
        except Exception as e:
            self.logger.warning(f"ESComplex not available: {e}")
        
        return metrics, tools
    
    def _run_radon_cc(self, path: str) -> List[ComplexityMetric]:
        """
        Ejecuta radon cc para análisis de complejidad ciclomática
        
        Args:
            path: Ruta del archivo o directorio
            
        Returns:
            Lista de ComplexityMetric
        """
        try:
            cmd = ['radon', 'cc', path, '-j', '-s']  # JSON output, show complexity
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                self.logger.warning(f"Radon cc failed: {result.stderr}")
                return []
            
            # Parsear salida JSON
            metrics = self._parse_radon_output(result.stdout)
            return metrics
            
        except FileNotFoundError:
            self.logger.warning("Radon not installed. Install with: pip install radon")
            return []
        except subprocess.TimeoutExpired:
            self.logger.error("Radon timeout")
            return []
        except Exception as e:
            self.logger.error(f"Error running radon: {e}")
            return []
    
    def _parse_radon_output(self, output: str) -> List[ComplexityMetric]:
        """
        Parsea la salida JSON de radon
        
        Format:
        {
            "file.py": [
                {
                    "type": "function",
                    "name": "my_function",
                    "lineno": 10,
                    "col_offset": 0,
                    "endline": 20,
                    "complexity": 5,
                    "rank": "A"
                }
            ]
        }
        """
        metrics = []
        
        try:
            data = json.loads(output)
            
            for file_path, items in data.items():
                for item in items:
                    complexity = item.get('complexity', 0)
                    lines = item.get('endline', 0) - item.get('lineno', 0) + 1
                    
                    # Determinar nivel de complejidad
                    level = self._get_complexity_level(complexity, item.get('type', 'function'))
                    
                    metric = ComplexityMetric(
                        name=item.get('name', 'unknown'),
                        type=item.get('type', 'function'),
                        file_path=file_path,
                        line_number=item.get('lineno', 0),
                        cyclomatic_complexity=complexity,
                        cognitive_complexity=0,  # Radon no calcula cognitive
                        lines_of_code=lines,
                        parameters=0,  # No disponible en radon cc
                        nesting_depth=0,  # No disponible
                        complexity_level=level,
                        description=self._get_complexity_description(complexity, level)
                    )
                    
                    metrics.append(metric)
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing radon JSON: {e}")
        except Exception as e:
            self.logger.error(f"Error processing radon output: {e}")
        
        return metrics
    
    def _run_escomplex(self, path: str, is_typescript: bool) -> List[ComplexityMetric]:
        """
        Ejecuta escomplex para JavaScript/TypeScript
        
        Args:
            path: Ruta del archivo o directorio
            is_typescript: True si es TypeScript
            
        Returns:
            Lista de ComplexityMetric
        """
        try:
            # escomplex o complexity-report
            cmd = ['escomplex', path, '--format', 'json']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                self.logger.warning(f"ESComplex failed: {result.stderr}")
                return []
            
            metrics = self._parse_escomplex_output(result.stdout)
            return metrics
            
        except FileNotFoundError:
            self.logger.warning("ESComplex not installed. Install with: npm install -g escomplex")
            return []
        except subprocess.TimeoutExpired:
            self.logger.error("ESComplex timeout")
            return []
        except Exception as e:
            self.logger.error(f"Error running escomplex: {e}")
            return []
    
    def _parse_escomplex_output(self, output: str) -> List[ComplexityMetric]:
        """Parsea la salida JSON de escomplex"""
        metrics = []
        
        try:
            data = json.loads(output)
            
            # ESComplex format puede variar
            functions = data.get('functions', [])
            
            for func in functions:
                complexity = func.get('cyclomatic', 0)
                
                level = self._get_complexity_level(complexity, 'function')
                
                metric = ComplexityMetric(
                    name=func.get('name', 'anonymous'),
                    type='function',
                    file_path=data.get('path', 'unknown'),
                    line_number=func.get('line', 0),
                    cyclomatic_complexity=complexity,
                    cognitive_complexity=0,
                    lines_of_code=func.get('sloc', {}).get('logical', 0),
                    parameters=func.get('params', 0),
                    nesting_depth=0,
                    complexity_level=level,
                    description=self._get_complexity_description(complexity, level)
                )
                
                metrics.append(metric)
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing escomplex JSON: {e}")
        except Exception as e:
            self.logger.error(f"Error processing escomplex output: {e}")
        
        return metrics
    
    def _get_complexity_level(self, complexity: int, item_type: str) -> ComplexityLevel:
        """Determina el nivel de complejidad"""
        thresholds = self.thresholds['cyclomatic'].get(item_type, self.thresholds['cyclomatic']['function'])
        
        if complexity <= thresholds['low']:
            return ComplexityLevel.LOW
        elif complexity <= thresholds['moderate']:
            return ComplexityLevel.MODERATE
        elif complexity <= thresholds['high']:
            return ComplexityLevel.HIGH
        elif complexity <= thresholds['critical']:
            return ComplexityLevel.VERY_HIGH
        else:
            return ComplexityLevel.CRITICAL
    
    def _get_complexity_description(self, complexity: int, level: ComplexityLevel) -> str:
        """Genera descripción del issue de complejidad"""
        descriptions = {
            ComplexityLevel.LOW: f"Complejidad baja ({complexity}). Código simple y fácil de mantener.",
            ComplexityLevel.MODERATE: f"Complejidad moderada ({complexity}). Código aceptable.",
            ComplexityLevel.HIGH: f"Complejidad alta ({complexity}). Considere refactorizar.",
            ComplexityLevel.VERY_HIGH: f"Complejidad muy alta ({complexity}). Refactorización recomendada.",
            ComplexityLevel.CRITICAL: f"Complejidad crítica ({complexity}). Refactorización urgente."
        }
        return descriptions.get(level, f"Complejidad: {complexity}")
    
    def _calculate_aggregate_metrics(self, metrics: List[ComplexityMetric], 
                                     tools_executed: List[str]) -> ComplexityAnalysisResult:
        """
        Calcula métricas agregadas del análisis
        
        Args:
            metrics: Lista de métricas individuales
            tools_executed: Herramientas ejecutadas
            
        Returns:
            ComplexityAnalysisResult con métricas agregadas
        """
        if not metrics:
            return ComplexityAnalysisResult(
                total_functions=0,
                average_complexity=0.0,
                max_complexity=0,
                high_complexity_count=0,
                critical_complexity_count=0,
                complexity_metrics=[],
                complexity_score=100.0,
                complexity_grade='A+',
                tools_executed=tools_executed
            )
        
        # Calcular estadísticas
        total = len(metrics)
        complexities = [m.cyclomatic_complexity for m in metrics]
        avg_complexity = sum(complexities) / total if total > 0 else 0
        max_complexity = max(complexities) if complexities else 0
        
        # Contar funciones problemáticas
        high_count = sum(1 for m in metrics if m.cyclomatic_complexity > 10)
        critical_count = sum(1 for m in metrics if m.cyclomatic_complexity > 20)
        
        # Calcular score (100 - penalizaciones)
        score = 100.0
        score -= (avg_complexity - 5) * 2  # -2 puntos por cada unidad sobre 5
        score -= high_count * 3  # -3 puntos por función compleja
        score -= critical_count * 10  # -10 puntos por función crítica
        score = max(0, min(100, score))
        
        grade = self._score_to_grade(score)
        
        return ComplexityAnalysisResult(
            total_functions=total,
            average_complexity=round(avg_complexity, 2),
            max_complexity=max_complexity,
            high_complexity_count=high_count,
            critical_complexity_count=critical_count,
            complexity_metrics=metrics,
            complexity_score=round(score, 1),
            complexity_grade=grade,
            tools_executed=tools_executed
        )
    
    def _score_to_grade(self, score: float) -> str:
        """Convierte score a grado"""
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
