from .club import Club
from .event import Event
from dataclasses import dataclass
from decimal import Decimal
import datetime as dt


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
