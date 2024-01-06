import datetime as dt

import scrapy

from epl_scrapy.items import MatchItem
from epl_scrapy.utils import import_symbol

BASE_MATCH_URL = "https://www.premierleague.com/match/"


class EPLMatchSpider2024(scrapy.Spider):
    """Spider v2 for season 2023/2024 onwards

    as website changes the content in late 2023.
    """

    name = "arsenal_match_spider_2024"
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
        """Tell Scrapy to use `parse_match` to process url."""

        match_ids = import_symbol(
            module="".join(["epl_scrapy.match_ids.season_", self.season]),
            symbol="match_ids",
        )

        self.start_urls = ["".join([BASE_MATCH_URL, match_id]) for match_id in match_ids]

        for start_url in self.start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_match,
                cb_kwargs={"match_id": start_url.split("/")[-1]},
            )

    def parse_match(self, response, match_id):
        # Extract data from the response here
        match = MatchItem()

        match["match_id"] = match_id
        match["gameweek"] = self._parse_gameweek(response)
        match["kickoff"] = self._parse_kickoff(response)
        match["referee"] = self._parse_referee(response)
        match["home"] = self._parse_home(response)
        match["away"] = self._parse_away(response)
        match["fulltime_score"] = self._parse_fulltime_score(response)
        match["halftime_score"] = self._parse_halftime_score(response)

        yield match

    def close(self, reason):
        start_time = self.crawler.stats.get_value("start_time")
        finish_time = self.crawler.stats.get_value("finish_time")
        print("Total run time: ", finish_time - start_time)

    def _parse_gameweek(self, response):
        return response.xpath(
            "//div[@class='mc-header__gameweek-selector-current-content']/div[@class='mc-header__gameweek-selector-current-gameweek mc-header__gameweek-selector-current-gameweek--short']/text()"
        ).get()

    def _parse_fulltime_score(self, response):
        return response.xpath("string(//div[@class='mc-summary__score js-mc-score'])").get()

    def _parse_halftime_score(self, response):
        return response.xpath("string(//span[@class='js-mc-half-time-score'])").get().strip()

    def _parse_kickoff(self, response):
        dt_str = response.xpath("//span[@class='renderKOContainer']/@data-kickoff").get()

        kickoff = dt.datetime.fromtimestamp(int(dt_str) / 1000)
        return kickoff.strftime("%a %d %B %Y")

    def _parse_home(self, response):
        query = "//div[contains(@class, 'mc-summary__team home')]/a[contains(@class, 'mc-summary__team-name-link')]//span[@class='mc-summary__team-name u-show-phablet']/text()"
        return response.xpath(query).get()

    def _parse_away(self, response):
        query = "//div[contains(@class, 'mc-summary__team away')]/a[contains(@class, 'mc-summary__team-name-link')]//span[@class='mc-summary__team-name u-show-phablet']/text()"

        return response.xpath(query).get()

    def _parse_referee(self, response):
        # There are 4 elements with class=mc-summary__info
        elements = response.css('.mc-summary__info')
        # Element with referee info should be the last one
        text = elements[-1].xpath('string()').get().strip()
        _, referee = text.split("Ref: ")
        return referee
