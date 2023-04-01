import requests
from lxml import html
from page_object import Match
from pages.match.match_detail_page import MatchDetailPage

from constants import match_ids
from helper import calculate_execution_time

# Define the command-line arguments



    
def get_matches(match_ids):
    matches = []
    for match_id in match_ids:
        # Make the request to the URL
        response = requests.get(f"{match_url}{match_id}")
        doc = html.fromstring(response.content)
        match_page = MatchDetailPage(doc=doc)
        match: Match = match_page.extract()
        matches.append(match)
    return matches


if __name__ == "__main__":

    match_url = "https://www.premierleague.com/match/"
    with calculate_execution_time():
        get_matches(match_ids=match_ids)
