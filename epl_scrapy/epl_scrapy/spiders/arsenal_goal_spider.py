from importlib import import_module

import scrapy
from epl_scrapy.items import GoalItem
from epl_scrapy.utils import import_symbol

BASE_MATCH_URL = "https://www.premierleague.com/match/"


class BaseGoalSpider(scrapy.Spider):
    name = "epl_goals"

    def start_requests(self):

        match_ids = import_symbol(
            module="".join(["epl_scrapy.match_ids.season_", self.season]),
            symbol="match_ids",
        )
        
        self.start_urls = ["".join([BASE_MATCH_URL, match_id]) for match_id in match_ids]

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
