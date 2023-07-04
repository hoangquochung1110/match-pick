from base import BaseMatchSpider
from epl_scrapy.match_ids.season_2020 import match_ids

BASE_MATCH_URL = "https://www.premierleague.com/match/"


class ARS2020MatchSpider(BaseMatchSpider):
    """Matches of Arsenal in season 2019/20."""

    name = "epl"
    start_urls = ["".join([BASE_MATCH_URL, match_id]) for match_id in match_ids]
