# match-pick

## How to run project

### Crawl Arsenal's match data from https://www.premierleague.com (supported in seasons from 2020 onwards)

for example, to scrape match (score, kickoff, referee, etc.) in season 2023 and output it as csv file:

```shell
scrapy crawl arsenal_match_spider_2024 -a season=2024 -O output.csv
```
