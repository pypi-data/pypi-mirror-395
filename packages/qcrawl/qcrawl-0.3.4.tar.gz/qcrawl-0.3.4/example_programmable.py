import asyncio

from qcrawl.core.item import Item
from qcrawl.core.spider import Spider
from qcrawl.runner.run import SpiderRunner


class ProgrammaticSpider(Spider):
    name = "programmatic_spider"
    start_urls = ["https://quotes.toscrape.com/"]

    # Per-spider overrides (use canonical UPPERCASE keys when possible)
    custom_settings = {
        "CONCURRENCY": 2,
        "DELAY_PER_DOMAIN": 0.5,
        "USER_AGENT": "ProgrammaticCrawler/1.0",
    }

    async def parse(self, response):
        # Minimal parse implementation: yield one item with URL and status
        yield Item(data={"url": response.url, "status": response.status_code})


async def main():
    runner = SpiderRunner(
        settings={
            "CONCURRENCY": 4,  # global override for this run
            "CONCURRENCY_PER_DOMAIN": 2,
            "TIMEOUT": 45.0,
            "LOG_LEVEL": "INFO",
        }
    )

    await runner.crawl(ProgrammaticSpider)


if __name__ == "__main__":
    asyncio.run(main())


# class Settings(BaseSettings, frozen=True):
#     api_key: str = Field(..., env="ACME_API_KEY")
#     backend: str = Field(default="openai", env="ACME_BACKEND")
#     debug: bool = Field(default=False, env="ACME_DEBUG")
#
#
# settings = Settings()
#
#
# class FastSpider(Spider):
#     custom_settings = {CONCURRENCY}
