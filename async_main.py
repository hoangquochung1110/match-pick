import asyncio

import httpx
from lxml import html

from match_picker.calendar_listeners import setup_calendar_event_handlers
from match_picker.constants import match_ids
from match_picker.helper import calculate_execution_time
from modelers import Match
from pages.match.match_detail_page import MatchDetailPage

match_url = "https://www.premierleague.com/match/"


async def get_match(match_id) -> Match:
    """Async Extract match data from EPL page."""
    async with httpx.AsyncClient() as client:
        url = f"{match_url}{match_id}"
        res = await client.get(url)
        doc = html.fromstring(res.content)

        match_page = MatchDetailPage(doc=doc, url=url)
        return match_page.extract()


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
