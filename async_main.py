from lxml import html
from page_object import Match, Goal
import itertools
from pages.match.match_detail_page import MatchDetailPage
from decimal import Decimal
from collections import defaultdict
import aiohttp
import asyncio
from helper import calculate_execution_time
from constants import match_ids
import httpx


match_url = "https://www.premierleague.com/match/"


async def get_match(match_id):
    """Async Extract match data from EPL page."""
    async with httpx.AsyncClient() as client:
            res = await client.get(f"{match_url}{match_id}")
            doc = html.fromstring(res.content)
            match_page = MatchDetailPage(doc=doc)
            match: Match = match_page.extract()
            return match

async def get_matches(match_ids):
    """Extract matches data from EPL page."""
    tasks = [get_match(match_id) for match_id in match_ids]
    matches = await asyncio.gather(*tasks)
    return matches

if __name__ == "__main__":
    with calculate_execution_time():
        matches = asyncio.run(get_matches(match_ids=match_ids))
        import ipdb; ipdb.set_trace()
