from dataclasses import dataclass
import datetime as dt
from decimal import Decimal
from lxml import html


@dataclass
class Club:
    long: str
    short: str = ""

@dataclass
class Match:
    url: str
    ext_id: str|int
    kickoff: dt
    home: Club
    away: Club
    score: str
    half_time_score: str
    events: list["Event"] = None
    home_events: list["Event"] = None
    away_events: list["Event"] = None
    referee: str = ""

    def __repr__(self) -> str:
        return f"""
            Match: {self.ext_id} {self.home.short} {self.score} {self.away.short}
        """

@dataclass
class Event:
    match: int
    minute: int
    

@dataclass
class Goal(Event):
    scorer: str
    label: str
    assist: str = ""


@dataclass
class Assist(Event):
    player: str


@dataclass
class MatchStats:
    possession: Decimal
    shots_on_target: int
    shots: int
    touches: int
    passes: int
    tackles: int
    clearances: int
    corners: int
    offsides: int
    yellow_cards: int
    fouls_conceded: int


class Component:
    def __init__(self, doc, path) -> None:
        self.doc = doc
        self.component: html.HtmlElement = doc.find_class(path)[0]
