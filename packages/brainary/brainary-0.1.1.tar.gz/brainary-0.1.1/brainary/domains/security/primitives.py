"""
Security Analysis Primitives

Updated primitives for vulnerability detection using the new security domain library.
"""

from typing import Any, Dict, List, Optional
import time
import logging

from brainary.primitive.base import (
    CorePrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.llm.manager import get_llm_manager
from brainary.domains.security.vulnerability_detector import VulnerabilityDetector
from brainary.domains.security.cwe_database import CWEDatabase

logger = logging.getLogger(__name__)


class PerceiveCode(CorePrimitive):
    """
    Perceive and parse code from repository.
    
    Enhanced with vulnerability pattern detection.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "perceive_code"
        self._hint = (
            "Use to parse and analyze source code structure. Extracts code patterns, "
            "identifies potential vulnerability indicators, and prepares code for "
            "security analysis. Use when ingesting code for vulnerability scanning."
        )
        self.detector = VulnerabilityDetector()
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs for code perception."""
        if "code" not in kwargs and "file_path" not in kwargs:
            raise ValueError("Either 'code' or 'file_path' must be provided")
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate resource cost for parsing code."""
        code = kwargs.get("code", "")
        lines = len(code.split("\n")) if code else 0
        
        return ResourceEstimate(
            tokens=lines * 10,
            latency_ms=50,
            memory_slots=1,
        )
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback code perception (no-op for read-only operation)."""
        pass  # Read-only operation, nothing to rollback
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        code: Optional[str] = None,
        file_path: Optional[str] = None,
        **kwargs
    ) -> PrimitiveResult:
        """
        Parse code and extract structure.
        
        Args:
            context: Execution context
            working_memory: Working memory
            code: Source code string
            file_path: Optional file path
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with parsed code data
        """
        start_time = time.time()
        
        if code is None and file_path is None:
            return PrimitiveResult(
                success=False,
                content=None,
                error="Either 'code' or 'file_path' must be provided",
                confidence=ConfidenceMetrics(overall=0.0),
                cost=CostMetrics(tokens=0, latency_ms=0),
                execution_mode=context.execution_mode,
                primitive_name=self._name,
            )
        
        # Read code from file if needed
        if code is None and file_path:
            try:
                with open(file_path, 'r') as f:
                    code = f.read()
            except Exception as e:
                return PrimitiveResult(
                    success=False,
                    content=None,
                    error=f"Failed to read file: {e}",
                    confidence=ConfidenceMetrics(overall=0.0),
                    cost=CostMetrics(tokens=0, latency_ms=0),
                    execution_mode=context.execution_mode,
                    primitive_name=self._name,
                )
        
        # Parse code structure
        lines = code.split("\n")
        
        # Quick pattern-based vulnerability detection
        patterns = self._extract_patterns(code)
        
        # Prepare parsed data
        parsed_data = {
            "file_path": file_path or "unknown",
            "lines": len(lines),
            "code": code,
            "patterns": patterns,
            "has_suspicious_patterns": len(patterns) > 0,
        }
        
        # Store in working memory
        memory_id = working_memory.store(
            content=parsed_data,
            importance=0.7,
            tags=["code", "parsed", file_path or "unknown"],
        )
        
        execution_time = (time.time() - start_time) * 1000
        
        return PrimitiveResult(
            success=True,
            content=parsed_data,
            confidence=ConfidenceMetrics(overall=0.95),
            cost=CostMetrics(
                tokens=len(lines) * 10,
                latency_ms=execution_time,
                memory_slots=1,
            ),
            execution_mode=context.execution_mode,
            primitive_name=self._name,
            metadata={
                "memory_id": memory_id,
                "pattern_count": len(patterns),
            }
        )
    
    def _extract_patterns(self, code: str) -> List[str]:
        """Extract potential vulnerability patterns."""
        patterns = []
        
        # Use detector's initial pattern detection
        # This is a lightweight check before full analysis
        if 'execute(' in code and ('+' in code or 'f"' in code) and 'SELECT' in code.upper():
            patterns.append("sql_concatenation")
        
        if ('<' in code and '>' in code) and '+' in code:
            patterns.append("html_concatenation")
        
        if any(kw in code.upper() for kw in ['PASSWORD', 'API_KEY', 'SECRET']):
            if '=' in code and ('"' in code or "'" in code):
                patterns.append("hardcoded_credentials")
        
        if 'open(' in code and '+' in code:
            patterns.append("path_concatenation")
        
        if 'random.randint' in code or 'random.random' in code:
            patterns.append("weak_random")
        
        if 'pickle.load' in code or 'yaml.load' in code:
            patterns.append("insecure_deserialization")
        
        if 'os.system(' in code or ('subprocess' in code and 'shell=True' in code):
            patterns.append("command_injection")
        
        if 'MD5' in code or 'md5' in code or 'SHA1' in code or 'sha1' in code:
            patterns.append("weak_crypto")
        
        if 'requests.' in code or 'urlopen(' in code:
            patterns.append("potential_ssrf")
        
        if 'etree.parse' in code or 'ElementTree.parse' in code:
            patterns.append("potential_xxe")
        
        return patterns


