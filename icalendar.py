from icalendar import Calendar, Event
import pytz
from datetime import datetime
cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

event = Event()
event.add('summary', 'Python meeting about calendaring')
event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=pytz.utc))
event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=pytz.utc))
event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=pytz.utc))
cal.add_component(event)
import tempfile, os
directory = tempfile.mkdtemp()
print(f"{directory=}")
f = open(os.path.join(directory, 'example.ics'), 'wb')
f.write(cal.to_ical())
f.close()
