"""
Website Scraper - Intelligent Web Scraping with Playwright and LLM Support

A production-grade web scraper featuring:
- Playwright-based browser automation with stealth capabilities
- Optional LLM integration for intelligent content extraction
- Multiple output formats (JSON, Markdown, CSV)
- Cloudflare bypass and human-like behavior simulation
- Cross-platform support (Windows, macOS, Linux)

Basic Usage:
    from website_scraper import WebScraper
    
    async with WebScraper("https://example.com") as scraper:
        results, stats = await scraper.scrape()

With LLM:
    from website_scraper import WebScraper, ScraperConfig
    
    config = ScraperConfig(
        base_url="https://example.com",
        llm_provider="openai",
        llm_api_key="sk-...",
    )
    async with WebScraper(config=config) as scraper:
        results, stats = await scraper.scrape()

Synchronous Usage:
    scraper = WebScraper("https://example.com")
    results, stats = scraper.scrape_sync()
"""

__version__ = "0.2.0"
__author__ = "Misha Lubich"
__email__ = "michaelle.lubich@gmail.com"

# Main scraper classes
from .scraper import WebScraper, ScraperConfig, scrape_url

# Browser automation
from .browser import PlaywrightDriver, PlaywrightConfig, StealthConfig

# LLM integration
from .llm import (
    BaseLLMProvider,
    LLMConfig,
    LLMProviderType,
    create_llm_provider,
    ExtractedContent,
    ScoredLink,
)

# Content extraction
from .extractors import (
    ContentExtractor,
    ExtractedPageData,
    LinkExtractor,
    LinkInfo,
)

# Export functionality
from .exporters import (
    BaseExporter,
    ExportConfig,
    ScrapingResult,
    ScrapingStats,
    JSONExporter,
    MarkdownExporter,
    CSVExporter,
    create_exporter,
    ExporterType,
)

__all__ = [
    # Version
    "__version__",
    "__author__",
    "__email__",
    # Main classes
    "WebScraper",
    "ScraperConfig",
    "scrape_url",
    # Browser
    "PlaywrightDriver",
    "PlaywrightConfig",
    "StealthConfig",
    # LLM
    "BaseLLMProvider",
    "LLMConfig",
    "LLMProviderType",
    "create_llm_provider",
    "ExtractedContent",
    "ScoredLink",
    # Extractors
    "ContentExtractor",
    "ExtractedPageData",
    "LinkExtractor",
    "LinkInfo",
    # Exporters
    "BaseExporter",
    "ExportConfig",
    "ScrapingResult",
    "ScrapingStats",
    "JSONExporter",
    "MarkdownExporter",
    "CSVExporter",
    "create_exporter",
    "ExporterType",
]
