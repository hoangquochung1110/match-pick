from scrapy.item import Field, Item


class MatchItem(Item):
    fulltime_score = Field()
