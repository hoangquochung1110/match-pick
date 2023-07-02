import datetime as dt

import scrapy
from items.match_item import MatchItem


class MatchSpider(scrapy.Spider):
    name = "epl"
    start_urls = [
        'https://www.premierleague.com/match/74941',
    ]

    def start_requests(self):
        """Tell Scrapy to use `parse_match` to process url."""
        for start_url in self.start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_match,
            )

    def parse_match(self, response):
        # Extract data from the response here
        full_time_score = response.css(".score.fullTime")
        halftime_score = response.xpath("//div[@class='halfTime']/node()")[2]
        match = MatchItem()
        match["fulltime_score"] = full_time_score.xpath("string()").get().strip()
        match["halftime_score"] = halftime_score.get().strip()
        match["kickoff"] = self._parse_kickoff(response)
        yield match

    def _parse_kickoff(self, response):
        dt_str = response.xpath("//div[@class='matchDate renderMatchDateContainer']/@data-kickoff").get()
        kickoff = dt.datetime.fromtimestamp(int(dt_str)/1000)
        return kickoff.strftime("%a %d %B %Y")
