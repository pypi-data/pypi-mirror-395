"""
Extractors for GitHub user profile information.
"""

import json
import logging
import re
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup

from .constants import DEFAULT_USER_AGENT, GITHUB_BASE_URL
from .exceptions import ExtractionError

logger = logging.getLogger(__name__)


class AttributeExtractor:
    """
    Extracts profile attributes from GitHub user pages.
    """

    def _extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the display name of the user.
        
        Args:
            soup: BeautifulSoup object of the user's GitHub profile.
            
        Returns:
            User's display name or None if not found.
        """
        element = soup.find("span", {"class": "p-name vcard-fullname d-block overflow-hidden"})
        if element:
            name = element.get_text(strip=True)
            return name if name else None
        return None

    def _extract_biography(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the biography of the user.
        
        Args:
            soup: BeautifulSoup object of the user's GitHub profile.
            
        Returns:
            User's biography or None if not found.
        """
        element = soup.find("div", {"class": "p-note user-profile-bio mb-3 js-user-profile-bio f4"})
        if element:
            biography = element.get("data-bio-text")
            if not biography:
                biography = element.get_text(strip=True)
            return biography if biography else None
        return None

    def _extract_company(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the company of the user.
        
        Args:
            soup: BeautifulSoup object of the user's GitHub profile.
            
        Returns:
            User's company or None if not found.
        """
        element = soup.find("span", {"class": "p-org"})
        if element:
            company = element.get_text(strip=True)
            return company if company else None
        return None

    def _extract_location(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the location of the user.
        
        Args:
            soup: BeautifulSoup object of the user's GitHub profile.
            
        Returns:
            User's location or None if not found.
        """
        element = soup.find("span", {"class": "p-label"})
        if element:
            location = element.get_text(strip=True)
            return location if location else None
        return None

    def _extract_social_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract social media links from the user's profile.
        
        Args:
            soup: BeautifulSoup object of the user's GitHub profile.
            
        Returns:
            Dictionary mapping platform names to URLs.
        """
        social_links = {}
        social_elements = soup.select('li[itemprop="social"] a, .vcard-detail a[rel="nofollow me"]')
        
        platform_mapping = {
            'twitter.com': 'x',
            'x.com': 'x',
            'linkedin.com': 'linkedin',
            'instagram.com': 'instagram',
            'youtube.com': 'youtube',
            'facebook.com': 'facebook',
            'tiktok.com': 'tiktok'
        }
        
        for element in social_elements:
            href = element.get('href', '')
            if not href:
                continue
                
            platform_name = None
            for domain, name in platform_mapping.items():
                if domain in href:
                    platform_name = name
                    break
            
            if platform_name:
                social_links[platform_name] = href
            else:
                try:
                    domain = href.split('/')[2] if '/' in href else 'unknown'
                    social_links[domain] = href
                except IndexError:
                    logger.warning(f"Could not parse social link: {href}")
        
        return social_links
    
    def extract_attributes(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        """
        Extract all profile attributes from a user's GitHub page.
        
        Args:
            soup: BeautifulSoup object of the user's GitHub profile.
            
        Returns:
            Dictionary containing extracted profile attributes.
        """
        try:
            return {
                "name": self._extract_name(soup),
                "biography": self._extract_biography(soup),
                "company": self._extract_company(soup),
                "location": self._extract_location(soup),
                "social_links": self._extract_social_links(soup)
            }
        except Exception as e:
            logger.error(f"Error extracting attributes: {e}")
            raise ExtractionError(f"Failed to extract profile attributes: {e}")


class EmailExtractor:
    """
    Extracts email addresses from GitHub users' commit history.
    """

    def __init__(self, username: str) -> None:
        """
        Initialize email extractor for a specific user.
        
        Args:
            username: GitHub username to extract email for.
        """
        self.username = username
        self.repo_name: Optional[str] = None
        self.latest_commit_hash: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': DEFAULT_USER_AGENT})

    def _get_user_repo(self) -> None:
        """
        Get the name of the user's latest repository.
        
        Raises:
            ExtractionError: If no repositories found or request fails.
        """
        try:
            url = f"{GITHUB_BASE_URL}/{self.username}/?tab=repositories"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            repo_element = soup.find("a", {"itemprop": "name codeRepository"})
            
            if not repo_element:
                raise ExtractionError(f"No repositories found for user {self.username}")
                
            self.repo_name = repo_element.get_text(strip=True)
            logger.debug(f"Found repository: {self.repo_name} for user {self.username}")
            
        except requests.RequestException as e:
            raise ExtractionError(f"Failed to fetch repositories for {self.username}: {e}")

    def _get_latest_commit(self) -> None:
        """
        Get the hash of the latest commit in the user's repository.
        
        Raises:
            ExtractionError: If commit information cannot be extracted.
        """
        if not self.repo_name:
            raise ExtractionError("Repository name not set")
            
        try:
            url = f"{GITHUB_BASE_URL}/{self.username}/{self.repo_name}/commits"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            script_element = soup.find("script", {"data-target": "react-app.embeddedData"})
            
            if not script_element:
                raise ExtractionError("Could not find commit data in page")
                
            json_data = json.loads(script_element.get_text(strip=True))
            commit_groups = json_data.get("payload", {}).get("commitGroups", [])
            
            if not commit_groups or not commit_groups[0].get("commits"):
                raise ExtractionError("No commits found in repository")
                
            self.latest_commit_hash = commit_groups[0]["commits"][0]["oid"]
            logger.debug(f"Found latest commit: {self.latest_commit_hash}")
            
        except (requests.RequestException, json.JSONDecodeError, KeyError, IndexError) as e:
            raise ExtractionError(f"Failed to get latest commit for {self.username}: {e}")
        
    def _extract_email_from_patch(self) -> Optional[str]:
        """
        Extract email from the patch file of the latest commit.
        
        Returns:
            Email address if found and not a noreply address, None otherwise.
        """
        if not self.repo_name or not self.latest_commit_hash:
            return None
            
        try:
            url = f"{GITHUB_BASE_URL}/{self.username}/{self.repo_name}/commit/{self.latest_commit_hash}.patch"
            response = self.session.get(url)
            response.raise_for_status()
            
            email_pattern = r'<([^>]+)>'
            match = re.search(email_pattern, response.text)
            
            if match:
                email = match.group(1)
                if "noreply" not in email.lower():
                    logger.debug(f"Extracted email: {email} for user {self.username}")
                    return email
                else:
                    logger.debug(f"Skipping noreply email for user {self.username}")
                    
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch patch file for {self.username}: {e}")
            
        return None

    def extract_email(self) -> Optional[str]:
        """
        Extract the user's email address from their commit history.
        
        Returns:
            Email address if found, None otherwise.
            
        Raises:
            ExtractionError: If the extraction process fails.
        """
        try:
            self._get_user_repo()
            self._get_latest_commit()
            return self._extract_email_from_patch()
        except ExtractionError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error extracting email for {self.username}: {e}")
            return None