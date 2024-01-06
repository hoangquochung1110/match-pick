import scrapy
from scrapy_playwright.page import PageMethod


class ArsenalMatchListSpider(scrapy.Spider):

    name = "arsenal match list"
    start_urls = ["https://www.premierleague.com/results?co=1&se=578&cl=1"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse_latest_match,
            meta=dict(
                        playwright=True,
                        playwright_include_page=True,
                        playwright_page_methods=[
                                    PageMethod("evaluate", "document.querySelector('#onetrust-accept-btn-handler').click()"),
                                    PageMethod("evaluate", "document.querySelector('#advertClose').click()"),
                                    PageMethod("evaluate", "window.scrollBy(0, 500)"),
                                     # This where we can implement scrolling if we want
                                     PageMethod(
                                         'wait_for_selector', 'span.match-fixture__container')
                                ]
            )        
        )
    
    def parse_latest_match(self, response):
        """Get match_id of latest finished match."""
        matches = response.xpath("//li[@class='match-fixture']")
        latest_match = None
        for match in matches:
            if match.attrib.get("data-comp-match-item-status") == "U":
                break
            latest_match = match
        if latest_match:
            yield {"match_id": match.attrib.get("data-comp-match-item")}
        # Return -1 if the season hasn't started yet.
        yield {"match_id": -1}
