"""
Intelligent Web Scraper

A production-grade web scraper with Playwright browser automation,
optional LLM-powered content extraction, and multiple output formats.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Set
from urllib.parse import urlparse
import logging.handlers

from tqdm import tqdm

from .browser import PlaywrightDriver, PlaywrightConfig, StealthConfig
from .extractors import ContentExtractor, ExtractedPageData, LinkExtractor, LinkInfo
from .exporters import (
    BaseExporter,
    ExportConfig,
    ScrapingResult,
    ScrapingStats,
    create_exporter,
    ExporterType,
)
from .llm import BaseLLMProvider, LLMConfig, create_llm_provider, LLMProviderType


logger = logging.getLogger(__name__)


@dataclass
class ScraperConfig:
    """Configuration for the web scraper."""
    
    # Target settings
    base_url: str = ""
    max_pages: int = 100
    max_depth: Optional[int] = None
    same_domain_only: bool = True
    
    # Browser settings
    browser_type: str = "chromium"
    headless: bool = True
    
    # Timing settings
    min_delay: float = 1.0
    max_delay: float = 3.0
    page_timeout: int = 30000
    navigation_timeout: int = 60000
    
    # Retry settings
    max_retries: int = 3
    retry_delay: float = 2.0
    
    # LLM settings
    llm_provider: str = "off"
    llm_api_key: Optional[str] = None
    llm_model: Optional[str] = None
    crawl_goal: Optional[str] = None
    
    # Export settings
    output_format: str = "json"
    output_path: Optional[str] = None
    
    # Logging settings
    log_dir: str = "logs"
    verbose: bool = True
    
    # Feature flags
    simulate_human: bool = True
    handle_cloudflare: bool = True
    extract_links: bool = True
    extract_images: bool = False


class WebScraper:
    """
    Intelligent web scraper with browser automation and optional LLM support.
    
    Features:
    - Playwright-based browser automation with stealth capabilities
    - Optional LLM integration for intelligent content extraction
    - Multiple output formats (JSON, Markdown, CSV)
    - Cloudflare bypass and human-like behavior simulation
    - Comprehensive logging and progress tracking
    
    Usage:
        # Basic usage
        async with WebScraper("https://example.com") as scraper:
            results, stats = await scraper.scrape()
        
        # With LLM
        config = ScraperConfig(
            base_url="https://example.com",
            llm_provider="openai",
            llm_api_key="sk-...",
        )
        async with WebScraper(config=config) as scraper:
            results, stats = await scraper.scrape()
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        config: Optional[ScraperConfig] = None,
        **kwargs,
    ):
        """
        Initialize the web scraper.
        
        Args:
            base_url: URL to start scraping from
            config: Full scraper configuration
            **kwargs: Override individual config options
        """
        # Handle config
        if config:
            self.config = config
        else:
            self.config = ScraperConfig(base_url=base_url or "", **kwargs)
        
        if base_url:
            self.config.base_url = base_url
        
        # Parse domain
        parsed = urlparse(self.config.base_url)
        self.domain = parsed.netloc
        self.base_url = self.config.base_url
        
        # Initialize components (lazy)
        self._driver: Optional[PlaywrightDriver] = None
        self._llm_provider: Optional[BaseLLMProvider] = None
        self._content_extractor: Optional[ContentExtractor] = None
        self._link_extractor: Optional[LinkExtractor] = None
        
        # State tracking
        self._visited_urls: Set[str] = set()
        self._url_queue: List[str] = []
        self._results: List[ScrapingResult] = []
        self._failed_urls: List[str] = []
        
        # Setup logging
        self._setup_logging()
    
    async def __aenter__(self) -> "WebScraper":
        """Async context manager entry."""
        await self._initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self._cleanup()
    
    def _setup_logging(self) -> None:
        """Configure logging with file handlers."""
        log_dir = Path(self.config.log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Configure scraper logger
        self.logger = logging.getLogger(f'WebScraper.{id(self)}')
        self.logger.setLevel(logging.DEBUG if self.config.verbose else logging.INFO)
        self.logger.propagate = False
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler for all logs
        log_file = log_dir / f'{timestamp}.log'
        file_handler = logging.handlers.RotatingFileHandler(
            str(log_file),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8',
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        
        # Debug file handler
        debug_file = log_dir / f'debug_{timestamp}.log'
        debug_handler = logging.handlers.RotatingFileHandler(
            str(debug_file),
            maxBytes=10 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8',
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s'
        ))
        self.logger.addHandler(debug_handler)
        
        self.log_file = log_file
    
    async def _initialize(self) -> None:
        """Initialize all components."""
        self.logger.info(f"Initializing scraper for {self.base_url}")
        
        # Initialize browser driver
        stealth_config = StealthConfig(
            min_delay=self.config.min_delay,
            max_delay=self.config.max_delay,
        )
        
        playwright_config = PlaywrightConfig(
            browser_type=self.config.browser_type,
            headless=self.config.headless,
            stealth_config=stealth_config,
            default_timeout=self.config.page_timeout,
            navigation_timeout=self.config.navigation_timeout,
            max_retries=self.config.max_retries,
            retry_delay=self.config.retry_delay,
        )
        
        self._driver = PlaywrightDriver(playwright_config)
        await self._driver.start()
        
        # Initialize LLM provider if configured
        if self.config.llm_provider and self.config.llm_provider.lower() != "off":
            try:
                self._llm_provider = create_llm_provider(
                    self.config.llm_provider,
                    api_key=self.config.llm_api_key,
                    model=self.config.llm_model,
                )
                self.logger.info(f"LLM provider initialized: {self.config.llm_provider}")
            except Exception as e:
                self.logger.warning(f"Failed to initialize LLM provider: {e}")
                self._llm_provider = None
        
        # Initialize extractors
        self._content_extractor = ContentExtractor(
            include_links=self.config.extract_links,
            include_images=self.config.extract_images,
        )
        
        self._link_extractor = LinkExtractor(
            base_domain=self.domain,
            include_external=not self.config.same_domain_only,
            max_depth=self.config.max_depth,
        )
        
        self.logger.info("Scraper initialization complete")
    
    async def _cleanup(self) -> None:
        """Cleanup resources."""
        self.logger.info("Cleaning up scraper resources")
        
        if self._driver:
            await self._driver.close()
            self._driver = None
        
        # Close log handlers
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)
    
    async def scrape(
        self,
        show_progress: bool = True,
    ) -> tuple[List[ScrapingResult], ScrapingStats]:
        """
        Execute the scraping process.
        
        Args:
            show_progress: Whether to show progress bar
            
        Returns:
            Tuple of (results list, statistics)
        """
        start_time = time.time()
        start_datetime = datetime.utcnow().isoformat() + "Z"
        
        self.logger.info(f"Starting scrape of {self.base_url}")
        
        # Initialize queue with base URL
        self._url_queue = [self.base_url]
        self._visited_urls = set()
        self._results = []
        self._failed_urls = []
        
        # Create progress bar
        pbar = None
        if show_progress:
            pbar = tqdm(
                total=1,
                desc="Scraping",
                unit="pages",
                dynamic_ncols=True,
            )
        
        total_links_found = 0
        
        try:
            while self._url_queue and len(self._visited_urls) < self.config.max_pages:
                url = self._url_queue.pop(0)
                
                if url in self._visited_urls:
                    continue
                
                self._visited_urls.add(url)
                
                # Process URL
                result = await self._process_url(url)
                
                if result:
                    self._results.append(result)
                    
                    # Extract and queue new links
                    if self.config.extract_links:
                        new_links = await self._extract_and_score_links(url, result)
                        total_links_found += len(new_links)
                        
                        for link in new_links:
                            if link not in self._visited_urls and link not in self._url_queue:
                                self._url_queue.append(link)
                else:
                    self._failed_urls.append(url)
                
                # Update progress
                if pbar:
                    pbar.total = max(
                        pbar.total,
                        len(self._visited_urls) + len(self._url_queue)
                    )
                    pbar.n = len(self._visited_urls)
                    pbar.refresh()
                
                # Delay between requests
                delay = self._get_delay()
                await asyncio.sleep(delay)
        
        finally:
            if pbar:
                pbar.n = len(self._visited_urls)
                pbar.refresh()
                pbar.close()
        
        # Calculate statistics
        end_time = time.time()
        duration = end_time - start_time
        
        avg_load_time = 0.0
        if self._results:
            avg_load_time = sum(r.load_time_ms for r in self._results) / len(self._results)
        
        stats = ScrapingStats(
            total_pages=len(self._visited_urls),
            successful_pages=len(self._results),
            failed_pages=len(self._failed_urls),
            total_links_found=total_links_found,
            total_links_followed=len(self._visited_urls) - 1,
            start_time=start_datetime,
            end_time=datetime.utcnow().isoformat() + "Z",
            duration_seconds=duration,
            start_url=self.base_url,
            domain=self.domain,
            avg_load_time_ms=avg_load_time,
            llm_provider=self.config.llm_provider if self._llm_provider else None,
        )
        
        self.logger.info(f"Scraping complete: {stats.successful_pages}/{stats.total_pages} pages")
        
        return self._results, stats
    
    async def _process_url(self, url: str) -> Optional[ScrapingResult]:
        """Process a single URL and extract content."""
        self.logger.info(f"Processing: {url}")
        
        try:
            # Create new page
            page = await self._driver.new_page()
            
            try:
                start_time = time.time()
                
                # Navigate to URL
                response = await self._driver.goto(
                    page,
                    url,
                    simulate_human=self.config.simulate_human,
                    handle_cloudflare=self.config.handle_cloudflare,
                )
                
                load_time = (time.time() - start_time) * 1000
                
                if not response:
                    self.logger.warning(f"Failed to load: {url}")
                    return None
                
                # Get page content
                html = await self._driver.get_page_content(page)
                title = await self._driver.get_title(page)
                
                # Extract content
                extracted = self._content_extractor.extract(html, url)
                
                # Create result
                # Convert headings from list of dicts to dict format expected by ScrapingResult
                headings_dict = {}
                for heading in extracted.headings:
                    level = heading.get("level", "h1")
                    if level not in headings_dict:
                        headings_dict[level] = []
                    headings_dict[level].append(heading.get("text", ""))
                
                # Combine internal and external links
                all_links = [
                    {"url": link, "type": "internal"} for link in extracted.internal_links
                ] + [
                    {"url": link, "type": "external"} for link in extracted.external_links
                ]
                
                result = ScrapingResult(
                    url=url,
                    title=title or extracted.title,
                    content=extracted.text or extracted.main_content,
                    meta_description=extracted.meta_description,
                    headings=headings_dict,
                    links=all_links,
                    images=[{"src": img.get("src", ""), "alt": img.get("alt", "")} for img in extracted.images],
                    scraped_at=datetime.utcnow().isoformat() + "Z",
                    load_time_ms=load_time,
                    status_code=response.status if response else 0,
                )
                
                # LLM enhancement if available
                if self._llm_provider:
                    result = await self._enhance_with_llm(result, html)
                
                self.logger.debug(f"Successfully processed: {url}")
                return result
                
            finally:
                await page.close()
        
        except Exception as e:
            self.logger.error(f"Error processing {url}: {str(e)}")
            return None
    
    async def _enhance_with_llm(
        self,
        result: ScrapingResult,
        html: str,
    ) -> ScrapingResult:
        """Enhance scraping result with LLM analysis."""
        if not self._llm_provider:
            return result
        
        try:
            self.logger.debug(f"Enhancing with LLM: {result.url}")
            
            # Extract content
            extracted = await self._llm_provider.analyze_content(
                html,
                result.url,
                extraction_goal=self.config.crawl_goal,
            )
            
            # Update result with LLM analysis
            if extracted.main_content:
                result.content = extracted.main_content
            if extracted.summary:
                result.summary = extracted.summary
            if extracted.topics:
                result.topics = extracted.topics
            if extracted.content_type != "unknown":
                result.content_type = extracted.content_type
            
            result.llm_analysis = extracted.to_dict()
            
        except Exception as e:
            self.logger.warning(f"LLM enhancement failed: {str(e)}")
        
        return result
    
    async def _extract_and_score_links(
        self,
        current_url: str,
        result: ScrapingResult,
    ) -> List[str]:
        """Extract links and optionally score them with LLM."""
        links = []
        
        # Get links from result
        raw_links = [link.get("url") for link in result.links if link.get("url")]
        
        # Filter to same domain if configured
        if self.config.same_domain_only:
            raw_links = [
                link for link in raw_links
                if urlparse(link).netloc == self.domain
            ]
        
        # LLM scoring if available
        if self._llm_provider and raw_links:
            try:
                page_context = f"Title: {result.title}\nURL: {current_url}"
                scored_links = await self._llm_provider.analyze_links(
                    [{"url": url, "text": ""} for url in raw_links[:30]],
                    page_context,
                    crawl_goal=self.config.crawl_goal,
                )
                
                # Get high-scoring links
                links = [
                    link.url for link in scored_links
                    if link.should_follow and link.relevance_score > 0.3
                ]
            except Exception as e:
                self.logger.warning(f"LLM link scoring failed: {e}")
                links = raw_links[:20]  # Fallback
        else:
            links = raw_links[:20]  # Limit without LLM
        
        return links
    
    def _get_delay(self) -> float:
        """Get random delay between requests."""
        import random
        return random.uniform(self.config.min_delay, self.config.max_delay)
    
    async def export(
        self,
        results: Optional[List[ScrapingResult]] = None,
        stats: Optional[ScrapingStats] = None,
        output_path: Optional[str] = None,
        format: Optional[str] = None,
    ) -> str:
        """
        Export scraping results to file.
        
        Args:
            results: Results to export (default: last scrape results)
            stats: Statistics to include (default: last scrape stats)
            output_path: Output file path
            format: Export format (json, markdown, csv)
            
        Returns:
            Path to exported file
        """
        results = results or self._results
        output_path = output_path or self.config.output_path
        format = format or self.config.output_format
        
        if not results:
            raise ValueError("No results to export")
        
        exporter = create_exporter(format)
        
        if output_path:
            return await exporter.export_to_file(results, output_path, stats)
        else:
            return await exporter.export(results, stats)
    
    # Synchronous wrapper for non-async usage
    def scrape_sync(self, show_progress: bool = True) -> tuple[List[ScrapingResult], ScrapingStats]:
        """
        Synchronous wrapper for scraping.
        
        This is a convenience method for non-async code.
        For better performance, use the async version.
        """
        async def _run():
            async with self:
                return await self.scrape(show_progress)
        
        return asyncio.run(_run())


# Convenience function for simple scraping
async def scrape_url(
    url: str,
    llm_provider: str = "off",
    llm_api_key: Optional[str] = None,
    output_format: str = "json",
    max_pages: int = 10,
    **kwargs,
) -> tuple[List[ScrapingResult], ScrapingStats]:
    """
    Convenience function to scrape a URL.
    
    Args:
        url: URL to scrape
        llm_provider: LLM provider to use (off, openai, anthropic, gemini, ollama)
        llm_api_key: API key for LLM provider
        output_format: Output format (json, markdown, csv)
        max_pages: Maximum pages to scrape
        **kwargs: Additional scraper config options
        
    Returns:
        Tuple of (results, stats)
    """
    config = ScraperConfig(
        base_url=url,
        llm_provider=llm_provider,
        llm_api_key=llm_api_key,
        output_format=output_format,
        max_pages=max_pages,
        **kwargs,
    )
    
    async with WebScraper(config=config) as scraper:
        return await scraper.scrape()
