from event import subscribe
from collections import Counter
from page_object import Goal, Match

def handle_player_with_hattrick(match):
    scorers: list[str] = [goal.scorer for goal in match.events if isinstance(goal, Goal)]
    counter = Counter(scorers)
    for player_name, goal_count in counter.most_common(1):
        if goal_count > 2:
            print(f"{player_name} scores a hattrick")


def handler_match_with_three_goals_margin(match: Match):
    print("Match with 3 or more margin")


def setup_calendar_event_handlers():
    subscribe("match_extracted", handle_player_with_hattrick)
    subscribe("match_extracted", handler_match_with_three_goals_margin)
