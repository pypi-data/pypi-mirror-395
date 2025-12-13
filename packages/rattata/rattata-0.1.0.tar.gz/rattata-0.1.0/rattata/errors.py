"""Custom exceptions for rattata package."""


class RattataError(Exception):
    """Base exception for all rattata errors."""

    pass


class SchemaError(RattataError):
    """Raised when schema structure is invalid."""

    pass


class ConversionError(RattataError):
    """Raised when conversion fails."""

    pass


class UnsupportedTypeError(RattataError):
    """Raised when a type cannot be converted."""

    pass
