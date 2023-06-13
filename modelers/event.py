from dataclasses import dataclass


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