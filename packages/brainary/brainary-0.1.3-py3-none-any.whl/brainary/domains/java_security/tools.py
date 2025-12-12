"""
Security Analysis Tools

Tool wrappers for static analysis, including CodeQL integration.
"""

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Any
from enum import Enum


class ToolStatus(Enum):
    """Tool execution status"""
    SUCCESS = "success"
    ERROR = "error"
    NOT_FOUND = "not_found"
    TIMEOUT = "timeout"


@dataclass
class ToolResult:
    """Result from tool execution"""
    status: ToolStatus
    findings: List[Dict[str, Any]]
    output: str
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class CodeQLTool:
    """
    CodeQL static analysis tool wrapper.
    
    Agents can use this tool to run CodeQL queries on Java code.
    """
    
    def __init__(self, codeql_path: Optional[str] = None, database_path: Optional[str] = None):
        """
        Initialize CodeQL tool.
        
        Args:
            codeql_path: Path to CodeQL CLI (defaults to 'codeql' in PATH)
            database_path: Path to CodeQL database (can be set later)
        """
        self.codeql_path = codeql_path or "codeql"
        self.database_path = database_path
        self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if CodeQL is available"""
        try:
            result = subprocess.run(
                [self.codeql_path, "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def is_available(self) -> bool:
        """Check if CodeQL is available"""
        return self._check_availability()
    
    def create_database(self, source_path: str, database_path: Optional[str] = None,
                       language: str = "java") -> ToolResult:
        """
        Create CodeQL database from source code.
        
        Args:
            source_path: Path to source code
            database_path: Path where database will be created
            language: Programming language (default: java)
        
        Returns:
            ToolResult with database creation status
        """
        if database_path is None:
            database_path = tempfile.mkdtemp(prefix="codeql_db_")
        
        try:
            cmd = [
                self.codeql_path,
                "database", "create",
                database_path,
                f"--language={language}",
                f"--source-root={source_path}"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                self.database_path = database_path
                return ToolResult(
                    status=ToolStatus.SUCCESS,
                    findings=[],
                    output=result.stdout,
                    metadata={"database_path": database_path}
                )
            else:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    findings=[],
                    output=result.stdout,
                    error=result.stderr
                )
        
        except subprocess.TimeoutExpired:
            return ToolResult(
                status=ToolStatus.TIMEOUT,
                findings=[],
                output="",
                error="Database creation timed out"
            )
        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                findings=[],
                output="",
                error=str(e)
            )
    
    def run_query(self, query_path: str, database_path: Optional[str] = None,
                  format: str = "sarif") -> ToolResult:
        """
        Run a CodeQL query.
        
        Args:
            query_path: Path to .ql query file or query name
            database_path: Path to CodeQL database (uses default if not provided)
            format: Output format (sarif, csv, json)
        
        Returns:
            ToolResult with query findings
        """
        db_path = database_path or self.database_path
        if not db_path:
            return ToolResult(
                status=ToolStatus.ERROR,
                findings=[],
                output="",
                error="No database path provided"
            )
        
        try:
            # Create temp file for results
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{format}', delete=False) as f:
                output_path = f.name
            
            cmd = [
                self.codeql_path,
                "database", "analyze",
                db_path,
                query_path,
                f"--format={format}",
                f"--output={output_path}"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180  # 3 minutes timeout
            )
            
            # Read results
            findings = []
            with open(output_path, 'r') as f:
                content = f.read()
                if format == "json":
                    findings = json.loads(content)
                elif format == "sarif":
                    sarif_data = json.loads(content)
                    findings = self._parse_sarif(sarif_data)
            
            # Cleanup temp file
            Path(output_path).unlink()
            
            if result.returncode == 0:
                return ToolResult(
                    status=ToolStatus.SUCCESS,
                    findings=findings,
                    output=result.stdout,
                    metadata={"query": query_path}
                )
            else:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    findings=findings,
                    output=result.stdout,
                    error=result.stderr
                )
        
        except subprocess.TimeoutExpired:
            return ToolResult(
                status=ToolStatus.TIMEOUT,
                findings=[],
                output="",
                error="Query execution timed out"
            )
        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                findings=[],
                output="",
                error=str(e)
            )
    
    def run_security_suite(self, database_path: Optional[str] = None) -> ToolResult:
        """
        Run standard security query suite for Java.
        
        Args:
            database_path: Path to CodeQL database
        
        Returns:
            ToolResult with all security findings
        """
        # Use built-in security query suite
        return self.run_query("java-security-extended.qls", database_path)
    
    def _parse_sarif(self, sarif_data: Dict) -> List[Dict[str, Any]]:
        """Parse SARIF format to simplified findings"""
        findings = []
        
        try:
            for run in sarif_data.get("runs", []):
                for result in run.get("results", []):
                    rule_id = result.get("ruleId", "unknown")
                    message = result.get("message", {}).get("text", "")
                    level = result.get("level", "warning")
                    
                    locations = []
                    for location in result.get("locations", []):
                        phys_loc = location.get("physicalLocation", {})
                        artifact = phys_loc.get("artifactLocation", {})
                        region = phys_loc.get("region", {})
                        
                        locations.append({
                            "file": artifact.get("uri", ""),
                            "start_line": region.get("startLine", 0),
                            "end_line": region.get("endLine", 0),
                            "start_column": region.get("startColumn", 0),
                            "snippet": region.get("snippet", {}).get("text", "")
                        })
                    
                    findings.append({
                        "rule_id": rule_id,
                        "message": message,
                        "level": level,
                        "locations": locations
                    })
        except Exception as e:
            # Return empty list on parse error
            pass
        
        return findings


class PatternMatcher:
    """
    Simple regex-based pattern matching tool.
    
    Lightweight alternative to CodeQL for basic pattern detection.
    """
    
    def __init__(self):
        self.patterns = {}
    
    def add_pattern(self, name: str, regex: str, description: str):
        """Add a detection pattern"""
        import re
        self.patterns[name] = {
            "regex": re.compile(regex, re.MULTILINE),
            "description": description
        }
    
    def scan_file(self, file_path: str) -> ToolResult:
        """
        Scan a file for patterns.
        
        Args:
            file_path: Path to file to scan
        
        Returns:
            ToolResult with pattern matches
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            findings = []
            for name, pattern_info in self.patterns.items():
                regex = pattern_info["regex"]
                matches = regex.finditer(content)
                
                for match in matches:
                    # Calculate line number
                    line_num = content[:match.start()].count('\n') + 1
                    
                    findings.append({
                        "pattern": name,
                        "description": pattern_info["description"],
                        "file": file_path,
                        "line": line_num,
                        "match": match.group(0),
                        "context": self._get_context(content, match.start(), match.end())
                    })
            
            return ToolResult(
                status=ToolStatus.SUCCESS,
                findings=findings,
                output=f"Found {len(findings)} matches",
                metadata={"file": file_path}
            )
        
        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                findings=[],
                output="",
                error=str(e)
            )
    
    def scan_directory(self, dir_path: str, extensions: Optional[List[str]] = None) -> ToolResult:
        """
        Scan directory recursively.
        
        Args:
            dir_path: Directory to scan
            extensions: File extensions to scan (default: ['.java'])
        
        Returns:
            ToolResult with all findings
        """
        if extensions is None:
            extensions = ['.java']
        
        all_findings = []
        scanned_files = 0
        errors = []
        
        try:
            path = Path(dir_path)
            for ext in extensions:
                for file_path in path.rglob(f"*{ext}"):
                    result = self.scan_file(str(file_path))
                    scanned_files += 1
                    
                    if result.status == ToolStatus.SUCCESS:
                        all_findings.extend(result.findings)
                    else:
                        errors.append(f"{file_path}: {result.error}")
            
            return ToolResult(
                status=ToolStatus.SUCCESS,
                findings=all_findings,
                output=f"Scanned {scanned_files} files, found {len(all_findings)} matches",
                error="\n".join(errors) if errors else None,
                metadata={"scanned_files": scanned_files}
            )
        
        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                findings=all_findings,
                output="",
                error=str(e)
            )
    
    def _get_context(self, content: str, start: int, end: int, 
                     context_lines: int = 2) -> str:
        """Get surrounding context for a match"""
        lines = content.split('\n')
        match_line = content[:start].count('\n')
        
        start_line = max(0, match_line - context_lines)
        end_line = min(len(lines), match_line + context_lines + 1)
        
        context = '\n'.join(lines[start_line:end_line])
        return context


