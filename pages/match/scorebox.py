from functools import partialmethod
from typing import Literal

from epl import Assist, Club, Goal, Match
from match_picker.extract import (
    GoalEvent,
    condense_spaces,
    parse_assist_event_string,
    parse_goal_event_string
)
from match_picker.page_object import Component


class Scorebox(Component):
    """Represent component with `scoreboxContainer` classs."""

    def extract(self) -> Match:
        home_team = self.get_team_home()
        away_team = self.get_team_away()
        home_events = self.get_goals_home()
        away_events = self.get_goals_away()
        return Match(
            ext_id=self.match_id,
            home=Club(*home_team),
            away=Club(*away_team),
            score=self.get_score(),
            url="",
            events=home_events+away_events,
            home_events=home_events,
            away_events=away_events,
        )

    @property
    def match_id(self):
        return self.component.getparent().attrib["data-id"]

    def get_score(self) -> str:
        score_fulltime_element = self.component.find_class("score fullTime")
        return score_fulltime_element[0].text_content()
    
    def get_half_time_score(self):
        half_time = self.component.find_class("halfTime")[0]
        return half_time.text_content().strip().split("\n")[1].strip()

    def get_team(self, side: Literal["home", "away"]) -> tuple:
        class_selector = f"team {side}"
        raw_display = self.component.find_class(class_selector)[0].text_content()
        formatted_text = condense_spaces(raw_display.strip(), separator="_")
        long, short = formatted_text.split("_")
        return (long, short)

    get_team_home = partialmethod(get_team, "home")
    get_team_away = partialmethod(get_team, "away")
    
    def get_goals(self, side: Literal["home", "away"]):
        """Retrieve goal events only (exclude red cards)."""
        match_events = []
        match_events_container = self.component.find_class(
            "matchEvents matchEventsContainer",
        )[0]
        side_event_container = match_events_container.find_class(f"{side}")[0]
        for event in side_event_container.find_class("event"):
            formatted_text = condense_spaces(event.text_content()).strip()
            try:
                events: GoalEvent = parse_goal_event_string(formatted_text)
            except ValueError as exc:
                print(exc)
            else:
                for event in events:
                    goal = Goal(match=self.match_id,minute=event.minute,scorer=event.player,label=event.label)
                    match_events.append(goal)
        return match_events

    get_goals_home = partialmethod(get_goals, "home")
    get_goals_away = partialmethod(get_goals, "away")

    def get_assists(self, side: Literal["home", "away"]):
        assist_each_side = []
        assist_container = self.component.find_class("assists")[0]
        for assist in assist_container.find_class(f"{side}"):
            formatted_text = condense_spaces(assist.text_content()).strip()
            if not formatted_text:
                return assist_each_side
            for player_and_minute in formatted_text.split("' "):
                player, minute = parse_assist_event_string(player_and_minute)
                assist_each_side.append(
                    Assist(
                        match=self.match_id,
                        minute=minute,
                        player=player,
                    )
                )
        return assist_each_side

    get_assists_home = partialmethod(get_assists, "home")
    get_assists_away = partialmethod(get_assists, "away")

