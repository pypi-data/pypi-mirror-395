#!/usr/bin/env python3
"""
Python Linting Implementation for SemBicho
Integración específica de flake8, black, y pylint
"""

import os
import json
import subprocess
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from .scanner import Vulnerability
from .linting_engine import LintingEngine, LintSeverity, LintCategory, LintingMetrics


class PythonLintingEngine:
    """Motor especializado para linting de Python"""
    
    # Mapeo detallado de reglas flake8 a categorías
    FLAKE8_RULE_MAPPING = {
        # Errores de indentación
        'E101': {'category': LintCategory.FORMAT, 'severity': LintSeverity.MEDIUM, 'name': 'indentation contains mixed spaces and tabs'},
        'E111': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'indentation is not a multiple of four'},
        'E112': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'expected an indented block'},
        'E113': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'unexpected indentation'},
        'E114': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'indentation is not a multiple of four (comment)'},
        'E115': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'expected an indented block (comment)'},
        'E116': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'unexpected indentation (comment)'},
        'E117': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'over-indented'},
        'E121': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'continuation line under-indented for hanging indent'},
        'E122': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'continuation line missing indentation or outdented'},
        'E123': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'closing bracket does not match indentation of opening bracket'},
        'E124': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'closing bracket does not match visual indentation'},
        'E125': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'continuation line with same indent as next logical line'},
        'E126': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'continuation line over-indented for hanging indent'},
        'E127': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'continuation line over-indented for visual indent'},
        'E128': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'continuation line under-indented for visual indent'},
        'E129': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'visually indented line with same indent as next logical line'},
        'E131': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'continuation line unaligned for hanging indent'},
        'E133': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'closing bracket is missing indentation'},
        
        # Errores de espacios en blanco
        'E201': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'whitespace after opening bracket'},
        'E202': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'whitespace before closing bracket'},
        'E203': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'whitespace before colon'},
        'E204': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'whitespace after colon'},
        'E211': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'whitespace before opening bracket'},
        'E221': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'multiple spaces before operator'},
        'E222': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'multiple spaces after operator'},
        'E223': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'tab before operator'},
        'E224': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'tab after operator'},
        'E225': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'missing whitespace around operator'},
        'E226': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'missing whitespace around arithmetic operator'},
        'E227': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'missing whitespace around bitwise or shift operator'},
        'E228': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'missing whitespace around modulo operator'},
        'E231': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'missing whitespace after comma'},
        'E241': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'multiple spaces after comma'},
        'E242': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'tab after comma'},
        'E251': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'unexpected spaces around keyword / parameter equals'},
        'E261': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'at least two spaces before inline comment'},
        'E262': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'inline comment should start with #'},
        'E265': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'block comment should start with #'},
        'E266': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'too many leading # for block comment'},
        'E271': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'multiple spaces after keyword'},
        'E272': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'multiple spaces before keyword'},
        'E273': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'tab after keyword'},
        'E274': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'tab before keyword'},
        'E275': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'missing whitespace after keyword'},
        
        # Errores de líneas en blanco
        'E301': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'expected 1 blank line, found 0'},
        'E302': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'expected 2 blank lines, found 0'},
        'E303': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'too many blank lines'},
        'E304': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'blank lines found after function decorator'},
        'E305': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'expected 2 blank lines after class or function definition'},
        'E306': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'expected 1 blank line before a nested definition'},
        
        # Errores de importaciones
        'E401': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'multiple imports on one line'},
        'E402': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'module level import not at top of file'},
        
        # Errores de longitud de línea
        'E501': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'line too long'},
        'E502': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'the backslash is redundant between brackets'},
        
        # Errores de sintaxis
        'E701': {'category': LintCategory.STYLE, 'severity': LintSeverity.MEDIUM, 'name': 'multiple statements on one line (colon)'},
        'E702': {'category': LintCategory.STYLE, 'severity': LintSeverity.MEDIUM, 'name': 'multiple statements on one line (semicolon)'},
        'E703': {'category': LintCategory.STYLE, 'severity': LintSeverity.MEDIUM, 'name': 'statement ends with a semicolon'},
        'E704': {'category': LintCategory.STYLE, 'severity': LintSeverity.MEDIUM, 'name': 'multiple statements on one line (def)'},
        'E711': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'comparison to None should be done with is and is not'},
        'E712': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'comparison to True should be done with is and is not'},
        'E713': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'test for membership should be not in'},
        'E714': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'test for object identity should be is not'},
        'E721': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'do not compare types, use isinstance()'},
        'E722': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'do not use bare except'},
        'E731': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'do not assign a lambda expression, use a def'},
        'E741': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'ambiguous variable name'},
        'E742': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'ambiguous class definition'},
        'E743': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'ambiguous function definition'},
        
        # Warnings
        'W191': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'indentation contains tabs'},
        'W291': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'trailing whitespace'},
        'W292': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'no newline at end of file'},
        'W293': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'blank line contains whitespace'},
        'W391': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'blank line at end of file'},
        'W503': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'line break before binary operator'},
        'W504': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'line break after binary operator'},
        'W601': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'deprecated feature'},
        'W602': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'deprecated form of raising exception'},
        'W603': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'deprecated use of <> operator'},
        'W604': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'deprecated use of backticks'},
        'W605': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'invalid escape sequence'},
        'W606': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'deprecated feature'},
        
        # Errores de flake8 (análisis estático)
        'F401': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'imported but unused'},
        'F402': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'import shadowed by loop var'},
        'F403': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'import * used; unable to detect undefined names'},
        'F404': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'future import(s) not at beginning of file'},
        'F405': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'name may be undefined, or defined from star imports'},
        'F811': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'redefinition of unused name'},
        'F812': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'list comprehension redefines name'},
        'F821': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'undefined name'},
        'F822': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'undefined name in __all__'},
        'F823': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'local variable referenced before assignment'},
        'F831': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'duplicate argument name'},
        'F841': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'local variable is assigned to but never used'},
        'F901': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'raise NotImplemented should be raise NotImplementedError'},
        
        # Complejidad ciclomática (mccabe)
        'C901': {'category': LintCategory.MAINTAINABILITY, 'severity': LintSeverity.MEDIUM, 'name': 'function is too complex'},
    }
    
    # Mapeo de severidades de Pylint
    PYLINT_SEVERITY_MAPPING = {
        'convention': LintSeverity.LOW,
        'refactor': LintSeverity.MEDIUM,
        'warning': LintSeverity.MEDIUM,
        'error': LintSeverity.HIGH,
        'fatal': LintSeverity.CRITICAL
    }
    
    # Categorías de reglas de Pylint
    PYLINT_CATEGORY_MAPPING = {
        'C': LintCategory.STYLE,              # Convention
        'R': LintCategory.MAINTAINABILITY,    # Refactor
        'W': LintCategory.BEST_PRACTICE,      # Warning
        'E': LintCategory.BEST_PRACTICE,      # Error
        'F': LintCategory.BEST_PRACTICE,      # Fatal
        'I': LintCategory.BEST_PRACTICE,      # Information
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """Inicializa el motor de linting para Python"""
        self.config = config or {}
        self.flake8_config = self.config.get('flake8', {})
        self.black_config = self.config.get('black', {})
        self.pylint_config = self.config.get('pylint', {})
        
    def run_flake8(self, path: str) -> List[Vulnerability]:
        """
        Ejecuta flake8 en el path especificado
        
        Args:
            path: Ruta del archivo o directorio
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        # Construir comando flake8
        cmd = ['flake8']
        
        # Configuraciones desde sembicho-quality.yml
        max_line_length = self.flake8_config.get('max_line_length', 88)
        ignore_rules = self.flake8_config.get('ignore', [])
        
        cmd.extend(['--max-line-length', str(max_line_length)])
        if ignore_rules:
            cmd.extend(['--ignore', ','.join(ignore_rules)])
        
        cmd.append(path)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # flake8 retorna código 1 si encuentra issues
            if result.returncode not in [0, 1]:
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
            
            vulnerabilities = self._parse_flake8_output(result.stdout, path)
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("flake8 execution timed out")
        except FileNotFoundError:
            raise RuntimeError("flake8 not found. Install with: pip install flake8")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"flake8 failed: {e.stderr}")
            
        return vulnerabilities
    
    def run_black(self, path: str, check_only: bool = True) -> List[Vulnerability]:
        """
        Ejecuta black para verificar formato
        
        Args:
            path: Ruta del archivo o directorio
            check_only: Si True, solo verifica sin modificar
            
        Returns:
            Lista de vulnerabilidades de formato
        """
        vulnerabilities = []
        
        # Construir comando black
        cmd = ['black']
        
        if check_only:
            cmd.append('--check')
            cmd.append('--diff')
        
        # Configuraciones
        line_length = self.black_config.get('line_length', 88)
        target_version = self.black_config.get('target_version', ['py38'])
        
        cmd.extend(['--line-length', str(line_length)])
        for version in target_version:
            cmd.extend(['--target-version', version])
        
        cmd.append(path)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # black retorna código 1 si encontró archivos que necesitan formato
            if result.returncode == 1:
                vulnerabilities = self._parse_black_output(result.stdout, path)
            elif result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("black execution timed out")
        except FileNotFoundError:
            raise RuntimeError("black not found. Install with: pip install black")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"black failed: {e.stderr}")
            
        return vulnerabilities
    
    def run_pylint(self, path: str) -> List[Vulnerability]:
        """
        Ejecuta pylint en el path especificado
        
        Args:
            path: Ruta del archivo o directorio
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        # Construir comando pylint
        cmd = ['pylint', '--output-format=json']
        
        # Configuraciones
        disable_rules = self.pylint_config.get('disable', [])
        if disable_rules:
            cmd.extend(['--disable', ','.join(disable_rules)])
        
        cmd.append(path)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # pylint puede ser lento
            )
            
            # pylint puede retornar códigos diferentes según los issues encontrados
            # No es crítico el código de salida, parseamos la salida JSON
            
            if result.stdout.strip():
                vulnerabilities = self._parse_pylint_output(result.stdout, path)
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("pylint execution timed out")
        except FileNotFoundError:
            raise RuntimeError("pylint not found. Install with: pip install pylint")
        except Exception as e:
            raise RuntimeError(f"pylint failed: {str(e)}")
            
        return vulnerabilities
    
    def _parse_flake8_output(self, output: str, base_path: str) -> List[Vulnerability]:
        """Parsea la salida de flake8"""
        vulnerabilities = []
        
        for line in output.strip().split('\n'):
            if not line.strip():
                continue
                
            # Formato: ./file.py:line:col: code message
            match = re.match(r'^(.+):(\d+):(\d+):\s+([A-Z]\d+)\s+(.+)$', line)
            if not match:
                continue
                
            file_path, line_num, col_num, rule_id, message = match.groups()
            
            # Obtener información de la regla
            rule_info = self.FLAKE8_RULE_MAPPING.get(rule_id, {
                'category': LintCategory.BEST_PRACTICE,
                'severity': LintSeverity.LOW,
                'name': 'unknown rule'
            })
            
            vulnerability = Vulnerability(
                file=file_path,
                line=int(line_num),
                rule_id=rule_id,
                severity=rule_info['severity'].value,
                message=f"{rule_info['name']}: {message}",
                tool='flake8',
                category='quality',
                impact=self._severity_to_impact(rule_info['severity']),
                likelihood='high',
                remediation_effort='low' if rule_info['category'] == LintCategory.FORMAT else 'medium'
            )
            
            vulnerabilities.append(vulnerability)
            
        return vulnerabilities
    
    def _parse_black_output(self, output: str, base_path: str) -> List[Vulnerability]:
        """Parsea la salida de black --diff"""
        vulnerabilities = []
        
        # Buscar archivos que necesitan reformateo
        lines = output.split('\n')
        current_file = None
        
        for line in lines:
            if line.startswith('--- '):
                # Extraer nombre del archivo
                # Formato: --- a/path/to/file.py
                parts = line.split('\t')[0].split(' ', 1)
                if len(parts) > 1:
                    current_file = parts[1].replace('a/', '')
                    
            elif line.startswith('would reformat') and current_file:
                # Crear vulnerabilidad para archivo que necesita formato
                vulnerability = Vulnerability(
                    file=current_file,
                    line=1,
                    rule_id='BLACK_FORMAT',
                    severity=LintSeverity.LOW.value,
                    message=f"File needs reformatting according to Black style",
                    tool='black',
                    category='quality',
                    impact='low',
                    likelihood='high',
                    remediation_effort='low'
                )
                
                vulnerabilities.append(vulnerability)
                current_file = None
        
        # Si no hay mensajes específicos pero hay salida, es que hay archivos para reformatear
        if not vulnerabilities and output.strip() and 'would reformat' in output:
            # Crear vulnerabilidad genérica
            vulnerability = Vulnerability(
                file=base_path,
                line=1,
                rule_id='BLACK_FORMAT',
                severity=LintSeverity.LOW.value,
                message="Files need reformatting according to Black style",
                tool='black',
                category='quality',
                impact='low',
                likelihood='high',
                remediation_effort='low'
            )
            vulnerabilities.append(vulnerability)
            
        return vulnerabilities
    
    def _parse_pylint_output(self, output: str, base_path: str) -> List[Vulnerability]:
        """Parsea la salida JSON de pylint"""
        vulnerabilities = []
        
        try:
            data = json.loads(output)
            
            for item in data:
                rule_id = item.get('message-id', item.get('symbol', 'unknown'))
                msg_type = item.get('type', 'convention')
                
                # Mapear severidad
                severity = self.PYLINT_SEVERITY_MAPPING.get(msg_type, LintSeverity.LOW)
                
                # Mapear categoría por prefijo del tipo
                category = LintCategory.BEST_PRACTICE
                if msg_type:
                    category = self.PYLINT_CATEGORY_MAPPING.get(msg_type[0].upper(), LintCategory.BEST_PRACTICE)
                
                vulnerability = Vulnerability(
                    file=item.get('path', base_path),
                    line=item.get('line', 1),
                    rule_id=rule_id,
                    severity=severity.value,
                    message=item.get('message', ''),
                    tool='pylint',
                    category='quality',
                    impact=self._severity_to_impact(severity),
                    likelihood='high',
                    remediation_effort='medium' if severity in [LintSeverity.HIGH, LintSeverity.CRITICAL] else 'low'
                )
                
                vulnerabilities.append(vulnerability)
                
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse pylint JSON output: {e}")
            
        return vulnerabilities
    
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
    
    def run_full_analysis(self, path: str) -> Tuple[List[Vulnerability], Dict[str, any]]:
        """
        Ejecuta análisis completo de Python (flake8 + black + pylint)
        
        Args:
            path: Ruta del archivo o directorio
            
        Returns:
            Tuple con vulnerabilidades y métricas
        """
        start_time = time.time()
        all_vulnerabilities = []
        tools_executed = []
        tool_results = {}
        
        # Ejecutar flake8
        try:
            flake8_vulns = self.run_flake8(path)
            all_vulnerabilities.extend(flake8_vulns)
            tools_executed.append('flake8')
            tool_results['flake8'] = {
                'issues': len(flake8_vulns),
                'categories': self._categorize_issues(flake8_vulns)
            }
        except Exception as e:
            tool_results['flake8'] = {'error': str(e)}
        
        # Ejecutar black
        try:
            black_vulns = self.run_black(path)
            all_vulnerabilities.extend(black_vulns)
            tools_executed.append('black')
            tool_results['black'] = {
                'issues': len(black_vulns),
                'files_need_formatting': len(black_vulns)
            }
        except Exception as e:
            tool_results['black'] = {'error': str(e)}
        
        # Ejecutar pylint
        try:
            pylint_vulns = self.run_pylint(path)
            all_vulnerabilities.extend(pylint_vulns)
            tools_executed.append('pylint')
            tool_results['pylint'] = {
                'issues': len(pylint_vulns),
                'categories': self._categorize_issues(pylint_vulns)
            }
        except Exception as e:
            tool_results['pylint'] = {'error': str(e)}
        
        execution_time = time.time() - start_time
        
        # Calcular métricas
        metrics = self._calculate_python_metrics(all_vulnerabilities, tools_executed, execution_time)
        
        return all_vulnerabilities, {
            'metrics': metrics,
            'tool_results': tool_results,
            'execution_time': execution_time
        }
    
    def _categorize_issues(self, vulnerabilities: List[Vulnerability]) -> Dict[str, int]:
        """Categoriza issues por tipo"""
        categories = {
            'style': 0,
            'format': 0,
            'best_practice': 0,
            'maintainability': 0,
            'performance': 0
        }
        
        for vuln in vulnerabilities:
            # Categorización simplificada basada en mensaje y tool
            message_lower = vuln.message.lower()
            
            if vuln.tool == 'black' or 'format' in message_lower or 'indentation' in message_lower:
                categories['format'] += 1
            elif 'style' in message_lower or 'naming' in message_lower:
                categories['style'] += 1
            elif 'complex' in message_lower or vuln.rule_id == 'C901':
                categories['maintainability'] += 1
            elif 'performance' in message_lower:
                categories['performance'] += 1
            else:
                categories['best_practice'] += 1
                
        return categories
    
    def _calculate_python_metrics(self, vulnerabilities: List[Vulnerability], 
                                tools_executed: List[str], execution_time: float) -> Dict[str, any]:
        """Calcula métricas específicas para Python"""
        
        total_issues = len(vulnerabilities)
        categories = self._categorize_issues(vulnerabilities)
        
        # Calcular score (penalizar más los issues de maintainability y best_practice)
        score = 100.0
        score -= categories['format'] * 0.5        # Formato es menos crítico
        score -= categories['style'] * 1.0         # Estilo es moderado
        score -= categories['best_practice'] * 2.0 # Best practices son importantes
        score -= categories['maintainability'] * 3.0  # Mantenibilidad es crítica
        score -= categories['performance'] * 2.5   # Performance es importante
        
        score = max(0.0, score)
        
        return {
            'total_issues': total_issues,
            'categories': categories,
            'tools_executed': tools_executed,
            'execution_time': execution_time,
            'quality_score': round(score, 1),
            'grade': self._score_to_grade(score),
            'auto_fixable': categories['format']  # Formato es generalmente auto-fixable
        }
    
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