from lxml import html
from .scorebox_component import ScoreboxComponent


class Page:
    def __init__(self, doc: html.Element) -> None:
        self.doc = doc


class MatchDetailPage(Page):
    """Represent a match detail."""

    @property
    def scorebox(self):
        return ScoreboxComponent(doc=self.doc, path="scoreboxContainer")

    def extract(self):
        return self.scorebox.extract()
