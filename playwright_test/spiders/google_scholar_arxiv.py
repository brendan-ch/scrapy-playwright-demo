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
    visited_scholar_pages: set[str] = set()

    starting_result_limit = 100
    """Limit the number of results, or the number of pagination links followed.
    The start= value of the page visited will not exceed this value."""

    downloads_enabled = False
    """If set to true (via argument passed by user), the spider will attempt to
    access PDF download links and download papers into the tmp folder."""

    def start_requests(self):
        query = getattr(self, "query", None)
        if query is None:
            raise ValueError
        else:
            query += " site:arxiv.org"

        self.downloads_enabled = getattr(self, "download", None) == "1"
    
        url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}"
        yield scrapy.Request(url, meta={"playwright": True})
    
    def parse(self, response, **kwargs):
        if response.request.url.count("scholar.google.com") == 0:
            # Hand off to helper function
            yield self.handle_follow(response)
        else:
            # Grab links to articles
            selectors_containing_links = response.xpath("//div[h3]")
            headings = selectors_containing_links.xpath(".//h3[a]")
            for heading_selector in headings:
                href = heading_selector.css("::attr(href)").get()
                # Select the href attribute
                yield {
                    "site": "scholar.google.com",
                    "href": href,
                    "title": ''.join(heading_selector.css("::text").getall()),
                }

                # Follow the link
                yield response.follow(href)

            # Grab links to additional results for selectors that are in tables
            link_selectors_in_tables = response.xpath("//table//a")
            for link_selector in link_selectors_in_tables:
                href: str = link_selector.css("::attr(href)").get()
                if "/scholar?start=" in href and href not in self.visited_scholar_pages:
                    # For context, a typical paged Google Scholar link looks like this:
                    # https://scholar.google.com/scholar?start=10&q=artificial+intelligence&hl=en&as_sdt=0,31
                    # This bit grabs the starting position (the query parameter to start)

                    start_str = ""
                    start_pos = href.find("start=") + 6
                    while href[start_pos].isdigit():
                        start_str += href[start_pos]
                        start_pos += 1
                    
                    start = int(start_str)
                    if start < self.starting_result_limit:
                        self.visited_scholar_pages.add(href)
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