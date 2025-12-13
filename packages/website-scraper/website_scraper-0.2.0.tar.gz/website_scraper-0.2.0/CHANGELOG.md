# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-12-07

### Added

- **Playwright Browser Automation**: Complete rewrite using Playwright for JavaScript rendering and better compatibility
- **Stealth Mode**: Anti-detection features including:
  - Removal of automation indicators
  - Human-like behavior simulation (mouse movements, scrolling, reading delays)
  - Realistic browser fingerprints
  - Cloudflare bypass capabilities
- **LLM Integration**: Optional AI-powered features with support for:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
  - Google Gemini
  - Ollama (local models)
- **Intelligent Content Extraction**: LLM-powered identification of main content vs ads/navigation
- **Smart Navigation**: LLM-guided link scoring and crawl decisions
- **Multiple Output Formats**:
  - JSON (with metadata and statistics)
  - JSON Lines (for large datasets)
  - Markdown (clean, readable output)
  - CSV/TSV (for data analysis)
- **Modern Python Packaging**: Migration to `pyproject.toml` (PEP 517/518)
- **Async Architecture**: Full async/await support for better performance
- **Comprehensive Test Suite**: 80%+ test coverage with pytest
- **Cross-Platform Support**: Windows, macOS, and Linux compatibility

### Changed

- **Breaking**: Replaced `requests` + `BeautifulSoup` with Playwright
- **Breaking**: API is now async-first (synchronous wrapper available)
- **Breaking**: Configuration via `ScraperConfig` dataclass instead of kwargs
- Improved logging with rotating file handlers
- Better error handling and retry logic
- Progress bar improvements

### Removed

- Dependency on `requests`, `beautifulsoup4`, `fake-useragent`, `lxml`
- Legacy `setup.py` (replaced with `pyproject.toml`)
- `requirements.txt` and `requirements-dev.txt` (deps now in pyproject.toml)
- Multiprocessing-based parallelism (replaced with async)

### Migration Guide

#### From 0.1.x to 0.2.0

**Old API (0.1.x):**
```python
from website_scraper import WebScraper

scraper = WebScraper(
    base_url="https://example.com",
    delay_range=(1, 3),
    max_retries=3,
)
data, stats = scraper.scrape()
```

**New API (0.2.0):**
```python
import asyncio
from website_scraper import WebScraper, ScraperConfig

async def main():
    config = ScraperConfig(
        base_url="https://example.com",
        min_delay=1.0,
        max_delay=3.0,
        max_retries=3,
    )
    async with WebScraper(config=config) as scraper:
        results, stats = await scraper.scrape()

asyncio.run(main())

# Or use synchronous wrapper:
scraper = WebScraper("https://example.com")
results, stats = scraper.scrape_sync()
```

## [0.1.1] - 2024-01-15

### Fixed

- SSL verification issues on some platforms
- XML content type detection
- Progress bar display issues

## [0.1.0] - 2024-01-01

### Added

- Initial release
- Multiprocessing support for faster scraping
- Rate limiting and random delays
- Rotating User-Agents
- Comprehensive logging system
- Progress tracking
- JSON output format
- CLI interface

