"""
Main scraper class for GitHub stargazers and their profile information.
"""

import csv
import json
import logging
import time
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from .constants import (
    DEFAULT_FILENAME,
    DEFAULT_REQUEST_DELAY,
    DEFAULT_USER_AGENT,
    GITHUB_BASE_URL,
    RATE_LIMIT_DELAY,
    RATE_LIMIT_RETRY_ATTEMPTS,
    SUPPORTED_FORMATS,
)
from .exceptions import (
    FileFormatError,
    InvalidRepositoryURLError,
    RateLimitExceededError,
)
from .extractors import AttributeExtractor, EmailExtractor

logger = logging.getLogger(__name__)


class Scraper:
    """
    Scraper for GitHub stargazers and their profile information.
    """
    
    def __init__(self, request_delay: float = DEFAULT_REQUEST_DELAY) -> None:
        """
        Initialize the scraper.
        
        Args:
            request_delay: Delay between requests in seconds.
        """
        self.request_delay = request_delay
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': DEFAULT_USER_AGENT})

    def _parse_repository_url(self, url: str) -> tuple[str, str]:
        """
        Parse repository URL to extract author and repository name.
        
        Args:
            url: GitHub repository URL.
            
        Returns:
            Tuple of (author, repository).
            
        Raises:
            InvalidRepositoryURLError: If URL format is invalid.
        """
        try:
            url = url.replace('www.github.com', 'github.com')
            
            parts = url.strip('/').split('/')
            
            github_index = -1
            for i, part in enumerate(parts):
                if 'github.com' in part:
                    github_index = i
                    break
                    
            if github_index == -1 or len(parts) < github_index + 3:
                raise InvalidRepositoryURLError(f"Invalid repository URL format: {url}")
                
            author = parts[github_index + 1]
            repository = parts[github_index + 2]
            
            if not author or not repository:
                raise InvalidRepositoryURLError(f"Could not extract author/repository from URL: {url}")
                
            logger.info(f"Parsed repository: {author}/{repository}")
            return author, repository
            
        except (IndexError, AttributeError) as e:
            raise InvalidRepositoryURLError(f"Invalid repository URL format: {url}") from e

    def _find_all_stargazers(self, author: str, repository: str, page: int = 1, 
                            limit: Optional[int] = None) -> List[str]:
        """
        Find usernames of all stargazers of the repository.
        
        Args:
            author: Repository owner/author.
            repository: Repository name.
            page: Starting page number.
            limit: Maximum number of stargazers to collect.
            
        Returns:
            List of usernames.
            
        Raises:
            RateLimitExceededError: If rate limit is exceeded.
        """
        usernames = []
        current_page = page
        retry_count = 0
        
        while True:
            if limit and len(usernames) >= limit:
                break
                
            logger.info(f"Finding stargazers of {author}/{repository} on page {current_page}...")

            url = f'{GITHUB_BASE_URL}/{author}/{repository}/stargazers?page={current_page}'
            
            try:
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    stargazers = soup.find_all("a", {"class": "d-inline-block"})

                    if not stargazers:
                        logger.info("No more stargazers found, reached end of pages")
                        break

                    for stargazer in stargazers:
                        if limit and len(usernames) >= limit:
                            break
                            
                        href = stargazer.get("href")
                        if href and href.startswith('/'):
                            username = href[1:]
                            usernames.append(username)
                        
                    current_page += 1
                    retry_count = 0
                    
                elif response.status_code == 429:
                    retry_count += 1
                    if retry_count > RATE_LIMIT_RETRY_ATTEMPTS:
                        raise RateLimitExceededError("Rate limit exceeded, max retries reached")
                        
                    logger.warning(f"Rate limited, waiting {RATE_LIMIT_DELAY}s... (attempt {retry_count})")
                    time.sleep(RATE_LIMIT_DELAY)
                    continue
                    
                else:
                    logger.error(f"Failed to fetch stargazers: HTTP {response.status_code}")
                    break
                    
            except requests.RequestException as e:
                logger.error(f"Request failed for page {current_page}: {e}")
                break
                
        logger.info(f"Found {len(usernames)} stargazers total")
        return usernames

    def _apply_filter(self, stargazer_info: Dict[str, any], filter_attrs: List[str]) -> bool:
        """
        Check if stargazer meets filter criteria.
        
        Args:
            stargazer_info: The stargazer information dictionary.
            filter_attrs: List of attributes that must be non-null/non-empty.
            
        Returns:
            True if stargazer meets all filter criteria.
        """
        for attr in filter_attrs:
            value = stargazer_info.get(attr)
            if value is None or value == "" or (isinstance(value, (list, dict)) and not value):
                return False
        return True

    def _fill_email_template(self, template: str, stargazer_info: Dict[str, any], 
                            author: str, repository: str) -> str:
        """
        Fill email template with stargazer information.
        
        Args:
            template: Email template string with placeholders.
            stargazer_info: Stargazer information to fill template.
            author: Repository author.
            repository: Repository name.
            
        Returns:
            Filled email template.
        """
        try:
            name = stargazer_info.get('name') or stargazer_info['username']
            name_parts = name.split(' ') if name else [stargazer_info['username']]
            
            template_data = {
                'first-name': name_parts[0],
                'last-name': name_parts[1] if len(name_parts) > 1 else name_parts[0],
                'name': name,
                'username': stargazer_info['username'],
                'repository_name': f"{author}/{repository}",
                'company': stargazer_info.get('company', ''),
                'location': stargazer_info.get('location', ''),
                'github_url': stargazer_info['github_url']
            }
            
            return template.format(**template_data)
            
        except (KeyError, IndexError) as e:
            logger.warning(f"Template placeholder error for {stargazer_info.get('username', 'unknown')}: {e}")
            return template

    def _extract_user_profile(self, username: str) -> Optional[Dict[str, any]]:
        """
        Extract profile information for a single user.
        
        Args:
            username: GitHub username to extract profile for.
            
        Returns:
            Dictionary with user profile information or None if extraction fails.
        """
        try:
            profile_url = f"{GITHUB_BASE_URL}/{username}"
            response = self.session.get(profile_url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                attr_extractor = AttributeExtractor()
                attributes = attr_extractor.extract_attributes(soup)
                
                stargazer_info = {
                    "username": username,
                    "github_url": f"{GITHUB_BASE_URL}/{username}",
                    **attributes
                }

                try:
                    email_extractor = EmailExtractor(username)
                    email = email_extractor.extract_email()
                    stargazer_info["email"] = email
                except Exception as e:
                    logger.debug(f"Could not extract email for {username}: {e}")
                    stargazer_info["email"] = None

                return stargazer_info
                
            elif response.status_code == 404:
                logger.warning(f"Profile not found for user: {username}")
            elif response.status_code == 429:
                logger.warning(f"Rate limited while fetching profile for {username}")
                time.sleep(RATE_LIMIT_DELAY)
            else:
                logger.warning(f"Failed to fetch profile for {username}: HTTP {response.status_code}")
                
        except requests.RequestException as e:
            logger.error(f"Request failed for user {username}: {e}")
            
        return None

    def scrape_stargazers(self, url: str, filter: Optional[List[str]] = None, 
                         limit: Optional[int] = None, 
                         email_template: Optional[str] = None) -> List[Dict[str, any]]:
        """
        Scrape stargazers and their profile information.
        
        Args:
            url: GitHub repository URL to scrape.
            filter: List of attributes that must be non-null for a user to be included.
            limit: Maximum number of stargazers to scrape.
            email_template: Email template to fill with user data.
            
        Returns:
            List of stargazer information dictionaries.
            
        Raises:
            InvalidRepositoryURLError: If repository URL is invalid.
            RateLimitExceededError: If rate limit is exceeded.
        """
        author, repository = self._parse_repository_url(url)
        
        usernames = self._find_all_stargazers(author, repository, limit=limit)
        
        if not usernames:
            logger.warning("No stargazers found")
            return []
        
        logger.info(f"Found {len(usernames)} stargazers. Extracting profile information...")
        
        stargazers = []
        
        for i, username in enumerate(usernames, 1):
            logger.info(f"[{i}/{len(usernames)}] Extracting info for {username}...")
            
            stargazer_info = self._extract_user_profile(username)
            
            if stargazer_info is None:
                continue
                
            if filter and not self._apply_filter(stargazer_info, filter):
                logger.debug(f"User {username} filtered out due to missing required attributes")
                continue

            if email_template:
                stargazer_info["outreach_email"] = self._fill_email_template(
                    email_template, stargazer_info, author, repository
                )
            
            stargazers.append(stargazer_info)

            if i < len(usernames):
                time.sleep(self.request_delay)
                
        logger.info(f"Successfully extracted information for {len(stargazers)} stargazers")
        return stargazers

    def save_as(self, data: List[Dict[str, any]], format: str, 
               filename: Optional[str] = None) -> None:
        """
        Save scraped data in specified format.
        
        Args:
            data: The stargazer data to save.
            format: Output format: 'csv', 'json', or 'txt'.
            filename: Output filename. If not provided, uses generic naming.
            
        Raises:
            FileFormatError: If unsupported format is specified.
        """
        if format.lower() not in SUPPORTED_FORMATS:
            raise FileFormatError(f"Unsupported format: {format}. Use one of: {', '.join(SUPPORTED_FORMATS)}")

        if not filename:
            filename = DEFAULT_FILENAME

        if not data:
            logger.warning("No data to save")
            return

        try:
            if format.lower() == 'csv':
                self._save_as_csv(data, f"{filename}.csv")
            elif format.lower() == 'json':
                self._save_as_json(data, f"{filename}.json")
            elif format.lower() == 'txt':
                self._save_as_txt(data, f"{filename}.txt")
                
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise

    def _save_as_csv(self, data: List[Dict[str, any]], filename: str) -> None:
        """
        Save data as CSV file.
        
        Args:
            data: Data to save.
            filename: Output filename.
        """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            flattened_data = []
            for row in data:
                csv_row = row.copy()
                if 'social_links' in csv_row and isinstance(csv_row['social_links'], dict):
                    social_links = csv_row.pop('social_links')
                    for key, value in social_links.items():
                        csv_row[f'social_{key}'] = value
                flattened_data.append(csv_row)
            
            if flattened_data:
                fieldnames = flattened_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(flattened_data)
                
        logger.info(f"Data saved to {filename}")

    def _save_as_json(self, data: List[Dict[str, any]], filename: str) -> None:
        """
        Save data as JSON file.
        
        Args:
            data: Data to save.
            filename: Output filename.
        """
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {filename}")

    def _save_as_txt(self, data: List[Dict[str, any]], filename: str) -> None:
        """
        Save email addresses as text file.
        
        Args:
            data: Data containing email addresses.
            filename: Output filename.
        """
        emails = [item.get('email') for item in data if item.get('email')]
        with open(filename, 'w', encoding='utf-8') as txtfile:
            for email in emails:
                txtfile.write(f"{email}\n")
        logger.info(f"{len(emails)} email addresses saved to {filename}")