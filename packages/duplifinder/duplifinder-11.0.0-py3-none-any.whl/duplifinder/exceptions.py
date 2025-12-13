# src/duplifinder/exceptions.py

"""Custom exceptions for Duplifinder."""

class DuplifinderError(Exception):
    """Base class for all Duplifinder exceptions."""
    pass

class ConfigError(DuplifinderError):
    """Raised when configuration is invalid or cannot be loaded."""
    pass

class FileProcessingError(DuplifinderError):
    """Raised when a file cannot be processed (parsing, encoding, etc)."""
    def __init__(self, message: str, filepath: str, reason: str = None):
        super().__init__(message)
        self.filepath = filepath
        self.reason = reason
