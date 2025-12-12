from qcrawl.core.spider import Spider


class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    async def parse(self, response):
        rv = self.response_view(response)

        for quote in rv.doc.cssselect("div.quote"):
            yield {
                "text": quote.cssselect("span.text")[0].text_content(),
                "author": quote.cssselect("small.author")[0].text_content(),
            }
