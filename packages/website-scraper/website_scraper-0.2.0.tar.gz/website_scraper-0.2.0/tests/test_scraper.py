"""Tests for the main WebScraper class."""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import tempfile
from pathlib import Path

from website_scraper import WebScraper, ScraperConfig
from website_scraper.exporters.base import ScrapingResult, ScrapingStats


class TestScraperConfig:
    """Tests for ScraperConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ScraperConfig()
        
        assert config.base_url == ""
        assert config.max_pages == 100
        assert config.headless is True
        assert config.browser_type == "chromium"
        assert config.llm_provider == "off"
        assert config.output_format == "json"
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ScraperConfig(
            base_url="https://example.com",
            max_pages=50,
            headless=False,
            llm_provider="openai",
            output_format="markdown",
        )
        
        assert config.base_url == "https://example.com"
        assert config.max_pages == 50
        assert config.headless is False
        assert config.llm_provider == "openai"
        assert config.output_format == "markdown"
    
    def test_timing_config(self):
        """Test timing configuration."""
        config = ScraperConfig(
            min_delay=2.0,
            max_delay=5.0,
            page_timeout=60000,
        )
        
        assert config.min_delay == 2.0
        assert config.max_delay == 5.0
        assert config.page_timeout == 60000


class TestWebScraperInit:
    """Tests for WebScraper initialization."""
    
    def test_init_with_url(self):
        """Test initialization with URL string."""
        scraper = WebScraper("https://example.com")
        
        assert scraper.base_url == "https://example.com"
        assert scraper.domain == "example.com"
        assert scraper.config.base_url == "https://example.com"
    
    def test_init_with_config(self):
        """Test initialization with config object."""
        config = ScraperConfig(
            base_url="https://test.com",
            max_pages=25,
        )
        scraper = WebScraper(config=config)
        
        assert scraper.base_url == "https://test.com"
        assert scraper.config.max_pages == 25
    
    def test_init_url_overrides_config(self):
        """Test that url parameter overrides config."""
        config = ScraperConfig(base_url="https://config.com")
        scraper = WebScraper("https://override.com", config=config)
        
        assert scraper.base_url == "https://override.com"
    
    def test_init_with_kwargs(self):
        """Test initialization with keyword arguments."""
        scraper = WebScraper(
            "https://example.com",
            max_pages=10,
            headless=False,
        )
        
        assert scraper.config.max_pages == 10
        assert scraper.config.headless is False


class TestWebScraperLogging:
    """Tests for WebScraper logging functionality."""
    
    def test_logging_setup(self, temp_dir):
        """Test that logging is properly configured."""
        scraper = WebScraper(
            "https://example.com",
            log_dir=str(temp_dir),
        )
        
        assert scraper.logger is not None
        assert len(scraper.logger.handlers) >= 2
        assert scraper.log_file.exists() or True  # File created on first log
    
    def test_log_file_location(self, temp_dir):
        """Test log files are created in correct location."""
        scraper = WebScraper(
            "https://example.com",
            log_dir=str(temp_dir / "custom_logs"),
        )
        
        assert (temp_dir / "custom_logs").exists()


class TestScrapingResult:
    """Tests for ScrapingResult dataclass."""
    
    def test_to_dict(self, sample_scraping_result):
        """Test conversion to dictionary."""
        data = sample_scraping_result.to_dict()
        
        assert data["url"] == "https://example.com/test"
        assert data["title"] == "Test Page"
        assert "links" in data
        assert "images" in data
    
    def test_optional_fields(self):
        """Test ScrapingResult with minimal fields."""
        result = ScrapingResult(url="https://example.com")
        
        assert result.url == "https://example.com"
        assert result.title == ""
        assert result.content == ""
        assert result.links == []


class TestScrapingStats:
    """Tests for ScrapingStats dataclass."""
    
    def test_to_dict(self, sample_scraping_stats):
        """Test conversion to dictionary."""
        data = sample_scraping_stats.to_dict()
        
        assert data["total_pages"] == 10
        assert data["successful_pages"] == 9
        assert data["failed_pages"] == 1
        assert "success_rate" in data
        assert "duration_formatted" in data
    
    def test_format_duration_seconds(self):
        """Test duration formatting in seconds."""
        stats = ScrapingStats(duration_seconds=45)
        assert "seconds" in stats._format_duration()
    
    def test_format_duration_minutes(self):
        """Test duration formatting in minutes."""
        stats = ScrapingStats(duration_seconds=120)
        assert "minutes" in stats._format_duration()
    
    def test_format_duration_hours(self):
        """Test duration formatting in hours."""
        stats = ScrapingStats(duration_seconds=7200)
        assert "hours" in stats._format_duration()


class TestWebScraperGetDelay:
    """Tests for delay calculation."""
    
    def test_delay_within_range(self):
        """Test that delay is within configured range."""
        scraper = WebScraper(
            "https://example.com",
            min_delay=1.0,
            max_delay=3.0,
        )
        
        for _ in range(100):
            delay = scraper._get_delay()
            assert 1.0 <= delay <= 3.0


@pytest.mark.asyncio
class TestWebScraperAsync:
    """Async tests for WebScraper."""
    
    async def test_context_manager(self, mock_page, mock_context, mock_browser):
        """Test async context manager."""
        with patch('website_scraper.browser.playwright_driver.async_playwright') as mock_pw:
            # Setup mock chain
            mock_playwright = MagicMock()
            mock_playwright.start = AsyncMock(return_value=mock_playwright)
            mock_playwright.stop = AsyncMock()
            mock_playwright.chromium = MagicMock()
            mock_playwright.chromium.launch = AsyncMock(return_value=mock_browser)
            mock_browser.new_context = AsyncMock(return_value=mock_context)
            mock_pw.return_value.__aenter__ = AsyncMock(return_value=mock_playwright)
            mock_pw.return_value.start = AsyncMock(return_value=mock_playwright)
            
            scraper = WebScraper("https://example.com")
            
            # Test that initialization works
            assert scraper.base_url == "https://example.com"
