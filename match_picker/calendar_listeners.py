import datetime as dt
from collections import Counter

from match_picker.event import subscribe
from match_picker.icalendar import create_calendar
from modelers import Goal, Match


def subscribe_to(event_type):
    """Decorator to facilitate event subscription."""

    def decorator(handler):
        subscribe(event_type, handler)
        return handler

    return decorator


@subscribe_to("match_extracted")
def handle_player_with_hattrick(match):
    scorers: list[str] = [goal.scorer for goal in match.events if isinstance(goal, Goal)]
    counter = Counter(scorers)
    for player_name, goal_count in counter.most_common(1):
        if goal_count > 2:
            print(f"{player_name} scores a hattrick")


@subscribe_to("match_extracted")
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
