import requests
from lxml import html

from match_picker.constants import match_ids
from match_picker.helper import calculate_execution_time
from modelers import Match
from pages.match.match_detail_page import MatchDetailPage


def get_matches(match_ids):
    matches = []
    for match_id in match_ids:
        url = f"{match_url}{match_id}"
        # Make the request to the URL
        response = requests.get(url)
        doc = html.fromstring(response.content)
        match_page = MatchDetailPage(doc=doc, url=url)
        match: Match = match_page.extract()
        matches.append(match)
    return matches


if __name__ == "__main__":

    match_url = "https://www.premierleague.com/match/"
    with calculate_execution_time():
        get_matches(match_ids=match_ids)
