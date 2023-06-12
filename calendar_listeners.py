from .event import subscribe

def handle_player_with_hattrick(match):
    print("Player with hattrick")

def handler_match_with_three_goals_margin():
    print("Match with 3 or more margin")

def setup_calendar_event_handlers():
    subscribe("match_extracted", handle_player_with_hattrick)
    subscribe("match_extracted", handler_match_with_three_goals_margin)
