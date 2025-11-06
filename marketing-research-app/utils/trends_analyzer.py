"""Analyze trends from Google Trends, Twitter, and other sources."""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests
from .config import Config

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except ImportError:
    PYTRENDS_AVAILABLE = False


class TrendsAnalyzer:
    """Analyze trending topics and patterns."""

    def __init__(self):
        self.headers = {
            'User-Agent': Config.USER_AGENT
        }

    def get_google_trends(
        self,
        company_name: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Get Google Trends data for the last N days.

        Args:
            company_name: Company name to search
            days: Number of days to look back

        Returns:
            Trends data
        """
        if not PYTRENDS_AVAILABLE:
            return {
                'status': 'library_missing',
                'note': 'pytrends library not available',
                'sample_data': self._get_sample_trends()
            }

        try:
            # Initialize pytrends
            pytrends = TrendReq(hl='en-US', tz=360)

            # Build payload
            keywords = [company_name]

            # Get date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"

            pytrends.build_payload(
                keywords,
                cat=0,
                timeframe=timeframe,
                geo='US'
            )

            # Get interest over time
            interest_over_time = pytrends.interest_over_time()

            # Get related queries
            related_queries = pytrends.related_queries()

            # Get trending searches
            trending_searches = pytrends.trending_searches(pn='united_states')

            return {
                'status': 'success',
                'company_name': company_name,
                'timeframe': timeframe,
                'interest_over_time': interest_over_time.to_dict() if not interest_over_time.empty else {},
                'related_queries': related_queries,
                'trending_searches': trending_searches.head(10).to_dict() if not trending_searches.empty else {},
                'summary': self._summarize_trends(interest_over_time, related_queries, trending_searches)
            }

        except Exception as e:
            print(f"Error getting Google Trends: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'sample_data': self._get_sample_trends()
            }

    def get_twitter_trends(self, location: str = 'United States') -> List[Dict[str, Any]]:
        """
        Get Twitter/X trending topics.

        Args:
            location: Location for trends

        Returns:
            List of trending topics
        """
        # Note: Twitter API v2 requires authentication
        # For MVP, return sample data

        return self._get_sample_twitter_trends()

    def get_tiktok_trends(self) -> List[Dict[str, Any]]:
        """
        Get TikTok trending sounds and hashtags.

        Returns:
            List of TikTok trends
        """
        # Note: TikTok Creative Center requires authentication
        # For MVP, return sample data

        return self._get_sample_tiktok_trends()

    def _summarize_trends(
        self,
        interest_over_time,
        related_queries,
        trending_searches
    ) -> str:
        """Summarize trends data."""
        summary_parts = []

        if not interest_over_time.empty:
            avg_interest = interest_over_time.iloc[:, 0].mean()
            summary_parts.append(f"Average search interest: {avg_interest:.1f}/100")

        if related_queries:
            summary_parts.append("Related search queries available")

        if not trending_searches.empty:
            summary_parts.append(f"Top {len(trending_searches)} trending searches included")

        return " | ".join(summary_parts) if summary_parts else "No data available"

    def _get_sample_trends(self) -> Dict[str, Any]:
        """Get sample Google Trends data for testing."""
        return {
            'this_week_trends': [
                {
                    'keyword': 'AI marketing',
                    'growth': '+150%',
                    'category': 'Technology',
                    'note': 'Sample trend data'
                },
                {
                    'keyword': 'Sustainable fashion',
                    'growth': '+75%',
                    'category': 'Lifestyle',
                    'note': 'Sample trend data'
                },
                {
                    'keyword': 'Short-form video',
                    'growth': '+200%',
                    'category': 'Marketing',
                    'note': 'Sample trend data'
                }
            ]
        }

    def _get_sample_twitter_trends(self) -> List[Dict[str, Any]]:
        """Get sample Twitter trends for testing."""
        return [
            {
                'platform': 'Twitter/X',
                'trend': '#MarketingMonday',
                'tweet_volume': '50K',
                'category': 'Marketing',
                'note': 'Sample trend data - requires Twitter API v2 for real data'
            },
            {
                'platform': 'Twitter/X',
                'trend': 'AI Tools',
                'tweet_volume': '120K',
                'category': 'Technology',
                'note': 'Sample trend data - requires Twitter API v2 for real data'
            },
            {
                'platform': 'Twitter/X',
                'trend': '#ContentCreation',
                'tweet_volume': '80K',
                'category': 'Content',
                'note': 'Sample trend data - requires Twitter API v2 for real data'
            }
        ]

    def _get_sample_tiktok_trends(self) -> List[Dict[str, Any]]:
        """Get sample TikTok trends for testing."""
        return [
            {
                'platform': 'TikTok',
                'trend': 'POV Videos',
                'views': '2.3B',
                'category': 'Video Format',
                'note': 'Sample trend data - requires TikTok Creative Center access'
            },
            {
                'platform': 'TikTok',
                'trend': 'Behind the Scenes',
                'views': '1.8B',
                'category': 'Content Type',
                'note': 'Sample trend data - requires TikTok Creative Center access'
            },
            {
                'platform': 'TikTok',
                'trend': 'Quick Tips',
                'views': '1.5B',
                'category': 'Educational',
                'note': 'Sample trend data - requires TikTok Creative Center access'
            }
        ]

    def get_weekly_trends_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of this week's trends across all platforms.

        Returns:
            Combined trends data
        """
        return {
            'google_trends': self._get_sample_trends(),
            'twitter_trends': self._get_sample_twitter_trends(),
            'tiktok_trends': self._get_sample_tiktok_trends(),
            'summary': 'This week shows strong interest in AI-powered marketing, short-form video content, and authentic behind-the-scenes content.',
            'timestamp': datetime.now().isoformat()
        }
