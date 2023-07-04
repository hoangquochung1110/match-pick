import datetime as dt

import scrapy
from epl_scrapy.items import MatchItem
from epl_scrapy.match_ids.season_2023 import match_ids

BASE_MATCH_URL = "https://www.premierleague.com/match/"


class MatchSpider(scrapy.Spider):
    name = "epl"
    start_urls = ["".join([BASE_MATCH_URL, match_id]) for match_id in match_ids]
    custom_settings = {
        # specifies exported fields and order in csv
        "FEED_EXPORT_FIELDS": [
            "match_id",
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

    def _parse_fulltime_score(self, response):
        return response.xpath("string(//div[@class='score fullTime'])").get()

    def _parse_halftime_score(self, response):
        return response.xpath("string(//div[@class='halfTime']/node()[3])").get().strip()

    def _parse_kickoff(self, response):
        dt_str = response.xpath(
            "//div[@class='matchDate renderMatchDateContainer']/@data-kickoff"
        ).get()
        kickoff = dt.datetime.fromtimestamp(int(dt_str) / 1000)
        return kickoff.strftime("%a %d %B %Y")

    def _parse_home(self, response):
        return response.xpath(
            "//div[@class='team home']/a[@class='teamName']/span[@class='short']/text()"
        ).get()

    def _parse_away(self, response):
        return response.xpath(
            "//div[@class='team away']/a[@class='teamName']/span[@class='short']/text()"
        ).get()

    def _parse_referee(self, response):
        return response.xpath("string(//div[@class='referee'])").get().strip()
