# match-pick
### Crawl Arsenal's match data from https://www.premierleague.com in season from 2020 to 2023

for example, to scrape match (score, kickoff, referee, etc.) in season 2023 and output it as csv file:

```shell
cd epl_scrapy && scrapy runspider epl_scrapy/spiders/arsenal_match_spider.py -a season=2023 -O output.csv
```

### Crawl Arsenal's goal data from https://www.premierleague.com in season from 2020 to 2023

For example, to scrape goals (scorer, minute) in season 2023 and output it as csv file:

```shell
cd epl_scrapy && scrapy runspider epl_scrapy/spiders/arsenal_goal_spider.py -a season=2023 -O arsenal_match_2023.csv
 ```