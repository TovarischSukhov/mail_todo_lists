from datetime import datetime
from icalendar import Event, vDatetime, vDate, Calendar

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


def create_ical(events):
    cal = Calendar()
    for e in events:
        cal.add_component(e)
    return cal


def save_ical(events):
    cal = create_ical(events)
    f = open('example.ics', 'wb')
    f.write(cal.to_ical())
    f.close()


# test
# event = create_event(datetime(2018,7,28,5,0,0), datetime(2018,7,28,21,0,0), 'купить картошку', 'купить картошку')
# save_ical(event)