class SecurityScanner:
    """
    Combined security scanning tool.
    
    Orchestrates multiple tools (CodeQL, pattern matching) for comprehensive analysis.
    """
    
    def __init__(self, use_codeql: bool = True):
        """
        Initialize scanner.
        
        Args:
            use_codeql: Whether to use CodeQL (if available)
        """
        self.codeql = CodeQLTool() if use_codeql else None
        self.pattern_matcher = PatternMatcher()
        self._load_default_patterns()
    
    def _load_default_patterns(self):
        """Load default security patterns"""
        from .knowledge import VulnerabilityKnowledgeBase
        
        kb = VulnerabilityKnowledgeBase()
        for pattern in kb.patterns.values():
            for code_pattern in pattern.code_patterns:
                self.pattern_matcher.add_pattern(
                    f"{pattern.cwe_id}_{code_pattern[:20]}",
                    code_pattern,
                    f"{pattern.name}: {pattern.description}"
                )
    
    def scan(self, target: str, use_codeql: bool = True, 
             use_patterns: bool = True) -> Dict[str, ToolResult]:
        """
        Run comprehensive security scan.
        
        Args:
            target: File or directory to scan
            use_codeql: Whether to use CodeQL
            use_patterns: Whether to use pattern matching
        
        Returns:
            Dictionary of tool results
        """
        results = {}
        
        # Pattern-based scan (fast)
        if use_patterns:
            if Path(target).is_file():
                results["patterns"] = self.pattern_matcher.scan_file(target)
            else:
                results["patterns"] = self.pattern_matcher.scan_directory(target)
        
        # CodeQL scan (slow but thorough)
        if use_codeql and self.codeql and self.codeql.is_available():
            # Create database if target is directory
            if Path(target).is_dir():
                db_result = self.codeql.create_database(target)
                if db_result.status == ToolStatus.SUCCESS:
                    # Run security suite
                    results["codeql"] = self.codeql.run_security_suite()
                else:
                    results["codeql"] = db_result
        
        return results
    
    def get_summary(self, results: Dict[str, ToolResult]) -> str:
        """Generate summary of scan results"""
        summary = "=== Security Scan Summary ===\n\n"
        
        total_findings = 0
        for tool_name, result in results.items():
            count = len(result.findings)
            total_findings += count
            summary += f"{tool_name.upper()}: {count} findings ({result.status.value})\n"
        
        summary += f"\nTotal Findings: {total_findings}\n"
        
        if total_findings > 0:
            summary += "\nTop Issues:\n"
            all_findings = []
            for result in results.values():
                all_findings.extend(result.findings)
            
            # Show first 5 findings
            for finding in all_findings[:5]:
                if "rule_id" in finding:
                    summary += f"  • {finding['rule_id']}: {finding['message']}\n"
                elif "pattern" in finding:
                    summary += f"  • {finding['pattern']} at line {finding['line']}\n"
        
        return summary
