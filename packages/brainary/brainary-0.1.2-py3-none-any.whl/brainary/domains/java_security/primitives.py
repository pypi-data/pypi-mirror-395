"""
Java Security Domain Primitives

Specialized primitives for vulnerability detection and security analysis.
"""

from typing import Any, Dict, List, Optional, Tuple
from brainary.primitive.base import CorePrimitive, PrimitiveResult
from brainary.core.context import ExecutionContext

from .knowledge import VulnerabilityKnowledgeBase, VulnerabilityPattern
from .tools import SecurityScanner, ToolResult, ToolStatus


class ThinkSecurityPrimitive(CorePrimitive):
    """
    Security-focused reasoning primitive.
    
    Analyzes code from a security perspective, identifying potential
    vulnerabilities and attack vectors using LLM reasoning.
    """
    
    def __init__(self):
        super().__init__()
        self.kb = VulnerabilityKnowledgeBase()
    
    def execute(self, context: ExecutionContext, code: str, 
                focus: Optional[str] = None) -> PrimitiveResult:
        """
        Think about security implications of code.
        
        Args:
            context: Execution context
            code: Code to analyze
            focus: Optional focus area (e.g., "injection", "crypto")
        
        Returns:
            PrimitiveResult with security analysis
        """
        # Build prompt for security analysis
        system_prompt = """You are a security expert specializing in Java vulnerability detection.
Analyze code for security vulnerabilities, focusing on OWASP Top 10 and common CWE patterns.

For each potential vulnerability:
1. Identify the specific CWE/OWASP category
2. Explain why it's vulnerable
3. Assess the severity and exploitability
4. Suggest specific remediation
"""
        
        # Add focus-specific guidance
        if focus:
            patterns = self.kb.search(focus)
            if patterns:
                system_prompt += f"\n\nFocus on these vulnerability types:\n"
                for pattern in patterns[:3]:
                    system_prompt += f"- {pattern.name} ({pattern.cwe_id}): {pattern.description}\n"
        
        user_prompt = f"""Analyze this Java code for security vulnerabilities:

```java
{code}
```

Provide a detailed security analysis including:
1. Identified vulnerabilities (with CWE IDs)
2. Severity assessment
3. Attack scenarios
4. Remediation recommendations
"""
        
        # Construct conversation with history
        messages = self.construct_conversation(
            context,
            system_message=system_prompt,
            user_message=user_prompt
        )
        
        # Execute with LLM
        response = context.execute_llm(messages)
        
        # Parse analysis from response
        analysis = self._parse_security_analysis(response)
        
        return PrimitiveResult(
            success=True,
            output=response,
            metadata={
                "vulnerabilities": analysis.get("vulnerabilities", []),
                "focus": focus,
                "severity_counts": analysis.get("severity_counts", {})
            }
        )
    
    def _parse_security_analysis(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured analysis"""
        # Simple parsing - extract CWE mentions
        import re
        
        vulnerabilities = []
        cwe_pattern = re.compile(r'CWE-\d+')
        
        for match in cwe_pattern.finditer(response):
            cwe_id = match.group(0)
            pattern = self.kb.get_pattern(cwe_id)
            if pattern:
                vulnerabilities.append({
                    "cwe_id": cwe_id,
                    "name": pattern.name,
                    "severity": pattern.severity.value
                })
        
        # Count severities
        severity_counts = {}
        for vuln in vulnerabilities:
            severity = vuln["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            "vulnerabilities": vulnerabilities,
            "severity_counts": severity_counts
        }


class AnalyzeCodePrimitive(CorePrimitive):
    """
    Code analysis primitive combining static analysis and LLM insights.
    
    Uses security tools (CodeQL, pattern matching) and LLM reasoning
    for comprehensive analysis.
    """
    
    def __init__(self):
        super().__init__()
        self.scanner = SecurityScanner(use_codeql=False)  # Pattern-based for speed
    
    def execute(self, context: ExecutionContext, target: str,
                deep_analysis: bool = False) -> PrimitiveResult:
        """
        Analyze code for vulnerabilities.
        
        Args:
            context: Execution context
            target: File or directory to analyze
            deep_analysis: Whether to use deep LLM analysis
        
        Returns:
            PrimitiveResult with analysis results
        """
        # Run static analysis
        scan_results = self.scanner.scan(target, use_codeql=False, use_patterns=True)
        
        # Extract findings
        all_findings = []
        for tool_result in scan_results.values():
            if tool_result.status == ToolStatus.SUCCESS:
                all_findings.extend(tool_result.findings)
        
        # If deep analysis requested, use LLM for validation
        if deep_analysis and all_findings:
            validated_findings = self._validate_with_llm(context, all_findings[:5])
            
            return PrimitiveResult(
                success=True,
                output=f"Found {len(all_findings)} potential issues, validated {len(validated_findings)}",
                metadata={
                    "findings": all_findings,
                    "validated": validated_findings,
                    "scan_results": {k: {"status": v.status.value, "count": len(v.findings)} 
                                    for k, v in scan_results.items()}
                }
            )
        else:
            return PrimitiveResult(
                success=True,
                output=f"Found {len(all_findings)} potential issues",
                metadata={
                    "findings": all_findings,
                    "scan_results": {k: {"status": v.status.value, "count": len(v.findings)} 
                                    for k, v in scan_results.items()}
                }
            )
    
    def _validate_with_llm(self, context: ExecutionContext, 
                          findings: List[Dict]) -> List[Dict]:
        """Use LLM to validate findings and reduce false positives"""
        validated = []
        
        for finding in findings:
            # Build validation prompt
            system_prompt = "You are a security expert. Validate if this is a true vulnerability or false positive."
            
            user_prompt = f"""
Pattern detected: {finding.get('pattern', 'unknown')}
File: {finding.get('file', 'unknown')}
Line: {finding.get('line', 0)}
Match: {finding.get('match', '')}

Context:
{finding.get('context', '')}

Is this a true vulnerability or false positive? Explain briefly.
"""
            
            messages = self.construct_conversation(
                context,
                system_message=system_prompt,
                user_message=user_prompt
            )
            
            response = context.execute_llm(messages)
            
            # Simple validation - check if LLM confirms vulnerability
            if "true vulnerability" in response.lower() or "vulnerable" in response.lower():
                finding["validation"] = response
                finding["confirmed"] = True
                validated.append(finding)
        
        return validated


class DetectVulnerabilityPrimitive(CorePrimitive):
    """
    Specialized vulnerability detection primitive.
    
    Focuses on specific vulnerability types using knowledge base
    and targeted detection strategies.
    """
    
    def __init__(self):
        super().__init__()
        self.kb = VulnerabilityKnowledgeBase()
    
    def execute(self, context: ExecutionContext, code: str,
                vulnerability_types: Optional[List[str]] = None) -> PrimitiveResult:
        """
        Detect specific vulnerability types.
        
        Args:
            context: Execution context
            code: Code to analyze
            vulnerability_types: CWE IDs or categories to focus on
        
        Returns:
            PrimitiveResult with detections
        """
        # Get patterns to check
        patterns_to_check = []
        if vulnerability_types:
            for vuln_type in vulnerability_types:
                if vuln_type.startswith("CWE-"):
                    pattern = self.kb.get_pattern(vuln_type)
                    if pattern:
                        patterns_to_check.append(pattern)
                else:
                    # Search by name/category
                    patterns_to_check.extend(self.kb.search(vuln_type))
        else:
            # Check all high/critical severity patterns
            from .knowledge import VulnerabilitySeverity
            patterns_to_check.extend(self.kb.get_by_severity(VulnerabilitySeverity.CRITICAL))
            patterns_to_check.extend(self.kb.get_by_severity(VulnerabilitySeverity.HIGH))
        
        # Build detection prompt
        system_prompt = """You are a vulnerability detection expert.
Analyze the code and determine if it contains the specified vulnerabilities.
Be precise and avoid false positives."""
        
        vulnerability_descriptions = "\n".join([
            f"- {p.cwe_id} ({p.name}): {p.description}\n  Indicators: {', '.join(p.indicators[:3])}"
            for p in patterns_to_check[:5]
        ])
        
        user_prompt = f"""Check for these vulnerabilities:

{vulnerability_descriptions}

Code to analyze:
```java
{code}
```

For each vulnerability found:
1. State the CWE ID and name
2. Point to the vulnerable code
3. Explain why it's vulnerable
4. Rate confidence (high/medium/low)
"""
        
        messages = self.construct_conversation(
            context,
            system_message=system_prompt,
            user_message=user_prompt
        )
        
        response = context.execute_llm(messages)
        
        # Parse detections
        detections = self._parse_detections(response, patterns_to_check)
        
        return PrimitiveResult(
            success=True,
            output=response,
            metadata={
                "detections": detections,
                "patterns_checked": [p.cwe_id for p in patterns_to_check]
            }
        )
    
    def _parse_detections(self, response: str, 
                         patterns: List[VulnerabilityPattern]) -> List[Dict]:
        """Parse LLM response into structured detections"""
        import re
        
        detections = []
        
        # Extract CWE mentions with confidence
        for pattern in patterns:
            if pattern.cwe_id in response:
                # Try to extract confidence
                confidence = "medium"
                if "high confidence" in response.lower():
                    confidence = "high"
                elif "low confidence" in response.lower():
                    confidence = "low"
                
                detections.append({
                    "cwe_id": pattern.cwe_id,
                    "name": pattern.name,
                    "severity": pattern.severity.value,
                    "confidence": confidence,
                    "pattern": pattern
                })
        
        return detections


class ValidateFindingPrimitive(CorePrimitive):
    """
    Validation primitive for verifying vulnerability findings.
    
    Performs deep analysis to confirm vulnerabilities and eliminate
    false positives using multi-perspective reasoning.
    """
    
    def __init__(self):
        super().__init__()
        self.kb = VulnerabilityKnowledgeBase()
    
    def execute(self, context: ExecutionContext, finding: Dict[str, Any],
                code_context: str) -> PrimitiveResult:
        """
        Validate a vulnerability finding.
        
        Args:
            context: Execution context
            finding: Finding to validate (must include cwe_id)
            code_context: Surrounding code context
        
        Returns:
            PrimitiveResult with validation result
        """
        cwe_id = finding.get("cwe_id", "")
        pattern = self.kb.get_pattern(cwe_id)
        
        if not pattern:
            return PrimitiveResult(
                success=False,
                output="Unknown vulnerability type",
                metadata={"valid": False, "reason": "Unknown CWE"}
            )
        
        # Build validation prompt with detailed checks
        system_prompt = f"""You are a security validation expert.
Validate if this is a TRUE VULNERABILITY or FALSE POSITIVE.

Vulnerability Type: {pattern.name} ({pattern.cwe_id})
Description: {pattern.description}

False Positive Checks:
{chr(10).join('- ' + check for check in pattern.false_positive_checks)}

Be thorough and consider:
1. Is user input actually involved?
2. Are there mitigating controls?
3. Is the vulnerable code actually reachable?
4. Does the context make it exploitable?
"""
        
        user_prompt = f"""
Finding: {finding.get('message', 'Potential vulnerability detected')}
Location: {finding.get('file', 'unknown')} line {finding.get('line', 0)}

Code Context:
```java
{code_context}
```

Is this a TRUE VULNERABILITY or FALSE POSITIVE?

Provide:
1. Verdict (TRUE VULNERABILITY / FALSE POSITIVE)
2. Confidence level (high/medium/low)
3. Reasoning
4. If true vulnerability: exploitability assessment
5. If false positive: what mitigates it
"""
        
        messages = self.construct_conversation(
            context,
            system_message=system_prompt,
            user_message=user_prompt
        )
        
        response = context.execute_llm(messages)
        
        # Parse validation result
        is_valid = "true vulnerability" in response.lower()
        confidence = self._extract_confidence(response)
        
        return PrimitiveResult(
            success=True,
            output=response,
            metadata={
                "valid": is_valid,
                "confidence": confidence,
                "cwe_id": cwe_id,
                "finding": finding
            }
        )
    
    def _extract_confidence(self, response: str) -> str:
        """Extract confidence level from response"""
        response_lower = response.lower()
        if "high confidence" in response_lower or "confidence: high" in response_lower:
            return "high"
        elif "low confidence" in response_lower or "confidence: low" in response_lower:
            return "low"
        else:
            return "medium"


class RecommendFixPrimitive(CorePrimitive):
    """
    Fix recommendation primitive.
    
    Provides specific, actionable remediation guidance for vulnerabilities.
    """
    
    def __init__(self):
        super().__init__()
        self.kb = VulnerabilityKnowledgeBase()
    
    def execute(self, context: ExecutionContext, vulnerability: Dict[str, Any],
                code: str) -> PrimitiveResult:
        """
        Recommend fix for vulnerability.
        
        Args:
            context: Execution context
            vulnerability: Vulnerability details (must include cwe_id)
            code: Vulnerable code
        
        Returns:
            PrimitiveResult with fix recommendations
        """
        cwe_id = vulnerability.get("cwe_id", "")
        pattern = self.kb.get_pattern(cwe_id)
        
        if not pattern:
            return PrimitiveResult(
                success=False,
                output="Cannot recommend fix for unknown vulnerability",
                metadata={"has_fix": False}
            )
        
        # Build fix recommendation prompt
        system_prompt = f"""You are a security remediation expert.
Provide specific, actionable fixes for {pattern.name} ({pattern.cwe_id}).

General Remediation: {pattern.remediation}

Secure Alternatives:
{chr(10).join('- ' + alt for alt in pattern.secure_alternatives)}

Secure Example:
{pattern.secure_example}
"""
        
        user_prompt = f"""
Vulnerable Code:
```java
{code}
```

Provide a SPECIFIC FIX for this code:
1. Exact code changes needed
2. Line-by-line transformation
3. Additional security measures
4. Testing recommendations

Be concrete and actionable.
"""
        
        messages = self.construct_conversation(
            context,
            system_message=system_prompt,
            user_message=user_prompt
        )
        
        response = context.execute_llm(messages)
        
        return PrimitiveResult(
            success=True,
            output=response,
            metadata={
                "has_fix": True,
                "cwe_id": cwe_id,
                "pattern": pattern.name,
                "secure_alternatives": pattern.secure_alternatives
            }
        )