class AnalyzeVulnerabilities(CorePrimitive):
    """
    Analyze code for security vulnerabilities using enhanced detector.
    
    Combines pattern matching with LLM-powered analysis.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "analyze_vulnerabilities"
        self._hint = (
            "Use to perform comprehensive security analysis on code. Detects "
            "vulnerabilities, assigns CWE IDs, determines severity, and provides "
            "mitigation guidance. Use after perceiving code structure."
        )
        self.detector = VulnerabilityDetector()
        self.cwe_db = CWEDatabase()
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs for vulnerability analysis."""
        if "code" not in kwargs and "parsed_code" not in kwargs:
            raise ValueError("Either 'code' or 'parsed_code' must be provided")
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate resource cost for vulnerability analysis."""
        code = kwargs.get("code", "")
        parsed_code = kwargs.get("parsed_code", {})
        
        code_lines = len(code.split("\n")) if code else parsed_code.get("lines", 0)
        estimated_tokens = code_lines * 15 + 500
        
        return ResourceEstimate(
            tokens=estimated_tokens,
            latency_ms=2000,
            memory_slots=2,
        )
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback vulnerability analysis (no-op for read-only operation)."""
        pass  # Read-only operation, nothing to rollback
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        code: Optional[str] = None,
        parsed_code: Optional[Dict[str, Any]] = None,
        enable_llm: bool = False,  # Disabled by default for testing
        **kwargs
    ) -> PrimitiveResult:
        """
        Analyze code for vulnerabilities.
        
        Args:
            context: Execution context
            working_memory: Working memory
            code: Raw code string
            parsed_code: Pre-parsed code data from PerceiveCode
            enable_llm: Whether to use LLM for enhanced analysis
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with vulnerability analysis
        """
        start_time = time.time()
        
        # Get code from parsed_code or direct input
        if parsed_code:
            code = parsed_code.get("code", code)
            file_path = parsed_code.get("file_path")
        else:
            file_path = kwargs.get("file_path")
        
        if not code:
            return PrimitiveResult(
                success=False,
                content=None,
                error="No code provided for analysis",
                confidence=ConfidenceMetrics(overall=0.0),
                cost=CostMetrics(tokens=0, latency_ms=0),
                execution_mode=context.execution_mode,
                primitive_name=self._name,
            )
        
        # Detect vulnerabilities using enhanced detector
        vulnerabilities = self.detector.detect_vulnerabilities(
            code=code,
            file_path=file_path,
            enable_llm=enable_llm
        )
        
        # Generate summary
        summary = self.detector.generate_summary(vulnerabilities)
        
        # Convert vulnerabilities to dict format
        vuln_list = [vuln.to_dict() for vuln in vulnerabilities]
        
        # Build result
        result_content = {
            "has_vulnerabilities": summary["has_vulnerabilities"],
            "vulnerabilities": vuln_list,
            "count": summary["total_vulnerabilities"],
            "summary": summary["summary"],
            "severity_breakdown": summary.get("severity_breakdown", {}),
            "type_breakdown": summary.get("type_breakdown", {}),
        }
        
        # Store in memory
        memory_id = working_memory.store(
            content=result_content,
            importance=0.9,
            tags=["vulnerabilities", "analysis", "security"],
        )
        
        execution_time = (time.time() - start_time) * 1000
        
        # Calculate confidence based on detection method
        confidence = 0.85 if vulnerabilities else 0.9
        
        return PrimitiveResult(
            success=True,
            content=result_content,
            confidence=ConfidenceMetrics(overall=confidence),
            cost=CostMetrics(
                tokens=len(code.split("\n")) * 15 + 500,
                latency_ms=execution_time,
                memory_slots=2,
            ),
            execution_mode=context.execution_mode,
            primitive_name=self._name,
            metadata={
                "memory_id": memory_id,
                "detection_method": "pattern_matching" if not enable_llm else "llm_enhanced",
                "cwe_count": len(set(v.cwe_id for v in vulnerabilities)),
            }
        )


