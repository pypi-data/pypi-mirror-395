"""
Core environment validation logic.

Combines schema validation and security checks to provide
comprehensive environment variable validation.
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass

from .schema import SchemaGenerator
from .security import SecurityValidator, SecurityLevel


@dataclass
class ValidationResult:
    """Result of environment validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def __str__(self) -> str:
        """Format validation result as string."""
        lines = []

        if self.is_valid:
            lines.append("[OK] Validation passed")
        else:
            lines.append("[ERROR] Validation failed")

        if self.errors:
            lines.append(f"\nErrors ({len(self.errors)}):")
            for error in self.errors:
                lines.append(f"  - {error}")

        if self.warnings:
            lines.append(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"  - {warning}")

        return "\n".join(lines)


class EnvValidator:
    """Validates environment files against schemas with security checks."""

    def __init__(self, security_level: SecurityLevel = SecurityLevel.PRODUCTION):
        """
        Initialize environment validator.

        Args:
            security_level: Security level to enforce
        """
        self.schema_generator = SchemaGenerator()
        self.security_validator = SecurityValidator(security_level)

    def validate_file(
        self,
        env_file: Path,
        schema_file: Optional[Path] = None
    ) -> ValidationResult:
        """
        Validate environment file against schema.

        Args:
            env_file: Path to .env file
            schema_file: Path to .env.schema.json file (optional)

        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []

        # Parse environment file
        try:
            variables = self.schema_generator.parse_env_file(env_file)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Failed to parse environment file: {e}"],
                warnings=[]
            )

        # Schema validation (if schema provided)
        if schema_file and schema_file.exists():
            try:
                schema = self.schema_generator.load_schema(schema_file)
                schema_errors = self.schema_generator.validate_against_schema(variables, schema)
                errors.extend(schema_errors)
            except Exception as e:
                errors.append(f"Failed to load or validate schema: {e}")

        # Security validation
        try:
            security_errors = self.security_validator.validate_all(variables)
            errors.extend(security_errors)

            # Check for exposed secrets (warnings only)
            exposed_warnings = self.security_validator.check_exposed_secrets(variables)
            warnings.extend(exposed_warnings)
        except Exception as e:
            errors.append(f"Security validation failed: {e}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def validate_variables(
        self,
        variables: Dict[str, str],
        schema: Optional[Dict] = None
    ) -> ValidationResult:
        """
        Validate a dictionary of variables.

        Args:
            variables: Dictionary of environment variables
            schema: Optional schema dictionary

        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []

        # Schema validation (if schema provided)
        if schema:
            try:
                schema_errors = self.schema_generator.validate_against_schema(variables, schema)
                errors.extend(schema_errors)
            except Exception as e:
                errors.append(f"Schema validation failed: {e}")

        # Security validation
        try:
            security_errors = self.security_validator.validate_all(variables)
            errors.extend(security_errors)

            exposed_warnings = self.security_validator.check_exposed_secrets(variables)
            warnings.extend(exposed_warnings)
        except Exception as e:
            errors.append(f"Security validation failed: {e}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
