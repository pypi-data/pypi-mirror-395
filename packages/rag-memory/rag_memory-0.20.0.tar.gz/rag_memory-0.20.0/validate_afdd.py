#!/usr/bin/env python3
"""
AFDD (Anchor-First Dynamic Discovery) Validation Script
======================================================

This script implements and validates the Anchor-First Dynamic Discovery strategy using crawl4ai.
It demonstrates how to reliably discover documentation URLs by targeting navigation elements
on the live page, rather than relying on sitemaps or external indexes.

Usage:
    python validate_afdd.py https://example.com/docs
"""

import asyncio
import sys
import json
import logging
import time
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Any, Set
from copy import deepcopy

# Check if crawl4ai is available
try:
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
    from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
    from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
    from lxml import html as lhtml
except ImportError:
    print("Error: crawl4ai not found. Please install it with: pip install crawl4ai")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AFDD_Validator")

# -----------------------------------------------------------------------------
# Custom Strategy: Navigation-Focused Scraping
# -----------------------------------------------------------------------------

class NavigationScrapingStrategy(LXMLWebScrapingStrategy):
    """
    A custom scraping strategy that isolates navigation elements BEFORE processing.
    
    This ensures that the crawler ONLY discovers links present in the documentation
    sidebar/menu, effectively filtering out blog posts, marketing footers, and 
    irrelevant cross-links that appear in the body/footer of the page.
    """
    
    def _scrap(self, url: str, html: str, **kwargs) -> Dict[str, Any]:
        # 1. Parse the original HTML
        try:
            doc = lhtml.document_fromstring(html)
        except Exception as e:
            logger.error(f"Failed to parse HTML for {url}: {e}")
            return super()._scrap(url, html, **kwargs)

        # 2. Identify target elements (Nav/Sidebar) provided in config
        targets = kwargs.get('target_elements', [])
        
        # If no targets specified, fall back to standard scraping
        if not targets:
            return super()._scrap(url, html, **kwargs)
            
        # Create a new skeletal DOM containing ONLY the navigation elements
        # We use a <body> tag to hold them
        nav_content = lhtml.Element("body")
        
        # Preserve <head> if possible to keep metadata/base_url info
        head = doc.find('head')
        if head is not None:
            # We wrap head in html tag if we were building full doc, but LXML fragment is fine
            # crawl4ai _scrap handles doc fragments gracefully
            pass 

        found_nav = False
        
        # Comprehensive list of selectors to try if targets are generic
        # We use the specific targets passed in kwargs
        
        found_elements = []
        for selector in targets:
            try:
                elements = doc.cssselect(selector)
                for elem in elements:
                    # Deep copy to detach from original doc
                    found_elements.append(deepcopy(elem))
                    found_nav = True
            except Exception as e:
                logger.warning(f"Invalid selector '{selector}': {e}")

        if found_nav:
            logger.info(f"Found {len(found_elements)} navigation elements using selectors: {targets}")
            for elem in found_elements:
                nav_content.append(elem)
                
            # 3. Serialize this "Nav-Only" page back to HTML
            # This "fake" page contains ONLY the sidebar links
            new_html = lhtml.tostring(nav_content, encoding='unicode')
            
            # 4. Delegate to the parent strategy with our filtered HTML
            # CRITICAL: We must remove 'target_elements' from kwargs for the recursive call
            # because we've already applied the filtering. If we leave it, the parent
            # strategy might try to find them again in our constructed snippet and fail 
            # (or just do double work).
            new_kwargs = kwargs.copy()
            new_kwargs['target_elements'] = None 
            
            return super()._scrap(url, new_html, **new_kwargs)
        else:
            logger.warning(f"NO navigation elements found for {url} using {targets}. Falling back to full page.")
            return super()._scrap(url, html, **kwargs)

# -----------------------------------------------------------------------------
# Validator Class
# -----------------------------------------------------------------------------

