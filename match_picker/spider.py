import scrapy


class MatchSpider(scrapy.Spider):
    name = "epl"
    start_urls = [
        'https://www.premierleague.com/match/74941',
    ]

    def parse(self, response):
        # Extract data from the response here
        full_time_score = response.css(".score.fullTime")

        yield {
            "full_time": full_time_score.xpath("string()").get().strip()
        }
