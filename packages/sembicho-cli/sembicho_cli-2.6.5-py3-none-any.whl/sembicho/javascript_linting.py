#!/usr/bin/env python3
"""
JavaScript/TypeScript Linting Implementation for SemBicho
Integración de ESLint, Prettier, y TSLint
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


class JavaScriptLintingEngine:
    """Motor especializado para linting de JavaScript/TypeScript"""
    
    # Mapeo de reglas ESLint populares
    ESLINT_RULE_MAPPING = {
        # Posibles errores
        'no-cond-assign': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow assignment in conditional expressions'},
        'no-console': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow use of console'},
        'no-constant-condition': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow use of constant expressions in conditions'},
        'no-control-regex': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow control characters in regular expressions'},
        'no-debugger': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow use of debugger'},
        'no-dupe-args': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow duplicate arguments in functions'},
        'no-dupe-keys': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow duplicate keys when creating object literals'},
        'no-duplicate-case': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow a duplicate case label'},
        'no-empty': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow empty statements'},
        'no-empty-character-class': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow the use of empty character classes in regular expressions'},
        'no-ex-assign': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow assigning to the exception in a catch block'},
        'no-extra-boolean-cast': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow double-negation boolean casts'},
        'no-extra-parens': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow unnecessary parentheses'},
        'no-extra-semi': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow unnecessary semicolons'},
        'no-func-assign': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow overwriting functions written as function declarations'},
        'no-inner-declarations': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow function or variable declarations in nested blocks'},
        'no-invalid-regexp': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow invalid regular expression strings in the RegExp constructor'},
        'no-irregular-whitespace': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'disallow irregular whitespace'},
        'no-obj-calls': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow the use of object properties of the global object'},
        'no-regex-spaces': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow multiple spaces in a regular expression literal'},
        'no-sparse-arrays': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow sparse arrays'},
        'no-unreachable': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow unreachable statements after a return, throw, continue, or break statement'},
        'use-isnan': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow comparisons with the value NaN'},
        'valid-typeof': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'ensure that the results of typeof are compared against a valid string'},
        
        # Mejores prácticas
        'accessor-pairs': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'enforces getter/setter pairs in objects'},
        'block-scoped-var': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'treat var statements as if they were block scoped'},
        'complexity': {'category': LintCategory.MAINTAINABILITY, 'severity': LintSeverity.MEDIUM, 'name': 'specify the maximum cyclomatic complexity allowed in a program'},
        'consistent-return': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'require return statements to either always or never specify values'},
        'curly': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'specify curly brace conventions for all control statements'},
        'default-case': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'require default case in switch statements'},
        'dot-notation': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'encourages use of dot notation whenever possible'},
        'eqeqeq': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'require the use of === and !=='},
        'guard-for-in': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'make sure for-in loops have an if statement'},
        'no-alert': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow the use of alert, confirm, and prompt'},
        'no-caller': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow use of arguments.caller or arguments.callee'},
        'no-div-regex': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow division operators explicitly at beginning of regular expression'},
        'no-else-return': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow else after a return in an if'},
        'no-eval': {'category': LintCategory.SECURITY, 'severity': LintSeverity.CRITICAL, 'name': 'disallow use of eval()'},
        'no-extend-native': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow adding to native types'},
        'no-extra-bind': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow unnecessary function binding'},
        'no-fallthrough': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow fallthrough of case statements'},
        'no-floating-decimal': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow the use of leading or trailing decimal points in numeric literals'},
        'no-implied-eval': {'category': LintCategory.SECURITY, 'severity': LintSeverity.CRITICAL, 'name': 'disallow use of eval()-like methods'},
        'no-iterator': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow usage of __iterator__ property'},
        'no-labels': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow use of labeled statements'},
        'no-lone-blocks': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow unnecessary nested blocks'},
        'no-loop-func': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow creation of functions within loops'},
        'no-multi-spaces': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'disallow use of multiple spaces'},
        'no-multi-str': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow use of multiline strings'},
        'no-native-reassign': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow reassignments of native objects'},
        'no-new': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow use of new operator when not part of the assignment or comparison'},
        'no-new-func': {'category': LintCategory.SECURITY, 'severity': LintSeverity.HIGH, 'name': 'disallow use of new operator for Function object'},
        'no-new-wrappers': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallows creating new instances of String, Number, and Boolean'},
        'no-octal': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow use of octal literals'},
        'no-octal-escape': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow use of octal escape sequences in string literals'},
        'no-param-reassign': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow reassignment of function parameters'},
        'no-proto': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow usage of __proto__ property'},
        'no-redeclare': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow declaring the same variable more then once'},
        'no-return-assign': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow use of assignment in return statement'},
        'no-script-url': {'category': LintCategory.SECURITY, 'severity': LintSeverity.HIGH, 'name': 'disallow use of javascript: urls'},
        'no-self-compare': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow comparisons where both sides are exactly the same'},
        'no-sequences': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow use of comma operator'},
        'no-throw-literal': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'restrict what can be thrown as an exception'},
        'no-unused-expressions': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow usage of expressions in statement position'},
        'no-void': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow use of void operator'},
        'no-warning-comments': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow usage of configurable warning terms in comments'},
        'no-with': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow use of the with statement'},
        'radix': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'require use of the second argument for parseInt()'},
        'vars-on-top': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'requires to declare all vars on top of their containing scope'},
        'wrap-iife': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require immediate function invocation to be wrapped in parentheses'},
        'yoda': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require or disallow Yoda conditions'},
        
        # Variables
        'no-catch-shadow': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow the catch clause parameter name being the same as a variable in the outer scope'},
        'no-delete-var': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow deletion of variables'},
        'no-label-var': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow labels that share a name with a variable'},
        'no-shadow': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow declaration of variables already declared in the outer scope'},
        'no-shadow-restricted-names': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow shadowing of names such as arguments'},
        'no-undef': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow use of undeclared variables'},
        'no-undef-init': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow use of undefined when initializing variables'},
        'no-undefined': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow use of undefined variable'},
        'no-unused-vars': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow declaration of variables that are not used in the code'},
        'no-use-before-define': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow use of variables before they are defined'},
        
        # Estilo
        'array-bracket-spacing': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'enforce spacing inside array brackets'},
        'brace-style': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'enforce one true brace style'},
        'camelcase': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require camel case names'},
        'comma-dangle': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow or enforce trailing commas'},
        'comma-spacing': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'enforce spacing before and after comma'},
        'comma-style': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'enforce one true comma style'},
        'computed-property-spacing': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'require or disallow padding inside computed properties'},
        'consistent-this': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'enforces consistent naming when capturing the current execution context'},
        'eol-last': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'enforce newline at the end of file'},
        'func-names': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require function expressions to have a name'},
        'func-style': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'enforces use of function declarations or expressions'},
        'indent': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'enforce consistent indentation'},
        'key-spacing': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'enforces spacing between keys and values in object literal properties'},
        'lines-around-comment': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'enforce empty lines around comments'},
        'linebreak-style': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'disallow mixed LF and CRLF as linebreaks'},
        'max-nested-callbacks': {'category': LintCategory.MAINTAINABILITY, 'severity': LintSeverity.MEDIUM, 'name': 'specify the maximum depth callbacks can be nested'},
        'new-cap': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require a capital letter for constructors'},
        'new-parens': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow the omission of parentheses when invoking a constructor'},
        'newline-after-var': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'allow/disallow an empty newline after var statement'},
        'no-array-constructor': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow use of the Array constructor'},
        'no-continue': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow use of the continue statement'},
        'no-inline-comments': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow comments inline after code'},
        'no-lonely-if': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow if as the only statement in an else block'},
        'no-mixed-spaces-and-tabs': {'category': LintCategory.FORMAT, 'severity': LintSeverity.MEDIUM, 'name': 'disallow mixed spaces and tabs for indentation'},
        'no-multiple-empty-lines': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'disallow multiple empty lines'},
        'no-nested-ternary': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow nested ternary expressions'},
        'no-new-object': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'disallow use of the Object constructor'},
        'no-spaced-func': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'disallow space between function identifier and application'},
        'no-ternary': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow the use of ternary operators'},
        'no-trailing-spaces': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'disallow trailing whitespace at the end of lines'},
        'no-underscore-dangle': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'disallow dangling underscores in identifiers'},
        'one-var': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'allow just one var statement per function'},
        'operator-assignment': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require assignment operator shorthand where possible'},
        'operator-linebreak': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'enforce operators to be placed before or after line breaks'},
        'padded-blocks': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'enforce padding within blocks'},
        'quote-props': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require quotes around object literal property names'},
        'quotes': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'specify whether double or single quotes should be used'},
        'semi': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require or disallow use of semicolons instead of ASI'},
        'semi-spacing': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'enforce spacing before and after semicolons'},
        'sort-vars': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'sort variables within the same declaration block'},
        'space-after-keywords': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'require a space after certain keywords'},
        'space-before-blocks': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'require or disallow space before blocks'},
        'space-before-function-paren': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'require or disallow space before function opening parenthesis'},
        'space-in-parens': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'require or disallow spaces inside parentheses'},
        'space-infix-ops': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'require spaces around operators'},
        'space-return-throw-case': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'require a space after return, throw, and case'},
        'space-unary-ops': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'require or disallow spaces before/after unary operators'},
        'spaced-comment': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require or disallow a space immediately following the // or /* in a comment'},
        'wrap-regex': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require regex literals to be wrapped in parentheses'},
        
        # ES6
        'arrow-parens': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require parens in arrow function arguments'},
        'arrow-spacing': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'require space before/after arrow function arrow'},
        'constructor-super': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'verify super() callings in constructors'},
        'generator-star-spacing': {'category': LintCategory.FORMAT, 'severity': LintSeverity.LOW, 'name': 'enforce the spacing around the * in generator functions'},
        'no-class-assign': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow modifying variables of class declarations'},
        'no-const-assign': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow modifying variables that are declared using const'},
        'no-this-before-super': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.HIGH, 'name': 'disallow to use this/super before super() calling in constructors'},
        'no-var': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'require let or const instead of var'},
        'object-shorthand': {'category': LintCategory.STYLE, 'severity': LintSeverity.LOW, 'name': 'require method and property shorthand syntax for object literals'},
        'prefer-const': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'suggest using const declaration for variables that are never modified'},
        'prefer-spread': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'suggest using the spread operator instead of .apply()'},
        'prefer-template': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.LOW, 'name': 'suggest using template literals instead of string concatenation'},
        'require-yield': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'disallow generator functions that do not have yield'},
        
        # React
        'react/jsx-uses-react': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'prevent React to be incorrectly marked as unused'},
        'react/jsx-uses-vars': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'prevent variables used in JSX to be incorrectly marked as unused'},
        'react/no-unknown-property': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'prevent usage of unknown DOM property'},
        'react/prop-types': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'prevent missing props validation in a React component definition'},
        'react/react-in-jsx-scope': {'category': LintCategory.BEST_PRACTICE, 'severity': LintSeverity.MEDIUM, 'name': 'prevent missing React when using JSX'},
    }
    
    # Mapeo de severidad de ESLint (0, 1, 2)
    ESLINT_SEVERITY_MAPPING = {
        0: LintSeverity.INFO,
        1: LintSeverity.LOW,
        2: LintSeverity.MEDIUM
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """Inicializa el motor de linting para JavaScript/TypeScript"""
        self.config = config or {}
        self.eslint_config = self.config.get('eslint', {})
        self.prettier_config = self.config.get('prettier', {})
        self.tslint_config = self.config.get('tslint', {})
        
    def run_eslint(self, path: str, is_typescript: bool = False) -> List[Vulnerability]:
        """
        Ejecuta ESLint en el path especificado
        
        Args:
            path: Ruta del archivo o directorio
            is_typescript: Si True, incluye extensiones TypeScript
            
        Returns:
            Lista de vulnerabilidades encontradas
        """
        vulnerabilities = []
        
        # Construir comando ESLint
        cmd = ['eslint', '--format=json']
        
        # Configuraciones
        if is_typescript:
            extensions = self.eslint_config.get('typescript_extensions', ['.ts', '.tsx'])
            cmd.extend(['--ext', ','.join(extensions)])
        else:
            extensions = self.eslint_config.get('extensions', ['.js', '.jsx'])
            cmd.extend(['--ext', ','.join(extensions)])
        
        # Config file (si existe)
        config_file = self.eslint_config.get('config_file')
        if config_file and os.path.exists(config_file):
            cmd.extend(['--config', config_file])
        
        cmd.append(path)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # ESLint retorna código 1 si encuentra issues
            if result.returncode not in [0, 1]:
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
            
            if result.stdout.strip():
                vulnerabilities = self._parse_eslint_output(result.stdout, path)
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("ESLint execution timed out")
        except FileNotFoundError:
            raise RuntimeError("ESLint not found. Install with: npm install -g eslint")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ESLint failed: {e.stderr}")
            
        return vulnerabilities
    
    def run_prettier(self, path: str, check_only: bool = True) -> List[Vulnerability]:
        """
        Ejecuta Prettier para verificar formato
        
        Args:
            path: Ruta del archivo o directorio
            check_only: Si True, solo verifica sin modificar
            
        Returns:
            Lista de vulnerabilidades de formato
        """
        vulnerabilities = []
        
        # Construir comando Prettier
        cmd = ['prettier']
        
        if check_only:
            cmd.append('--check')
        
        # Configuraciones
        if self.prettier_config.get('semi', True):
            cmd.append('--semi')
        else:
            cmd.append('--no-semi')
            
        if self.prettier_config.get('singleQuote', True):
            cmd.append('--single-quote')
            
        tab_width = self.prettier_config.get('tabWidth', 2)
        cmd.extend(['--tab-width', str(tab_width)])
        
        # Pattern para archivos
        cmd.append(f"{path}/**/*.{{js,jsx,ts,tsx}}" if os.path.isdir(path) else path)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                shell=True  # Necesario para glob patterns
            )
            
            # Prettier retorna código != 0 si encuentra archivos sin formato correcto
            if result.returncode != 0:
                vulnerabilities = self._parse_prettier_output(result.stderr, path)
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Prettier execution timed out")
        except FileNotFoundError:
            raise RuntimeError("Prettier not found. Install with: npm install -g prettier")
        except Exception as e:
            raise RuntimeError(f"Prettier failed: {str(e)}")
            
        return vulnerabilities
    
    def _parse_eslint_output(self, output: str, base_path: str) -> List[Vulnerability]:
        """Parsea la salida JSON de ESLint"""
        vulnerabilities = []
        
        try:
            data = json.loads(output)
            
            for file_result in data:
                file_path = file_result.get('filePath', base_path)
                messages = file_result.get('messages', [])
                
                for message in messages:
                    rule_id = message.get('ruleId', 'unknown')
                    severity_num = message.get('severity', 1)
                    
                    # Obtener información de la regla
                    rule_info = self.ESLINT_RULE_MAPPING.get(rule_id, {
                        'category': LintCategory.BEST_PRACTICE,
                        'severity': self.ESLINT_SEVERITY_MAPPING.get(severity_num, LintSeverity.LOW),
                        'name': 'unknown rule'
                    })
                    
                    # Override severity si ESLint dice que es error (2)
                    if severity_num == 2:
                        severity = LintSeverity.MEDIUM
                    else:
                        severity = rule_info.get('severity', self.ESLINT_SEVERITY_MAPPING[severity_num])
                    
                    vulnerability = Vulnerability(
                        file=file_path,
                        line=message.get('line', 1),
                        rule_id=rule_id,
                        severity=severity.value,
                        message=f"{rule_info.get('name', rule_id)}: {message.get('message', '')}",
                        tool='eslint',
                        category='quality',
                        impact=self._severity_to_impact(severity),
                        likelihood='high',
                        remediation_effort='low' if message.get('fix') else 'medium'
                    )
                    
                    vulnerabilities.append(vulnerability)
                    
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse ESLint JSON output: {e}")
            
        return vulnerabilities
    
    def _parse_prettier_output(self, output: str, base_path: str) -> List[Vulnerability]:
        """Parsea la salida de prettier --check"""
        vulnerabilities = []
        
        lines = output.strip().split('\n')
        
        for line in lines:
            # Prettier lista archivos que necesitan formato
            if line.strip() and not line.startswith('['):
                file_path = line.strip()
                
                vulnerability = Vulnerability(
                    file=file_path if os.path.isabs(file_path) else os.path.join(base_path, file_path),
                    line=1,
                    rule_id='PRETTIER_FORMAT',
                    severity=LintSeverity.LOW.value,
                    message="File needs reformatting according to Prettier style",
                    tool='prettier',
                    category='quality',
                    impact='low',
                    likelihood='high',
                    remediation_effort='low'
                )
                
                vulnerabilities.append(vulnerability)
                
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
    
    def run_full_analysis(self, path: str, is_typescript: bool = False) -> Tuple[List[Vulnerability], Dict[str, any]]:
        """
        Ejecuta análisis completo de JavaScript/TypeScript (ESLint + Prettier)
        
        Args:
            path: Ruta del archivo o directorio
            is_typescript: Si True, analiza como TypeScript
            
        Returns:
            Tuple con vulnerabilidades y métricas
        """
        start_time = time.time()
        all_vulnerabilities = []
        tools_executed = []
        tool_results = {}
        
        # Ejecutar ESLint
        try:
            eslint_vulns = self.run_eslint(path, is_typescript)
            all_vulnerabilities.extend(eslint_vulns)
            tools_executed.append('eslint')
            tool_results['eslint'] = {
                'issues': len(eslint_vulns),
                'categories': self._categorize_issues(eslint_vulns)
            }
        except Exception as e:
            tool_results['eslint'] = {'error': str(e)}
        
        # Ejecutar Prettier
        try:
            prettier_vulns = self.run_prettier(path)
            all_vulnerabilities.extend(prettier_vulns)
            tools_executed.append('prettier')
            tool_results['prettier'] = {
                'issues': len(prettier_vulns),
                'files_need_formatting': len(prettier_vulns)
            }
        except Exception as e:
            tool_results['prettier'] = {'error': str(e)}
        
        execution_time = time.time() - start_time
        
        # Calcular métricas
        metrics = self._calculate_js_metrics(all_vulnerabilities, tools_executed, execution_time)
        
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
            'performance': 0,
            'security': 0
        }
        
        for vuln in vulnerabilities:
            message_lower = vuln.message.lower()
            rule_id = vuln.rule_id.lower()
            
            # Categorización basada en regla y mensaje
            if vuln.tool == 'prettier' or 'format' in message_lower or 'spacing' in message_lower:
                categories['format'] += 1
            elif 'security' in message_lower or 'eval' in rule_id or 'script-url' in rule_id:
                categories['security'] += 1
            elif 'complexity' in message_lower or 'nested' in message_lower:
                categories['maintainability'] += 1
            elif 'performance' in message_lower:
                categories['performance'] += 1
            elif 'style' in message_lower or 'naming' in message_lower or 'quote' in rule_id:
                categories['style'] += 1
            else:
                categories['best_practice'] += 1
                
        return categories
    
    def _calculate_js_metrics(self, vulnerabilities: List[Vulnerability], 
                            tools_executed: List[str], execution_time: float) -> Dict[str, any]:
        """Calcula métricas específicas para JavaScript/TypeScript"""
        
        total_issues = len(vulnerabilities)
        categories = self._categorize_issues(vulnerabilities)
        
        # Calcular score (penalizar más los issues críticos)
        score = 100.0
        score -= categories['format'] * 0.5
        score -= categories['style'] * 1.0
        score -= categories['best_practice'] * 2.0
        score -= categories['maintainability'] * 2.5
        score -= categories['performance'] * 2.0
        score -= categories['security'] * 4.0  # Security es crítico
        
        score = max(0.0, score)
        
        return {
            'total_issues': total_issues,
            'categories': categories,
            'tools_executed': tools_executed,
            'execution_time': execution_time,
            'quality_score': round(score, 1),
            'grade': self._score_to_grade(score),
            'auto_fixable': categories['format']
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
