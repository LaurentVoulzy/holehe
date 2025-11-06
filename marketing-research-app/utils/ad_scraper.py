"""Scrape ads from Meta Ad Library, LinkedIn, and other sources."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
import re
from .config import Config


class AdScraper:
    """Scrape ads and posts from various platforms."""

    def __init__(self):
        self.headers = {
            'User-Agent': Config.USER_AGENT
        }

    def scrape_meta_ads(
        self,
        company_name: str,
        competitor_urls: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Scrape Meta Ad Library for company and competitors.

        Args:
            company_name: Target company name
            competitor_urls: List of competitor URLs

        Returns:
            Dictionary mapping company names to their ads
        """
        results = {}

        # Scrape ads for main company
        results[company_name] = self._scrape_meta_ads_for_company(company_name)

        # Scrape ads for competitors
        for url in competitor_urls:
            # Extract company name from URL
            competitor_name = self._extract_company_name(url)
            results[competitor_name] = self._scrape_meta_ads_for_company(competitor_name)
            time.sleep(1)  # Rate limiting

        return results

    def _scrape_meta_ads_for_company(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Scrape Meta Ad Library for a specific company.

        Args:
            company_name: Company name to search

        Returns:
            List of ad data
        """
        ads = []

        try:
            # Meta Ad Library search URL
            # Note: This is a simplified approach. For production, use Meta Graph API
            search_url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&q={company_name.replace(' ', '%20')}"

            response = requests.get(
                search_url,
                headers=self.headers,
                timeout=Config.REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Note: Meta's Ad Library uses dynamic JavaScript loading
                # For MVP, we'll return placeholder structure
                # In production, use Playwright or Meta Graph API

                ads.append({
                    'platform': 'Meta',
                    'company': company_name,
                    'status': 'active',
                    'note': 'Meta Ad Library requires JavaScript rendering or Graph API access',
                    'recommendation': 'Use Meta Graph API with access token for full data'
                })

        except Exception as e:
            print(f"Error scraping Meta ads for {company_name}: {e}")

        return ads

    def scrape_linkedin_posts(
        self,
        company_name: str,
        competitor_urls: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Scrape LinkedIn company posts.

        Args:
            company_name: Target company name
            competitor_urls: List of competitor URLs

        Returns:
            Dictionary mapping company names to their posts
        """
        results = {}

        # Scrape posts for main company
        results[company_name] = self._scrape_linkedin_posts_for_company(company_name)

        # Scrape posts for competitors
        for url in competitor_urls:
            competitor_name = self._extract_company_name(url)
            results[competitor_name] = self._scrape_linkedin_posts_for_company(competitor_name)
            time.sleep(1)  # Rate limiting

        return results

    def _scrape_linkedin_posts_for_company(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Scrape LinkedIn posts for a specific company.

        Args:
            company_name: Company name to search

        Returns:
            List of post data
        """
        posts = []

        try:
            # LinkedIn search URL
            search_url = f"https://www.linkedin.com/search/results/content/?keywords={company_name.replace(' ', '%20')}"

            response = requests.get(
                search_url,
                headers=self.headers,
                timeout=Config.REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Note: LinkedIn requires authentication for full access
                # For MVP, we'll return placeholder structure

                posts.append({
                    'platform': 'LinkedIn',
                    'company': company_name,
                    'status': 'requires_auth',
                    'note': 'LinkedIn scraping requires authentication',
                    'recommendation': 'Use LinkedIn API or authenticated browser session'
                })

        except Exception as e:
            print(f"Error scraping LinkedIn for {company_name}: {e}")

        return posts

    def scrape_google_ads(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Scrape Google Ads Transparency Center.

        Args:
            company_name: Company name to search

        Returns:
            List of ad data
        """
        ads = []

        try:
            # Google Ads Transparency Center URL
            search_url = f"https://adstransparency.google.com/?q={company_name.replace(' ', '+')}"

            response = requests.get(
                search_url,
                headers=self.headers,
                timeout=Config.REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                # Note: This also requires JavaScript rendering
                ads.append({
                    'platform': 'Google Ads',
                    'company': company_name,
                    'status': 'requires_js',
                    'note': 'Google Ads Transparency Center requires JavaScript rendering',
                    'recommendation': 'Use Playwright or Selenium for full data'
                })

        except Exception as e:
            print(f"Error scraping Google Ads for {company_name}: {e}")

        return ads

    def _extract_company_name(self, url: str) -> str:
        """
        Extract company name from URL.

        Args:
            url: Company URL

        Returns:
            Extracted company name
        """
        try:
            # Extract domain
            domain = url.replace('https://', '').replace('http://', '').replace('www.', '')
            domain = domain.split('/')[0]

            # Remove TLD
            name = domain.split('.')[0]

            # Capitalize
            return name.capitalize()

        except Exception:
            return url

    def get_sample_ads(self, company_name: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate sample ad data for testing.

        Args:
            company_name: Company name

        Returns:
            Sample ad data
        """
        return {
            'meta_ads': [
                {
                    'platform': 'Meta',
                    'company': company_name,
                    'ad_text': 'Sample ad text - Discover our latest products',
                    'cta': 'Shop Now',
                    'engagement': 'High',
                    'creative_type': 'Video',
                    'duration': '15s',
                    'note': 'This is sample data for MVP testing'
                }
            ],
            'linkedin_posts': [
                {
                    'platform': 'LinkedIn',
                    'company': company_name,
                    'post_text': 'Sample LinkedIn post about company updates',
                    'engagement': 'Medium',
                    'post_type': 'Image',
                    'note': 'This is sample data for MVP testing'
                }
            ]
        }
