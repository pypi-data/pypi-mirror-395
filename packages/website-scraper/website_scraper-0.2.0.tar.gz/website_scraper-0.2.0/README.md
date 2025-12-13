# Website Scraper 🕷️

[![PyPI version](https://badge.fury.io/py/website-scraper.svg)](https://badge.fury.io/py/website-scraper)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-80%25%2B%20coverage-green.svg)]()

**Intelligent web scraper with Playwright browser automation, optional LLM-powered content extraction, and Cloudflare bypass.**

A production-grade web scraper featuring:
- 🎭 **Playwright-based browser automation** with stealth capabilities
- 🤖 **Optional LLM integration** for intelligent content extraction (OpenAI, Anthropic, Gemini, Ollama)
- 🛡️ **Cloudflare bypass** and human-like behavior simulation
- 📄 **Multiple output formats** (JSON, Markdown, CSV)
- 🖥️ **Cross-platform support** (Windows, macOS, Linux)

## Installation

### Basic Installation

```bash
pip install website-scraper
```

### With LLM Support

```bash
# All LLM providers
pip install website-scraper[all-llm]

# Specific providers
pip install website-scraper[openai]
pip install website-scraper[anthropic]
pip install website-scraper[gemini]
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/ml-lubich/website-scraper.git
cd website-scraper

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev,all-llm]"

# Install Playwright browsers
playwright install chromium
```

## Quick Start

### Command Line

```bash
# Basic scraping
website-scraper https://example.com

# With LLM-powered extraction
website-scraper https://example.com --llm openai

# Export to Markdown
website-scraper https://example.com --format markdown --output results.md

# Scrape with visible browser (for debugging)
website-scraper https://example.com --no-headless

# Full options
website-scraper https://example.com \
    --llm anthropic \
    --max-pages 50 \
    --format json \
    --output data.json \
    --browser chromium \
    --min-delay 2 \
    --max-delay 5
```

### Python API

```python
import asyncio
from website_scraper import WebScraper, ScraperConfig

async def main():
    # Basic usage
    async with WebScraper("https://example.com") as scraper:
        results, stats = await scraper.scrape()
        print(f"Scraped {stats.successful_pages} pages")

asyncio.run(main())
```

### With LLM Integration

```python
import asyncio
from website_scraper import WebScraper, ScraperConfig

async def main():
    config = ScraperConfig(
        base_url="https://example.com",
        llm_provider="openai",  # or "anthropic", "gemini", "ollama"
        llm_api_key="sk-...",   # Or set OPENAI_API_KEY env var
        max_pages=20,
        output_format="markdown",
    )
    
    async with WebScraper(config=config) as scraper:
        results, stats = await scraper.scrape()
        
        # Export results
        output = await scraper.export(results, stats, "results.md")

asyncio.run(main())
```

### Synchronous Usage

```python
from website_scraper import WebScraper

# For simpler scripts that don't need async
scraper = WebScraper("https://example.com")
results, stats = scraper.scrape_sync()
```

## Features

### 🎭 Stealth Mode & Cloudflare Bypass

The scraper includes advanced anti-detection features:

- Removes automation indicators (`navigator.webdriver`)
- Realistic browser fingerprints (viewport, locale, timezone)
- Human-like behavior simulation:
  - Random mouse movements
  - Natural scrolling patterns
  - Reading delays based on content length
- Cloudflare challenge detection and waiting
- Rotating user agents and headers

### 🤖 LLM-Powered Intelligence

When LLM mode is enabled, the scraper can:

- **Smart Content Extraction**: Identify main content vs ads/navigation
- **Intelligent Navigation**: Score links by relevance, decide what to crawl
- **Data Structuring**: Convert messy HTML to clean structured data
- **Summarization**: Generate summaries of scraped content

Supported providers:
- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude)
- **Google Gemini**
- **Ollama** (local models)

### 📄 Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `json` | Structured JSON with metadata | APIs, data processing |
| `jsonl` | JSON Lines (one object per line) | Large datasets, streaming |
| `markdown` | Clean readable Markdown | Documentation, reports |
| `csv` | Comma-separated values | Spreadsheets, analysis |
| `tsv` | Tab-separated values | Data import |

## Configuration

### Environment Variables

```bash
# LLM API Keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."

# Ollama (if using non-default endpoint)
export OLLAMA_HOST="http://localhost:11434"
```

### ScraperConfig Options

```python
config = ScraperConfig(
    # Target settings
    base_url="https://example.com",
    max_pages=100,
    max_depth=None,  # None = unlimited
    same_domain_only=True,
    
    # Browser settings
    browser_type="chromium",  # chromium, firefox, webkit
    headless=True,
    
    # Timing
    min_delay=1.0,
    max_delay=3.0,
    page_timeout=30000,
    
    # Retry
    max_retries=3,
    
    # LLM
    llm_provider="off",  # off, openai, anthropic, gemini, ollama
    llm_api_key=None,
    llm_model=None,
    crawl_goal=None,  # Guide LLM navigation
    
    # Output
    output_format="json",
    output_path=None,
    
    # Logging
    log_dir="logs",
    verbose=True,
    
    # Features
    simulate_human=True,
    handle_cloudflare=True,
)
```

## CLI Reference

```
website-scraper [OPTIONS] URL

Arguments:
  URL                     URL to start scraping from

Output Options:
  -o, --output PATH       Output file path
  -f, --format FORMAT     Output format (json, jsonl, markdown, csv, tsv)

Scraping Options:
  --max-pages N           Maximum pages to scrape (default: 100)
  --max-depth N           Maximum link depth to follow
  --include-external      Include external links

Timing Options:
  -m, --min-delay SECS    Minimum delay between requests (default: 1.0)
  -M, --max-delay SECS    Maximum delay between requests (default: 3.0)
  --timeout SECS          Page load timeout (default: 30)

Browser Options:
  --browser TYPE          Browser: chromium, firefox, webkit (default: chromium)
  --headless              Run headless (default)
  --no-headless           Show browser window
  --no-stealth            Disable stealth features

LLM Options:
  --llm PROVIDER          LLM: off, openai, anthropic, gemini, ollama
  --api-key KEY           API key for LLM provider
  --model MODEL           Specific model to use
  --goal TEXT             Crawl goal for LLM navigation

Logging Options:
  -l, --log-dir DIR       Log directory (default: logs)
  -q, --quiet             Suppress progress bar
  -v, --verbose           Enable verbose logging

Other:
  -r, --retries N         Max retry attempts (default: 3)
  --version               Show version
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=website_scraper --cov-report=html

# Run specific test file
pytest tests/test_scraper.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black website_scraper tests

# Lint
ruff check website_scraper

# Type checking
mypy website_scraper
```

## Output Examples

### JSON Output

```json
{
  "metadata": {
    "exported_at": "2024-01-01T00:00:00Z",
    "total_results": 10
    },
    "stats": {
    "total_pages": 10,
    "successful_pages": 9,
    "success_rate": "90.0%",
    "duration_formatted": "2.5 minutes"
  },
  "data": [
    {
      "url": "https://example.com/page1",
      "title": "Page Title",
      "content": "Main content...",
      "summary": "AI-generated summary...",
      "topics": ["topic1", "topic2"]
    }
  ]
}
```

### Markdown Output

```markdown
# Web Scraping Results

## Statistics
| Metric | Value |
|--------|-------|
| Total Pages | 10 |
| Success Rate | 90% |

## Pages

### 1. Page Title
**URL:** https://example.com/page1

#### Summary
AI-generated summary of the page content...

#### Content
Main content extracted from the page...
```

## Troubleshooting

### Cloudflare Blocking

If you're still getting blocked:

1. Increase delays: `--min-delay 3 --max-delay 8`
2. Use non-headless mode to debug: `--no-headless`
3. Try a different browser: `--browser firefox`

### LLM Rate Limits

- Use smaller models: `--model gpt-3.5-turbo`
- Reduce max pages: `--max-pages 10`
- Use local Ollama: `--llm ollama`

### Memory Issues

For large scraping jobs:

- Reduce max pages
- Use JSONL format (streaming)
- Increase delays to reduce concurrent processing

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- [Playwright](https://playwright.dev/) for browser automation
- [OpenAI](https://openai.com/), [Anthropic](https://anthropic.com/), [Google](https://ai.google.dev/) for LLM APIs
- All contributors and users of this project
