import scrapy
from base import BaseGoalSpider
from epl_scrapy.match_ids.season_2022 import match_ids

BASE_MATCH_URL = "https://www.premierleague.com/match/"

class Arsenal2022GoalSpider(BaseGoalSpider):
    """Goals of Arsenal in season 2021/22."""

    start_urls = ["".join([BASE_MATCH_URL, match_id]) for match_id in match_ids]
