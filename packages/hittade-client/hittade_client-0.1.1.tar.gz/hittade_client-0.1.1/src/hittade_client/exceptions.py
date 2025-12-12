"""Exceptions for the Hittade API client."""


class HittadeError(Exception):
    """Base exception for Hittade client."""


class HittadeAPIError(HittadeError):
    """Exception raised when the API returns an error."""


class HittadeValidationError(HittadeError):
    """Exception raised when response validation fails."""
