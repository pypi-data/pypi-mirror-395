"""
Exceptions for XiaoShi AI Hub SDK
"""


class HubException(Exception):
    """Base exception for all Hub-related errors."""
    pass


class RepositoryNotFoundError(HubException):
    """Raised when a repository is not found."""
    pass


class FileNotFoundError(HubException):
    """Raised when a file is not found in the repository."""
    pass


class AuthenticationError(HubException):
    """Raised when authentication fails."""
    pass


class HTTPError(HubException):
    """Raised when an HTTP error occurs."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


