"""
Vulnerability Knowledge Base

Comprehensive knowledge base covering:
- OWASP Top 10 vulnerabilities
- Common Weakness Enumeration (CWE) patterns
- Java-specific security issues
- Detection patterns and remediation guidance
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class VulnerabilitySeverity(Enum):
    """Vulnerability severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class VulnerabilityCategory(Enum):
    """OWASP Top 10 and common categories"""
    INJECTION = "injection"
    BROKEN_AUTH = "broken_authentication"
    SENSITIVE_DATA = "sensitive_data_exposure"
    XXE = "xml_external_entities"
    BROKEN_ACCESS = "broken_access_control"
    SECURITY_MISCONFIG = "security_misconfiguration"
    XSS = "cross_site_scripting"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    VULNERABLE_COMPONENTS = "vulnerable_components"
    INSUFFICIENT_LOGGING = "insufficient_logging"
    CRYPTO_FAILURES = "cryptographic_failures"
    SSRF = "server_side_request_forgery"
    PATH_TRAVERSAL = "path_traversal"
    CODE_INJECTION = "code_injection"
    RACE_CONDITION = "race_condition"
    RESOURCE_LEAK = "resource_leak"


@dataclass
class VulnerabilityPattern:
    """Represents a vulnerability pattern with detection info"""
    cwe_id: str  # e.g., "CWE-89"
    name: str
    category: VulnerabilityCategory
    severity: VulnerabilitySeverity
    description: str
    
    # Detection patterns
    code_patterns: List[str]  # Regex or code patterns to detect
    vulnerable_apis: List[str]  # Vulnerable API calls
    codeql_queries: List[str]  # CodeQL query names
    
    # Context clues
    indicators: List[str]  # What to look for
    false_positive_checks: List[str]  # How to avoid false positives
    
    # Remediation
    remediation: str
    secure_alternatives: List[str]
    
    # Examples
    vulnerable_example: str
    secure_example: str
    
    # References
    references: List[str]


