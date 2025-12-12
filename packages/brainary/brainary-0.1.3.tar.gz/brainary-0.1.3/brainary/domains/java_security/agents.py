"""
Java Security Detection Agents

Multi-agent system for intelligent vulnerability detection.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

from brainary.core.context import ExecutionContext
from brainary.sdk.agents import Agent, AgentRole

from .primitives import (
    ThinkSecurityPrimitive,
    AnalyzeCodePrimitive,
    DetectVulnerabilityPrimitive,
    ValidateFindingPrimitive,
    RecommendFixPrimitive
)
from .knowledge import VulnerabilityKnowledgeBase
from .tools import SecurityScanner, ToolResult, ToolStatus


@dataclass
class SecurityFinding:
    """Represents a security finding"""
    cwe_id: str
    name: str
    severity: str
    file_path: str
    line_number: int
    code_snippet: str
    description: str
    confidence: str
    remediation: Optional[str] = None
    validated: bool = False


class ScannerAgent(Agent):
    """
    Scanner Agent: Initial code scanning and triage.
    
    Responsibilities:
    - Scan code for potential vulnerabilities
    - Run static analysis tools
    - Perform initial triage
    - Flag suspicious code patterns
    """
    
    def __init__(self, name: str = "SecurityScanner"):
        super().__init__(name=name, role=AgentRole.ANALYST)
        self.analyze_primitive = AnalyzeCodePrimitive()
        self.scanner = SecurityScanner(use_codeql=False)
    
    def execute(self, context: ExecutionContext, target: str,
                scan_options: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Scan target for vulnerabilities.
        
        Args:
            context: Execution context
            target: File or directory to scan
            scan_options: Optional scanning configuration
        
        Returns:
            Dictionary with scan results
        """
        scan_options = scan_options or {}
        
        # Update context with agent activity
        context.add_observation(f"ScannerAgent starting scan of {target}")
        
        # Execute analysis primitive
        result = self.analyze_primitive.execute(
            context,
            target,
            deep_analysis=scan_options.get("deep_analysis", False)
        )
        
        if not result.success:
            context.add_observation(f"Scan failed: {result.output}")
            return {"success": False, "error": result.output}
        
        findings = result.metadata.get("findings", [])
        context.add_observation(f"Scanner found {len(findings)} potential issues")
        
        # Organize findings by severity
        organized_findings = self._organize_findings(findings)
        
        return {
            "success": True,
            "findings_count": len(findings),
            "findings": findings,
            "organized": organized_findings,
            "metadata": result.metadata
        }
    
    def _organize_findings(self, findings: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize findings by severity/category"""
        organized = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": []
        }
        
        for finding in findings:
            # Try to determine severity from description or pattern
            description = finding.get("description", "").lower()
            if "sql injection" in description or "command injection" in description:
                organized["critical"].append(finding)
            elif "xss" in description or "path traversal" in description:
                organized["high"].append(finding)
            else:
                organized["medium"].append(finding)
        
        return organized


class AnalyzerAgent(Agent):
    """
    Analyzer Agent: Deep analysis and vulnerability assessment.
    
    Responsibilities:
    - Perform deep security analysis
    - Understand attack vectors
    - Assess exploitability
    - Provide technical details
    """
    
    def __init__(self, name: str = "SecurityAnalyzer"):
        super().__init__(name=name, role=AgentRole.RESEARCHER)
        self.think_primitive = ThinkSecurityPrimitive()
        self.detect_primitive = DetectVulnerabilityPrimitive()
        self.kb = VulnerabilityKnowledgeBase()
    
    def execute(self, context: ExecutionContext, findings: List[Dict],
                focus_areas: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze findings in depth.
        
        Args:
            context: Execution context
            findings: Findings from scanner
            focus_areas: Optional areas to focus on
        
        Returns:
            Dictionary with analysis results
        """
        context.add_observation(f"AnalyzerAgent analyzing {len(findings)} findings")
        
        analyzed_findings = []
        
        # Analyze each finding
        for finding in findings[:10]:  # Limit to top 10 for performance
            analysis = self._analyze_finding(context, finding, focus_areas)
            if analysis:
                analyzed_findings.append(analysis)
        
        context.add_observation(f"Completed analysis of {len(analyzed_findings)} findings")
        
        # Generate summary
        summary = self._generate_summary(analyzed_findings)
        
        return {
            "success": True,
            "analyzed_count": len(analyzed_findings),
            "findings": analyzed_findings,
            "summary": summary
        }
    
    def _analyze_finding(self, context: ExecutionContext, finding: Dict,
                        focus_areas: Optional[List[str]]) -> Optional[Dict]:
        """Analyze a single finding"""
        # Extract code if available
        code = finding.get("match", "") or finding.get("snippet", "")
        if not code:
            return None
        
        # Get context
        code_context = finding.get("context", code)
        
        # Use think primitive for analysis
        result = self.think_primitive.execute(
            context,
            code_context,
            focus=focus_areas[0] if focus_areas else None
        )
        
        if result.success:
            # Enhance finding with analysis
            finding["analysis"] = result.output
            finding["vulnerabilities"] = result.metadata.get("vulnerabilities", [])
            finding["severity_assessment"] = result.metadata.get("severity_counts", {})
            return finding
        
        return None
    
    def _generate_summary(self, findings: List[Dict]) -> str:
        """Generate analysis summary"""
        if not findings:
            return "No findings to analyze"
        
        summary = f"Analyzed {len(findings)} findings:\n\n"
        
        # Count vulnerability types
        vuln_types = {}
        for finding in findings:
            for vuln in finding.get("vulnerabilities", []):
                cwe_id = vuln.get("cwe_id")
                if cwe_id:
                    vuln_types[cwe_id] = vuln_types.get(cwe_id, 0) + 1
        
        if vuln_types:
            summary += "Vulnerability Distribution:\n"
            for cwe_id, count in sorted(vuln_types.items(), key=lambda x: x[1], reverse=True):
                pattern = self.kb.get_pattern(cwe_id)
                name = pattern.name if pattern else "Unknown"
                summary += f"  • {cwe_id} ({name}): {count}\n"
        
        return summary


class ValidatorAgent(Agent):
    """
    Validator Agent: Verification and false positive elimination.
    
    Responsibilities:
    - Validate findings
    - Eliminate false positives
    - Assess confidence levels
    - Confirm exploitability
    """
    
    def __init__(self, name: str = "SecurityValidator"):
        super().__init__(name=name, role=AgentRole.REVIEWER)
        self.validate_primitive = ValidateFindingPrimitive()
    
    def execute(self, context: ExecutionContext, findings: List[Dict]) -> Dict[str, Any]:
        """
        Validate findings.
        
        Args:
            context: Execution context
            findings: Findings to validate
        
        Returns:
            Dictionary with validation results
        """
        context.add_observation(f"ValidatorAgent validating {len(findings)} findings")
        
        validated_findings = []
        false_positives = []
        
        for finding in findings:
            validation = self._validate_finding(context, finding)
            
            if validation and validation.get("valid"):
                finding["validated"] = True
                finding["confidence"] = validation.get("confidence", "medium")
                finding["validation_notes"] = validation.get("output", "")
                validated_findings.append(finding)
            else:
                finding["validated"] = False
                finding["false_positive_reason"] = validation.get("output", "") if validation else "Unknown"
                false_positives.append(finding)
        
        context.add_observation(
            f"Validation complete: {len(validated_findings)} confirmed, "
            f"{len(false_positives)} false positives"
        )
        
        return {
            "success": True,
            "validated_count": len(validated_findings),
            "false_positive_count": len(false_positives),
            "validated_findings": validated_findings,
            "false_positives": false_positives
        }
    
    def _validate_finding(self, context: ExecutionContext, 
                         finding: Dict) -> Optional[Dict]:
        """Validate a single finding"""
        # Extract code context
        code_context = finding.get("context", "") or finding.get("match", "")
        if not code_context:
            return None
        
        # Need CWE ID for validation
        cwe_id = finding.get("cwe_id")
        if not cwe_id:
            # Try to extract from vulnerabilities
            vulns = finding.get("vulnerabilities", [])
            if vulns:
                cwe_id = vulns[0].get("cwe_id")
        
        if not cwe_id:
            return None
        
        # Prepare finding for validation
        validation_finding = {
            "cwe_id": cwe_id,
            "message": finding.get("description", ""),
            "file": finding.get("file", ""),
            "line": finding.get("line", 0)
        }
        
        # Execute validation primitive
        result = self.validate_primitive.execute(
            context,
            validation_finding,
            code_context
        )
        
        if result.success:
            return {
                "valid": result.metadata.get("valid", False),
                "confidence": result.metadata.get("confidence", "medium"),
                "output": result.output
            }
        
        return None


class ReporterAgent(Agent):
    """
    Reporter Agent: Results compilation and reporting.
    
    Responsibilities:
    - Compile final report
    - Prioritize findings
    - Provide remediation guidance
    - Generate actionable recommendations
    """
    
    def __init__(self, name: str = "SecurityReporter"):
        super().__init__(name=name, role=AgentRole.WRITER)
        self.recommend_primitive = RecommendFixPrimitive()
        self.kb = VulnerabilityKnowledgeBase()
    
    def execute(self, context: ExecutionContext, 
                validated_findings: List[Dict]) -> Dict[str, Any]:
        """
        Generate final report.
        
        Args:
            context: Execution context
            validated_findings: Validated vulnerability findings
        
        Returns:
            Dictionary with report data
        """
        context.add_observation(f"ReporterAgent generating report for {len(validated_findings)} findings")
        
        # Add remediation recommendations
        findings_with_fixes = []
        for finding in validated_findings:
            fix = self._get_remediation(context, finding)
            if fix:
                finding["remediation"] = fix
            findings_with_fixes.append(finding)
        
        # Generate report
        report = self._generate_report(findings_with_fixes)
        
        context.add_observation("Report generation complete")
        
        return {
            "success": True,
            "report": report,
            "findings": findings_with_fixes,
            "summary": self._generate_executive_summary(findings_with_fixes)
        }
    
    def _get_remediation(self, context: ExecutionContext, 
                        finding: Dict) -> Optional[str]:
        """Get remediation for a finding"""
        # Extract vulnerability info
        cwe_id = finding.get("cwe_id")
        if not cwe_id:
            vulns = finding.get("vulnerabilities", [])
            if vulns:
                cwe_id = vulns[0].get("cwe_id")
        
        if not cwe_id:
            return None
        
        code = finding.get("context", "") or finding.get("match", "")
        if not code:
            return None
        
        # Prepare vulnerability for recommendation
        vulnerability = {"cwe_id": cwe_id}
        
        # Execute recommendation primitive
        result = self.recommend_primitive.execute(context, vulnerability, code)
        
        if result.success:
            return result.output
        
        return None
    
    def _generate_report(self, findings: List[Dict]) -> str:
        """Generate detailed security report"""
        report = "=" * 80 + "\n"
        report += "JAVA SECURITY VULNERABILITY DETECTION REPORT\n"
        report += "=" * 80 + "\n\n"
        
        # Executive summary
        report += "EXECUTIVE SUMMARY\n"
        report += "-" * 80 + "\n"
        report += f"Total Vulnerabilities Found: {len(findings)}\n\n"
        
        # Count by severity
        severity_counts = {}
        for finding in findings:
            severity = finding.get("severity", "medium")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        for severity in ["critical", "high", "medium", "low"]:
            count = severity_counts.get(severity, 0)
            if count > 0:
                report += f"  {severity.upper()}: {count}\n"
        
        report += "\n"
        
        # Detailed findings
        report += "DETAILED FINDINGS\n"
        report += "-" * 80 + "\n\n"
        
        for i, finding in enumerate(findings, 1):
            report += f"[{i}] "
            
            # Get CWE info
            cwe_id = finding.get("cwe_id", "UNKNOWN")
            pattern = self.kb.get_pattern(cwe_id)
            name = pattern.name if pattern else finding.get("name", "Unknown Vulnerability")
            
            report += f"{name} ({cwe_id})\n"
            report += f"    Severity: {finding.get('severity', 'UNKNOWN').upper()}\n"
            report += f"    Confidence: {finding.get('confidence', 'medium').upper()}\n"
            report += f"    Location: {finding.get('file', 'unknown')} line {finding.get('line', 0)}\n"
            
            if finding.get("analysis"):
                report += f"\n    Analysis:\n"
                # Truncate analysis if too long
                analysis = finding["analysis"][:500]
                report += f"    {analysis}\n"
            
            if finding.get("remediation"):
                report += f"\n    Remediation:\n"
                # Truncate remediation if too long
                remediation = finding["remediation"][:500]
                report += f"    {remediation}\n"
            
            report += "\n"
        
        report += "=" * 80 + "\n"
        report += "END OF REPORT\n"
        report += "=" * 80 + "\n"
        
        return report
    
    def _generate_executive_summary(self, findings: List[Dict]) -> str:
        """Generate executive summary"""
        summary = f"Found {len(findings)} confirmed vulnerabilities.\n\n"
        
        # Priority issues
        critical = [f for f in findings if f.get("severity") == "critical"]
        high = [f for f in findings if f.get("severity") == "high"]
        
        if critical:
            summary += f"CRITICAL: {len(critical)} critical vulnerabilities require immediate attention.\n"
        if high:
            summary += f"HIGH: {len(high)} high-severity issues should be addressed soon.\n"
        
        summary += "\nRecommended Actions:\n"
        summary += "1. Address all critical vulnerabilities immediately\n"
        summary += "2. Review and fix high-severity issues\n"
        summary += "3. Plan remediation for medium/low severity findings\n"
        
        return summary
