from datetime import datetime
from icalendar import Event, vDatetime, vDate, cal
import tempfile, os

def create_event(*args):
    event = Event()

    if len(args) > 3:
        start = args[0]
        end = args[1]
        event.add('summary', args[2])
        event.add('description', args[3])
        event.add('dtstart', vDatetime(start))
        event.add('dtend', vDatetime(end))
    else:
        date = args[0]
        event.add('summary', args[1])
        event.add('description', args[2])
        event.add('dtstart', vDate(datetime(*date)))
        event.add('dtend', vDate(datetime(*date)))
    return event

def save_ical(event):
    directory = tempfile.mkdtemp()
    f = open(os.path.join(directory, 'example.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()


event = create_event(datetime(2018,7,28,5,0,0), datetime(2018,7,28,21,0,0), 'купить картошку', 'купить картошку')
save_ical(event)
