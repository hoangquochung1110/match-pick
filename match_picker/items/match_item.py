# To organize scraped data into structural pattern.

from scrapy.item import Field, Item


class MatchItem(Item):
    match_id = Field()
    home = Field()
    away = Field()
    fulltime_score = Field()
    halftime_score = Field()
    kickoff = Field()
    referee = Field()
