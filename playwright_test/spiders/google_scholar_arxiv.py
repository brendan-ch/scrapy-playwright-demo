import urllib.parse
import scrapy

# Spider which crawls Google Scholar search results filtered
# to results from arxiv.org, then follows a link to
# scrape the abstract of the paper.

# While currently limited in functionality to arxiv.org,
# this kind of crawling could be extended to include other
# websites later, potentially handing off parsing of specific
# websites to other spiders or a utility class.

class GoogleScholarArxiv(scrapy.Spider):
    name = "google_scholar_arxiv"
    allowed_domains = ["scholar.google.com", "arxiv.org"]

    def start_requests(self):
        query = getattr(self, "query", None)
        if query is None:
            raise ValueError
        else:
            query += " site:arxiv.org"

        url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}"
        yield scrapy.Request(url, meta={"playwright": True})
    
    def parse(self, response, **kwargs):
        if response.request.url.count("scholar.google.com") == 0:
            # Hand off to helper function
            yield self.handle_follow(response)
        else:
            selectors_containing_links = response.xpath("//div[h3]")
            headings = selectors_containing_links.xpath(".//h3[a]")
            for heading in headings:
                href = heading.css("::attr(href)").get()
                # Select the href attribute
                yield {
                    "site": "scholar.google.com",
                    "href": href,
                    "title": ''.join(heading.css("::text").getall()),
                }

                # Follow the link
                yield response.follow(href)

    def handle_follow(self, response):
        if response.request.url.count("arxiv.org") > 0:
            # arxiv.org logic
            title = response.css(".title::text").get()
            authors = response.css(".authors > a::text").getall()
            abstract = "".join(response.css(".abstract::text").getall()).strip()

            return {
                "site": "arxiv.org",
                "title": title,
                # Potential application: find out which authors
                # the researcher collaborates with the most
                "authors": authors,
                "abstract": abstract,
            }

        else:
            raise NotImplementedError