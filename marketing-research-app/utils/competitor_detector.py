"""Auto-detect competitors using web scraping and search."""
import requests
from bs4 import BeautifulSoup
import re
from typing import List
from urllib.parse import urlparse, quote_plus
from .config import Config


class CompetitorDetector:
    """Detect competitors for a given company."""

    def __init__(self):
        self.headers = {
            'User-Agent': Config.USER_AGENT
        }

    def detect_competitors(
        self,
        company_name: str,
        company_url: str,
        num_competitors: int = 3
    ) -> List[str]:
        """
        Auto-detect competitors using multiple strategies.

        Args:
            company_name: Name of the company
            company_url: Company website URL
            num_competitors: Number of competitors to find

        Returns:
            List of competitor URLs
        """
        competitors = []

        # Strategy 1: Google search for "X competitors" or "X alternatives"
        search_queries = [
            f"{company_name} competitors",
            f"{company_name} alternatives",
            f"companies like {company_name}"
        ]

        for query in search_queries:
            if len(competitors) >= num_competitors:
                break

            found = self._search_google(query, num_competitors - len(competitors))
            competitors.extend(found)

        # Remove duplicates and the company's own URL
        competitors = self._clean_competitor_list(competitors, company_url)

        return competitors[:num_competitors]

    def _search_google(self, query: str, limit: int = 5) -> List[str]:
        """
        Search Google for competitors.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of URLs
        """
        urls = []

        try:
            # Use DuckDuckGo HTML search (no API key needed)
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

            response = requests.get(
                search_url,
                headers=self.headers,
                timeout=Config.REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract URLs from results
                for result in soup.find_all('a', class_='result__url', limit=limit * 2):
                    href = result.get('href')
                    if href:
                        # Extract actual URL
                        url = self._extract_domain(href)
                        if url and self._is_valid_competitor_url(url):
                            urls.append(url)

                        if len(urls) >= limit:
                            break

        except Exception as e:
            print(f"Error searching for competitors: {e}")

        return urls

    def _extract_domain(self, url: str) -> str:
        """
        Extract clean domain from URL.

        Args:
            url: Raw URL

        Returns:
            Clean domain URL
        """
        try:
            # Remove DuckDuckGo redirect
            if '//duckduckgo.com' in url:
                # Extract the uddg parameter
                match = re.search(r'uddg=([^&]+)', url)
                if match:
                    url = match.group(1)

            parsed = urlparse(url)

            if parsed.scheme and parsed.netloc:
                return f"{parsed.scheme}://{parsed.netloc}"

            # Try to parse if missing scheme
            if url.startswith('www.') or '.' in url:
                return f"https://{url.split('/')[0]}"

        except Exception:
            pass

        return ""

    def _is_valid_competitor_url(self, url: str) -> bool:
        """
        Check if URL is valid for a competitor.

        Args:
            url: URL to check

        Returns:
            True if valid
        """
        # Skip these domains
        invalid_domains = [
            'google.com', 'facebook.com', 'twitter.com', 'linkedin.com',
            'youtube.com', 'wikipedia.org', 'reddit.com', 'quora.com',
            'amazon.com', 'forbes.com', 'techcrunch.com', 'bloomberg.com',
            'duckduckgo.com', 'bing.com'
        ]

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        for invalid in invalid_domains:
            if invalid in domain:
                return False

        return True

    def _clean_competitor_list(
        self,
        competitors: List[str],
        company_url: str
    ) -> List[str]:
        """
        Clean and deduplicate competitor list.

        Args:
            competitors: Raw list of competitor URLs
            company_url: Company's own URL to exclude

        Returns:
            Cleaned list
        """
        cleaned = []
        seen_domains = set()

        company_domain = urlparse(company_url).netloc.lower()

        for url in competitors:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # Skip if already seen or if it's the company's own domain
            if domain in seen_domains or domain == company_domain:
                continue

            seen_domains.add(domain)
            cleaned.append(url)

        return cleaned
