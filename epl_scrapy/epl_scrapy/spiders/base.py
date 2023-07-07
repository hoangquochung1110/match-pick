import datetime as dt

import scrapy
from epl_scrapy.items import GoalItem, MatchItem


class BaseMatchSpider(scrapy.Spider):
    """Matches of Arsenal in season 2022/23."""

    name = "epl"
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
            "//div[@class='matchCentre']/header/div[@class='dropDown']/div/div[@class='short']/text()"
        ).get()

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


class BaseGoalSpider(scrapy.Spider):
    name = "epl_goals"

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_goals,
                cb_kwargs={"match_id": start_url.split("/")[-1]}
            )
    
    def parse_goals(self, response, match_id):
        xpath_to_events = "//div[@class='matchEvents matchEventsContainer']/*/div[@class='event']"
        
        # To count number of events
        events = response.xpath(xpath_to_events)
        for idx in range(1, len(events)+1):
            xpath_to_each_event = f"({xpath_to_events})[{idx}]"
            player = response.xpath(
                f"{xpath_to_each_event}/*/text()"
            ).get()
            minutes = response.xpath(
                f"{xpath_to_each_event}/a/following-sibling::text()[1]"
            ).get().strip().split(", ")
            # It was either goal or own goal or red card or second yellow card.
            label = response.xpath(
                f"{xpath_to_each_event}/div/div/span/text()"
            ).get()
            # Determine it was scored by home or away team.
            side = response.xpath(
                f"{xpath_to_each_event}/parent::node()/@class"
            ).get()
            for minute in minutes:
                goal = GoalItem(
                    match_id=match_id,
                    player=player,
                    minute=minute,
                    label=label,
                    side=side,
                )
                yield goal
