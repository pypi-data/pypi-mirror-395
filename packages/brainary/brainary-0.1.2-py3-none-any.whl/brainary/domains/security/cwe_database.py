"""
CWE (Common Weakness Enumeration) Database

Provides structured information about security vulnerabilities based on CWE standard.
Updated with OWASP Top 10 2023 and modern vulnerability patterns.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class VulnerabilitySeverity(str, Enum):
    """Vulnerability severity levels following CVSS."""
    CRITICAL = "CRITICAL"  # 9.0-10.0
    HIGH = "HIGH"          # 7.0-8.9
    MEDIUM = "MEDIUM"      # 4.0-6.9
    LOW = "LOW"            # 0.1-3.9
    INFO = "INFO"          # 0.0


class VulnerabilityType(str, Enum):
    """Common vulnerability categories."""
    INJECTION = "INJECTION"
    BROKEN_AUTH = "BROKEN_AUTH"
    SENSITIVE_DATA = "SENSITIVE_DATA"
    XXE = "XXE"
    BROKEN_ACCESS = "BROKEN_ACCESS"
    SECURITY_MISCONFIG = "SECURITY_MISCONFIG"
    XSS = "XSS"
    INSECURE_DESERIALIZATION = "INSECURE_DESERIALIZATION"
    COMPONENTS_KNOWN_VULNS = "COMPONENTS_KNOWN_VULNS"
    INSUFFICIENT_LOGGING = "INSUFFICIENT_LOGGING"
    SSRF = "SSRF"
    PATH_TRAVERSAL = "PATH_TRAVERSAL"
    CRYPTO_FAILURE = "CRYPTO_FAILURE"
    OTHER = "OTHER"


@dataclass
class CWEInfo:
    """Information about a specific CWE."""
    cwe_id: str
    name: str
    description: str
    severity: VulnerabilitySeverity
    vulnerability_type: VulnerabilityType
    owasp_category: Optional[str] = None
    mitigation: Optional[str] = None
    examples: Optional[List[str]] = None
    references: Optional[List[str]] = None


class CWEDatabase:
    """
    Database of Common Weakness Enumerations (CWE).
    
    Updated for 2023-2024 with modern vulnerability patterns including:
    - OWASP Top 10 2021/2023
    - API Security Top 10
    - Cloud-native vulnerabilities
    - AI/ML security issues
    """
    
    def __init__(self):
        self._cwe_data = self._initialize_database()
    
    def _initialize_database(self) -> Dict[str, CWEInfo]:
        """Initialize CWE database with common vulnerabilities."""
        return {
            # === OWASP Top 10 2021 ===
            
            # A01:2021 - Broken Access Control
            "CWE-22": CWEInfo(
                cwe_id="CWE-22",
                name="Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')",
                description="Software uses external input to construct pathname intended to be within restricted directory, but doesn't properly neutralize special elements.",
                severity=VulnerabilitySeverity.HIGH,
                vulnerability_type=VulnerabilityType.PATH_TRAVERSAL,
                owasp_category="A01:2021 - Broken Access Control",
                mitigation="Use allowlist of acceptable paths. Validate and sanitize all inputs. Use path canonicalization.",
                examples=["../../../etc/passwd", "..\\..\\windows\\system32"],
                references=["https://cwe.mitre.org/data/definitions/22.html"]
            ),
            
            "CWE-79": CWEInfo(
                cwe_id="CWE-79",
                name="Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')",
                description="Software does not neutralize or incorrectly neutralizes user-controllable input before placing it in output used as web page.",
                severity=VulnerabilitySeverity.MEDIUM,
                vulnerability_type=VulnerabilityType.XSS,
                owasp_category="A03:2021 - Injection",
                mitigation="Use context-aware output encoding. Implement Content Security Policy. Validate and sanitize all user inputs.",
                examples=["<script>alert('XSS')</script>", "javascript:alert(1)"],
                references=["https://cwe.mitre.org/data/definitions/79.html"]
            ),
            
            "CWE-89": CWEInfo(
                cwe_id="CWE-89",
                name="Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')",
                description="Software constructs SQL commands using externally-influenced input but doesn't neutralize special elements.",
                severity=VulnerabilitySeverity.CRITICAL,
                vulnerability_type=VulnerabilityType.INJECTION,
                owasp_category="A03:2021 - Injection",
                mitigation="Use parameterized queries/prepared statements. Use ORM frameworks. Apply least privilege. Input validation.",
                examples=["' OR '1'='1", "1; DROP TABLE users--"],
                references=["https://cwe.mitre.org/data/definitions/89.html"]
            ),
            
            "CWE-798": CWEInfo(
                cwe_id="CWE-798",
                name="Use of Hard-coded Credentials",
                description="Software contains hard-coded credentials such as passwords or cryptographic keys.",
                severity=VulnerabilitySeverity.CRITICAL,
                vulnerability_type=VulnerabilityType.SENSITIVE_DATA,
                owasp_category="A07:2021 - Identification and Authentication Failures",
                mitigation="Use environment variables or secure vaults. Implement secrets management. Rotate credentials regularly.",
                examples=["PASSWORD = 'admin123'", "API_KEY = 'sk-1234567890'"],
                references=["https://cwe.mitre.org/data/definitions/798.html"]
            ),
            
            "CWE-327": CWEInfo(
                cwe_id="CWE-327",
                name="Use of a Broken or Risky Cryptographic Algorithm",
                description="Use of broken or risky cryptographic algorithm that is not recommended for use.",
                severity=VulnerabilitySeverity.HIGH,
                vulnerability_type=VulnerabilityType.CRYPTO_FAILURE,
                owasp_category="A02:2021 - Cryptographic Failures",
                mitigation="Use modern algorithms (AES-256, RSA-2048+). Avoid MD5, SHA1. Use TLS 1.2+. Regular crypto library updates.",
                examples=["MD5", "SHA1", "DES", "RC4"],
                references=["https://cwe.mitre.org/data/definitions/327.html"]
            ),
            
            "CWE-330": CWEInfo(
                cwe_id="CWE-330",
                name="Use of Insufficiently Random Values",
                description="Software uses insufficiently random values in security context.",
                severity=VulnerabilitySeverity.MEDIUM,
                vulnerability_type=VulnerabilityType.CRYPTO_FAILURE,
                owasp_category="A02:2021 - Cryptographic Failures",
                mitigation="Use cryptographically secure random number generators (secrets module in Python, SecureRandom in Java).",
                examples=["random.randint()", "Math.random()"],
                references=["https://cwe.mitre.org/data/definitions/330.html"]
            ),
            
            "CWE-502": CWEInfo(
                cwe_id="CWE-502",
                name="Deserialization of Untrusted Data",
                description="Application deserializes untrusted data without sufficiently verifying that data is valid.",
                severity=VulnerabilitySeverity.CRITICAL,
                vulnerability_type=VulnerabilityType.INSECURE_DESERIALIZATION,
                owasp_category="A08:2021 - Software and Data Integrity Failures",
                mitigation="Avoid deserializing untrusted data. Use safe parsers (JSON). Implement integrity checks. Type checking.",
                examples=["pickle.loads()", "yaml.load()", "unserialize()"],
                references=["https://cwe.mitre.org/data/definitions/502.html"]
            ),
            
            "CWE-611": CWEInfo(
                cwe_id="CWE-611",
                name="Improper Restriction of XML External Entity Reference",
                description="Software processes XML with XML parser that can resolve external entities.",
                severity=VulnerabilitySeverity.HIGH,
                vulnerability_type=VulnerabilityType.XXE,
                owasp_category="A05:2021 - Security Misconfiguration",
                mitigation="Disable XML external entities. Use less complex data formats (JSON). Validate XML schemas.",
                examples=["<!ENTITY xxe SYSTEM 'file:///etc/passwd'>"],
                references=["https://cwe.mitre.org/data/definitions/611.html"]
            ),
            
            "CWE-918": CWEInfo(
                cwe_id="CWE-918",
                name="Server-Side Request Forgery (SSRF)",
                description="Web application fetches remote resource without validating user-supplied URL.",
                severity=VulnerabilitySeverity.HIGH,
                vulnerability_type=VulnerabilityType.SSRF,
                owasp_category="A10:2021 - Server-Side Request Forgery",
                mitigation="Whitelist allowed domains/IPs. Disable redirects. Network segmentation. Input validation.",
                examples=["http://localhost/admin", "http://169.254.169.254/"],
                references=["https://cwe.mitre.org/data/definitions/918.html"]
            ),
            
            # === Additional Critical CWEs ===
            
            "CWE-78": CWEInfo(
                cwe_id="CWE-78",
                name="Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')",
                description="Software constructs OS commands using externally-influenced input.",
                severity=VulnerabilitySeverity.CRITICAL,
                vulnerability_type=VulnerabilityType.INJECTION,
                owasp_category="A03:2021 - Injection",
                mitigation="Use parameterized APIs. Validate input. Avoid shell execution. Use subprocess with shell=False.",
                examples=["; rm -rf /", "| cat /etc/passwd"],
                references=["https://cwe.mitre.org/data/definitions/78.html"]
            ),
            
            "CWE-787": CWEInfo(
                cwe_id="CWE-787",
                name="Out-of-bounds Write",
                description="Software writes data past end or before beginning of intended buffer.",
                severity=VulnerabilitySeverity.CRITICAL,
                vulnerability_type=VulnerabilityType.OTHER,
                owasp_category="Memory Safety",
                mitigation="Use memory-safe languages. Bounds checking. Address space layout randomization (ASLR).",
                examples=["Buffer overflow", "Heap overflow"],
                references=["https://cwe.mitre.org/data/definitions/787.html"]
            ),
            
            "CWE-862": CWEInfo(
                cwe_id="CWE-862",
                name="Missing Authorization",
                description="Software does not perform authorization check when user attempts to access resource.",
                severity=VulnerabilitySeverity.HIGH,
                vulnerability_type=VulnerabilityType.BROKEN_ACCESS,
                owasp_category="A01:2021 - Broken Access Control",
                mitigation="Implement proper authorization checks. Use RBAC/ABAC. Deny by default. Check on every request.",
                examples=["Direct object reference", "Privilege escalation"],
                references=["https://cwe.mitre.org/data/definitions/862.html"]
            ),
            
            "CWE-319": CWEInfo(
                cwe_id="CWE-319",
                name="Cleartext Transmission of Sensitive Information",
                description="Software transmits sensitive data in cleartext protocol.",
                severity=VulnerabilitySeverity.HIGH,
                vulnerability_type=VulnerabilityType.SENSITIVE_DATA,
                owasp_category="A02:2021 - Cryptographic Failures",
                mitigation="Use TLS/SSL for all sensitive data. Enforce HTTPS. Use encrypted protocols.",
                examples=["HTTP for passwords", "FTP for credentials"],
                references=["https://cwe.mitre.org/data/definitions/319.html"]
            ),
            
            "CWE-20": CWEInfo(
                cwe_id="CWE-20",
                name="Improper Input Validation",
                description="Product does not validate or incorrectly validates input.",
                severity=VulnerabilitySeverity.HIGH,
                vulnerability_type=VulnerabilityType.OTHER,
                owasp_category="A03:2021 - Injection",
                mitigation="Validate all inputs. Use allowlists. Type checking. Length limits. Format validation.",
                examples=["Missing validation", "Weak validation"],
                references=["https://cwe.mitre.org/data/definitions/20.html"]
            ),
            
            # === Modern/Cloud/API Vulnerabilities ===
            
            "CWE-1004": CWEInfo(
                cwe_id="CWE-1004",
                name="Sensitive Cookie Without 'HttpOnly' Flag",
                description="Software uses cookie to store sensitive information but doesn't use HttpOnly flag.",
                severity=VulnerabilitySeverity.MEDIUM,
                vulnerability_type=VulnerabilityType.SENSITIVE_DATA,
                owasp_category="A05:2021 - Security Misconfiguration",
                mitigation="Set HttpOnly flag on cookies. Use Secure flag. Set SameSite attribute.",
                examples=["Session cookie without HttpOnly"],
                references=["https://cwe.mitre.org/data/definitions/1004.html"]
            ),
            
            "CWE-352": CWEInfo(
                cwe_id="CWE-352",
                name="Cross-Site Request Forgery (CSRF)",
                description="Web application does not verify that request was intentionally provided by user.",
                severity=VulnerabilitySeverity.MEDIUM,
                vulnerability_type=VulnerabilityType.BROKEN_AUTH,
                owasp_category="A01:2021 - Broken Access Control",
                mitigation="Use CSRF tokens. Check Referer header. SameSite cookies. Double-submit cookies.",
                examples=["State-changing operations without CSRF protection"],
                references=["https://cwe.mitre.org/data/definitions/352.html"]
            ),
            
            "CWE-770": CWEInfo(
                cwe_id="CWE-770",
                name="Allocation of Resources Without Limits or Throttling",
                description="Software allocates resources without limits or throttling.",
                severity=VulnerabilitySeverity.MEDIUM,
                vulnerability_type=VulnerabilityType.OTHER,
                owasp_category="A04:2021 - Insecure Design",
                mitigation="Implement rate limiting. Set resource quotas. Timeout mechanisms. Request size limits.",
                examples=["No rate limiting on API", "Unlimited file uploads"],
                references=["https://cwe.mitre.org/data/definitions/770.html"]
            ),
            
            "CWE-200": CWEInfo(
                cwe_id="CWE-200",
                name="Exposure of Sensitive Information to an Unauthorized Actor",
                description="Product exposes sensitive information to actor not explicitly authorized to access it.",
                severity=VulnerabilitySeverity.MEDIUM,
                vulnerability_type=VulnerabilityType.SENSITIVE_DATA,
                owasp_category="A01:2021 - Broken Access Control",
                mitigation="Implement proper access controls. Redact sensitive data. Secure error messages.",
                examples=["Stack traces in production", "Debug info exposure"],
                references=["https://cwe.mitre.org/data/definitions/200.html"]
            ),
        }
    
    def get_cwe(self, cwe_id: str) -> Optional[CWEInfo]:
        """
        Get CWE information by ID.
        
        Args:
            cwe_id: CWE identifier (e.g., "CWE-89" or "89")
        
        Returns:
            CWEInfo object or None if not found
        """
        # Normalize CWE ID
        if not cwe_id.startswith("CWE-"):
            cwe_id = f"CWE-{cwe_id}"
        
        return self._cwe_data.get(cwe_id)
    
    def search_by_type(self, vuln_type: VulnerabilityType) -> List[CWEInfo]:
        """
        Search CWEs by vulnerability type.
        
        Args:
            vuln_type: Vulnerability type enum
        
        Returns:
            List of matching CWEInfo objects
        """
        return [
            cwe for cwe in self._cwe_data.values()
            if cwe.vulnerability_type == vuln_type
        ]
    
    def search_by_owasp(self, owasp_category: str) -> List[CWEInfo]:
        """
        Search CWEs by OWASP category.
        
        Args:
            owasp_category: OWASP category (e.g., "A01:2021")
        
        Returns:
            List of matching CWEInfo objects
        """
        return [
            cwe for cwe in self._cwe_data.values()
            if cwe.owasp_category and owasp_category in cwe.owasp_category
        ]
    
    def get_all_cwes(self) -> List[CWEInfo]:
        """Get all CWEs in database."""
        return list(self._cwe_data.values())
    
    def get_critical_cwes(self) -> List[CWEInfo]:
        """Get all critical severity CWEs."""
        return [
            cwe for cwe in self._cwe_data.values()
            if cwe.severity == VulnerabilitySeverity.CRITICAL
        ]
    
    def get_high_severity_cwes(self) -> List[CWEInfo]:
        """Get all high severity CWEs."""
        return [
            cwe for cwe in self._cwe_data.values()
            if cwe.severity == VulnerabilitySeverity.HIGH
        ]
    
    def __len__(self) -> int:
        """Return number of CWEs in database."""
        return len(self._cwe_data)
    
    def __contains__(self, cwe_id: str) -> bool:
        """Check if CWE exists in database."""
        if not cwe_id.startswith("CWE-"):
            cwe_id = f"CWE-{cwe_id}"
        return cwe_id in self._cwe_data
