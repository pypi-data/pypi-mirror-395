#!/usr/bin/env python3
"""
SemBicho SBOM Scanner Module
Generación de Software Bill of Materials (SBOM) y escaneo de CVEs
usando Syft + Grype
"""

import subprocess
import json
import logging
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SBOMComponent:
    """Componente de software del SBOM"""
    name: str
    version: str
    purl: str  # Package URL (universal identifier)
    licenses: List[str]
    cpe: Optional[str] = None  # Common Platform Enumeration
    ecosystem: str = ""  # npm, pypi, maven, etc.
    type: str = "library"  # library, application, framework, etc.
    supplier: Optional[str] = None
    hashes: Optional[Dict[str, str]] = None


@dataclass
class CVEFinding:
    """Vulnerabilidad CVE encontrada"""
    cve_id: str
    severity: str  # critical, high, medium, low
    cvss_score: float
    affected_component: str
    affected_version: str
    fixed_version: Optional[str]
    description: str
    references: List[str]
    published_date: str
    epss_score: Optional[float] = None  # Exploit Prediction Scoring System
    
    def to_dict(self):
        return asdict(self)


@dataclass
class SBOMMetrics:
    """Métricas del SBOM generado"""
    total_components: int
    components_by_ecosystem: Dict[str, int]
    components_with_licenses: int
    components_with_cpe: int
    unique_licenses: List[str]
    total_cves: int
    cves_by_severity: Dict[str, int]
    high_risk_components: List[str]  # Componentes con CVEs críticos
    outdated_components: List[Dict[str, str]]  # Componentes con versiones antiguas


