"""
Java Security Vulnerability Detection Domain

An intelligent, autonomous vulnerability detection system for Java applications,
powered by Brainary cognitive architecture. Combines LLM reasoning with
static analysis tools (CodeQL) for accurate, context-aware security analysis.

Key Features:
- Multi-agent detection system (Scanner, Analyzer, Validator, Reporter)
- Domain-specific primitives (AnalyzeCode, DetectVulnerability, ThinkSecurity, ValidateFinding, RecommendFix)
- CodeQL integration as agent tool
- OWASP Top 10 and CWE knowledge base (15 vulnerability patterns)
- Intelligent, autonomous operation with high accuracy

Example Usage:
    >>> from brainary.domains.java_security import JavaSecurityDetector, DetectionConfig
    >>> 
    >>> # Quick scan
    >>> detector = JavaSecurityDetector()
    >>> result = detector.quick_scan("path/to/java/project")
    >>> print(result["summary"])
    >>> 
    >>> # Thorough scan with validation and remediation
    >>> result = detector.thorough_scan("path/to/java/project", focus_areas=["injection"])
    >>> detector.export_report("security_report.txt")
"""

__version__ = '1.0.0'

from .detector import JavaSecurityDetector, DetectionConfig
from .agents import (
    ScannerAgent,
    AnalyzerAgent,
    ValidatorAgent,
    ReporterAgent,
    SecurityFinding
)
from .primitives import (
    AnalyzeCodePrimitive,
    DetectVulnerabilityPrimitive,
    ThinkSecurityPrimitive,
    ValidateFindingPrimitive,
    RecommendFixPrimitive
)
from .knowledge import (
    VulnerabilityKnowledgeBase,
    VulnerabilityPattern,
    VulnerabilitySeverity,
    VulnerabilityCategory
)
from .tools import (
    CodeQLTool,
    PatternMatcher,
    SecurityScanner,
    ToolResult,
    ToolStatus
)

__all__ = [
    # Main API
    'JavaSecurityDetector',
    'DetectionConfig',
    
    # Agents
    'ScannerAgent',
    'AnalyzerAgent',
    'ValidatorAgent',
    'ReporterAgent',
    'SecurityFinding',
    
    # Primitives
    'AnalyzeCodePrimitive',
    'DetectVulnerabilityPrimitive',
    'ThinkSecurityPrimitive',
    'ValidateFindingPrimitive',
    'RecommendFixPrimitive',
    
    # Knowledge
    'VulnerabilityKnowledgeBase',
    'VulnerabilityPattern',
    'VulnerabilitySeverity',
    'VulnerabilityCategory',
    
    # Tools
    'CodeQLTool',
    'PatternMatcher',
    'SecurityScanner',
    'ToolResult',
    'ToolStatus',
]
