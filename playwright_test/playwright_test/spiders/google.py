from typing import Any
import urllib.parse
import scrapy
from scrapy.settings import BaseSettings

# Spider which attempts to crawl a Google Search page

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]
    # start_urls = ["https://youtube.com/feed/trending"

    @classmethod
    def update_settings(cls, settings: BaseSettings) -> None:
        super().update_settings(settings)

        # These settings are necessary for playwright; they can be set here
        # or in the settings.py project file

        # settings.set("DOWNLOAD_HANDLERS", {
        #     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        #     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        # })

        # settings.set("TWISTED_REACTOR", "twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    def start_requests(self):
        url = "https://www.google.com/search?q=scrapy"

        query = getattr(self, "query", None)
        if query is not None:
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

        yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response, **kwargs):
        return {"url": response.url}