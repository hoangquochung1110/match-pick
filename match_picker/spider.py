import datetime as dt

import scrapy
from items.match_item import MatchItem


class MatchSpider(scrapy.Spider):
    name = "epl"
    start_urls = [
        'https://www.premierleague.com/match/74941',
        "https://www.premierleague.com/match/75001",
    ]
    custom_settings = {
        # specifies exported fields and order in csv
        'FEED_EXPORT_FIELDS': ["match_id", "home", "away", "fulltime_score", "halftime_score", "kickoff", "referee"],
    }

    def start_requests(self):
        """Tell Scrapy to use `parse_match` to process url."""
        for start_url in self.start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_match,
                cb_kwargs={"match_id": start_url.split("/")[-1]}
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

    def _parse_fulltime_score(self, response):
        full_time_score = response.css(".score.fullTime")
        return full_time_score.xpath("string()").get().strip()
    
    def _parse_halftime_score(self, response):
        halftime_score = response.xpath("//div[@class='halfTime']/node()")[2]
        return halftime_score.get().strip()

    def _parse_kickoff(self, response):
        dt_str = response.xpath("//div[@class='matchDate renderMatchDateContainer']/@data-kickoff").get()
        kickoff = dt.datetime.fromtimestamp(int(dt_str)/1000)
        return kickoff.strftime("%a %d %B %Y")
    
    def _parse_home(self, response):
        return response.xpath("//div[@class='team home']/a[@class='teamName']/span[@class='short']").xpath("string()").get()
    
    def _parse_away(self, response):
        return response.xpath("//div[@class='team away']/a[@class='teamName']/span[@class='short']").xpath("string()").get()

    def _parse_referee(self, response):
        return response.xpath("//div[@class='referee']").xpath("string()").get().strip()
