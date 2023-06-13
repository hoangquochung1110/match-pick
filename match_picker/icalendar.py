import datetime as dt
from ics import Calendar, Event
from slugify import slugify


def create_calendar(
    match_url: str,
    name: str,
    description: str,
    begin: dt.datetime,
    end: dt.datetime
):
    c = Calendar()
    e = Event(
        name=name,
        description=description,
        begin=begin,
        end=end,
        url=match_url
    )
    c.events.add(e)

    prefix = slugify(match_url, stopwords=["https", "www"])
    file_name = f"{prefix}.ics"
    with open(file_name, "w") as f:
        f.write(c.serialize())
