"""Custom exceptions for DumpConfluence"""


class ConfluenceBackupError(Exception):
    """Base exception for DumpConfluence errors"""

    pass


class AuthenticationError(ConfluenceBackupError):
    """Authentication failed"""

    pass


class ValidationError(ConfluenceBackupError):
    """Input validation failed"""

    pass


class NetworkError(ConfluenceBackupError):
    """Network/API communication error"""

    pass


class FileSystemError(ConfluenceBackupError):
    """File system operation error"""

    pass
