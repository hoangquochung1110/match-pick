import argparse
import requests
from lxml import html
from page_object import Match, Goal
import itertools
from pages.match.match_detail_page import MatchDetailPage
from decimal import Decimal
from collections import defaultdict


# Define the command-line arguments
parser = argparse.ArgumentParser(description="Make a request to a URL")
parser.add_argument("url", type=str, help="The URL to make a request to")


def sort_by_minute(goal: Goal):
    """Sort goals by minutes. Handle stoppage time."""
    x = goal.minute
    if "+" in x:
        x, y = x.split("+")
        return Decimal(".".join([x, y]))
    else:
        return int(x)

if __name__ == "__main__":
    # Parse the arguments

    match_ids = [
        "75181",
        "75174",
        "75161",
        "74971",
        "75156",
        "75141",
        "75021",
        # "75131",
        # "75125",
        # "75111",
        # "75109",
        # "75091",
        # "75082",
        # "75071",
        # "75070",
        # "75052",
        # "75041",
        # "75037",
        # "75014",
        # "75001",
        # "74991",
        # "74982",
        # "74966",
        # "74951",
        # "74941",
        # "74931",
        "74921",
        "74911",
    ]
    arsenal_matches = []
    home_matches = []
    away_matches = []
    home_goals = []
    away_goals = []

    match_url = "https://www.premierleague.com/match/"
    for match_id in match_ids:
        # Make the request to the URL
        response = requests.get(f"{match_url}{match_id}")
        doc = html.fromstring(response.content)
        match_page = MatchDetailPage(doc=doc)
        match: Match = match_page.extract()
        if match.home.short == "ARS":
            home_matches.append(match)
            home_goals.extend(match.home_events)
        elif match.away.short == "ARS":
            away_matches.append(match)
            away_goals.extend(match.away_events)
        arsenal_matches.append(match)

    sorted_home_goals = sorted(home_goals, key=sort_by_minute)
    sorted_away_goals = sorted(away_goals, key=sort_by_minute)

    home_goals_dict = defaultdict(list[Goal])
    for minute, group in itertools.groupby(sorted_home_goals, key=lambda goal: goal.minute):
        home_goals_dict[minute]=list(group)
    import ipdb; ipdb.set_trace()
