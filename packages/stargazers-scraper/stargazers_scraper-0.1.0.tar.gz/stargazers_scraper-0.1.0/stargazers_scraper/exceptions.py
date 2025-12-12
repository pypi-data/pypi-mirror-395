"""
Custom exceptions for the stargazers scraper package.
"""


class StargazersScraperError(Exception):
    """Base exception for all stargazers scraper errors."""
    pass


class InvalidRepositoryURLError(StargazersScraperError):
    """Raised when an invalid repository URL is provided."""
    pass


class RateLimitExceededError(StargazersScraperError):
    """Raised when GitHub rate limit is exceeded and retries are exhausted."""
    pass


class ProfileNotFoundError(StargazersScraperError):
    """Raised when a user profile cannot be found or accessed."""
    pass


class ExtractionError(StargazersScraperError):
    """Raised when data extraction fails."""
    pass


class FileFormatError(StargazersScraperError):
    """Raised when an unsupported file format is specified."""
    pass 