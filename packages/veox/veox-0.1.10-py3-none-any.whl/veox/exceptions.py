class VeoxError(Exception):
    """Base exception for Veox."""
    pass

class APIError(VeoxError):
    """API-related errors."""
    pass

class ValidationError(VeoxError):
    """Parameter validation errors."""
    pass

class ConnectionError(VeoxError):
    """Connection and network errors."""
    pass
