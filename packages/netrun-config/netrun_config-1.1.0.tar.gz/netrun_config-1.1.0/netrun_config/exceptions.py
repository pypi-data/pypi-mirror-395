"""
Configuration exceptions for netrun-config.

Provides custom exception types for configuration validation and loading errors.
"""


class ConfigError(Exception):
    """Base exception for configuration errors."""

    pass


class ValidationError(ConfigError):
    """Exception raised when configuration validation fails."""

    pass


class KeyVaultError(ConfigError):
    """Exception raised when Azure Key Vault operations fail."""

    pass
