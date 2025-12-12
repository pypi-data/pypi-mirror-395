"""
Java Security Vulnerability Detector

Main detector class orchestrating multi-agent vulnerability detection.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
import json

from brainary.core.context import ExecutionContext
from brainary.core.kernel import CognitiveKernel

from .agents import ScannerAgent, AnalyzerAgent, ValidatorAgent, ReporterAgent
from .knowledge import VulnerabilityKnowledgeBase
from .tools import SecurityScanner


@dataclass
class DetectionConfig:
    """Configuration for detection process"""
    deep_analysis: bool = True
    validate_findings: bool = True
    generate_remediation: bool = True
    max_findings: int = 50
    focus_areas: Optional[List[str]] = None
    confidence_threshold: str = "medium"  # low/medium/high


class JavaSecurityDetector:
    """
    Intelligent Java vulnerability detector.
    
    Uses multi-agent architecture powered by Brainary SDK to detect,
    analyze, validate, and report Java security vulnerabilities.
    
    Features:
    - Multi-agent detection pipeline
    - LLM-powered analysis
    - CodeQL integration
    - Knowledge base of OWASP/CWE patterns
    - Automated remediation recommendations
    """
    
    def __init__(self, kernel: Optional[CognitiveKernel] = None,
                 config: Optional[DetectionConfig] = None):
        """
        Initialize detector.
        
        Args:
            kernel: CognitiveKernel instance (creates new if not provided)
            config: Detection configuration
        """
        self.kernel = kernel or CognitiveKernel()
        self.config = config or DetectionConfig()
        
        # Initialize agents
        self.scanner_agent = ScannerAgent()
        self.analyzer_agent = AnalyzerAgent()
        self.validator_agent = ValidatorAgent()
        self.reporter_agent = ReporterAgent()
        
        # Initialize knowledge base
        self.kb = VulnerabilityKnowledgeBase()
        
        # Detection state
        self.last_detection_result = None
    
    def detect(self, target: str, config: Optional[DetectionConfig] = None) -> Dict[str, Any]:
        """
        Run complete vulnerability detection pipeline.
        
        Args:
            target: File or directory to analyze
            config: Optional detection configuration (overrides default)
        
        Returns:
            Dictionary with complete detection results
        """
        config = config or self.config
        
        # Create execution context
        context = ExecutionContext(program_id="java_security_detection")
        context.add_observation(f"Starting detection for {target}")
        
        # Phase 1: Scan
        scan_result = self._scan_phase(context, target, config)
        if not scan_result["success"]:
            return scan_result
        
        findings = scan_result.get("findings", [])
        context.add_observation(f"Scan phase complete: {len(findings)} findings")
        
        # Phase 2: Analyze
        if config.deep_analysis and findings:
            analysis_result = self._analyze_phase(context, findings, config)
            findings = analysis_result.get("findings", findings)
            context.add_observation(f"Analysis phase complete")
        
        # Phase 3: Validate
        if config.validate_findings and findings:
            validation_result = self._validate_phase(context, findings)
            validated_findings = validation_result.get("validated_findings", [])
            context.add_observation(
                f"Validation phase complete: {len(validated_findings)} confirmed"
            )
        else:
            validated_findings = findings
        
        # Phase 4: Report
        report_result = self._report_phase(context, validated_findings)
        
        # Compile final result
        final_result = {
            "success": True,
            "target": target,
            "config": {
                "deep_analysis": config.deep_analysis,
                "validate_findings": config.validate_findings,
                "generate_remediation": config.generate_remediation
            },
            "statistics": {
                "total_findings": len(findings),
                "validated_findings": len(validated_findings),
                "false_positives": len(findings) - len(validated_findings) if config.validate_findings else 0
            },
            "findings": validated_findings,
            "report": report_result.get("report", ""),
            "summary": report_result.get("summary", ""),
            "context": context
        }
        
        self.last_detection_result = final_result
        return final_result
    
    def _scan_phase(self, context: ExecutionContext, target: str,
                    config: DetectionConfig) -> Dict[str, Any]:
        """Execute scanning phase"""
        context.add_observation("Phase 1: Scanning")
        
        scan_options = {
            "deep_analysis": config.deep_analysis
        }
        
        try:
            result = self.scanner_agent.execute(context, target, scan_options)
            return result
        except Exception as e:
            context.add_observation(f"Scan phase error: {e}")
            return {"success": False, "error": str(e)}
    
    def _analyze_phase(self, context: ExecutionContext, findings: List[Dict],
                      config: DetectionConfig) -> Dict[str, Any]:
        """Execute analysis phase"""
        context.add_observation("Phase 2: Deep Analysis")
        
        # Limit findings if configured
        if config.max_findings:
            findings = findings[:config.max_findings]
        
        try:
            result = self.analyzer_agent.execute(
                context,
                findings,
                focus_areas=config.focus_areas
            )
            return result
        except Exception as e:
            context.add_observation(f"Analysis phase error: {e}")
            return {"success": False, "error": str(e), "findings": findings}
    
    def _validate_phase(self, context: ExecutionContext,
                       findings: List[Dict]) -> Dict[str, Any]:
        """Execute validation phase"""
        context.add_observation("Phase 3: Validation")
        
        try:
            result = self.validator_agent.execute(context, findings)
            return result
        except Exception as e:
            context.add_observation(f"Validation phase error: {e}")
            return {
                "success": False,
                "error": str(e),
                "validated_findings": findings
            }
    
    def _report_phase(self, context: ExecutionContext,
                     findings: List[Dict]) -> Dict[str, Any]:
        """Execute reporting phase"""
        context.add_observation("Phase 4: Reporting")
        
        try:
            result = self.reporter_agent.execute(context, findings)
            return result
        except Exception as e:
            context.add_observation(f"Reporting phase error: {e}")
            return {
                "success": False,
                "error": str(e),
                "report": "Report generation failed",
                "summary": str(e)
            }
    
    def quick_scan(self, target: str) -> Dict[str, Any]:
        """
        Run quick scan without deep analysis or validation.
        
        Args:
            target: File or directory to scan
        
        Returns:
            Dictionary with scan results
        """
        quick_config = DetectionConfig(
            deep_analysis=False,
            validate_findings=False,
            generate_remediation=False
        )
        
        return self.detect(target, quick_config)
    
    def thorough_scan(self, target: str, focus_areas: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run thorough scan with all features enabled.
        
        Args:
            target: File or directory to scan
            focus_areas: Optional vulnerability types to focus on
        
        Returns:
            Dictionary with complete results
        """
        thorough_config = DetectionConfig(
            deep_analysis=True,
            validate_findings=True,
            generate_remediation=True,
            focus_areas=focus_areas
        )
        
        return self.detect(target, thorough_config)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics from last detection"""
        if not self.last_detection_result:
            return {"error": "No detection has been run"}
        
        return self.last_detection_result.get("statistics", {})
    
    def export_report(self, output_path: str, format: str = "txt") -> bool:
        """
        Export last detection report.
        
        Args:
            output_path: Path to save report
            format: Format (txt, json, html)
        
        Returns:
            True if successful
        """
        if not self.last_detection_result:
            return False
        
        try:
            if format == "json":
                # Export as JSON
                data = {
                    "target": self.last_detection_result["target"],
                    "statistics": self.last_detection_result["statistics"],
                    "findings": self.last_detection_result["findings"],
                    "summary": self.last_detection_result["summary"]
                }
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=2)
            
            elif format == "txt":
                # Export as text report
                report = self.last_detection_result.get("report", "")
                with open(output_path, 'w') as f:
                    f.write(report)
            
            elif format == "html":
                # Export as HTML
                html = self._generate_html_report(self.last_detection_result)
                with open(output_path, 'w') as f:
                    f.write(html)
            
            else:
                return False
            
            return True
        
        except Exception as e:
            return False
    
    def _generate_html_report(self, result: Dict[str, Any]) -> str:
        """Generate HTML report"""
        findings = result.get("findings", [])
        stats = result.get("statistics", {})
        
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Java Security Vulnerability Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        .summary { background: #f0f0f0; padding: 20px; margin: 20px 0; }
        .finding { border: 1px solid #ddd; margin: 20px 0; padding: 20px; }
        .critical { border-left: 5px solid #d32f2f; }
        .high { border-left: 5px solid #f57c00; }
        .medium { border-left: 5px solid #fbc02d; }
        .low { border-left: 5px solid #388e3c; }
        .code { background: #f5f5f5; padding: 10px; font-family: monospace; }
    </style>
</head>
<body>
    <h1>Java Security Vulnerability Report</h1>
    
    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Target:</strong> {target}</p>
        <p><strong>Total Findings:</strong> {total}</p>
        <p><strong>Validated:</strong> {validated}</p>
        <p><strong>False Positives:</strong> {fp}</p>
    </div>
    
    <h2>Findings</h2>
""".format(
            target=result.get("target", "Unknown"),
            total=stats.get("total_findings", 0),
            validated=stats.get("validated_findings", 0),
            fp=stats.get("false_positives", 0)
        )
        
        for i, finding in enumerate(findings, 1):
            severity = finding.get("severity", "medium")
            cwe_id = finding.get("cwe_id", "UNKNOWN")
            
            html += f"""
    <div class="finding {severity}">
        <h3>[{i}] {finding.get("name", "Unknown")} ({cwe_id})</h3>
        <p><strong>Severity:</strong> {severity.upper()}</p>
        <p><strong>Location:</strong> {finding.get("file", "unknown")} line {finding.get("line", 0)}</p>
        <p><strong>Confidence:</strong> {finding.get("confidence", "medium").upper()}</p>
    </div>
"""
        
        html += """
</body>
</html>
"""
        return html
    
    def get_knowledge_base(self) -> VulnerabilityKnowledgeBase:
        """Get vulnerability knowledge base"""
        return self.kb
    
    def list_vulnerability_patterns(self) -> str:
        """List all available vulnerability patterns"""
        return self.kb.get_all_patterns_summary()
    
    def get_pattern_guidance(self, cwe_id: str) -> str:
        """Get detection guidance for a specific vulnerability"""
        return self.kb.get_detection_guidance(cwe_id)