class ValidateSecurityControls(CorePrimitive):
    """
    Validate presence and effectiveness of security controls.
    
    Checks for security best practices and defensive measures.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "validate_security_controls"
        self._hint = (
            "Use to validate security controls and best practices in code. "
            "Checks for input validation, output encoding, authentication, "
            "authorization, and other security measures."
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs for security control validation."""
        if "code" not in kwargs:
            raise ValueError("'code' parameter is required")
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate resource cost for security control validation."""
        code = kwargs.get("code", "")
        lines = len(code.split("\n")) if code else 0
        
        return ResourceEstimate(
            tokens=lines * 5,
            latency_ms=100,
            memory_slots=1,
        )
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback security control validation (no-op for read-only operation)."""
        pass  # Read-only operation, nothing to rollback
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        code: str,
        **kwargs
    ) -> PrimitiveResult:
        """
        Validate security controls.
        
        Args:
            context: Execution context
            working_memory: Working memory
            code: Source code
            **kwargs: Additional parameters
        
        Returns:
            PrimitiveResult with validation results
        """
        start_time = time.time()
        
        controls = {
            "input_validation": self._check_input_validation(code),
            "output_encoding": self._check_output_encoding(code),
            "authentication": self._check_authentication(code),
            "authorization": self._check_authorization(code),
            "crypto_usage": self._check_crypto(code),
            "error_handling": self._check_error_handling(code),
            "logging": self._check_logging(code),
        }
        
        # Calculate overall score
        present_controls = sum(1 for v in controls.values() if v["present"])
        total_controls = len(controls)
        security_score = present_controls / total_controls if total_controls > 0 else 0.0
        
        result = {
            "controls": controls,
            "security_score": security_score,
            "present_count": present_controls,
            "total_count": total_controls,
            "recommendation": self._generate_recommendation(security_score),
        }
        
        execution_time = (time.time() - start_time) * 1000
        
        return PrimitiveResult(
            success=True,
            content=result,
            confidence=ConfidenceMetrics(overall=0.8),
            cost=CostMetrics(
                tokens=len(code.split("\n")) * 5,
                latency_ms=execution_time,
                memory_slots=1,
            ),
            execution_mode=context.execution_mode,
            primitive_name=self._name,
        )
    
    def _check_input_validation(self, code: str) -> Dict[str, Any]:
        """Check for input validation."""
        indicators = [
            r'validate\(',
            r'isinstance\(',
            r'assert\s+\w+',
            r'raise\s+ValueError',
            r'if\s+not\s+\w+',
        ]
        
        import re
        present = any(re.search(pattern, code) for pattern in indicators)
        
        return {
            "present": present,
            "description": "Input validation checks" if present else "No input validation detected",
        }
    
    def _check_output_encoding(self, code: str) -> Dict[str, Any]:
        """Check for output encoding."""
        indicators = [r'escape\(', r'html\.escape', r'sanitize\(', r'encode\(']
        
        import re
        present = any(re.search(pattern, code) for pattern in indicators)
        
        return {
            "present": present,
            "description": "Output encoding present" if present else "No output encoding detected",
        }
    
    def _check_authentication(self, code: str) -> Dict[str, Any]:
        """Check for authentication."""
        indicators = [r'authenticate', r'login', r'verify_token', r'check_password']
        
        import re
        present = any(re.search(pattern, code, re.IGNORECASE) for pattern in indicators)
        
        return {
            "present": present,
            "description": "Authentication logic present" if present else "No authentication detected",
        }
    
    def _check_authorization(self, code: str) -> Dict[str, Any]:
        """Check for authorization."""
        indicators = [r'authorize', r'permission', r'access_control', r'@require_']
        
        import re
        present = any(re.search(pattern, code, re.IGNORECASE) for pattern in indicators)
        
        return {
            "present": present,
            "description": "Authorization checks present" if present else "No authorization detected",
        }
    
    def _check_crypto(self, code: str) -> Dict[str, Any]:
        """Check for cryptography usage."""
        indicators = [r'AES', r'RSA', r'secrets\.', r'hashlib\.sha256', r'bcrypt']
        
        import re
        present = any(re.search(pattern, code) for pattern in indicators)
        
        return {
            "present": present,
            "description": "Secure cryptography used" if present else "No cryptography detected",
        }
    
    def _check_error_handling(self, code: str) -> Dict[str, Any]:
        """Check for error handling."""
        indicators = [r'try:', r'except', r'raise', r'finally:']
        
        import re
        present = any(re.search(pattern, code) for pattern in indicators)
        
        return {
            "present": present,
            "description": "Error handling present" if present else "No error handling detected",
        }
    
    def _check_logging(self, code: str) -> Dict[str, Any]:
        """Check for security logging."""
        indicators = [r'logger\.', r'logging\.', r'log\(', r'audit']
        
        import re
        present = any(re.search(pattern, code, re.IGNORECASE) for pattern in indicators)
        
        return {
            "present": present,
            "description": "Logging present" if present else "No logging detected",
        }
    
    def _generate_recommendation(self, score: float) -> str:
        """Generate security recommendation."""
        if score >= 0.8:
            return "Good security posture. Continue monitoring."
        elif score >= 0.6:
            return "Moderate security. Consider adding missing controls."
        elif score >= 0.4:
            return "Weak security. Implement additional controls urgently."
        else:
            return "Critical: Minimal security controls detected. Immediate action required."
