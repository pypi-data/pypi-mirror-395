# stargazers-scraper

A Python package to scrape GitHub stargazers and extract their profile information for outreach and analysis.

## Features

- 🌟 Extract stargazers from any public GitHub repository
- 👤 Gather comprehensive profile information (name, bio, company, location, social links)
- 📧 Attempt to extract email addresses from commit history
- 🔄 Handle rate limiting automatically
- 📊 Export data in CSV, JSON, or TXT formats
- 🎯 Filter users by required attributes (email, company, etc.)
- ⚡ Limit scraping to first N stargazers for efficiency
- 📧 Generate personalized outreach emails with templates

## Installation

```bash
pip install stargazers-scraper
```

## Quick Start

### Basic Usage

```python
from stargazers_scraper import Scraper
from stargazers_scraper.logging_config import setup_logging

# Enable logging to see progress
setup_logging(level="INFO")

# Initialize scraper
scraper = Scraper()

# Scrape stargazers and their information
stargazers = scraper.scrape_stargazers("https://github.com/username/repository")

print(f"Found {len(stargazers)} stargazers")
print(stargazers[0])  # Show first stargazer's info
```

### Advanced Usage with Filtering & Limiting

```python
from stargazers_scraper import Scraper
from stargazers_scraper.logging_config import setup_logging

# Enable detailed logging
setup_logging(level="DEBUG")

# Initialize scraper with custom request delay
scraper = Scraper(request_delay=1.0)  # 1 second between requests

# Only get users with email AND company, limit to 50 stargazers
data = scraper.scrape_stargazers(
    url="https://github.com/username/repository",
    filter=["email", "company"],  # Only users with both email and company
    limit=50  # Only scrape first 50 stargazers
)

# Save the data
scraper.save_as(data, format="csv", filename="filtered_stargazers")
```

### Email Template Integration

```python
from stargazers_scraper import Scraper

email_template = """
Hello {first-name},

I noticed you starred {repository_name}. I've built something similar that might interest you.

Company: {company}
Location: {location}

Best regards,
Your Name
"""

scraper = Scraper()
data = scraper.scrape_stargazers(
    url="https://github.com/username/repository",
    email_template=email_template,
    limit=20
)

# Each user now includes a filled 'outreach_email' field
for user in data:
    if user.get('outreach_email'):
        print(f"Email for {user['username']}:")
        print(user['outreach_email'])
        print("-" * 50)
```

**Available Template Variables:**

- `{first-name}` - User's first name (from display name or username)
- `{last-name}` - User's last name (from display name or username)
- `{name}` - User's full display name (falls back to username)
- `{username}` - GitHub username
- `{repository_name}` - Repository name in "owner/repo" format
- `{company}` - User's company
- `{location}` - User's location
- `{github_url}` - User's GitHub profile URL


## Data Structure

Each stargazer object contains the following information:

```python
{
    "username": "testuser",
    "name": "Test User",
    "github_url": "https://github.com/testuser",
    "biography": "Software developer passionate about open source",
    "company": "Test Company",
    "location": "Berlin, Germany",
    "email": "testuser@gmail.com",
    "social_links": {
        "x": "https://x.com/testuser",
        "linkedin": "https://linkedin.com/in/testuser",
        "youtube": "https://youtube.com/@testuser",
        "instagram": "https://instagram.com/testuser",
        "example.com": "https://example.com"  # Other links
    },
    "outreach_email": "Filled email template"  # Only when template provided
}
```

## Configuration Options

### Scraper Configuration

```python
from stargazers_scraper import Scraper

# Configure request delays and behavior
scraper = Scraper(
    request_delay=0.5  # Delay between requests in seconds (default: 0.5)
)
```

### Logging Configuration

```python
from stargazers_scraper.logging_config import setup_logging

# Configure logging levels and format
setup_logging(
    level="DEBUG",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format_string="%(asctime)s - %(levelname)s - %(message)s"
)
```

## Advanced Usage

### Email Extraction

The package attempts to extract email addresses by analyzing users' commit history:

- Looks for the user's most recent repository
- Finds their latest commit
- Extracts email from the commit's patch file
- Filters out GitHub's `noreply` addresses

**Note**: Email extraction success depends on users' GitHub privacy settings and commit practices.

### Data Export

Export your scraped data in multiple formats:

```python
from stargazers_scraper import Scraper

scraper = Scraper()
data = scraper.scrape_stargazers("https://github.com/username/repo", limit=50)

# Export as CSV (social links flattened as separate columns)
scraper.save_as(data, format="csv", filename="stargazers.csv")

# Export as JSON (preserves nested structure)
scraper.save_as(data, format="json", filename="stargazers.json")

# Export as TXT (email addresses only, one per line)
scraper.save_as(data, format="txt", filename="emails.txt")
```

### Filtering Options

Filter users by any combination of attributes:

```python
# Users with email addresses
data = scraper.scrape_stargazers(url, filter=["email"])

# Users with company and location info
data = scraper.scrape_stargazers(url, filter=["company", "location"])

# Users with social media presence
data = scraper.scrape_stargazers(url, filter=["social_links"])

# Multiple criteria
data = scraper.scrape_stargazers(url, filter=["email", "company", "location"])
```

## Best Practices

### Rate Limiting & Ethics

This package respects GitHub's terms of service and includes built-in protections:

- Automatic delays between requests (configurable)
- Rate limit detection and retry logic
- Respectful request headers with user agent identification
- Timeout handling for network issues

**Please use responsibly:**

- Don't spam users with unsolicited emails


## Use Cases

- **Developer Outreach**: Find developers interested in your project for collaboration
- **Market Research**: Analyze the community around specific technologies
- **Recruitment**: Identify potential candidates who star relevant repositories
- **Community Building**: Reach out to engaged users for feedback or beta testing
- **Academic Research**: Study open source communities and developer behavior

## Requirements

- Python 3.7+
- BeautifulSoup4 ≥4.9.3
- Requests ≥2.25.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
