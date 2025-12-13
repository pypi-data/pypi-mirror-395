"""Custom exceptions for DocuSync."""


class DocuSyncError(Exception):
    """Base exception for all DocuSync errors."""


class ConfigurationError(DocuSyncError):
    """Raised when there's an error in configuration."""


class RepositoryError(DocuSyncError):
    """Raised when there's an error with repository operations."""


class GitError(RepositoryError):
    """Raised when there's an error with Git operations."""


class FileOperationError(DocuSyncError):
    """Raised when there's an error with file operations."""
