import scrapy
from scrapy.settings import BaseSettings

class PlaywrightSpider(scrapy.Spider):
    name = "playwright_1"
    allowed_domains = ["youtube.com", "httpbin.org"]
    # start_urls = ["https://youtube.com/feed/trending"]

    @classmethod
    def update_settings(cls, settings: BaseSettings) -> None:
        super().update_settings(settings)
        settings.set("DOWNLOAD_HANDLERS", {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        })

        settings.set("TWISTED_REACTOR", "twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    def start_requests(self):
        yield scrapy.Request("https://httpbin.org/get", meta={"playwright": True})
        yield scrapy.FormRequest("https://httpbin.org/post", formdata={"foo": "bar"}, metadata={"playwright": True})

    def parse(self, response, **kwargs):
        return {"url": response.url}