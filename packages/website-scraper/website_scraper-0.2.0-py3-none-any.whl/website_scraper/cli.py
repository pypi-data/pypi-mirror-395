#!/usr/bin/env python3
"""
Command-line interface for the Intelligent Web Scraper.

Usage:
    website-scraper https://example.com
    website-scraper https://example.com --llm openai --format markdown
    website-scraper https://example.com --output results.json --max-pages 50
"""

import argparse
import asyncio
import os
import sys
import json
import logging
from pathlib import Path

from .scraper import WebScraper, ScraperConfig, scrape_url
from .exporters import create_exporter, ExporterType


def setup_console_logging(verbose: bool = False) -> None:
    """Setup console logging for CLI."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]
    )


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='website-scraper',
        description='Intelligent web scraper with Playwright and optional LLM support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic scraping
  website-scraper https://example.com

  # With LLM-powered extraction
  website-scraper https://example.com --llm openai

  # Export to markdown
  website-scraper https://example.com --format markdown --output results.md

  # Full options
  website-scraper https://example.com \\
      --llm anthropic \\
      --max-pages 50 \\
      --format json \\
      --output data.json \\
      --browser chromium \\
      --headless

Environment variables:
  OPENAI_API_KEY      API key for OpenAI
  ANTHROPIC_API_KEY   API key for Anthropic
  GOOGLE_API_KEY      API key for Google Gemini
        """
    )
    
    # Required arguments
    parser.add_argument(
        'url',
        help='URL to start scraping from'
    )
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path'
    )
    output_group.add_argument(
        '-f', '--format',
        type=str,
        choices=['json', 'jsonl', 'markdown', 'csv', 'tsv'],
        default='json',
        help='Output format (default: json)'
    )
    
    # Scraping options
    scrape_group = parser.add_argument_group('Scraping Options')
    scrape_group.add_argument(
        '--max-pages',
        type=int,
        default=100,
        help='Maximum number of pages to scrape (default: 100)'
    )
    scrape_group.add_argument(
        '--max-depth',
        type=int,
        default=None,
        help='Maximum link depth to follow'
    )
    scrape_group.add_argument(
        '--same-domain',
        action='store_true',
        default=True,
        help='Only follow links on the same domain (default: True)'
    )
    scrape_group.add_argument(
        '--include-external',
        action='store_true',
        help='Include external links'
    )
    
    # Timing options
    timing_group = parser.add_argument_group('Timing Options')
    timing_group.add_argument(
        '-m', '--min-delay',
        type=float,
        default=1.0,
        help='Minimum delay between requests in seconds (default: 1.0)'
    )
    timing_group.add_argument(
        '-M', '--max-delay',
        type=float,
        default=3.0,
        help='Maximum delay between requests in seconds (default: 3.0)'
    )
    timing_group.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Page load timeout in seconds (default: 30)'
    )
    
    # Browser options
    browser_group = parser.add_argument_group('Browser Options')
    browser_group.add_argument(
        '--browser',
        type=str,
        choices=['chromium', 'firefox', 'webkit'],
        default='chromium',
        help='Browser to use (default: chromium)'
    )
    browser_group.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run browser in headless mode (default: True)'
    )
    browser_group.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser with visible window (for debugging)'
    )
    browser_group.add_argument(
        '--no-stealth',
        action='store_true',
        help='Disable stealth/human simulation features'
    )
    
    # LLM options
    llm_group = parser.add_argument_group('LLM Options')
    llm_group.add_argument(
        '--llm',
        type=str,
        choices=['off', 'openai', 'anthropic', 'gemini', 'ollama'],
        default='off',
        help='LLM provider for intelligent extraction (default: off)'
    )
    llm_group.add_argument(
        '--api-key',
        type=str,
        help='API key for LLM provider (or use environment variable)'
    )
    llm_group.add_argument(
        '--model',
        type=str,
        help='Specific LLM model to use'
    )
    llm_group.add_argument(
        '--goal',
        type=str,
        help='Crawl goal description for LLM-guided navigation'
    )
    
    # Logging options
    log_group = parser.add_argument_group('Logging Options')
    log_group.add_argument(
        '-l', '--log-dir',
        type=str,
        default='logs',
        help='Directory for log files (default: logs)'
    )
    log_group.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress progress bar'
    )
    log_group.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    # Retry options
    retry_group = parser.add_argument_group('Retry Options')
    retry_group.add_argument(
        '-r', '--retries',
        type=int,
        default=3,
        help='Maximum retry attempts (default: 3)'
    )
    
    # Version
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.2.0'
    )
    
    return parser


async def run_scraper(args: argparse.Namespace) -> int:
    """Run the scraper with parsed arguments."""
    # Build configuration
    config = ScraperConfig(
        base_url=args.url,
        max_pages=args.max_pages,
        max_depth=args.max_depth,
        same_domain_only=not args.include_external,
        browser_type=args.browser,
        headless=not args.no_headless,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
        page_timeout=args.timeout * 1000,
        navigation_timeout=args.timeout * 2 * 1000,
        max_retries=args.retries,
        llm_provider=args.llm,
        llm_api_key=args.api_key,
        llm_model=args.model,
        crawl_goal=args.goal,
        output_format=args.format,
        output_path=args.output,
        log_dir=args.log_dir,
        verbose=args.verbose,
        simulate_human=not args.no_stealth,
        handle_cloudflare=not args.no_stealth,
    )
    
    try:
        async with WebScraper(config=config) as scraper:
            # Run scraping
            results, stats = await scraper.scrape(show_progress=not args.quiet)
            
            # Export results
            exporter = create_exporter(args.format)
            output = await exporter.export(results, stats)
            
            if args.output:
                # Write to file
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Add extension if needed
                if not output_path.suffix:
                    output_path = output_path.with_suffix(exporter.file_extension)
                
                output_path.write_text(output, encoding='utf-8')
                
                if not args.quiet:
                    print(f"\nResults saved to: {output_path}", file=sys.stderr)
                    print(f"Pages scraped: {stats.successful_pages}/{stats.total_pages}", file=sys.stderr)
                    print(f"Duration: {stats._format_duration()}", file=sys.stderr)
            else:
                # Print to stdout
                print(output)
            
            return 0
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_console_logging(args.verbose)
    
    # Validate LLM API key
    if args.llm != 'off' and args.llm != 'ollama':
        api_key = args.api_key
        if not api_key:
            # Check environment variables
            env_vars = {
                'openai': 'OPENAI_API_KEY',
                'anthropic': 'ANTHROPIC_API_KEY',
                'gemini': 'GOOGLE_API_KEY',
            }
            env_var = env_vars.get(args.llm)
            if env_var and not os.environ.get(env_var):
                parser.error(
                    f"LLM provider '{args.llm}' requires API key. "
                    f"Set {env_var} environment variable or use --api-key"
                )
    
    # Run async scraper
    return asyncio.run(run_scraper(args))


if __name__ == '__main__':
    sys.exit(main())
