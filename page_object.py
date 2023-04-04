from dataclasses import dataclass
import datetime as dt
from decimal import Decimal


@dataclass
class Club:
    long: str
    short: str = ""

@dataclass
class Match:
    ext_id: str|int
    kickoff: dt = ""
    home: Club = None
    away: Club = None
    score: str = ""
    url: str = ""
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
