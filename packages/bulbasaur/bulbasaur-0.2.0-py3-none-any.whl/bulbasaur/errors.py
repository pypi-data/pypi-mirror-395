"""Custom exceptions for Bulbasaur."""


class BulbasaurError(Exception):
    """Base exception for all Bulbasaur errors."""

    pass


class ConversionError(BulbasaurError):
    """Raised when a conversion operation fails."""

    pass


class UnsupportedTypeError(BulbasaurError):
    """Raised when a type cannot be converted."""

    pass


class SchemaError(BulbasaurError):
    """Raised when a schema structure is invalid."""

    pass
