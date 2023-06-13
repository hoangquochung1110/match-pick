from dataclasses import dataclass


@dataclass
class Club:
    long: str
    short: str = ""
