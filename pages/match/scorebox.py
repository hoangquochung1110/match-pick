from typing import Literal
from functools import partialmethod
from lxml import html
from extract import GoalEvent, condense_spaces, parse_goal_event_string
from page_object import Club, Match, Goal

class Component:
    def __init__(self, doc, path) -> None:
        self.doc = doc
        self.component: html.HtmlElement = doc.find_class(path)[0]

class Scorebox(Component):
    """Represent component with `scoreboxContainer` classs."""

    def extract(self) -> Match:
        home_team = self.get_team_home()
        away_team = self.get_team_away()
        home_events = self.get_events_home()
        away_events = self.get_events_away()
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

    def get_team(self, side: Literal["home", "away"]) -> tuple:
        class_selector = f"team {side}"
        raw_display = self.component.find_class(class_selector)[0].text_content()
        formatted_text = condense_spaces(raw_display.strip(), separator="_")
        long, short = formatted_text.split("_")
        return (long, short)

    get_team_home = partialmethod(get_team, "home")
    get_team_away = partialmethod(get_team, "away")
    
    def get_events(self, side: Literal["home", "away"]):
        """Locate the icon (.i.e: ball, yellow card) to determine
        
        kind of events.
        """
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

    get_events_home = partialmethod(get_events, "home")
    get_events_away = partialmethod(get_events, "away")
