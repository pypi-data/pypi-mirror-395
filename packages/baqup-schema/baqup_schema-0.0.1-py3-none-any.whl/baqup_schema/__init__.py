"""
baqup-schema - JSON Schema validation for baqup agent configuration.

This package provides:
- Schema validation for baqup agent configuration
- Environment variable loading with type coercion
- Custom format validators (path, hostname, etc.)

Part of the baqup project: https://github.com/baqupio/baqup

Example:
    from baqup_schema import load_from_env, validate

    # Load and validate from environment variables
    config = load_from_env("agent-schema.json")

    # Or validate an existing dict
    result = validate(schema, config_dict)
    if not result.valid:
        print(result.errors)
"""

__version__ = "0.0.1"
__all__ = ["validate", "load_from_env", "ValidationResult", "ValidationError"]

from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationError:
    """A single validation error."""
    path: str
    message: str
    keyword: str


@dataclass
class ValidationResult:
    """Result of schema validation."""
    valid: bool
    errors: list[ValidationError] | None = None


_PLACEHOLDER_MESSAGE = (
    "baqup-schema is currently a placeholder package. "
    "Full implementation coming soon. "
    "See https://github.com/baqupio/baqup for updates."
)


def validate(schema: dict[str, Any], config: dict[str, Any]) -> ValidationResult:
    """
    Validate a configuration object against a baqup agent schema.

    Args:
        schema: The JSON Schema object
        config: The configuration object to validate

    Returns:
        ValidationResult with any errors

    Raises:
        NotImplementedError: This is a placeholder package
    """
    raise NotImplementedError(_PLACEHOLDER_MESSAGE)


def load_from_env(
    schema_path: str,
    *,
    prefix: str = "BAQUP_",
    apply_defaults: bool = True,
    coerce_types: bool = True,
) -> dict[str, Any]:
    """
    Load configuration from environment variables based on schema.

    Args:
        schema_path: Path to the JSON Schema file
        prefix: Environment variable prefix (default: "BAQUP_")
        apply_defaults: Apply default values from schema
        coerce_types: Coerce string values to schema-defined types

    Returns:
        The loaded and validated configuration dict

    Raises:
        NotImplementedError: This is a placeholder package
    """
    raise NotImplementedError(_PLACEHOLDER_MESSAGE)
