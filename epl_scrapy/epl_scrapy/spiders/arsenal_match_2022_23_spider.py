import scrapy
from base import BaseMatchSpider
from epl_scrapy.match_ids.season_2023 import match_ids

BASE_MATCH_URL = "https://www.premierleague.com/match/"


class ARS2023MatchSpider(BaseMatchSpider):
    """Matches of Arsenal in season 2022/23."""

    name = "epl"
    start_urls = ["".join([BASE_MATCH_URL, match_id]) for match_id in match_ids]

    def start_requests(self):
        """Tell Scrapy to use `parse_match` to process url."""
        for start_url in self.start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_match,
                cb_kwargs={"match_id": start_url.split("/")[-1]},
            )