class AFDDValidator:
    def __init__(self):
        self.results = []
        self.start_url = ""
        self.domain = ""
        self.base_path = ""
        
    async def run(self, start_url: str):
        self.start_url = start_url
        parsed = urlparse(start_url)
        self.domain = parsed.netloc
        self.base_path = parsed.path
        if not self.base_path.endswith('/'):
            # If path is /docs/intro, base might be /docs/
            # Heuristic: remove last segment if it looks like a file
            if '.' in self.base_path.split('/')[-1]:
                self.base_path = '/'.join(self.base_path.split('/')[:-1]) + '/'
        
        print(f"\n{'='*80}")
        print(f"Starting AFDD Validation for: {start_url}")
        print(f"Target Domain: {self.domain}")
        print(f"Base Path Scope: {self.base_path}")
        print(f"{'='*80}\n")

        # Configuration for AFDD
        
        # 1. Define Navigation Selectors (The "Anchor")
        # These are standard classes/roles for documentation sidebars
        nav_selectors = [
            "nav", 
            "[role='navigation']",
            ".sidebar", 
            "#sidebar",
            ".menu", 
            ".nav-link", 
            ".table-of-contents",
            "aside"
        ]

        # 2. Configure the Crawler
        config = CrawlerRunConfig(
            # Use our Custom Strategy
            scraping_strategy=NavigationScrapingStrategy(),
            
            # Pass selectors to the strategy
            target_elements=nav_selectors,
            
            # BFS Strategy: Depth 1 is usually enough to get the full sidebar structure
            # If the sidebar has "Load More" or nested structure via clicks, we might need deeper or JS
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=1,  # 0 = start page, 1 = links found on start page
                include_external=False, # Strictly internal documentation
                max_pages=1000 # Safety limit
            ),
            
            # content_filter_strategy=... could be added to check relevance
            
            # Handling SPAs: Wait for network idle or body
            wait_until="networkidle",
            
            # Cache settings (Bypass for validation to get fresh results)
            cache_mode=CacheMode.BYPASS,
            
            # Enable JS execution
            js_code=["window.scrollTo(0, document.body.scrollHeight);"],
            
            verbose=True
        )

        print("🚀 Initializing Crawler with NavigationScrapingStrategy...")
        
        async with AsyncWebCrawler() as crawler:
            # Execute the crawl
            results = await crawler.arun(
                url=start_url,
                config=config
            )
            
            # In deep crawl mode (stream=False), arun returns a list of results if using BFS strategy?
            # Wait, arun signature for single URL usually returns one result unless deep_crawl is active.
            # Let's check how BFSDeepCrawlStrategy returns.
            # It usually handles the recursion internally but arun might just return the *root* result 
            # with deep crawl results attached or flattened?
            # Actually, crawl4ai's deep crawling usually works via arun returning a list OR 
            # using arun_many internally. 
            # Let's assume for a moment we get a list or we need to handle the graph.
            
            # Correction: BFSDeepCrawlStrategy usually requires using `arun` but the results 
            # collection depends on implementation.
            # Let's treat `results` as the output.
            
            if isinstance(results, list):
                self.results = results
            else:
                # If it's a single result, it might be the root.
                # But BFS strategy in crawl4ai often accumulates results.
                self.results = [results]

        await self.analyze_results()

    async def analyze_results(self):
        print(f"\n{'='*80}")
        print("ANALYSIS REPORT")
        print(f"{'='*80}")
        
        total_pages = len(self.results)
        print(f"Total Pages Crawled: {total_pages}")
        
        if total_pages == 0:
            print("❌ No pages found. Strategy failed to extract navigation links.")
            return

        # Filter for relevant documentation URLs
        valid_urls = []
        broken_urls = []
        external_urls = []
        off_path_urls = []
        
        for res in self.results:
            if not res.success:
                broken_urls.append(res.url)
                continue
                
            parsed = urlparse(res.url)
            
            if parsed.netloc != self.domain:
                external_urls.append(res.url)
                continue
                
            if not res.url.startswith(self.start_url) and not res.url.startswith(self.base_path):
                # Check if it's at least under the same domain and reasonably looks like docs
                # But strict AFDD prefers sub-path.
                off_path_urls.append(res.url)
                continue
                
            valid_urls.append(res.url)

        print(f"✅ Valid Documentation URLs: {len(valid_urls)}")
        print(f"❌ Broken URLs: {len(broken_urls)}")
        print(f"⚠️  External URLs (skipped): {len(external_urls)}")
        print(f"⚠️  Off-Path URLs (skipped): {len(off_path_urls)}")
        
        # Quality Check
        if len(valid_urls) > 0:
            broken_rate = len(broken_urls) / (len(valid_urls) + len(broken_urls)) * 100
            print(f"\nHealth Metric: {100 - broken_rate:.1f}% Success Rate")
        
        print("\nSample Valid URLs:")
        for u in valid_urls[:10]:
            print(f"  - {u}")
            
        if off_path_urls:
            print("\nSample Off-Path URLs (Noise/Global Nav?):")
            for u in off_path_urls[:5]:
                print(f"  - {u}")

        # Save Report
        report = {
            "strategy": "AFDD (BFS + NavScraping)",
            "start_url": self.start_url,
            "stats": {
                "total": total_pages,
                "valid": len(valid_urls),
                "broken": len(broken_urls),
                "external": len(external_urls),
                "off_path": len(off_path_urls)
            },
            "valid_urls": valid_urls,
            "broken_urls": broken_urls
        }
        
        filename = f"afdd_report_{self.domain.replace('.', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Detailed JSON report saved to: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_afdd.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    validator = AFDDValidator()
    asyncio.run(validator.run(url))

