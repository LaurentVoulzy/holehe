"""Configuration and settings for the marketing research app."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""

    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

    # Claude API settings
    CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
    CLAUDE_MAX_TOKENS = 8000

    # Scraping settings
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    # App settings
    DEFAULT_COMPETITORS_COUNT = 3
    COMPETITORS_OPTIONS = [3, 5, 7]

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        errors = []

        if not cls.ANTHROPIC_API_KEY:
            errors.append("ANTHROPIC_API_KEY is required")

        return errors
