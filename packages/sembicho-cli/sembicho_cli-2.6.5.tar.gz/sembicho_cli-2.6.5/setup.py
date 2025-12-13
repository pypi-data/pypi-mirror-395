#!/usr/bin/env python3
"""
Setup script para SemBicho CLI
Herramienta autocontenida de análisis estático de seguridad
"""

from setuptools import setup, find_packages
import os

# Leer el README para la descripción larga
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README_CLI.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "SemBicho CLI - Herramienta autocontenida de análisis estático de seguridad"

# Leer requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-'):
                    # Extraer solo el nombre del paquete (sin comentarios)
                    req = line.split('#')[0].strip()
                    if req and '==' in req:
                        requirements.append(req)
    return requirements

setup(
    name="sembicho-cli",
    version="2.6.5",
    author="SemBicho Team",
    author_email="info@sembicho.com",
    description="SAST + SBOM (CycloneDX/SPDX) + CVE Scanning (OSV/Safety/NVD) - Análisis de seguridad empresarial completo",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Claudio-Barrios-83/sembicho-cli",
    project_urls={
        "Bug Tracker": "https://github.com/Claudio-Barrios-83/sembicho-cli/issues",
        "Documentation": "https://github.com/Claudio-Barrios-83/sembicho-cli",
        "Source Code": "https://github.com/Claudio-Barrios-83/sembicho-cli",
    },
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'urllib3>=2.0.7',
        'python-dateutil>=2.8.2',
        'chardet>=5.2.0',
        'jinja2>=3.1.2',
        'markupsafe>=2.1.3',
        'pyyaml>=6.0.1',
        'toml>=0.10.2',
        'regex>=2023.8.8',
        'keyring>=24.3.0',
        'colorama>=0.4.6',
        'radon>=6.0.1',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology", 
        "Topic :: Security",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    # Eliminado: duplicidad de install_requires
    extras_require={
        "cve": [
            "safety>=2.3.0",     # Python CVE scanning (recomendado para producción)
        ],
        "quality": [
            "radon>=6.0.1",      # Complexity analysis para Python
            "flake8>=6.0.0",     # Linting para Python
            "black>=23.0.0",     # Formatting para Python
            "pylint>=3.0.0",     # Linting avanzado para Python
        ],
        "all": [
            "radon>=6.0.1",
            "flake8>=6.0.0",
            "black>=23.0.0",
            "pylint>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sembicho=sembicho.__main__:main",
            "sembicho-cli=sembicho.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "sembicho": ["*.json"],
        "": ["*.md", "*.txt"],
    },
    keywords=[
        "security", "static-analysis", "vulnerability-scanner", 
        "code-analysis", "security-testing", "devops", "ci-cd",
        "python", "javascript", "java", "php", "go", "csharp",
        "sast", "security-scanner", "vulnerability-detection"
    ],
    zip_safe=False,
)