class SBOMScanner:
    """Scanner de SBOM usando Syft + Grype"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Inicializa el scanner de SBOM
        
        Args:
            logger: Logger opcional, si no se provee se crea uno nuevo
        """
        self.logger = logger or logging.getLogger('sembicho.sbom')
        self.syft_available = False
        self.grype_available = False
        self._check_tools()
    
    def _check_tools(self) -> Dict[str, bool]:
        """
        Verificar que Syft y Grype estén instalados
        
        Returns:
            Dict con disponibilidad de herramientas
        """
        # Verificar Syft
        try:
            result = subprocess.run(['syft', 'version'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                self.syft_available = True
                version = result.stdout.split('\n')[0] if result.stdout else ''
                self.logger.info(f"✅ Syft disponible: {version}")
            else:
                self._log_syft_installation()
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            self._log_syft_installation()
        
        # Verificar Grype
        try:
            result = subprocess.run(['grype', 'version'], 
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                self.grype_available = True
                version = result.stdout.split('\n')[0] if result.stdout else ''
                self.logger.info(f"✅ Grype disponible: {version}")
            else:
                self._log_grype_installation()
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            self._log_grype_installation()
        
        return {
            'syft': self.syft_available,
            'grype': self.grype_available
        }
    
    def _log_syft_installation(self):
        """Logea instrucciones de instalación de Syft"""
        self.logger.warning("⚠️  Syft no encontrado")
        self.logger.info("📦 Para instalar Syft:")
        self.logger.info("   Linux/Mac: curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh")
        self.logger.info("   Windows: scoop install syft  o  choco install syft")
    
    def _log_grype_installation(self):
        """Logea instrucciones de instalación de Grype"""
        self.logger.warning("⚠️  Grype no encontrado")
        self.logger.info("🔍 Para instalar Grype:")
        self.logger.info("   Linux/Mac: curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh")
        self.logger.info("   Windows: scoop install grype  o  choco install grype")
    
    def generate_sbom(self, 
                     path: str, 
                     output_format: str = 'cyclonedx-json',
                     scope: str = 'all-layers') -> Dict:
        """
        Genera SBOM usando Syft
        
        Args:
            path: Ruta al proyecto o imagen Docker (format: dir:path or docker:image)
            output_format: cyclonedx-json, spdx-json, syft-json
            scope: all-layers, squashed (solo para Docker images)
        
        Returns:
            SBOM en formato JSON
        """
        if not self.syft_available:
            self.logger.error("❌ Syft no está disponible. No se puede generar SBOM.")
            return {}
        
        try:
            # Determinar si es directorio o imagen Docker
            if not path.startswith('docker:') and not path.startswith('dir:'):
                # Asumir que es un directorio
                path = f'dir:{path}'
            
            # Ejecutar Syft
            cmd = ['syft', path, '-o', output_format, '-q']
            
            # Agregar scope si es imagen Docker
            if path.startswith('docker:') and scope:
                cmd.extend(['--scope', scope])
            
            self.logger.info(f"🔍 Generando SBOM: {path}")
            self.logger.debug(f"Comando: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True, 
                                  timeout=300)  # 5 minutos timeout
            
            if not result.stdout:
                self.logger.error("❌ Syft no devolvió datos")
                return {}
            
            sbom = json.loads(result.stdout)
            
            # Validar estructura básica
            if output_format == 'cyclonedx-json':
                components = sbom.get('components', [])
            elif output_format == 'spdx-json':
                components = sbom.get('packages', [])
            else:
                components = sbom.get('artifacts', [])
            
            self.logger.info(f"✅ SBOM generado exitosamente")
            self.logger.info(f"   Componentes encontrados: {len(components)}")
            self.logger.info(f"   Formato: {output_format}")
            
            # Agregar metadata adicional
            sbom['_metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'generator': 'sembicho-sbom-scanner',
                'syft_version': self._get_syft_version(),
                'source_path': path
            }
            
            return sbom
            
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout generando SBOM (5 minutos excedidos)")
            self.logger.info("💡 Intenta con un directorio más pequeño o excluye node_modules/")
            return {}
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Error ejecutando Syft: {e.stderr}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ SBOM generado no es JSON válido: {e}")
            self.logger.debug(f"Output: {result.stdout[:500]}")
            return {}
        except Exception as e:
            self.logger.error(f"❌ Error inesperado generando SBOM: {e}")
            return {}
    
    def scan_vulnerabilities(self, 
                           sbom_path_or_data: str | Dict,
                           fail_on: Optional[str] = None) -> List[CVEFinding]:
        """
        Escanea vulnerabilidades usando Grype desde un SBOM
        
        Args:
            sbom_path_or_data: Ruta al archivo SBOM o dict con SBOM
            fail_on: Severidad mínima para fallar (critical, high, medium, low)
        
        Returns:
            Lista de CVEs encontrados
        """
        if not self.grype_available:
            self.logger.error("❌ Grype no está disponible. No se pueden escanear CVEs.")
            return []
        
        try:
            # Si recibimos un dict, guardarlo temporalmente
            temp_file = None
            if isinstance(sbom_path_or_data, dict):
                temp_file = tempfile.NamedTemporaryFile(mode='w', 
                                                       suffix='.json', 
                                                       delete=False)
                json.dump(sbom_path_or_data, temp_file)
                temp_file.close()
                sbom_path = temp_file.name
            else:
                sbom_path = sbom_path_or_data
            
            # Verificar que el archivo existe
            if not os.path.exists(sbom_path):
                self.logger.error(f"❌ Archivo SBOM no encontrado: {sbom_path}")
                return []
            
            # Ejecutar Grype
            cmd = ['grype', f'sbom:{sbom_path}', '-o', 'json', '-q']
            
            # Agregar filtro de severidad si se especifica
            if fail_on:
                cmd.extend(['--fail-on', fail_on])
            
            self.logger.info(f"🔍 Escaneando vulnerabilidades...")
            self.logger.debug(f"Comando: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True,
                                  timeout=300)  # Permitir que falle con exit code != 0
            
            # Limpiar archivo temporal si existe
            if temp_file:
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            
            if not result.stdout:
                self.logger.warning("⚠️  Grype no devolvió datos (posiblemente sin vulnerabilidades)")
                return []
            
            grype_output = json.loads(result.stdout)
            
            # Parsear resultados
            findings = []
            matches = grype_output.get('matches', [])
            
            for match in matches:
                vuln = match.get('vulnerability', {})
                artifact = match.get('artifact', {})
                
                # Extraer versión fixed si existe
                fixed_version = None
                fix_info = vuln.get('fix', {})
                if fix_info:
                    versions = fix_info.get('versions', [])
                    if versions:
                        fixed_version = versions[0]
                
                finding = CVEFinding(
                    cve_id=vuln.get('id', 'UNKNOWN'),
                    severity=vuln.get('severity', 'UNKNOWN').lower(),
                    cvss_score=self._extract_cvss(vuln),
                    affected_component=artifact.get('name', ''),
                    affected_version=artifact.get('version', ''),
                    fixed_version=fixed_version,
                    description=vuln.get('description', '')[:500],  # Limitar descripción
                    references=vuln.get('urls', []),
                    published_date=vuln.get('publishedDate', ''),
                    epss_score=self._extract_epss(vuln)
                )
                findings.append(finding)
            
            # Logging de resultados
            self.logger.info(f"✅ CVE Scan completado")
            self.logger.info(f"   Total vulnerabilidades: {len(findings)}")
            
            # Agrupar por severidad para logging
            by_severity = {}
            for finding in findings:
                by_severity.setdefault(finding.severity, []).append(finding)
            
            for sev in ['critical', 'high', 'medium', 'low']:
                count = len(by_severity.get(sev, []))
                if count > 0:
                    emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '⚪'}
                    self.logger.info(f"   {emoji.get(sev, '')} {sev.upper()}: {count}")
            
            return findings
            
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout escaneando CVEs (5 minutos excedidos)")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Respuesta de Grype no es JSON válido: {e}")
            self.logger.debug(f"Output: {result.stdout[:500]}")
            return []
        except Exception as e:
            self.logger.error(f"❌ Error inesperado escaneando CVEs: {e}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return []
    
    def _extract_cvss(self, vuln: Dict) -> float:
        """
        Extrae el CVSS score más alto disponible
        
        Args:
            vuln: Diccionario de vulnerabilidad de Grype
        
        Returns:
            CVSS score (0.0 si no disponible)
        """
        cvss = vuln.get('cvss', [])
        if not cvss:
            return 0.0
        
        # Buscar CVSS v3.1 primero, luego v3.0, luego v2
        for version in ['3.1', '3.0', '2.0']:
            for metric in cvss:
                if str(metric.get('version', '')).startswith(version):
                    score = metric.get('metrics', {}).get('baseScore')
                    if score:
                        return float(score)
        
        # Fallback: primer score disponible
        first_metric = cvss[0].get('metrics', {})
        return float(first_metric.get('baseScore', 0))
    
    def _extract_epss(self, vuln: Dict) -> Optional[float]:
        """
        Extrae el EPSS score (Exploit Prediction Scoring System)
        
        Args:
            vuln: Diccionario de vulnerabilidad
        
        Returns:
            EPSS score o None
        """
        # EPSS aún no está en Grype por defecto, pero podría agregarse
        # Dejamos la función para futuras versiones
        return None
    
    def _get_syft_version(self) -> str:
        """Obtiene la versión de Syft instalada"""
        try:
            result = subprocess.run(['syft', 'version'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            return result.stdout.split('\n')[0].strip()
        except:
            return 'unknown'
    
    def scan_docker_image(self, 
                         image_name: str,
                         scan_cve: bool = True) -> Tuple[Dict, List[CVEFinding]]:
        """
        Escanea imagen Docker: genera SBOM + CVE scan
        
        Args:
            image_name: Nombre de la imagen (ej: myapp:latest, python:3.11)
            scan_cve: Si se deben escanear CVEs después del SBOM
        
        Returns:
            Tupla (sbom, cve_findings)
        """
        self.logger.info(f"🐳 Escaneando imagen Docker: {image_name}")
        
        # Generar SBOM de la imagen
        sbom = self.generate_sbom(f'docker:{image_name}')
        
        if not sbom:
            self.logger.error("❌ No se pudo generar SBOM de la imagen Docker")
            return {}, []
        
        # Escanear CVEs si se solicita
        cve_findings = []
        if scan_cve:
            cve_findings = self.scan_vulnerabilities(sbom)
        
        return sbom, cve_findings
    
    def generate_metrics(self, 
                        sbom: Dict, 
                        cve_findings: Optional[List[CVEFinding]] = None) -> SBOMMetrics:
        """
        Genera métricas del SBOM y CVEs
        
        Args:
            sbom: SBOM en formato CycloneDX o SPDX
            cve_findings: Lista opcional de CVEs encontrados
        
        Returns:
            SBOMMetrics con estadísticas
        """
        # Detectar formato del SBOM
        if 'bomFormat' in sbom and sbom['bomFormat'] == 'CycloneDX':
            components = sbom.get('components', [])
            format_type = 'cyclonedx'
        elif 'spdxVersion' in sbom:
            components = sbom.get('packages', [])
            format_type = 'spdx'
        else:
            # Formato Syft nativo
            components = sbom.get('artifacts', [])
            format_type = 'syft'
        
        # Contar componentes por ecosistema
        by_ecosystem = {}
        components_with_licenses = 0
        components_with_cpe = 0
        unique_licenses = set()
        
        for comp in components:
            # Ecosistema
            if format_type == 'cyclonedx':
                purl = comp.get('purl', '')
                if purl:
                    ecosystem = purl.split('/')[0].replace('pkg:', '')
                    by_ecosystem[ecosystem] = by_ecosystem.get(ecosystem, 0) + 1
                
                # Licencias
                licenses = comp.get('licenses', [])
                if licenses:
                    components_with_licenses += 1
                    for lic in licenses:
                        if isinstance(lic, dict):
                            if 'license' in lic:
                                unique_licenses.add(lic['license'].get('id', 'unknown'))
                        else:
                            unique_licenses.add(str(lic))
                
                # CPE
                if comp.get('cpe'):
                    components_with_cpe += 1
            
            elif format_type == 'spdx':
                # SPDX tiene diferente estructura
                name = comp.get('name', '')
                if 'Package' in comp.get('SPDXID', ''):
                    ecosystem = 'unknown'  # SPDX no siempre especifica ecosistema
                    by_ecosystem[ecosystem] = by_ecosystem.get(ecosystem, 0) + 1
        
        # Métricas de CVEs
        cves_by_severity = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        high_risk_components = []
        
        if cve_findings:
            for finding in cve_findings:
                severity = finding.severity.lower()
                if severity in cves_by_severity:
                    cves_by_severity[severity] += 1
                
                # Componentes de alto riesgo (CVEs críticos)
                if severity == 'critical':
                    comp_name = f"{finding.affected_component}@{finding.affected_version}"
                    if comp_name not in high_risk_components:
                        high_risk_components.append(comp_name)
        
        return SBOMMetrics(
            total_components=len(components),
            components_by_ecosystem=by_ecosystem,
            components_with_licenses=components_with_licenses,
            components_with_cpe=components_with_cpe,
            unique_licenses=list(unique_licenses),
            total_cves=len(cve_findings) if cve_findings else 0,
            cves_by_severity=cves_by_severity,
            high_risk_components=high_risk_components,
            outdated_components=[]  # TODO: implementar detección de versiones antiguas
        )
    
    def export_sbom(self, 
                   sbom: Dict, 
                   output_path: str,
                   format: str = 'json') -> bool:
        """
        Exporta SBOM a archivo
        
        Args:
            sbom: SBOM data
            output_path: Ruta del archivo de salida
            format: json (default) o xml
        
        Returns:
            True si se exportó correctamente
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                if format == 'json':
                    json.dump(sbom, f, indent=2, ensure_ascii=False)
                else:
                    self.logger.error(f"❌ Formato no soportado: {format}")
                    return False
            
            self.logger.info(f"✅ SBOM exportado: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error exportando SBOM: {e}")
            return False


# Función helper para uso rápido
def quick_scan(path: str, scan_cve: bool = True) -> Tuple[Dict, List[CVEFinding], SBOMMetrics]:
    """
    Escaneo rápido: SBOM + CVE + Métricas
    
    Args:
        path: Ruta al proyecto o imagen Docker
        scan_cve: Si se deben escanear CVEs
    
    Returns:
        Tupla (sbom, cve_findings, metrics)
    """
    scanner = SBOMScanner()
    
    # Generar SBOM
    sbom = scanner.generate_sbom(path)
    if not sbom:
        return {}, [], None
    
    # Escanear CVEs
    cve_findings = []
    if scan_cve:
        cve_findings = scanner.scan_vulnerabilities(sbom)
    
    # Generar métricas
    metrics = scanner.generate_metrics(sbom, cve_findings)
    
    return sbom, cve_findings, metrics
