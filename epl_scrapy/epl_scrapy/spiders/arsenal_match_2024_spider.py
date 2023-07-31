import scrapy
from epl_scrapy.items import MatchItem
from scrapy_playwright.page import PageMethod

BASE_MATCH_URL = "https://www.premierleague.com/match/"


class ArsenalMatch2024Spider(scrapy.Spider):

    name = "Arsenal matches in 2023/24 season"

    def start_requests(self):
        self.start_urls = [
            "".join([BASE_MATCH_URL, self.match_id])
        ]
        for start_url in self.start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_match,
                cb_kwargs={"match_id": self.match_id},
                meta=dict(
                            playwright=True,
                            playwright_include_page=True,
                            playwright_page_methods=[
                                        PageMethod("wait_for_selector", "div.mcBlogStream"),
                                        PageMethod("wait_for_selector", "div.fixtures-abridged-header__title"),
                                        PageMethod("evaluate", "window.scrollBy(0, 500)"),
                            ]
                )   
            )

    def parse_match(self, response, match_id):
        # Extract data from the response here
        match = MatchItem()

        match["match_id"] = match_id
        match["kickoff"] = self._parse_kickoff(response)
        match["referee"] = self._parse_referee(response)
        match["home"] = self._parse_home(response)
        match["away"] = self._parse_away(response)
        match["fulltime_score"] = self._parse_fulltime_score(response)
        match["halftime_score"] = self._parse_halftime_score(response)
        yield match

    def _parse_home(self, response):
        return response.xpath(
            "//div[@class='mc-summary__team home t39']/a/span[@class='mc-summary__team-name u-show-phablet']/text()"
        ).get()

    def _parse_away(self, response):
        return response.xpath(
            "//div[@class='mc-summary__team away t39']/a/span[@class='mc-summary__team-name u-show-phablet']/text()"
        ).get()

    def _parse_fulltime_score(self, response):
        return response.xpath(
            "string(//div[@class='mc-summary__score js-mc-score'])"
        ).get().replace(" ", "")

    def _parse_halftime_score(self, response):
        return response.xpath("string(//div[@class='mc-summary__half-time js-mc-half-time-score-container']/node()[2])").get().strip()
    
    def _parse_kickoff(self, response):
        return response.xpath(
            "//div[@class='mc-summary__info']/text()"
        ).get()

    def _parse_referee(self, response):
        return response.xpath(
            "//strong[contains(text(), 'Referee')]/following-sibling::text()"
        ).get()