class VulnerabilityKnowledgeBase:
    """
    Knowledge base for Java vulnerability detection.
    
    Contains patterns, detection strategies, and remediation guidance
    for common Java vulnerabilities.
    """
    
    def __init__(self):
        self.patterns: Dict[str, VulnerabilityPattern] = {}
        self._load_patterns()
    
    def _load_patterns(self):
        """Load all vulnerability patterns"""
        self._add_sql_injection()
        self._add_xss()
        self._add_path_traversal()
        self._add_xxe()
        self._add_insecure_deserialization()
        self._add_hardcoded_credentials()
        self._add_weak_crypto()
        self._add_insecure_random()
        self._add_command_injection()
        self._add_ldap_injection()
        self._add_ssrf()
        self._add_unsafe_reflection()
        self._add_resource_leaks()
        self._add_race_conditions()
        self._add_null_pointer()
    
    def get_pattern(self, cwe_id: str) -> Optional[VulnerabilityPattern]:
        """Get pattern by CWE ID"""
        return self.patterns.get(cwe_id)
    
    def get_by_category(self, category: VulnerabilityCategory) -> List[VulnerabilityPattern]:
        """Get all patterns for a category"""
        return [p for p in self.patterns.values() if p.category == category]
    
    def get_by_severity(self, severity: VulnerabilitySeverity) -> List[VulnerabilityPattern]:
        """Get all patterns for a severity level"""
        return [p for p in self.patterns.values() if p.severity == severity]
    
    def search(self, query: str) -> List[VulnerabilityPattern]:
        """Search patterns by name, description, or indicators"""
        query = query.lower()
        results = []
        for pattern in self.patterns.values():
            if (query in pattern.name.lower() or
                query in pattern.description.lower() or
                any(query in ind.lower() for ind in pattern.indicators)):
                results.append(pattern)
        return results
    
    # Pattern definitions
    
    def _add_sql_injection(self):
        """CWE-89: SQL Injection"""
        self.patterns["CWE-89"] = VulnerabilityPattern(
            cwe_id="CWE-89",
            name="SQL Injection",
            category=VulnerabilityCategory.INJECTION,
            severity=VulnerabilitySeverity.CRITICAL,
            description="Untrusted data concatenated into SQL queries without proper sanitization",
            
            code_patterns=[
                r'Statement\.execute\w*\([^?]*\+',
                r'String\.format.*SELECT.*FROM',
                r'"SELECT.*"\s*\+',
                r'createQuery\([^?]*\+',
            ],
            
            vulnerable_apis=[
                "Statement.execute",
                "Statement.executeQuery",
                "Statement.executeUpdate",
                "createQuery (with concatenation)"
            ],
            
            codeql_queries=[
                "java/sql-injection",
                "java/concatenated-sql-query"
            ],
            
            indicators=[
                "String concatenation in SQL queries",
                "User input directly in SQL",
                "No parameterized queries",
                "Dynamic query construction"
            ],
            
            false_positive_checks=[
                "Check if input is validated/sanitized",
                "Verify if PreparedStatement is used",
                "Check for ORM framework usage",
                "Validate if query is actually dynamic"
            ],
            
            remediation="Use PreparedStatement with parameterized queries. Never concatenate user input into SQL.",
            
            secure_alternatives=[
                "PreparedStatement with ? placeholders",
                "Named parameters in JPA/Hibernate",
                "Criteria API",
                "Query builders with parameterization"
            ],
            
            vulnerable_example='''
// VULNERABLE
String query = "SELECT * FROM users WHERE username = '" + userInput + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(query);
''',
            
            secure_example='''
// SECURE
String query = "SELECT * FROM users WHERE username = ?";
PreparedStatement pstmt = conn.prepareStatement(query);
pstmt.setString(1, userInput);
ResultSet rs = pstmt.executeQuery();
''',
            
            references=[
                "OWASP A03:2021 - Injection",
                "CWE-89: SQL Injection",
                "https://owasp.org/www-community/attacks/SQL_Injection"
            ]
        )
    
    def _add_xss(self):
        """CWE-79: Cross-Site Scripting"""
        self.patterns["CWE-79"] = VulnerabilityPattern(
            cwe_id="CWE-79",
            name="Cross-Site Scripting (XSS)",
            category=VulnerabilityCategory.XSS,
            severity=VulnerabilitySeverity.HIGH,
            description="Untrusted data rendered in HTML without proper encoding",
            
            code_patterns=[
                r'\.innerHTML\s*=',
                r'\.write\([^)]*\+',
                r'response\.getWriter\(\)\.print\w*\(',
                r'<%= .*request\.getParameter',
            ],
            
            vulnerable_apis=[
                "HttpServletResponse.getWriter().write",
                "PrintWriter.println",
                "JSP expression <%= %>",
                "innerHTML assignment"
            ],
            
            codeql_queries=[
                "java/xss",
                "java/reflected-xss",
                "java/stored-xss"
            ],
            
            indicators=[
                "User input in HTML output",
                "No output encoding",
                "Direct rendering of request parameters",
                "innerHTML or document.write usage"
            ],
            
            false_positive_checks=[
                "Check for HTML encoding functions",
                "Verify if framework auto-escapes",
                "Check Content-Security-Policy headers",
                "Validate output context (HTML/JS/URL)"
            ],
            
            remediation="Always encode output based on context. Use framework escaping features or OWASP Java Encoder.",
            
            secure_alternatives=[
                "OWASP Java Encoder",
                "Framework auto-escaping (JSF, Spring)",
                "Content-Security-Policy headers",
                "Template engines with auto-escaping"
            ],
            
            vulnerable_example='''
// VULNERABLE
String username = request.getParameter("name");
out.println("<div>Welcome " + username + "</div>");
''',
            
            secure_example='''
// SECURE
String username = request.getParameter("name");
String encoded = Encode.forHtml(username);
out.println("<div>Welcome " + encoded + "</div>");
''',
            
            references=[
                "OWASP A03:2021 - Injection (XSS)",
                "CWE-79: Cross-Site Scripting",
                "https://owasp.org/www-community/attacks/xss/"
            ]
        )
    
    def _add_path_traversal(self):
        """CWE-22: Path Traversal"""
        self.patterns["CWE-22"] = VulnerabilityPattern(
            cwe_id="CWE-22",
            name="Path Traversal",
            category=VulnerabilityCategory.PATH_TRAVERSAL,
            severity=VulnerabilitySeverity.HIGH,
            description="File paths constructed from user input without validation",
            
            code_patterns=[
                r'new File\([^)]*request\.getParameter',
                r'new FileInputStream\([^)]*\+',
                r'Paths\.get\([^)]*request',
                r'\.getResource\([^)]*\+',
            ],
            
            vulnerable_apis=[
                "File constructor",
                "FileInputStream constructor",
                "FileReader constructor",
                "Paths.get",
                "ServletContext.getResource"
            ],
            
            codeql_queries=[
                "java/path-injection",
                "java/zipslip"
            ],
            
            indicators=[
                "User input in file paths",
                "No path validation",
                "../ sequence not checked",
                "Direct file access from parameters"
            ],
            
            false_positive_checks=[
                "Check for path canonicalization",
                "Verify whitelist validation",
                "Check for base directory restriction",
                "Validate if path is user-controlled"
            ],
            
            remediation="Validate and canonicalize file paths. Use whitelist of allowed paths. Check for path traversal sequences.",
            
            secure_alternatives=[
                "Path canonicalization (getCanonicalPath)",
                "Whitelist validation",
                "Base directory checks",
                "Use resource identifiers instead of paths"
            ],
            
            vulnerable_example='''
// VULNERABLE
String filename = request.getParameter("file");
File file = new File("/app/files/" + filename);
FileInputStream fis = new FileInputStream(file);
''',
            
            secure_example='''
// SECURE
String filename = request.getParameter("file");
File file = new File("/app/files/", filename);
String canonical = file.getCanonicalPath();
if (!canonical.startsWith("/app/files/")) {
    throw new SecurityException("Invalid path");
}
FileInputStream fis = new FileInputStream(file);
''',
            
            references=[
                "OWASP A01:2021 - Broken Access Control",
                "CWE-22: Path Traversal",
                "https://owasp.org/www-community/attacks/Path_Traversal"
            ]
        )
    
    def _add_xxe(self):
        """CWE-611: XML External Entity"""
        self.patterns["CWE-611"] = VulnerabilityPattern(
            cwe_id="CWE-611",
            name="XML External Entity (XXE)",
            category=VulnerabilityCategory.XXE,
            severity=VulnerabilitySeverity.HIGH,
            description="XML parser configured to process external entities",
            
            code_patterns=[
                r'DocumentBuilderFactory\.newInstance\(\)',
                r'SAXParserFactory\.newInstance\(\)',
                r'XMLInputFactory\.newInstance\(\)',
                r'TransformerFactory\.newInstance\(\)',
            ],
            
            vulnerable_apis=[
                "DocumentBuilderFactory",
                "SAXParserFactory",
                "XMLInputFactory",
                "TransformerFactory"
            ],
            
            codeql_queries=[
                "java/xxe",
                "java/unsafe-xml-parsing"
            ],
            
            indicators=[
                "XML parsing without security features",
                "External entity processing enabled",
                "No DTD disabling",
                "Default XML parser configuration"
            ],
            
            false_positive_checks=[
                "Check if external entities disabled",
                "Verify security features set",
                "Check for secure XML library usage",
                "Validate XML source is trusted"
            ],
            
            remediation="Disable external entity processing and DTD. Set FEATURE_SECURE_PROCESSING.",
            
            secure_alternatives=[
                "Disable FEATURE_EXTERNAL_GENERAL_ENTITIES",
                "Disable FEATURE_EXTERNAL_PARAMETER_ENTITIES",
                "Disable DOCTYPE declarations",
                "Enable FEATURE_SECURE_PROCESSING"
            ],
            
            vulnerable_example='''
// VULNERABLE
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(inputStream);
''',
            
            secure_example='''
// SECURE
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setExpandEntityReferences(false);
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(inputStream);
''',
            
            references=[
                "OWASP A05:2021 - Security Misconfiguration",
                "CWE-611: XML External Entity",
                "https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing"
            ]
        )
    
    def _add_insecure_deserialization(self):
        """CWE-502: Insecure Deserialization"""
        self.patterns["CWE-502"] = VulnerabilityPattern(
            cwe_id="CWE-502",
            name="Insecure Deserialization",
            category=VulnerabilityCategory.INSECURE_DESERIALIZATION,
            severity=VulnerabilitySeverity.CRITICAL,
            description="Deserialization of untrusted data without validation",
            
            code_patterns=[
                r'ObjectInputStream.*readObject',
                r'XMLDecoder.*readObject',
                r'XStream.*fromXML',
                r'\.deserialize\(',
            ],
            
            vulnerable_apis=[
                "ObjectInputStream.readObject",
                "XMLDecoder.readObject",
                "XStream.fromXML",
                "JSON deserialization (unsafe)"
            ],
            
            codeql_queries=[
                "java/unsafe-deserialization",
                "java/object-deserialization"
            ],
            
            indicators=[
                "Deserialization of external data",
                "No class whitelist",
                "No integrity checks",
                "Trusting serialized data"
            ],
            
            false_positive_checks=[
                "Check for class whitelist validation",
                "Verify digital signature checking",
                "Check if data source is trusted",
                "Validate deserialization library security"
            ],
            
            remediation="Avoid deserialization of untrusted data. Use safe formats like JSON with schema validation.",
            
            secure_alternatives=[
                "JSON with schema validation",
                "Whitelist-based deserialization",
                "Digital signature verification",
                "Use safe deserialization libraries"
            ],
            
            vulnerable_example='''
// VULNERABLE
ObjectInputStream ois = new ObjectInputStream(inputStream);
MyObject obj = (MyObject) ois.readObject();
''',
            
            secure_example='''
// SECURE - Use JSON instead
ObjectMapper mapper = new ObjectMapper();
// Configure safely
mapper.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL, 
                           JsonTypeInfo.As.PROPERTY);
MyObject obj = mapper.readValue(jsonString, MyObject.class);
''',
            
            references=[
                "OWASP A08:2021 - Software and Data Integrity Failures",
                "CWE-502: Deserialization of Untrusted Data",
                "https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data"
            ]
        )
    
    def _add_hardcoded_credentials(self):
        """CWE-798: Hardcoded Credentials"""
        self.patterns["CWE-798"] = VulnerabilityPattern(
            cwe_id="CWE-798",
            name="Hardcoded Credentials",
            category=VulnerabilityCategory.BROKEN_AUTH,
            severity=VulnerabilitySeverity.HIGH,
            description="Credentials hardcoded in source code",
            
            code_patterns=[
                r'password\s*=\s*"[^"]+"',
                r'api[_-]?key\s*=\s*"[^"]+"',
                r'secret\s*=\s*"[^"]+"',
                r'private[_-]?key\s*=\s*"[^"]+"',
            ],
            
            vulnerable_apis=[
                "Direct password assignment",
                "Hardcoded connection strings",
                "Embedded API keys",
                "Static secrets"
            ],
            
            codeql_queries=[
                "java/hardcoded-credential",
                "java/hardcoded-password"
            ],
            
            indicators=[
                "String literals with password/key/secret",
                "Credentials in configuration files in repo",
                "No environment variable usage",
                "Static credential fields"
            ],
            
            false_positive_checks=[
                "Check if it's a placeholder/example",
                "Verify if used in tests only",
                "Check for obfuscation/encoding",
                "Validate if actually used for auth"
            ],
            
            remediation="Store credentials in environment variables, key vaults, or secure configuration services.",
            
            secure_alternatives=[
                "Environment variables",
                "AWS Secrets Manager",
                "Azure Key Vault",
                "HashiCorp Vault",
                "Configuration service with encryption"
            ],
            
            vulnerable_example='''
// VULNERABLE
String password = "MySecretPassword123!";
String apiKey = "sk_live_51HqK8hLkj...";
conn = DriverManager.getConnection(url, "admin", password);
''',
            
            secure_example='''
// SECURE
String password = System.getenv("DB_PASSWORD");
String apiKey = System.getenv("API_KEY");
if (password == null || apiKey == null) {
    throw new IllegalStateException("Missing credentials");
}
conn = DriverManager.getConnection(url, "admin", password);
''',
            
            references=[
                "OWASP A07:2021 - Identification and Authentication Failures",
                "CWE-798: Use of Hard-coded Credentials",
                "https://cwe.mitre.org/data/definitions/798.html"
            ]
        )
    
    def _add_weak_crypto(self):
        """CWE-327: Weak Cryptography"""
        self.patterns["CWE-327"] = VulnerabilityPattern(
            cwe_id="CWE-327",
            name="Weak Cryptographic Algorithm",
            category=VulnerabilityCategory.CRYPTO_FAILURES,
            severity=VulnerabilitySeverity.HIGH,
            description="Use of weak or broken cryptographic algorithms",
            
            code_patterns=[
                r'Cipher\.getInstance\("DES',
                r'Cipher\.getInstance\("MD5',
                r'MessageDigest\.getInstance\("MD5',
                r'MessageDigest\.getInstance\("SHA-1',
                r'Cipher\.getInstance\("RSA/ECB',
            ],
            
            vulnerable_apis=[
                "DES encryption",
                "MD5 hashing",
                "SHA-1 hashing",
                "RSA with ECB mode",
                "RC4 cipher"
            ],
            
            codeql_queries=[
                "java/weak-cryptographic-algorithm",
                "java/insecure-cipher"
            ],
            
            indicators=[
                "DES/3DES/RC4 usage",
                "MD5/SHA-1 for security purposes",
                "ECB mode cipher",
                "Insufficient key sizes"
            ],
            
            false_positive_checks=[
                "Check if used for non-security purposes",
                "Verify algorithm usage context",
                "Check key sizes",
                "Validate mode of operation"
            ],
            
            remediation="Use strong algorithms: AES-256, SHA-256/SHA-3, RSA-2048+. Use authenticated encryption modes (GCM).",
            
            secure_alternatives=[
                "AES-256 with GCM mode",
                "SHA-256 or SHA-3",
                "RSA-2048 or higher",
                "ChaCha20-Poly1305",
                "Argon2 for password hashing"
            ],
            
            vulnerable_example='''
// VULNERABLE
Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
MessageDigest md = MessageDigest.getInstance("MD5");
byte[] hash = md.digest(data);
''',
            
            secure_example='''
// SECURE
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, iv));

// For hashing
MessageDigest md = MessageDigest.getInstance("SHA-256");
byte[] hash = md.digest(data);
''',
            
            references=[
                "OWASP A02:2021 - Cryptographic Failures",
                "CWE-327: Use of Broken Cryptographic Algorithm",
                "https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure"
            ]
        )
    
    def _add_insecure_random(self):
        """CWE-330: Insecure Random"""
        self.patterns["CWE-330"] = VulnerabilityPattern(
            cwe_id="CWE-330",
            name="Weak Random Number Generation",
            category=VulnerabilityCategory.CRYPTO_FAILURES,
            severity=VulnerabilitySeverity.MEDIUM,
            description="Use of predictable random number generators for security purposes",
            
            code_patterns=[
                r'new Random\(',
                r'Math\.random\(',
                r'ThreadLocalRandom',
            ],
            
            vulnerable_apis=[
                "java.util.Random",
                "Math.random()",
                "ThreadLocalRandom"
            ],
            
            codeql_queries=[
                "java/insecure-randomness"
            ],
            
            indicators=[
                "java.util.Random for security",
                "Math.random() for tokens/keys",
                "Predictable PRNG usage",
                "No SecureRandom for crypto"
            ],
            
            false_positive_checks=[
                "Check usage context (game vs security)",
                "Verify if used for sensitive data",
                "Check if SecureRandom used elsewhere",
                "Validate randomness requirements"
            ],
            
            remediation="Use SecureRandom for all security-sensitive random number generation (tokens, keys, IVs, salts).",
            
            secure_alternatives=[
                "SecureRandom",
                "SecureRandom.getInstanceStrong()",
                "OS-provided randomness"
            ],
            
            vulnerable_example='''
// VULNERABLE
Random random = new Random();
String token = String.valueOf(random.nextLong());
byte[] sessionKey = new byte[16];
random.nextBytes(sessionKey);
''',
            
            secure_example='''
// SECURE
SecureRandom secureRandom = new SecureRandom();
String token = new BigInteger(130, secureRandom).toString(32);
byte[] sessionKey = new byte[16];
secureRandom.nextBytes(sessionKey);
''',
            
            references=[
                "OWASP A02:2021 - Cryptographic Failures",
                "CWE-330: Use of Insufficiently Random Values",
                "https://cwe.mitre.org/data/definitions/330.html"
            ]
        )
    
    def _add_command_injection(self):
        """CWE-78: OS Command Injection"""
        self.patterns["CWE-78"] = VulnerabilityPattern(
            cwe_id="CWE-78",
            name="OS Command Injection",
            category=VulnerabilityCategory.CODE_INJECTION,
            severity=VulnerabilitySeverity.CRITICAL,
            description="User input passed to system commands without sanitization",
            
            code_patterns=[
                r'Runtime\.getRuntime\(\)\.exec\([^)]*\+',
                r'ProcessBuilder.*\.command\([^)]*\+',
                r'new ProcessBuilder\([^)]*request',
            ],
            
            vulnerable_apis=[
                "Runtime.exec",
                "ProcessBuilder",
                "ProcessBuilder.command"
            ],
            
            codeql_queries=[
                "java/command-injection",
                "java/concatenated-command-line"
            ],
            
            indicators=[
                "User input in command strings",
                "String concatenation with exec",
                "No input validation",
                "Shell invocation"
            ],
            
            false_positive_checks=[
                "Check for input validation/whitelisting",
                "Verify if command is parameterized",
                "Check for shell metacharacter filtering",
                "Validate if input is user-controlled"
            ],
            
            remediation="Avoid exec if possible. Use ProcessBuilder with array arguments. Validate/whitelist all inputs.",
            
            secure_alternatives=[
                "ProcessBuilder with array arguments",
                "Whitelist validation",
                "Native Java alternatives to shell commands",
                "Restricted execution environments"
            ],
            
            vulnerable_example='''
// VULNERABLE
String filename = request.getParameter("file");
Runtime.getRuntime().exec("ls -la " + filename);
''',
            
            secure_example='''
// SECURE
String filename = request.getParameter("file");
// Validate filename
if (!filename.matches("[a-zA-Z0-9._-]+")) {
    throw new IllegalArgumentException("Invalid filename");
}
ProcessBuilder pb = new ProcessBuilder("ls", "-la", filename);
Process p = pb.start();
''',
            
            references=[
                "OWASP A03:2021 - Injection",
                "CWE-78: OS Command Injection",
                "https://owasp.org/www-community/attacks/Command_Injection"
            ]
        )
    
    def _add_ldap_injection(self):
        """CWE-90: LDAP Injection"""
        self.patterns["CWE-90"] = VulnerabilityPattern(
            cwe_id="CWE-90",
            name="LDAP Injection",
            category=VulnerabilityCategory.INJECTION,
            severity=VulnerabilitySeverity.HIGH,
            description="User input concatenated into LDAP queries without sanitization",
            
            code_patterns=[
                r'DirContext\.search\([^)]*\+',
                r'".*\(.*=.*"\s*\+',
                r'LdapContext.*search\([^)]*\+',
            ],
            
            vulnerable_apis=[
                "DirContext.search",
                "LdapContext.search",
                "InitialDirContext.search"
            ],
            
            codeql_queries=[
                "java/ldap-injection"
            ],
            
            indicators=[
                "String concatenation in LDAP filters",
                "User input in LDAP queries",
                "No filter escaping",
                "Dynamic LDAP query construction"
            ],
            
            false_positive_checks=[
                "Check for LDAP escaping functions",
                "Verify parameterization",
                "Check input validation",
                "Validate if query is actually dynamic"
            ],
            
            remediation="Escape special LDAP characters. Use parameterized queries or LDAP encoding libraries.",
            
            secure_alternatives=[
                "LDAP DN/filter encoding",
                "OWASP ESAPI encoders",
                "Input validation/whitelisting",
                "Safe LDAP libraries"
            ],
            
            vulnerable_example='''
// VULNERABLE
String username = request.getParameter("user");
String filter = "(uid=" + username + ")";
NamingEnumeration results = ctx.search("ou=users", filter, controls);
''',
            
            secure_example='''
// SECURE
String username = request.getParameter("user");
// Escape LDAP special characters
String escapedUsername = escapeLDAPSearchFilter(username);
String filter = "(uid=" + escapedUsername + ")";
NamingEnumeration results = ctx.search("ou=users", filter, controls);

// Or use SearchControls with proper escaping library
''',
            
            references=[
                "OWASP A03:2021 - Injection",
                "CWE-90: LDAP Injection",
                "https://owasp.org/www-community/attacks/LDAP_Injection"
            ]
        )
    
    def _add_ssrf(self):
        """CWE-918: Server-Side Request Forgery"""
        self.patterns["CWE-918"] = VulnerabilityPattern(
            cwe_id="CWE-918",
            name="Server-Side Request Forgery (SSRF)",
            category=VulnerabilityCategory.SSRF,
            severity=VulnerabilitySeverity.HIGH,
            description="Server makes requests to attacker-controlled URLs",
            
            code_patterns=[
                r'new URL\([^)]*request',
                r'HttpClient.*execute\([^)]*request',
                r'openConnection\([^)]*request',
                r'RestTemplate.*\([^)]*request',
            ],
            
            vulnerable_apis=[
                "URL.openConnection",
                "HttpClient.execute",
                "RestTemplate methods",
                "HttpURLConnection"
            ],
            
            codeql_queries=[
                "java/ssrf"
            ],
            
            indicators=[
                "User-controlled URLs in requests",
                "No URL validation",
                "Internal network accessible",
                "No whitelist of allowed hosts"
            ],
            
            false_positive_checks=[
                "Check for URL validation/whitelisting",
                "Verify network segmentation",
                "Check for protocol restrictions",
                "Validate if URL is user-controlled"
            ],
            
            remediation="Validate and whitelist allowed URLs/hosts. Disable redirects. Use network segmentation.",
            
            secure_alternatives=[
                "URL whitelist validation",
                "Disable HTTP redirects",
                "Network-level access controls",
                "Use resource identifiers instead of URLs"
            ],
            
            vulnerable_example='''
// VULNERABLE
String imageUrl = request.getParameter("url");
URL url = new URL(imageUrl);
InputStream is = url.openStream();
''',
            
            secure_example='''
// SECURE
String imageUrl = request.getParameter("url");
URL url = new URL(imageUrl);

// Validate host whitelist
String host = url.getHost();
if (!isAllowedHost(host)) {
    throw new SecurityException("Host not allowed");
}

// Validate protocol
if (!url.getProtocol().equals("https")) {
    throw new SecurityException("Only HTTPS allowed");
}

InputStream is = url.openStream();
''',
            
            references=[
                "OWASP A10:2021 - Server-Side Request Forgery",
                "CWE-918: Server-Side Request Forgery",
                "https://owasp.org/www-community/attacks/Server_Side_Request_Forgery"
            ]
        )
    
    def _add_unsafe_reflection(self):
        """CWE-470: Unsafe Reflection"""
        self.patterns["CWE-470"] = VulnerabilityPattern(
            cwe_id="CWE-470",
            name="Unsafe Reflection",
            category=VulnerabilityCategory.CODE_INJECTION,
            severity=VulnerabilitySeverity.HIGH,
            description="Class names or method names from user input used in reflection",
            
            code_patterns=[
                r'Class\.forName\([^)]*request',
                r'\.getMethod\([^)]*request',
                r'\.invoke\([^)]*request',
                r'ClassLoader.*loadClass\([^)]*request',
            ],
            
            vulnerable_apis=[
                "Class.forName",
                "Method.invoke",
                "ClassLoader.loadClass",
                "Constructor.newInstance"
            ],
            
            codeql_queries=[
                "java/unsafe-reflection"
            ],
            
            indicators=[
                "User input in Class.forName",
                "Dynamic method invocation",
                "No class whitelist",
                "Unrestricted reflection"
            ],
            
            false_positive_checks=[
                "Check for class whitelist",
                "Verify reflection usage context",
                "Check access modifiers",
                "Validate if truly user-controlled"
            ],
            
            remediation="Avoid reflection with user input. Use whitelist of allowed classes/methods.",
            
            secure_alternatives=[
                "Factory pattern with whitelisting",
                "Strategy pattern",
                "Configuration-driven approach",
                "Enum-based dispatching"
            ],
            
            vulnerable_example='''
// VULNERABLE
String className = request.getParameter("class");
Class<?> clazz = Class.forName(className);
Object instance = clazz.newInstance();
''',
            
            secure_example='''
// SECURE
String className = request.getParameter("class");
// Whitelist validation
Set<String> allowedClasses = Set.of("com.app.SafeClass1", "com.app.SafeClass2");
if (!allowedClasses.contains(className)) {
    throw new SecurityException("Class not allowed");
}
Class<?> clazz = Class.forName(className);
Object instance = clazz.newInstance();
''',
            
            references=[
                "CWE-470: Unsafe Reflection",
                "https://cwe.mitre.org/data/definitions/470.html"
            ]
        )
    
    def _add_resource_leaks(self):
        """CWE-772: Resource Leaks"""
        self.patterns["CWE-772"] = VulnerabilityPattern(
            cwe_id="CWE-772",
            name="Resource Leak",
            category=VulnerabilityCategory.RESOURCE_LEAK,
            severity=VulnerabilitySeverity.MEDIUM,
            description="Resources not properly closed, causing memory/resource leaks",
            
            code_patterns=[
                r'new FileInputStream\([^)]*\)(?!;?\s*try)',
                r'new BufferedReader\([^)]*\)(?!;?\s*try)',
                r'\.openConnection\(\)(?!;?\s*try)',
                r'new Statement\([^)]*\)(?!;?\s*try)',
            ],
            
            vulnerable_apis=[
                "FileInputStream without try-with-resources",
                "Connection without close",
                "Statement without close",
                "InputStream/Reader without close"
            ],
            
            codeql_queries=[
                "java/resource-leak"
            ],
            
            indicators=[
                "Resource creation without try-with-resources",
                "Missing close() calls",
                "No finally block",
                "Resources not closed on exception"
            ],
            
            false_positive_checks=[
                "Check for try-with-resources",
                "Verify finally block",
                "Check for explicit close()",
                "Validate resource ownership"
            ],
            
            remediation="Use try-with-resources for all AutoCloseable resources. Ensure close() in finally.",
            
            secure_alternatives=[
                "try-with-resources statement",
                "Apache Commons IOUtils.closeQuietly",
                "Spring's resource templates",
                "Automatic resource management"
            ],
            
            vulnerable_example='''
// VULNERABLE
FileInputStream fis = new FileInputStream(file);
byte[] data = new byte[fis.available()];
fis.read(data);
// Missing close() - resource leak
''',
            
            secure_example='''
// SECURE
try (FileInputStream fis = new FileInputStream(file)) {
    byte[] data = new byte[fis.available()];
    fis.read(data);
} // Automatically closed
''',
            
            references=[
                "CWE-772: Missing Release of Resource",
                "https://cwe.mitre.org/data/definitions/772.html"
            ]
        )
    
    def _add_race_conditions(self):
        """CWE-362: Race Condition"""
        self.patterns["CWE-362"] = VulnerabilityPattern(
            cwe_id="CWE-362",
            name="Race Condition",
            category=VulnerabilityCategory.RACE_CONDITION,
            severity=VulnerabilitySeverity.MEDIUM,
            description="Concurrent access to shared resources without proper synchronization",
            
            code_patterns=[
                r'static\s+\w+\s+\w+\s*=.*(?!synchronized)',
                r'if\s*\([^)]*!=\s*null\).*\{[^}]*\.\w+\(',
                r'\.get\([^)]*\).*\.set\(',
            ],
            
            vulnerable_apis=[
                "Static mutable fields",
                "Check-then-act patterns",
                "Double-checked locking (wrong)",
                "Unsynchronized collections"
            ],
            
            codeql_queries=[
                "java/unsafe-double-checked-locking",
                "java/unsynchronized-static-access"
            ],
            
            indicators=[
                "Shared mutable state",
                "Check-then-act without locking",
                "Compound operations on shared data",
                "No synchronization"
            ],
            
            false_positive_checks=[
                "Check for synchronization",
                "Verify thread-safety guarantees",
                "Check for concurrent collections",
                "Validate if actually shared"
            ],
            
            remediation="Use proper synchronization (synchronized, locks), atomic operations, or thread-safe collections.",
            
            secure_alternatives=[
                "synchronized blocks/methods",
                "java.util.concurrent.locks",
                "AtomicInteger, AtomicReference",
                "ConcurrentHashMap",
                "Immutable objects"
            ],
            
            vulnerable_example='''
// VULNERABLE - check-then-act race
private static Map<String, User> cache = new HashMap<>();

public User getUser(String id) {
    if (!cache.containsKey(id)) {  // Race here
        cache.put(id, loadUser(id));
    }
    return cache.get(id);
}
''',
            
            secure_example='''
// SECURE - use concurrent collection
private static ConcurrentHashMap<String, User> cache = new ConcurrentHashMap<>();

public User getUser(String id) {
    return cache.computeIfAbsent(id, this::loadUser);
}
''',
            
            references=[
                "CWE-362: Concurrent Execution using Shared Resource",
                "https://cwe.mitre.org/data/definitions/362.html"
            ]
        )
    
    def _add_null_pointer(self):
        """CWE-476: NULL Pointer Dereference"""
        self.patterns["CWE-476"] = VulnerabilityPattern(
            cwe_id="CWE-476",
            name="NULL Pointer Dereference",
            category=VulnerabilityCategory.SECURITY_MISCONFIG,
            severity=VulnerabilitySeverity.LOW,
            description="Dereferencing potentially null references without checks",
            
            code_patterns=[
                r'\.get\([^)]*\)\.\w+',
                r'request\.getParameter\([^)]*\)\.\w+',
                r'map\.get\([^)]*\)\.\w+',
            ],
            
            vulnerable_apis=[
                "Map.get().method()",
                "getParameter().method()",
                "Unchecked nullable returns"
            ],
            
            codeql_queries=[
                "java/dereferenced-value-may-be-null"
            ],
            
            indicators=[
                "Direct method call on nullable",
                "No null checks",
                "Chained calls on nullable types",
                "Assumption of non-null"
            ],
            
            false_positive_checks=[
                "Check for null validation",
                "Verify non-null contracts",
                "Check for Optional usage",
                "Validate data flow analysis"
            ],
            
            remediation="Add null checks or use Optional. Validate inputs and map retrievals.",
            
            secure_alternatives=[
                "Optional<T>",
                "Objects.requireNonNull()",
                "Null-safe navigation",
                "@NonNull annotations"
            ],
            
            vulnerable_example='''
// VULNERABLE
String value = map.get(key).toUpperCase();  // NPE if null
User user = request.getAttribute("user");
String name = user.getName();  // NPE if null
''',
            
            secure_example='''
// SECURE
String value = Optional.ofNullable(map.get(key))
                       .map(String::toUpperCase)
                       .orElse("DEFAULT");

User user = (User) request.getAttribute("user");
String name = (user != null) ? user.getName() : "Anonymous";
''',
            
            references=[
                "CWE-476: NULL Pointer Dereference",
                "https://cwe.mitre.org/data/definitions/476.html"
            ]
        )
    
    def get_detection_guidance(self, cwe_id: str) -> str:
        """Get detailed detection guidance for a vulnerability"""
        pattern = self.get_pattern(cwe_id)
        if not pattern:
            return f"No pattern found for {cwe_id}"
        
        guidance = f"""
Detection Guidance for {pattern.name} ({pattern.cwe_id})

SEVERITY: {pattern.severity.value.upper()}
CATEGORY: {pattern.category.value}

DESCRIPTION:
{pattern.description}

WHAT TO LOOK FOR:
"""
        for indicator in pattern.indicators:
            guidance += f"  • {indicator}\n"
        
        guidance += "\nCODE PATTERNS:\n"
        for code_pattern in pattern.code_patterns[:3]:
            guidance += f"  • {code_pattern}\n"
        
        guidance += "\nFALSE POSITIVE CHECKS:\n"
        for check in pattern.false_positive_checks:
            guidance += f"  • {check}\n"
        
        guidance += f"\nREMEDIATION:\n{pattern.remediation}\n"
        
        return guidance
    
    def get_all_patterns_summary(self) -> str:
        """Get summary of all patterns"""
        summary = "=== Vulnerability Knowledge Base ===\n\n"
        
        by_severity = {}
        for pattern in self.patterns.values():
            severity = pattern.severity.value
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(pattern)
        
        for severity in ["critical", "high", "medium", "low", "info"]:
            if severity in by_severity:
                summary += f"\n{severity.upper()} SEVERITY ({len(by_severity[severity])}):\n"
                for pattern in by_severity[severity]:
                    summary += f"  • {pattern.cwe_id}: {pattern.name}\n"
        
        summary += f"\nTotal Patterns: {len(self.patterns)}\n"
        return summary
