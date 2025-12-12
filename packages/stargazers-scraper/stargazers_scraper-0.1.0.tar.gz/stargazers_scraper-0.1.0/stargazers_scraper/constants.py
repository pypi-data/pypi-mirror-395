"""
Constants and configuration for the stargazers scraper package.
"""

DEFAULT_USER_AGENT = "stargazers-scraper/0.1.0 (https://github.com/jschwarz/stargazers-scraper)"
DEFAULT_REQUEST_DELAY = 0.5
RATE_LIMIT_DELAY = 5
RATE_LIMIT_RETRY_ATTEMPTS = 3

GITHUB_BASE_URL = "https://github.com"

SUPPORTED_FORMATS = ["csv", "json", "txt"]

DEFAULT_FILENAME = "stargazers"