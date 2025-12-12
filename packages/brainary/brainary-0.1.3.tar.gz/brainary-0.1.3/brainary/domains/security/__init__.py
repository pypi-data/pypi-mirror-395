"""
Security Domain for Brainary

Provides vulnerability detection, security analysis, and threat assessment capabilities.
"""

from brainary.domains.security.vulnerability_detector import (
    VulnerabilityDetector,
    VulnerabilityReport,
    VulnerabilitySeverity,
    VulnerabilityType,
)
from brainary.domains.security.primitives import (
    PerceiveCode,
    AnalyzeVulnerabilities,
    ValidateSecurityControls,
)
from brainary.domains.security.cwe_database import CWEDatabase, CWEInfo

__all__ = [
    # Main detector
    "VulnerabilityDetector",
    "VulnerabilityReport",
    "VulnerabilitySeverity",
    "VulnerabilityType",
    # Primitives
    "PerceiveCode",
    "AnalyzeVulnerabilities",
    "ValidateSecurityControls",
    # CWE database
    "CWEDatabase",
    "CWEInfo",
]
