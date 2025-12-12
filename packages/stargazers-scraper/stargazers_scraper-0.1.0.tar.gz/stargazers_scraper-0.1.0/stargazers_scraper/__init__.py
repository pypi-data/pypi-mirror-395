"""
Stargazers Scraper

A Python package to scrape GitHub stargazers and extract their profile information.
"""

__version__ = "0.1.0"
__author__ = "Jona Schwarz"
__email__ = "jona.schwarz@code.berlin"

from .main import Scraper
from .exceptions import (
    StargazersScraperError,
    InvalidRepositoryURLError,
    RateLimitExceededError,
    ProfileNotFoundError,
    ExtractionError,
    FileFormatError,
)
from . import logging_config

__all__ = [
    "Scraper",
    "StargazersScraperError",
    "InvalidRepositoryURLError", 
    "RateLimitExceededError",
    "ProfileNotFoundError",
    "ExtractionError",
    "FileFormatError",
    "logging_config",
]

