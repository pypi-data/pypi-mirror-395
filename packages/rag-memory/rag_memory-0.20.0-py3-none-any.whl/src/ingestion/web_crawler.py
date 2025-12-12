"""Web crawler for documentation ingestion using Crawl4AI."""

import asyncio
import logging
import os
import sys
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse, urljoin

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
)
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from src.ingestion.models import CrawlError, CrawlResult

logger = logging.getLogger(__name__)


@contextmanager
def suppress_crawl4ai_stdout():
    """
    Context manager to suppress Crawl4AI's stdout logging.

    Crawl4AI writes progress messages like [FETCH], [SCRAPE], [COMPLETE] directly
    to stdout, which interferes with MCP's JSON-RPC protocol over stdio transport.

    This redirects stdout to stderr temporarily during crawl operations.
    """
    original_stdout = sys.stdout
    try:
        # Redirect stdout to stderr (or to devnull if you want to suppress completely)
        sys.stdout = sys.stderr
        yield
    finally:
        # Restore original stdout
        sys.stdout = original_stdout


class WebCrawler:
    """Crawls web pages for documentation ingestion."""

    def __init__(self, headless: bool = True, verbose: bool = False, delay_seconds: float = 2.0):
        """
        Initialize web crawler.

        Args:
            headless: Run browser in headless mode (default: True)
            verbose: Enable verbose logging (default: False)
            delay_seconds: Seconds to wait between page navigations in multi-page crawls (default: 2.0)
        """
        self.headless = headless
        self.verbose = verbose
        self.delay_seconds = delay_seconds
        self.visited_urls: Set[str] = set()  # Track visited URLs to prevent duplicates

        # Browser configuration
        # Extra args to prevent Playwright multi-process deadlocks in Docker
        # See: https://github.com/microsoft/playwright/issues/4761
        self.browser_config = BrowserConfig(
            headless=headless,
            verbose=verbose,
            extra_args=[
                "--disable-dev-shm-usage",     # Don't use /dev/shm (shared memory)
                "--no-sandbox",                 # Disable Chrome sandbox (required in Docker)
                "--single-process",             # CRITICAL - force single process to prevent deadlock
                "--no-zygote",                  # CRITICAL - prevent process forking
                "--disable-features=IsolateOrigins,site-per-process",  # Disable multi-process features
            ],
        )

        # Content filter to remove navigation noise and reduce document-to-document relationships
        # in knowledge graph extraction. Uses algorithmic text density + link density scoring.
        # Issue: Web pages contain navigation elements (links, breadcrumbs, sidebars) that confuse
        # Graphiti's LLM-based entity extraction, causing extraction of document structure instead of
        # semantic relationships. PruningContentFilter removes ~50-55% of navigation clutter while
        # preserving 100% of valuable documentation content.
        # See: Issue 10 in TASKS_AND_ISSUES.md for detailed analysis
        content_filter = PruningContentFilter(
            threshold=0.40,           # Lower threshold (0.35-0.40) more permissive for documentation sites
            threshold_type="fixed",   # Fixed mode is more predictable than dynamic
            min_word_threshold=5      # Keep small but meaningful content blocks
        )

        # Wrap filter in markdown generator (filter must be passed through generator, not directly)
        self.markdown_generator = DefaultMarkdownGenerator(
            content_filter=content_filter
        )

        # Crawler run configuration (for single-page crawls)
        self.crawler_config = CrawlerRunConfig(
            markdown_generator=self.markdown_generator,  # Pass generator with filter to clean content
            cache_mode=CacheMode.BYPASS,  # Always fetch fresh content
            word_count_threshold=10,  # Minimum words to consider valid content
            excluded_tags=[
                "nav", "footer", "header", "aside",  # Remove navigation
                "form", "iframe", "script", "style",  # Remove interactive/styling elements
                "noscript", "meta", "link"  # Remove non-content elements
            ],
            remove_overlay_elements=True,  # Remove popups/modals
        )

        logger.info(f"WebCrawler initialized (headless={headless}, verbose={verbose})")
        logger.info(f"Content filtering enabled: PruningContentFilter (threshold=0.40, fixed mode)")

    async def crawl_page(self, url: str, crawl_root_url: Optional[str] = None) -> CrawlResult:
        """
        Crawl a single web page.

        Args:
            url: URL to crawl
            crawl_root_url: Root URL for the crawl session (defaults to url)

        Returns:
            CrawlResult with page content and metadata
        """
        if not crawl_root_url:
            crawl_root_url = url

        crawl_timestamp = datetime.now(timezone.utc)
        crawl_session_id = str(uuid.uuid4())

        logger.info(f"Crawling page: {url}")

        try:
            with suppress_crawl4ai_stdout():
                async with AsyncWebCrawler(config=self.browser_config) as crawler:
                    result = await crawler.arun(
                        url=url,
                        config=self.crawler_config,
                    )

                    if not result.success:
                        error = CrawlError(
                            url=url,
                            error_type="crawl_failed",
                            error_message=result.error_message or "Unknown error",
                            timestamp=crawl_timestamp,
                            status_code=result.status_code,
                        )
                        logger.error(f"Failed to crawl {url}: {error.error_message}")
                        return CrawlResult(
                            url=url,
                            content="",
                            metadata={},
                            success=False,
                            error=error,
                            status_code=result.status_code,
                        )

                    # Extract metadata
                    metadata = self._build_metadata(
                        url=url,
                        crawl_root_url=crawl_root_url,
                        crawl_timestamp=crawl_timestamp,
                        crawl_session_id=crawl_session_id,
                        crawl_depth=0,  # Single page = depth 0
                        result=result,
                    )

                    # Use filtered markdown output to reduce navigation noise
                    # fit_markdown is ONLY populated when PruningContentFilter is used
                    # Falls back to markdown_with_citations if filtered version not available
                    content = result.markdown.fit_markdown or result.markdown.markdown_with_citations

                    logger.info(
                        f"Successfully crawled {url} ({len(content)} chars, "
                        f"status={result.status_code})"
                    )

                    return CrawlResult(
                        url=url,
                        content=content,
                        metadata=metadata,
                        success=True,
                        links_found=result.links.get("internal", []) if result.links else [],
                        redirected_url=result.redirected_url,
                        status_code=result.status_code,
                    )

        except Exception as e:
            error = CrawlError(
                url=url,
                error_type=type(e).__name__,
                error_message=str(e),
                timestamp=crawl_timestamp,
            )
            logger.exception(f"Exception while crawling {url}")
            return CrawlResult(
                url=url,
                content="",
                metadata={},
                success=False,
                error=error,
                status_code=None,  # No status code for exceptions
            )

    def _build_metadata(
        self,
        url: str,
        crawl_root_url: str,
        crawl_timestamp: datetime,
        crawl_session_id: str,
        crawl_depth: int,
        result,
        parent_url: Optional[str] = None,
    ) -> Dict:
        """
        Build metadata dictionary for a crawled page.

        Args:
            url: Page URL
            crawl_root_url: Root URL of the crawl
            crawl_timestamp: Timestamp of the crawl
            crawl_session_id: Unique session ID
            crawl_depth: Depth level in the crawl tree
            result: Crawl4AI result object
            parent_url: Optional parent page URL

        Returns:
            Metadata dictionary
        """
        # Use redirected URL if available (handles cross-domain redirects)
        final_url = result.redirected_url or url
        parsed = urlparse(final_url)

        metadata = {
            # PAGE IDENTITY
            "source": final_url,
            "content_type": "web_page",
            # CRAWL CONTEXT (for re-crawl management - CRITICAL)
            "crawl_root_url": crawl_root_url,
            "crawl_timestamp": crawl_timestamp.isoformat(),
            "crawl_session_id": crawl_session_id,
            "crawl_depth": crawl_depth,
            # PAGE METADATA
            "title": result.metadata.get("title", ""),
            "description": result.metadata.get("description", ""),
            "domain": parsed.netloc,
            # OPTIONAL BUT USEFUL
            "language": result.metadata.get("language", "en"),
            "status_code": result.status_code,
            "content_length": len(result.markdown.raw_markdown),
            "crawler_version": "crawl4ai-0.7.4",
        }

        if parent_url:
            metadata["parent_url"] = parent_url

        return metadata

    async def crawl_with_depth(
        self,
        url: str,
        max_depth: int = 1,
        max_pages: int = float('inf'),
        crawl_root_url: Optional[str] = None,
    ) -> List[CrawlResult]:
        """
        Crawl a website following links up to max_depth and max_pages.

        Uses sequential crawling with explicit delays between page navigations
        to avoid overwhelming servers or triggering anti-bot protection.

        Args:
            url: Starting URL
            max_depth: Maximum depth to crawl (0 = only starting page, 1 = starting + direct links, etc.)
            max_pages: Maximum number of pages to crawl (default: unlimited)
            crawl_root_url: Root URL for the crawl session (defaults to url)

        Returns:
            List of CrawlResult objects, one per page crawled (limited to max_pages)
        """
        if not crawl_root_url:
            crawl_root_url = url

        crawl_timestamp = datetime.now(timezone.utc)
        crawl_session_id = str(uuid.uuid4())

        logger.info(
            f"Starting deep crawl from {url} (max_depth={max_depth}, max_pages={max_pages}, session={crawl_session_id})"
        )

        results: List[CrawlResult] = []
        visited: Set[str] = set()
        queue: List[tuple] = [(url, 0, None)]  # (url, depth, parent_url)
        base_domain = urlparse(url).netloc

        try:
            while queue and len(results) < max_pages:
                current_url, depth, parent_url = queue.pop(0)

                # Skip if already visited
                if current_url in visited:
                    continue

                visited.add(current_url)

                # Crawl the page
                logger.info(f"Crawling page {len(results)+1}/{max_pages}: {current_url} (depth={depth})")
                result = await self.crawl_page(current_url, crawl_root_url=crawl_root_url)

                # Update metadata with depth and parent
                if result.success:
                    result.metadata["crawl_depth"] = depth
                    result.metadata["crawl_timestamp"] = crawl_timestamp.isoformat()
                    result.metadata["crawl_session_id"] = crawl_session_id
                    if parent_url:
                        result.metadata["parent_url"] = parent_url

                results.append(result)

                # Update base_domain if first page redirected to different domain
                # This handles cases like python.langchain.com -> docs.langchain.com
                if len(results) == 1 and result.success and result.redirected_url:
                    redirected_domain = urlparse(result.redirected_url).netloc
                    if redirected_domain != base_domain:
                        logger.info(
                            f"Redirect detected: {base_domain} -> {redirected_domain}, "
                            f"updating base domain for link filtering"
                        )
                        base_domain = redirected_domain

                # If successful and within depth limit, add internal links to queue
                if result.success and depth < max_depth and result.links_found:
                    for link in result.links_found:
                        # links_found contains dicts with 'href' key
                        link_url = link if isinstance(link, str) else link.get('href')
                        if not link_url:
                            continue

                        # Normalize and filter links
                        absolute_url = urljoin(current_url, link_url)
                        link_domain = urlparse(absolute_url).netloc

                        # Only follow same-domain links not yet visited
                        if link_domain == base_domain and absolute_url not in visited:
                            # Don't exceed max_pages
                            if len(results) + len(queue) < max_pages:
                                queue.append((absolute_url, depth + 1, current_url))

                # Rate limiting: Wait before next request (except after last page)
                if queue and len(results) < max_pages:
                    await asyncio.sleep(self.delay_seconds)

            logger.info(
                f"Deep crawl completed: {len(results)} pages crawled, "
                f"{sum(1 for r in results if r.success)} successful"
            )
            return results

        except Exception as e:
            error = CrawlError(
                url=url,
                error_type=type(e).__name__,
                error_message=str(e),
                timestamp=crawl_timestamp,
            )
            logger.exception(f"Exception during deep crawl from {url}")
            # Return whatever we managed to crawl plus the error
            if not results:
                results.append(
                    CrawlResult(
                        url=url,
                        content="",
                        metadata={},
                        success=False,
                        error=error,
                        status_code=None,  # No status code for exceptions
                    )
                )
            return results


async def crawl_single_page(url: str, headless: bool = True, verbose: bool = False) -> CrawlResult:
    """
    Convenience function to crawl a single page.

    Args:
        url: URL to crawl
        headless: Run browser in headless mode
        verbose: Enable verbose logging

    Returns:
        CrawlResult with page content and metadata
    """
    crawler = WebCrawler(headless=headless, verbose=verbose)
    return await crawler.crawl_page(url)
