import urllib.parse
import scrapy

# Spider which crawls Google Scholar search results, returning links and titles.

class GoogleScholar(scrapy.Spider):
    name = "google_scholar"
    allowed_domains = ["scholar.google.com"]

    def start_requests(self):
        url = "https://scholar.google.com/scholar?q=scrapy"

        query = getattr(self, "query", None)
        if query is not None:
            url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}"

        yield scrapy.Request(url, meta={"playwright": True})
    
    def parse(self, response, **kwargs):
        selectors_containing_links = response.xpath("//div[h3]")
        headings = selectors_containing_links.xpath(".//h3[a]")
        for heading in headings:
            # Select the href attribute
            yield {
                "href": heading.css("::attr(href)").get(),
                # TODO: fix text extraction
                "title": heading.css("::text").get(),
            }
        