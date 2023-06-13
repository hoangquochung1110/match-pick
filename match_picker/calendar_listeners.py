from match_picker.event import subscribe
from collections import Counter
from epl import Goal, Match
from match_picker.icalendar import create_calendar
import datetime as dt


def handle_player_with_hattrick(match):
    scorers: list[str] = [goal.scorer for goal in match.events if isinstance(goal, Goal)]
    counter = Counter(scorers)
    for player_name, goal_count in counter.most_common(1):
        if goal_count > 2:
            print(f"{player_name} scores a hattrick")


def handler_match_with_three_goals_margin(match: Match):
    left, right = match.score.split("-")
    if match.home.short.upper() == "ARS" and int(left) - int(right) > 2:
        print("Match with 3 or more margin")
        create_calendar(
            match_url=match.url,
            name=str(match),
            description=match.url,
            begin=match.kickoff + dt.timedelta(weeks=52),
            end=match.kickoff + dt.timedelta(weeks=52),
        )


def setup_calendar_event_handlers():
    """Register actions after match extraction."""
    subscribe("match_extracted", handle_player_with_hattrick)
    subscribe("match_extracted", handler_match_with_three_goals_margin)
