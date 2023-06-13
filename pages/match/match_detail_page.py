from lxml import html

from match_picker.event import post_event
from modelers import Club, Match

from .matchbar import Matchbar
from .scorebox import Scorebox


class Page:
    def __init__(self, doc: html.Element, url: str) -> None:
        self.doc = doc
        self.url = url


class MatchDetailPage(Page):
    """Represent a match detail."""

    @property
    def scorebox(self):
        return Scorebox(doc=self.doc, path="scoreboxContainer")

    @property
    def matchbar(self):
        return Matchbar(doc=self.doc, path="matchBar")
    
    def _extract(self):
        home_team = self.scorebox.get_team_home()
        away_team = self.scorebox.get_team_away()
        home_goals = self.scorebox.get_goals_home()
        home_assists = self.scorebox.get_assists_home()
        away_goals = self.scorebox.get_goals_away()
        away_assists = self.scorebox.get_assists_away()

        home_events = home_goals + home_assists
        away_events = away_goals + away_assists

        match = Match(
            ext_id=self.scorebox.match_id,
            url=self.url,
            kickoff=self.matchbar.get_kickoff(),
            home=Club(*home_team),
            away=Club(*away_team),
            score=self.scorebox.get_score(),
            half_time_score=self.scorebox.get_half_time_score(),
            events=home_events+away_events,
            home_events=home_events,
            away_events=away_events,
            referee=self.matchbar.get_referee(),
        )

        post_event("match_extracted", match)

        return match        

    def extract(self):
        return self._extract()
