#!/usr/bin/env python3
"""SemBicho CLI - Production Ready with Auth & Quality"""

import argparse
import sys
import os
from pathlib import Path
from dataclasses import asdict
import json
from datetime import datetime

from .__version__ import __version__
from .scanner import SemBichoScanner
from .auth_module import SemBichoAuth
from .linting_engine import LintingEngine
from .complexity_engine import ComplexityEngine
from .quality_integrator import QualityScannerIntegrator

def main():
    # Descripción mejorada con ejemplos
    description = """
SemBicho CLI - Enterprise Security Analysis Tool

QUICK START:
  sembicho cicd --path ./src --upload  # [CI/CD] Complete CI/CD analysis
  sembicho scan --path ./myproject --output report.json
  sembicho auth login --token YOUR_JWT_TOKEN

EXAMPLES:
  # CI/CD Complete Analysis (Security + Quality + Upload)
  sembicho cicd --path . --upload --fail-on high
  sembicho cicd --path ./src --output reports/ --pipeline-id "build-123"
  
  # Scan for vulnerabilities
  sembicho scan --path . --output results.json --upload
  
  # Code quality analysis
  sembicho quality lint --path src/
  sembicho quality complexity --path app/
  sembicho quality all --path .
  
  # Authentication
  sembicho auth login --token eyJhbGc...
  sembicho auth status
  sembicho auth logout
  
  # Version info
  sembicho version
  sembicho --version

DOCUMENTATION:
  https://docs.sembicho.com
  https://app.sembicho.com
"""
    
    parser = argparse.ArgumentParser(
        prog='sembicho', 
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version=f'v{__version__}')
    subparsers = parser.add_subparsers(dest='command')
    
    # Scan
    scan_parser = subparsers.add_parser(
        'scan', 
        help='Scan code for security vulnerabilities',
        description='Analyze code for security issues and generate detailed vulnerability reports'
    )
    scan_parser.add_argument('--path', '-p', required=True, help='Path to directory or file to scan')
    scan_parser.add_argument('--output', '-o', help='Output JSON file path (default: sembicho-report.json)')
    scan_parser.add_argument('--upload', action='store_true', help='Upload results to backend automatically (requires auth)')
    scan_parser.add_argument('--pipeline-id', help='Pipeline ID for tracking scans (auto-generated if not provided)')
    
    # API Integration
    scan_parser.add_argument('--api-url', help='Backend API URL for uploading results')
    scan_parser.add_argument('--token', help='JWT authentication token for API')
    
    # CI/CD Mode
    scan_parser.add_argument('--ci-mode', action='store_true', help='Enable CI/CD optimized output')
    scan_parser.add_argument('--fail-on', help='Fail on severities (comma-separated: critical,high,medium,low)')
    
    # SBOM
    scan_parser.add_argument('--sbom-format', choices=['cyclonedx-json', 'spdx-json', 'syft-json'], 
                            default='cyclonedx-json', help='SBOM format (default: cyclonedx-json)')
    scan_parser.add_argument('--skip-sbom', action='store_true', help='Skip SBOM generation')
    
    # Auth (Enterprise feature)
    auth_parser = subparsers.add_parser(
        'auth', 
        help='Manage authentication with SemBicho backend',
        description='Authenticate using JWT tokens from https://app.sembicho.com'
    )
    auth_sub = auth_parser.add_subparsers(dest='auth_command')
    
    # Auth login (token-based)
    login_parser = auth_sub.add_parser(
        'login', 
        help='Login with JWT token',
        description='Authenticate using JWT token from dashboard or SEMBICHO_TOKEN env var'
    )
    login_parser.add_argument('--token', '-t', help='JWT token from https://app.sembicho.com/settings/tokens or env SEMBICHO_TOKEN')
    login_parser.add_argument('--api-url', help='Backend API URL (default: https://sembichobackend.onrender.com)')
    
    # Auth logout  
    auth_sub.add_parser(
        'logout', 
        help='Logout and clear stored credentials',
        description='Remove stored JWT token from secure keyring'
    )
    
    # Auth status
    auth_sub.add_parser(
        'status', 
        help='Check authentication and connectivity status',
        description='Verify backend connection and token validation'
    )
    
    # Quality commands (formerly integrated in scan)
    quality_parser = subparsers.add_parser(
        'quality', 
        help='Analyze code quality metrics',
        description='Run linting, complexity analysis, or combined quality checks'
    )
    quality_sub = quality_parser.add_subparsers(dest='quality_command')
    
    # Lint command
    lint_parser = quality_sub.add_parser(
        'lint', 
        help='Run code linting analysis',
        description='Check code style and quality issues using flake8/pylint'
    )
    lint_parser.add_argument('--path', '-p', required=True, help='Path to directory or file to analyze')
    lint_parser.add_argument('--language', '-l', choices=['python', 'javascript'], help='Target language (auto-detected if not specified)')
    lint_parser.add_argument('--output', '-o', help='Save results to JSON file')
    lint_parser.add_argument('--format', choices=['json', 'console'], default='console', help='Output format (default: console)')
    
    # Complexity command
    complexity_parser = quality_sub.add_parser(
        'complexity', 
        help='Analyze cyclomatic complexity',
        description='Measure code complexity using radon (McCabe complexity metrics)'
    )
    complexity_parser.add_argument('--path', '-p', required=True, help='Path to directory or file to analyze')
    complexity_parser.add_argument('--threshold', '-t', choices=['low', 'moderate', 'high'], default='moderate', help='Complexity threshold (default: moderate)')
    complexity_parser.add_argument('--output', '-o', help='Save results to JSON file')
    complexity_parser.add_argument('--format', choices=['json', 'console'], default='console', help='Output format (default: console)')
    
    # Quality (all-in-one)
    quality_all_parser = quality_sub.add_parser(
        'all', 
        help='Run complete quality analysis',
        description='Execute both linting and complexity analysis in one command'
    )
    quality_all_parser.add_argument('--path', '-p', required=True, help='Path to directory or file to analyze')
    quality_all_parser.add_argument('--output', '-o', help='Save combined results to JSON file')
    quality_all_parser.add_argument('--format', choices=['json', 'console'], default='console', help='Output format (default: console)')
    
    # CI/CD All-in-one command
    cicd_parser = subparsers.add_parser(
        'cicd',
        help='Complete analysis for CI/CD pipelines',
        description='Run security scan + quality analysis (lint + complexity) + auto-upload in one command'
    )
    cicd_parser.add_argument('--path', '-p', required=True, help='Path to directory to analyze')
    cicd_parser.add_argument('--output', '-o', help='Output directory for reports (default: ./sembicho-reports)')
    cicd_parser.add_argument('--upload', action='store_true', help='Upload results to backend automatically (requires auth)')
    cicd_parser.add_argument('--pipeline-id', help='Pipeline ID for tracking (auto-generated if not provided)')
    cicd_parser.add_argument('--fail-on', choices=['critical', 'high', 'medium', 'low'], help='Fail build if vulnerabilities of this severity or higher are found')
    
    # Version
    subparsers.add_parser(
        'version', 
        help='Show CLI version',
        description='Display the current version of SemBicho CLI'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    elif args.command == 'auth':
        auth_handler = SemBichoAuth()
        
        if not args.auth_command:
            print("Auth commands: login, logout, status")
            print("Run 'sembicho auth --help' for more info")
            return
        
        if args.auth_command == 'login':
            # Get token from args or environment variable or interactive input
            token = args.token or os.environ.get('SEMBICHO_TOKEN')
            
            if not token:
                # Interactive input
                print("\n[AUTH] SemBicho CLI - Token Authentication")
                print("=" * 50)
                token = input("\n[TOKEN] Enter your JWT token: ").strip()
            
            if not token:
                print("\n[ERROR] Error: Token is required")
                print("\n[DOCS] How to get your token:")
                print("   1. Go to https://app.sembicho.com")
                print("   2. Login with your credentials")
                print("   3. Navigate to Settings > API Tokens")
                print("   4. Click 'Generate New Token'")
                print("   5. Copy the token")
                print("\n[LOCAL] Usage:")
                print("   sembicho auth login --token YOUR_TOKEN")
                print("   # OR")
                print("   export SEMBICHO_TOKEN=YOUR_TOKEN")
                print("   sembicho auth login")
                sys.exit(1)
            
            print("\n[RETRY] Validating token...")
            if auth_handler.login_with_token(token, args.api_url):
                print("\n[OK] Authentication successful!")
                status = auth_handler.get_auth_status()
                print(f"   [USER] User: {status['username']}")
                print(f"   [API] API: {status['api_url']}")
                print(f"   [DATE] Login: {status['last_login']}")
                print("\n[TIP] You can now use authenticated features:")
                print("   - Upload scan results: sembicho scan --path . --upload")
                print("   - View dashboard: https://app.sembicho.com/dashboard")
                print("   - Check status: sembicho auth status")
            else:
                print("\n[ERROR] Authentication failed")
                print("   Please check your token and try again")
                sys.exit(1)
        
        elif args.auth_command == 'logout':
            if auth_handler.logout():
                print("[OK] Logged out successfully")
            else:
                print("[ERROR] Logout failed")
        
        elif args.auth_command == 'status':
            status = auth_handler.get_auth_status()
            print(f"Authentication Status:")
            print(f"  Authenticated: {'[OK] Yes' if status['authenticated'] else '[ERROR] No'}")
            print(f"  Username: {status['username']}")
            print(f"  API URL: {status['api_url']}")
            print(f"  Last Login: {status['last_login']}")
            print(f"  Config: {status['config_path']}")
            
            # Test connection based on authentication status
            if status['authenticated']:
                # User has token, test authenticated connection
                if auth_handler.test_authenticated_connection():
                    print(f"  Backend: [OK] Connected & Authenticated")
                else:
                    print(f"  Backend: [ERROR] Authentication Failed (invalid token)")
            else:
                # No token, test basic connectivity only
                if auth_handler.test_connection():
                    print(f"  Backend: [WARN] Reachable (not authenticated)")
                else:
                    print(f"  Backend: [ERROR] Unreachable")
    
    elif args.command == 'scan':
        target = Path(args.path).resolve()
        if not target.exists():
            print(f"\n Error: Path not found: {target}")
            sys.exit(1)
        
        print(f"\n SemBicho CLI v{__version__} - Security Scan")
        print(f" Target: {target}")
        
        # Initialize scanner
        scanner = SemBichoScanner()
        
        # Run security scan
        result = scanner.scan_directory(str(target))
        
        # Save results if output specified
        output_file = args.output or 'sembicho-report.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(result), f, indent=2, ensure_ascii=False)
        
        print(f"\n Scan Results:")
        print(f"   Files scanned: {result.quality_metrics.total_files_scanned}")
        print(f"   Total vulnerabilities: {result.total_vulnerabilities}")
        print(f"   -- Critical: {result.severity_counts.get('critical', 0)}")
        print(f"   -- High: {result.severity_counts.get('high', 0)}")
        print(f"   -- Medium: {result.severity_counts.get('medium', 0)}")
        print(f"   -- Low: {result.severity_counts.get('low', 0)}")
        print(f"\n Report saved to: {output_file}")
        
        # Upload to backend if requested
        if args.upload or (args.api_url and args.token):
            # Determine API URL and token
            api_url = args.api_url
            token = args.token
            
            # Try to get from auth if not provided
            if not api_url or not token:
                auth_handler = SemBichoAuth()
                if auth_handler.is_authenticated():
                    config = auth_handler.get_config()
                    api_url = api_url or config.get('api_url')
                    token = token or auth_handler.get_stored_token()
                else:
                    print("\n [WARN] Not authenticated. Cannot upload results.")
                    print("   Run: sembicho auth login --token YOUR_TOKEN")
                    if not args.api_url or not args.token:
                        print("   Or provide --api-url and --token arguments")
                        sys.exit(1)
            
            # Ensure URL ends with /reports
            if api_url and not api_url.endswith('/reports'):
                api_url = f"{api_url.rstrip('/')}/reports"
            
            # Generate pipeline ID if not provided
            pipeline_id = args.pipeline_id
            if not pipeline_id:
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                pipeline_id = f"scan-{timestamp}"
            
            print(f"\n Uploading results to backend...")
            print(f"   API: {api_url}")
            print(f"   Pipeline ID: {pipeline_id}")
            
            # Upload using scanner's send_to_api method
            success = scanner.send_to_api(
                api_url=api_url,
                token=token,
                pipeline_id=pipeline_id
            )
            
            if success:
                print(f"\n ✅ Results uploaded successfully!")
                print(f"   View at: https://app.sembicho.com/dashboard")
            else:
                print(f"\n ❌ Failed to upload results")
                print(f"   Check your token and API URL")
                sys.exit(1)
        
        # CI Mode: Fail on severity threshold
        if args.fail_on and args.fail_on.strip():
            severity_map = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
            threshold = severity_map.get(args.fail_on.lower())
            
            if threshold is not None:
                should_fail = False
                if threshold <= 0 and result.severity_counts.get('critical', 0) > 0:
                    should_fail = True
                elif threshold <= 1 and result.severity_counts.get('high', 0) > 0:
                    should_fail = True
                elif threshold <= 2 and result.severity_counts.get('medium', 0) > 0:
                    should_fail = True
                elif threshold <= 3 and result.severity_counts.get('low', 0) > 0:
                    should_fail = True
                
                if should_fail:
                    print(f"\n ❌ Build FAILED: Found vulnerabilities at or above '{args.fail_on}' severity")
                    sys.exit(1)
                else:
                    print(f"\n ✅ Build PASSED: No vulnerabilities at or above '{args.fail_on}' severity")
    
    elif args.command == 'quality':
        if not args.quality_command:
            print("Quality commands: lint, complexity, all")
            print("Run 'sembicho quality --help' for more info")
            return
        
        target = Path(args.path).resolve()
        if not target.exists():
            print(f"\n Error: Path not found: {target}")
            sys.exit(1)
        
        print(f"\n SemBicho CLI v{__version__} - Quality Analysis")
        print(f" Target: {target}")
        
        if args.quality_command == 'lint':
            print(f"\n Running linting analysis...")
            engine = LintingEngine()
            
            # Determine language
            language = args.language
            if not language:
                # Auto-detect based on file extension
                if target.suffix == '.py':
                    language = 'python'
                elif target.suffix in ['.js', '.jsx', '.ts', '.tsx']:
                    language = 'javascript'
                else:
                    print(f"Unsupported file type: {target.suffix}")
                    print("Supported: .py, .js, .jsx, .ts, .tsx")
                    sys.exit(1)
            
            # Run linting analysis
            vulnerabilities, metrics = engine.run_linting_analysis(str(target), language)
            
            # Display results
            if args.format == 'console':
                print(f"\n Linting Results:")
                print(f"   Issues Found: {len(vulnerabilities)}")
                print(f"   Total Lint Issues: {metrics.total_lint_issues}")
                print(f"   Style Issues: {metrics.style_issues}")
                print(f"   Performance Issues: {metrics.performance_issues}")
                print(f"   Linting Score: {metrics.linting_score:.1f}/100")
                
                for vuln in vulnerabilities[:10]:  # Show first 10
                    severity_icon = {"CRITICAL": "[FAIL]", "HIGH": "[WARN]", "MEDIUM": "[WARN]", "LOW": "[INFO]"}.get(vuln.severity, "-")
                    print(f"   {severity_icon} {vuln.severity}: {vuln.message} (Line {vuln.line})")
                if len(vulnerabilities) > 10:
                    print(f"   ... and {len(vulnerabilities) - 10} more issues")
            
            if args.output:
                result_data = {
                    "vulnerabilities": [asdict(v) for v in vulnerabilities],
                    "metrics": asdict(metrics),
                    "summary": {
                        "total_issues": len(vulnerabilities),
                        "language": language,
                        "file": str(target)
                    }
                }
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result_data, f, indent=2, ensure_ascii=False)
                print(f"\n Results saved to: {args.output}")
        
        elif args.quality_command == 'complexity':
            print(f"\n Running complexity analysis...")
            engine = ComplexityEngine()
            
            # Determine language
            if target.suffix == '.py':
                language = 'python'
            elif target.suffix in ['.js', '.jsx', '.ts', '.tsx']:
                language = 'javascript'
            else:
                print(f"Complexity analysis supports Python (.py) and JavaScript (.js, .jsx, .ts, .tsx) files")
                sys.exit(1)
            
            result = engine.analyze_complexity(str(target), language)
            
            # Display results
            if args.format == 'console':
                print(f"\n Complexity Results:")
                print(f"   Functions Analyzed: {result.total_functions}")
                print(f"   Average Complexity: {result.average_complexity:.2f}")
                print(f"   Max Complexity: {result.max_complexity}")
                print(f"   Complexity Grade: {result.complexity_grade}")
                print(f"   Complexity Score: {result.complexity_score:.1f}/100")
                print(f"   High Complexity (>10): {result.high_complexity_count}")
                print(f"   Critical Complexity (>20): {result.critical_complexity_count}")
                
                # Show complexity metrics
                if result.complexity_metrics:
                    print(f"\n   Top Complex Functions:")
                    sorted_metrics = sorted(result.complexity_metrics, key=lambda x: x.cyclomatic_complexity, reverse=True)
                    for metric in sorted_metrics[:5]:  # Top 5 most complex
                        level_icon = {"LOW": "[OK]", "MODERATE": "[WARN]", "HIGH": "[WARN]", "CRITICAL": "[FAIL]"}.get(metric.complexity_level.value.upper(), "-")
                        print(f"   {level_icon} {metric.name}: {metric.cyclomatic_complexity} ({metric.complexity_level.value}) - Line {metric.line_number}")
                else:
                    print(f"   No functions found for analysis")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(asdict(result), f, indent=2, ensure_ascii=False)
                print(f"\n Results saved to: {args.output}")
        
        elif args.quality_command == 'all':
            print(f"\n Running complete quality analysis...")
            integrator = QualityScannerIntegrator()
            result = integrator.analyze_quality(str(target))
            
            # Display summary
            if args.format == 'console':
                print(f"\n Quality Analysis Results:")
                print(f"   Quality Grade: {result.quality_grade}")
                print(f"   Quality Score: {result.quality_score:.1f}/100")
                print(f"   Total Issues: {result.total_quality_issues}")
                print(f"   Execution Time: {result.execution_time:.2f}s")
                
                print(f"\n Issue Breakdown:")
                print(f"   Linting Issues: {len(result.linting_issues)}")
                print(f"   Complexity Issues: {len(result.complexity_issues)}")
                print(f"   Code Smells: {len(result.code_smells)}")
                
                # Show top issues
                all_issues = result.linting_issues + result.complexity_issues + result.code_smells
                if all_issues:
                    print(f"\n Top Issues:")
                    for issue in all_issues[:5]:  # Top 5 issues
                        severity_icon = {"CRITICAL": "[FAIL]", "HIGH": "[WARN]", "MEDIUM": "[WARN]", "LOW": "[INFO]"}.get(issue.severity, "-")
                        print(f"   {severity_icon} {issue.severity}: {issue.message} (Line {issue.line})")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(asdict(result), f, indent=2, ensure_ascii=False)
                print(f"\n Results saved to: {args.output}")
    
    elif args.command == 'cicd':
        print(f"\n{'='*70}")
        print(f"  [CI/CD] SemBicho CI/CD Complete Analysis v{__version__}")
        print(f"{'='*70}\n")
        
        target = Path(args.path).resolve()
        if not target.exists():
            print(f"\n[ERROR] Error: Path not found: {target}")
            sys.exit(1)
        
        # Create output directory
        output_dir = Path(args.output) if args.output else Path('./sembicho-reports')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        pipeline_id = args.pipeline_id or f"cicd-{timestamp}"
        
        print(f"[FILE] Target: {target}")
        print(f"[METRICS] Pipeline ID: {pipeline_id}")
        print(f"[SAVE] Output Directory: {output_dir}\n")
        
        # === 1. SECURITY SCAN ===
        print(f"{'-'*70}")
        print("[SECURE] Step 1/3: Security Vulnerability Scan")
        print(f"{'-'*70}")
        scanner = SemBichoScanner()
        security_result = scanner.scan_directory(str(target))
        
        security_file = output_dir / f'security-{timestamp}.json'
        with open(security_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(security_result), f, indent=2, ensure_ascii=False)
        
        print(f"   Files scanned: {security_result.quality_metrics.total_files_scanned}")
        print(f"   Vulnerabilities: {security_result.total_vulnerabilities}")
        print(f"   -- Critical: {security_result.severity_counts.get('critical', 0)}")
        print(f"   -- High: {security_result.severity_counts.get('high', 0)}")
        print(f"   -- Medium: {security_result.severity_counts.get('medium', 0)}")
        print(f"   -- Low: {security_result.severity_counts.get('low', 0)}")
        print(f"   [SAVE] Saved: {security_file.name}\n")
        
        # === 2. QUALITY ANALYSIS ===
        print(f"{'-'*70}")
        print("[METRICS] Step 2/3: Code Quality Analysis (Lint + Complexity)")
        print(f"{'-'*70}")
        
        integrator = QualityScannerIntegrator()
        quality_result = integrator.analyze_quality(str(target))
        
        quality_file = output_dir / f'quality-{timestamp}.json'
        with open(quality_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(quality_result), f, indent=2, ensure_ascii=False)
        
        print(f"   Quality Score: {quality_result.quality_score:.1f}/100")
        print(f"   Quality Grade: {quality_result.quality_grade}")
        print(f"   Total Issues: {quality_result.total_quality_issues}")
        print(f"   [SAVE] Saved: {quality_file.name}\n")
        
        # === 3. UPLOAD TO BACKEND ===
        if args.upload:
            print(f"{'-'*70}")
            print("[UPLOAD] Step 3/3: Uploading to Backend")
            print(f"{'-'*70}")
            
            auth_handler = SemBichoAuth()
            if not auth_handler.is_authenticated():
                print("[ERROR] Not authenticated. Please login first:")
                print("   python -m sembicho auth login --token YOUR_TOKEN")
                sys.exit(1)
            
            try:
                import requests
                config = auth_handler.get_config()
                token = auth_handler.get_stored_token()
                
                # Combine results
                combined_report = {
                    "pipelineId": pipeline_id,
                    "data": {
                        "security": asdict(security_result),
                        "quality": asdict(quality_result),
                        "timestamp": timestamp,
                        "path": str(target)
                    }
                }
                
                response = requests.post(
                    f"{config['api_url']}/reports",
                    json=combined_report,
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print("[OK] Report uploaded successfully!")
                    print(f"   Pipeline ID: {pipeline_id}")
                    print(f"   View at: https://app.sembicho.com/dashboard\n")
                else:
                    print(f"[ERROR] Upload failed: {response.status_code}")
                    print(f"   {response.text}\n")
            except Exception as e:
                print(f"[ERROR] Upload error: {e}\n")
        
        # === SUMMARY ===
        print(f"{'='*70}")
        print("[LIST] CI/CD Analysis Summary")
        print(f"{'='*70}")
        print(f"   Security Vulnerabilities: {security_result.total_vulnerabilities}")
        print(f"   Quality Score: {quality_result.quality_score:.1f}/100")
        print(f"   Reports Directory: {output_dir}")
        print(f"{'='*70}\n")
        
        # === FAIL ON THRESHOLD ===
        if args.fail_on:
            severity_map = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
            threshold = severity_map[args.fail_on]
            
            should_fail = False
            if threshold <= 0 and security_result.severity_counts.get('critical', 0) > 0:
                should_fail = True
            elif threshold <= 1 and security_result.severity_counts.get('high', 0) > 0:
                should_fail = True
            elif threshold <= 2 and security_result.severity_counts.get('medium', 0) > 0:
                should_fail = True
            elif threshold <= 3 and security_result.severity_counts.get('low', 0) > 0:
                should_fail = True
            
            if should_fail:
                print(f"[ERROR] Build FAILED: Found vulnerabilities at or above '{args.fail_on}' severity level")
                sys.exit(1)
            else:
                print(f"[OK] Build PASSED: No vulnerabilities at or above '{args.fail_on}' severity level")
    
    elif args.command == 'version':
        print(f"SemBicho CLI v{__version__}")

if __name__ == '__main__':
    main()
