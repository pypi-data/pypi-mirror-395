import logging

from cssselect import SelectorError

from qcrawl.core.item import Item
from qcrawl.core.spider import Spider

logger = logging.getLogger(__name__)


class Quotes(Spider):
    name = "quotes_css"
    start_urls = ["https://quotes.toscrape.com/"]

    custom_settings = {
        "CONCURRENCY": 10,
        "CONCURRENCY_PER_DOMAIN": 10,
        "DELAY_PER_DOMAIN": 0.25,
        "MAX_DEPTH": 0,  # unlimited depth
        "TIMEOUT": 30.0,
        "MAX_RETRIES": 3,
        "USER_AGENT": "qCrawl-Examples/1.0",
        "REQUIRED_FIELDS": ["text", "author"],
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html",
            "User-Agent": "qCrawl-Examples/1.0",
        },
        "PIPELINES": {
            "qcrawl.pipelines.validation.ValidationPipeline": 200,
        },
    }

    async def parse(self, response):
        rv = self.response_view(response)

        # Safe cssselect usage: catch SelectorError (unsupported/invalid selectors)
        try:
            quotes = rv.doc.cssselect("div.quote")
        except SelectorError:
            # Skip page gracefully (engine will not treat as an error)
            return

        for q in quotes:
            try:
                text = q.cssselect("span.text")[0].text_content().strip()
                author = q.cssselect("small.author")[0].text_content().strip()
                tags = [t.text_content().strip() for t in q.cssselect("div.tags a.tag")]
            except (IndexError, SelectorError):
                # Missing node or inner selector problem — skip this item
                continue

            yield Item(data={"url": response.url, "text": text, "author": author, "tags": tags})

        # Follow pagination (use rv.follow to resolve correctly)
        next_a = rv.doc.cssselect("li.next a")
        if next_a:
            href = next_a[0].get("href")
            if href:
                yield rv.follow(href)
