"""
SemBicho - Static Application Security Testing Tool
Paquete principal para análisis estático de seguridad
"""

from .__version__ import __version__  # Fuente única de versión
from .scanner import SemBichoScanner, Vulnerability, ScanResult

__author__ = "SemBicho Team"
__license__ = "MIT"

__all__ = ["SemBichoScanner", "Vulnerability", "ScanResult", "__version__"]
