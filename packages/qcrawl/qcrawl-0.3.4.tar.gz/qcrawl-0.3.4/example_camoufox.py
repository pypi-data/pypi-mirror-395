"""Example spider using Camoufox browser automation for JavaScript rendering.

This example demonstrates:
- Using Camoufox downloader for JavaScript-rendered pages
- Configuring browser contexts (desktop and mobile)
- Executing page methods (wait for selectors, click, etc.)
- Handling anti-bot scenarios with stealth browser

Requirements:
    pip install qcrawl[camoufox]

Run:
    qcrawl example_camoufox:BrowserSpider
    # or with custom settings:
    qcrawl example_camoufox:BrowserSpider --setting CAMOUFOX_MAX_CONTEXTS=5

    # To run the interactive spider:
    qcrawl example_camoufox:InteractiveBrowserSpider
"""

import logging

from qcrawl.core.item import Item
from qcrawl.core.page import PageMethod
from qcrawl.core.request import Request
from qcrawl.core.spider import Spider

logger = logging.getLogger(__name__)


class BrowserSpider(Spider):
    """Spider that uses Camoufox browser automation for rendering JavaScript."""

    name = "browser_spider"
    start_urls = ["https://quotes.toscrape.com/js/"]

    custom_settings = {
        # Enable Camoufox downloader for 'camoufox://' protocol
        "DOWNLOAD_HANDLERS": {
            "http": "qcrawl.downloaders.HTTPDownloader",
            "https": "qcrawl.downloaders.HTTPDownloader",
            "camoufox": "qcrawl.downloaders.CamoufoxDownloader",
        },
        # Define browser contexts (different viewport sizes, user agents, etc.)
        "CAMOUFOX_CONTEXTS": {
            "default": {
                "viewport": {"width": 1280, "height": 720},
                "ignore_https_errors": False,
            },
            "mobile": {
                "viewport": {"width": 375, "height": 667},
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
            },
        },
        # Browser pool settings
        "CAMOUFOX_MAX_CONTEXTS": 2,  # Max browser contexts
        "CAMOUFOX_MAX_PAGES_PER_CONTEXT": 3,  # Max concurrent pages per context
        "CAMOUFOX_DEFAULT_NAVIGATION_TIMEOUT": 30000.0,  # milliseconds
        # Launch options (headless mode, args, etc.)
        "CAMOUFOX_LAUNCH_OPTIONS": {
            "headless": True,  # Run in headless mode
            "args": [],
        },
        # General spider settings
        "CONCURRENCY": 5,
        "DELAY_PER_DOMAIN": 0.5,
        "USER_AGENT": "qCrawl-Camoufox/1.0",
    }

    async def start_requests(self):
        """Generate initial requests using Camoufox downloader."""
        for url in self.start_urls:
            # Use 'use_handler' meta to specify which downloader to use
            yield Request(
                url=url,
                meta={
                    "use_handler": "camoufox",  # Use Camoufox downloader
                    "camoufox_context": "default",  # Which browser context to use
                    # Execute page methods before/after navigation
                    "camoufox_page_methods": [PageMethod("wait_for_selector", ".quote")],
                },
            )

    async def parse(self, response):
        """Parse JavaScript-rendered HTML response."""
        rv = self.response_view(response)

        # Extract quotes from rendered page
        quotes = rv.doc.cssselect("div.quote")
        logger.info(f"Found {len(quotes)} quotes on {response.url}")

        for q in quotes:
            try:
                text = q.cssselect("span.text")[0].text_content().strip()
                author = q.cssselect("small.author")[0].text_content().strip()
                tags = [t.text_content().strip() for t in q.cssselect("div.tags a.tag")]
            except IndexError:
                continue

            yield Item(data={"url": response.url, "text": text, "author": author, "tags": tags})

        # Follow pagination links
        next_a = rv.doc.cssselect("li.next a")
        if next_a:
            href = next_a[0].get("href")
            if href:
                yield rv.follow(
                    href,
                    meta={
                        "use_handler": "camoufox",
                        "camoufox_context": "default",
                        "camoufox_page_methods": [PageMethod("wait_for_selector", ".quote")],
                    },
                )


class InteractiveBrowserSpider(Spider):
    """Example spider showing advanced Camoufox features."""

    name = "interactive_browser"
    start_urls = ["https://quotes.toscrape.com/scroll"]

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "qcrawl.downloaders.HTTPDownloader",
            "https": "qcrawl.downloaders.HTTPDownloader",
            "camoufox": "qcrawl.downloaders.CamoufoxDownloader",
        },
        "CAMOUFOX_CONTEXTS": {"default": {"viewport": {"width": 1280, "height": 720}}},
        "CAMOUFOX_MAX_CONTEXTS": 1,
        "CAMOUFOX_MAX_PAGES_PER_CONTEXT": 1,
        "CAMOUFOX_LAUNCH_OPTIONS": {"headless": True},
        "CONCURRENCY": 1,
    }

    async def start_requests(self):
        """Generate requests with custom page interactions."""
        for url in self.start_urls:
            yield Request(
                url=url,
                meta={
                    "use_handler": "camoufox",
                    "camoufox_include_page": True,  # Keep page object for manual interaction
                    "camoufox_page_methods": [
                        PageMethod("wait_for_selector", ".quote"),
                        PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
                        PageMethod("wait_for_timeout", 2000),
                    ],
                },
            )

    async def parse(self, response):
        """Parse response and demonstrate manual page interaction."""
        rv = self.response_view(response)

        # If we have the page object, we can interact with it directly
        if "camoufox_page" in response.meta:
            page = response.meta["camoufox_page"]
            logger.info(f"Got page object: {page}")

            # You can perform additional interactions here
            # e.g., page.click(), page.fill(), page.screenshot(), etc.

            # IMPORTANT: Close the page when done
            await page.close()

        # Extract data from the rendered page
        quotes = rv.doc.cssselect("div.quote")
        logger.info(f"Found {len(quotes)} quotes on {response.url}")

        for q in quotes:
            try:
                text = q.cssselect("span.text")[0].text_content().strip()
                author = q.cssselect("small.author")[0].text_content().strip()
            except IndexError:
                continue

            yield Item(data={"url": response.url, "text": text, "author": author})


# To run this spider programmatically:
# import asyncio
# from qcrawl.runner.run import SpiderRunner
#
# async def main():
#     runner = SpiderRunner()
#     await runner.crawl(BrowserSpider)
#
# if __name__ == "__main__":
#     asyncio.run(main())
