import scrapy
from epl_scrapy.items import GoalItem
from epl_scrapy.match_ids.season_2022 import match_ids

BASE_MATCH_URL = "https://www.premierleague.com/match/"

class Arsenal2022GoalSpider(scrapy.Spider):
    """Goals of Arsenal in season 2021/22."""

    name = "epl_goals"
    start_urls = ["".join([BASE_MATCH_URL, match_id]) for match_id in match_ids]

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_goals,
                cb_kwargs={"match_id": start_url.split("/")[-1]}
            )
    
    def parse_goals(self, response, match_id):
        base_xpath_query = "//div[@class='matchEvents matchEventsContainer']/*/div[@class='event']"
        events = response.xpath(base_xpath_query)
        for idx in range(1, len(events)+1):
            player = response.xpath(
                f"({base_xpath_query})[{idx}]/*/text()"
            ).get()
            minutes = response.xpath(
                f"({base_xpath_query})[{idx}]/a/following-sibling::text()[1]").get().strip().split(", ")
            label = response.xpath(
                f"({base_xpath_query})[{idx}]/div/div/span/text()"
            ).get()
            for minute in minutes:
                goal = GoalItem(
                    match_id=match_id,
                    player=player,
                    minute=minute,
                    label=label,
                )
                yield goal
