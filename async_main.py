from lxml import html
from page_object import Match
from pages.match.match_detail_page import MatchDetailPage
import asyncio
from helper import calculate_execution_time
from constants import match_ids
import httpx
from event import post_event
from calendar_listeners import setup_calendar_event_handlers

match_url = "https://www.premierleague.com/match/"


async def get_match(match_id):
    """Async Extract match data from EPL page."""
    async with httpx.AsyncClient() as client:
            url = f"{match_url}{match_id}"
            res = await client.get(url)
            doc = html.fromstring(res.content)

            match_page = MatchDetailPage(doc=doc, url=url)
            match: Match = match_page.extract()

            post_event("match_extracted", match)
            
            return match

async def get_matches(match_ids):
    """Extract matches data from EPL page."""
    tasks = [get_match(match_id) for match_id in match_ids]
    matches = await asyncio.gather(*tasks)
    return matches

if __name__ == "__main__":
    # Init listener to do business logic
    setup_calendar_event_handlers()

    with calculate_execution_time():
        matches = asyncio.run(get_matches(match_ids=match_ids))
