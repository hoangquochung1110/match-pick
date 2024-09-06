import re

import scrapy
from scrapy_playwright.page import PageMethod

from epl_scrapy.items import MatchItem


class ArsenalMatchListSpider(scrapy.Spider):

    name = "arsenal_match_list_2024"
    start_urls = ["https://www.premierleague.com/results?co=1&se=578&cl=1"]
    custom_settings = {
        # specifies exported fields and order in csv
        "FEED_EXPORT_FIELDS": [
            "match_id",
            "gameweek",
            "home",
            "away",
            "fulltime_score",
            "halftime_score",
            "kickoff",
            "referee",
        ],
    }

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
                    PageMethod('wait_for_selector', 'span.match-fixture__container'),
                ]
            )        
        )
    
    def parse_latest_match(self, response):
        """Get match_id of latest finished match."""
        for match in response.xpath("//li[@class='match-fixture']"):
            match_item = MatchItem()
            match_item["match_id"] = match.attrib.get("data-comp-match-item")
            first_span = match.xpath(".//span[@class='match-fixture__teams ']")[0]
            score_span = first_span.xpath(".//span[@class='match-fixture__score ']").get()
            score = re.sub(r'<[^>]+>', '', score_span)  # remove HTML tags
            extracted_score = score.strip()  # trim whitespace
            match_item["fulltime_score"] = extracted_score
            yield match_item
