import tomllib
import datetime
import zoneinfo
import re


def make_current_entry(date, location, name, institution, title, abstract):
    time = f"<time datetime='{date}'>{date.strftime("%-d %B, %H:%M")}</time>"
    summary = f"{time}, {location}: {name} ({institution}), {title}"
    return (f"<details><summary>{summary}</summary>{abstract}</details>")


def make_past_entry(date, name, institution, title, abstract):
    time = f"<time datetime='{date}'>{date.strftime("%-d %B %Y, %H:%M")}</time>"
    summary = f"{time}: {name} ({institution}), {title}"
    return (f"<details><summary>{summary}</summary>{abstract}</details>")


strip = lambda s: re.sub("<[^>]*>", "", s)

strip.__doc__ = "Remove HTML tags from string"

localise = lambda d: datetime.datetime.combine(d.date(), d.time(), zoneinfo.ZoneInfo('Europe/London'))
localise.__doc__ = "Add Europe/London time zone to datetime objects"
hour = datetime.timedelta(hours=1)

stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
with open("calendar.ics", "w") as c: 
    print("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//hertsmathphys.github.io//calendar//EN\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\n", file=c, end='')
    with open("data.toml", "rb") as f:
        for entry in tomllib.load(f).values():
            print("BEGIN:VEVENT\r\n", file=c, end='')
            date = entry['date'].strftime("%Y%m%d")
            time_begin = entry['date'].strftime("%H%M%S")
            time_end = (entry['date'] + hour).strftime("%H%M%S")
            print(f"DTSTART;VALUE=DATE:{date}T{time_begin}\r\n", file=c, end='')
            print(f"DTEND;VALUE=DATE:{date}T{time_end}\r\n", file=c, end='')
            print(f"SUMMARY:{strip(entry['name'])} ({strip(entry['institution'])}), {strip(entry.get('title','TBA'))}\r\n", file=c, end='')
            print(f"DESCRIPTION:{strip(entry.get('abstract','TBA'))}\r\n", file=c, end='')
            print(f"UID:{strip(entry['name']).replace(' ', '')+date}@hertsmathphys.github.io\r\n", file=c, end='')
            print(f"DTSTAMP:{stamp}\r\n", file=c, end='')
            print("STATUS:CONFIRMED\r\nTRANSP:TRANSPARENT\r\nSEQUENCE:0\r\nEND:VEVENT\r\n", file=c, end='')
    print("END:VCALENDAR\r\n", file=c, end='')


current_academic_year_start = datetime.datetime((n:=datetime.datetime.now()).year - (n.month < 7), month=7, day=1)

current_year_entries = ""
with open("data.toml", "rb") as f:
    for entry in filter( lambda e: e['date'] >= current_academic_year_start, sorted(tomllib.load(f).values(), key=lambda e: e['date'], reverse=False)):
        current_year_entries += make_current_entry(
            entry['date'],
            entry['location'],
            entry['name'],
            entry['institution'],
            entry.get('title', 'TBA'),
            entry.get('abstract', 'TBA')
        )

past_year_entries = ""
with open("data.toml", "rb") as f:
    for entry in filter(lambda e: e['date'] < current_academic_year_start, sorted(tomllib.load(f).values(), key=lambda e: e['date'], reverse=True)):
        past_year_entries += make_past_entry(
            entry['date'],
            entry['name'],
            entry['institution'],
            entry.get('title', 'TBA'),
            entry.get('abstract', 'TBA')
        )

with open("index.html", "w") as f:
    print(open("template.html", "r").read().replace("$current_year", current_year_entries).replace("$past_years", past_year_entries), file=f)
