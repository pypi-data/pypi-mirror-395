"""
Configuration Validator for Linux SSH MCP
Provides configuration file validation, security checks, and best practices recommendations
"""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ValidationIssue:
    """Configuration validation issue"""
    severity: str  # "error", "warning", "info"
    field: str
    message: str
    suggestion: Optional[str] = None
    auto_fixable: bool = False


@dataclass
class ValidationResult:
    """Configuration validation result"""
    valid: bool
    issues: List[ValidationIssue]
    suggestions: List[str]
    security_score: int
    best_practices_score: int

    def __post_init__(self):
        if not self.issues:
            self.issues = []
        if not self.suggestions:
            self.suggestions = []


class ConfigValidator:
    """Configuration file validator with security and best practices checks"""

    def __init__(self):
        """Initialize configuration validator"""
        self.required_fields = {
            "version": str,
            "servers": dict
        }

        self.server_required_fields = {
            "id": str,
            "host": str,
            "username": str
        }

    async def validate_configuration(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate configuration file"""
        issues = []
        suggestions = []

        # Basic structure validation
        structure_issues = self._validate_structure(config)
        issues.extend(structure_issues)

        if structure_issues and any(issue.severity == "error" for issue in structure_issues):
            return ValidationResult(
                valid=False,
                issues=issues,
                suggestions=suggestions,
                security_score=0,
                best_practices_score=0
            )

        # Server configuration validation
        if "servers" in config:
            server_issues, server_suggestions = self._validate_servers(config["servers"])
            issues.extend(server_issues)
            suggestions.extend(server_suggestions)

        # Security validation
        security_score, security_issues = self._validate_security(config)
        issues.extend(security_issues)

        # Best practices validation
        best_practices_score, best_practices_issues = self._validate_best_practices(config)
        issues.extend(best_practices_issues)

        # Overall validation result
        has_errors = any(issue.severity == "error" for issue in issues)
        has_critical_warnings = len([i for i in issues if i.severity == "warning"]) > 5

        return ValidationResult(
            valid=not has_errors and not has_critical_warnings,
            issues=issues,
            suggestions=suggestions,
            security_score=security_score,
            best_practices_score=best_practices_score
        )

    def _validate_structure(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate basic configuration structure"""
        issues = []

        # Check if configuration is a dictionary
        if not isinstance(config, dict):
            issues.append(ValidationIssue(
                severity="error",
                field="root",
                message="Configuration must be a JSON object",
                suggestion="Ensure configuration file starts with '{' and ends with '}'"
            ))
            return issues

        # Check required fields
        for field, field_type in self.required_fields.items():
            if field not in config:
                issues.append(ValidationIssue(
                    severity="error",
                    field=field,
                    message=f"Missing required field: {field}",
                    auto_fixable=True
                ))
            elif not isinstance(config[field], field_type):
                issues.append(ValidationIssue(
                    severity="error",
                    field=field,
                    message=f"Field '{field}' must be of type {field_type.__name__}"
                ))

        # Validate version
        if "version" in config:
            version = config["version"]
            if isinstance(version, str) and not re.match(r'^\d+\.\d+$', version):
                issues.append(ValidationIssue(
                    severity="error",
                    field="version",
                    message="Version must be in format 'X.Y' (e.g., '2.0')",
                    auto_fixable=True
                ))

        return issues

    def _validate_servers(self, servers: Dict[str, Any]) -> tuple[List[ValidationIssue], List[str]]:
        """Validate server configurations"""
        issues = []
        suggestions = []

        if not isinstance(servers, dict):
            issues.append(ValidationIssue(
                severity="error",
                field="servers",
                message="Servers field must be a dictionary",
                suggestion="Servers should be defined as key-value pairs"
            ))
            return issues, suggestions

        if not servers:
            suggestions.append("Consider adding at least one server configuration")
            return issues, suggestions

        for server_id, server_config in servers.items():
            # Check server ID consistency
            if server_config.get("id") and server_config["id"] != server_id:
                issues.append(ValidationIssue(
                    severity="error",
                    field=f"servers.{server_id}.id",
                    message=f"Server ID '{server_config['id']}' doesn't match key '{server_id}'",
                    suggestion="Ensure server ID matches configuration key",
                    auto_fixable=True
                ))

            # Validate required server fields
            for field, field_type in self.server_required_fields.items():
                if field not in server_config:
                    issues.append(ValidationIssue(
                        severity="error",
                        field=f"servers.{server_id}.{field}",
                        message=f"Missing required field: {field}"
                    ))
                elif not isinstance(server_config[field], field_type):
                    issues.append(ValidationIssue(
                        severity="error",
                        field=f"servers.{server_id}.{field}",
                        message=f"Field '{field}' must be of type {field_type.__name__}"
                    ))

            # Validate optional fields
            if "port" in server_config:
                port = server_config["port"]
                if not isinstance(port, int) or port < 1 or port > 65535:
                    issues.append(ValidationIssue(
                        severity="error",
                        field=f"servers.{server_id}.port",
                        message="Port must be an integer between 1 and 65535",
                        auto_fixable=True
                    ))

            if "timeout" in server_config:
                timeout = server_config["timeout"]
                if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
                    issues.append(ValidationIssue(
                        severity="warning",
                        field=f"servers.{server_id}.timeout",
                        message="Timeout should be between 1 and 300 seconds",
                        auto_fixable=True
                    ))

            # Authentication validation
            has_password = bool(server_config.get("password", ""))
            has_key_file = bool(server_config.get("key_file"))

            if not has_password and not has_key_file:
                issues.append(ValidationIssue(
                    severity="error",
                    field=f"servers.{server_id}.authentication",
                    message="Server must have either password or key_file configured"
                ))
            elif has_password and has_key_file:
                suggestions.append(f"Server {server_id} has both password and key_file configured. Consider using key_file only for better security.")

            # Host validation
            if "host" in server_config:
                host = server_config["host"]
                if not self._is_valid_hostname(host):
                    issues.append(ValidationIssue(
                        severity="warning",
                        field=f"servers.{server_id}.host",
                        message=f"Host '{host}' may not be a valid hostname or IP address"
                    ))

        return issues, suggestions

    def _validate_security(self, config: Dict[str, Any]) -> tuple[int, List[ValidationIssue]]:
        """Validate security configuration"""
        issues = []
        score = 100

        servers = config.get("servers", {})

        # Check for password authentication
        password_auth_count = 0
        for server_config in servers.values():
            if server_config.get("password"):
                password_auth_count += 1
                issues.append(ValidationIssue(
                    severity="warning",
                    field="security.password_auth",
                    message=f"Server {server_config.get('id', 'unknown')} uses password authentication",
                    suggestion="Consider using SSH key authentication for better security"
                ))

        if password_auth_count > 0:
            score -= 20 * (password_auth_count / max(len(servers), 1))

        # Check for default ports
        default_port_count = sum(1 for s in servers.values() if s.get("port", 22) == 22)
        if default_port_count > 0:
            score -= 10
            issues.append(ValidationIssue(
                severity="info",
                field="security.default_ports",
                message=f"{default_port_count} server(s) use default SSH port 22",
                suggestion="Consider using non-standard ports for better security"
            ))

        # Check settings for security best practices
        settings = config.get("settings", {})
        if not settings.get("host_key_checking", True):
            score -= 30
            issues.append(ValidationIssue(
                severity="error",
                field="settings.host_key_checking",
                message="Host key checking is disabled",
                suggestion="Enable host key checking to prevent man-in-the-middle attacks"
            ))

        return max(0, int(score)), issues

    def _validate_best_practices(self, config: Dict[str, Any]) -> tuple[int, List[ValidationIssue]]:
        """Validate configuration best practices"""
        issues = []
        score = 100

        # Check for description fields
        servers = config.get("servers", {})
        servers_without_desc = sum(1 for s in servers.values() if not s.get("description"))
        if servers_without_desc > 0:
            score -= 5
            issues.append(ValidationIssue(
                severity="info",
                field="best_practices.descriptions",
                message=f"{servers_without_desc} server(s) lack descriptions",
                suggestion="Add descriptions to servers for better organization"
            ))

        # Check for grouping
        groups = config.get("groups", {})
        if not groups and len(servers) > 1:
            score -= 10
            issues.append(ValidationIssue(
                severity="info",
                field="best_practices.grouping",
                message="Multiple servers without grouping",
                suggestion="Consider organizing servers into groups for easier management"
            ))

        # Check for scripts
        scripts = config.get("scripts", {})
        if not scripts:
            score -= 5
            issues.append(ValidationIssue(
                severity="info",
                field="best_practices.scripts",
                message="No pre-defined scripts configured",
                suggestion="Add common command scripts to automate repetitive tasks"
            ))

        # Check timeout values
        for server_id, server_config in servers.items():
            timeout = server_config.get("timeout", 30)
            if timeout > 60:
                score -= 2
                issues.append(ValidationIssue(
                    severity="warning",
                    field=f"best_practices.timeout.{server_id}",
                    message=f"Server {server_id} has long timeout ({timeout}s)",
                    suggestion="Consider reducing timeout for faster error detection"
                ))

        return max(0, int(score)), issues

    def _is_valid_hostname(self, hostname: str) -> bool:
        """Check if hostname is valid"""
        # IPv4 address pattern
        ipv4_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

        # IPv6 address pattern (simplified)
        ipv6_pattern = r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'

        # Hostname pattern
        hostname_pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$)'

        return bool(re.match(ipv4_pattern, hostname) or
                      re.match(ipv6_pattern, hostname) or
                      re.match(hostname_pattern, hostname))

    async def generate_fixes(self, config: Dict[str, Any], issues: List[ValidationIssue]) -> Dict[str, Any]:
        """Generate automatic fixes for applicable issues"""
        fixed_config = config.copy()
        applied_fixes = []

        for issue in issues:
            if not issue.auto_fixable:
                continue

            try:
                field_parts = issue.field.split('.')

                if len(field_parts) >= 3 and field_parts[0] == "servers":
                    # Server-level fixes
                    server_id = field_parts[1]
                    server_field = field_parts[2]

                    if server_id in fixed_config["servers"]:
                        if server_field == "id" and fixed_config["servers"][server_id].get("id") != server_id:
                            fixed_config["servers"][server_id]["id"] = server_id
                            applied_fixes.append(f"Fixed server ID for {server_id}")

                        elif server_field == "port" and server_field in fixed_config["servers"][server_id]:
                            if not isinstance(fixed_config["servers"][server_id][server_field], int):
                                fixed_config["servers"][server_id][server_field] = 22
                                applied_fixes.append(f"Fixed port for {server_id}")

                elif field_parts[0] in ["version", "servers", "settings"]:
                    # Top-level fixes
                    if field_parts[0] == "version" and "version" in fixed_config:
                        if not isinstance(fixed_config["version"], str):
                            fixed_config["version"] = "2.0"
                            applied_fixes.append("Fixed configuration version")

            except Exception as e:
                logger.warning(f"Failed to apply fix for {issue.field}: {e}")

        return {
            "fixed_config": fixed_config,
            "applied_fixes": applied_fixes,
            "remaining_issues": [i for i in issues if not i.auto_fixable]
        }