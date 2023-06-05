from datetime import datetime
from ics import Calendar, Event

c = Calendar()
e = Event()
e.summary = "My cool event"
e.description = "A meaningful description"
e.begin = datetime.fromisoformat("2022-06-06T12:05:23+02:00")
e.end = datetime.fromisoformat("2022-06-06T13:05:23+02:00")
c.events.add(e)
c
# Calendar(extra=Container('VCALENDAR', []), extra_params={}, version='2.0', prodid='ics.py 0.8.0-dev0 - http://git.io/lLljaA', scale=None, method=None, events=[Event(extra=Container('VEVENT', []), extra_params={}, timespan=EventTimespan(begin_time=datetime.datetime(2022, 6, 6, 12, 5, 23, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200))), end_time=None, duration=None, precision='second'), summary=None, uid='ed7975c7-01f1-42eb-bfc4-435afd76b33d@ed79.org', description=None, location=None, url=None, status=None, created=None, last_modified=None, dtstamp=datetime.datetime(2022, 6, 6, 19, 28, 14, 575558, tzinfo=Timezone.from_tzid('UTC')), alarms=[], attach=[], classification=None, transparent=None, organizer=None, geo=None, attendees=[], categories=[])], todos=[])
with open("my.ics", "w") as f:
    f.write(c.serialize())
