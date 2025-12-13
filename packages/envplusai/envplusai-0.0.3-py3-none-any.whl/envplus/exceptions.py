class EnvError(Exception):
    """Base exception for envplus."""
    pass

class MissingEnvError(EnvError):
    """Raised when a required environment variable is missing."""
    pass

class ValidationError(EnvError):
    """Raised when an environment variable value is invalid."""
    pass
