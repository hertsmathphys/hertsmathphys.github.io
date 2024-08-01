import tomllib
import datetime
import re

strip = lambda s: re.sub("<[^>]*>", "", s)
strip.__doc__ = "Remove HTML tags from string"

stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
with open("calendar.ics", "w") as c: 
    print("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//hertsmathphys.github.io//calendar//EN\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\n", file=c, end='')
    with open("data.toml", "rb") as f:
        for entry in tomllib.load(f).values():
            print("BEGIN:VEVENT\r\n", file=c, end='')
            date = entry['date'].strftime("%Y%m%d")
            print(f"DTSTART;VALUE=DATE:{date}T150000\r\n", file=c, end='')
            print(f"DTEND;VALUE=DATE:{date}T160000\r\n", file=c, end='')
            print(f"SUMMARY:{strip(entry['name'])} ({strip(entry['institution'])}), {strip(entry.get('title','TBA'))}\r\n", file=c, end='')
            print(f"DESCRIPTION:{strip(entry.get('abstract','TBA'))}\r\n", file=c, end='')
            print(f"UID:{strip(entry['name']).replace(' ', '')+date}@hertsmathphys.github.io\r\n", file=c, end='')
            print(f"DTSTAMP:{stamp}\r\n", file=c, end='')
            print("STATUS:CONFIRMED\r\nTRANSP:TRANSPARENT\r\nSEQUENCE:0\r\nEND:VEVENT\r\n", file=c, end='')
    print("END:VCALENDAR\r\n", file=c, end='')

s = ""
with open("data.toml", "rb") as f:
    for entry in sorted(tomllib.load(f).values(), key=lambda e: e['date']):
        s += f"<details><summary><time datetime='{entry['date']}'>{entry['date']}</time>: {entry['name']} ({entry['institution']}), {entry.get('title','TBA')}</summary>{entry.get('abstract','TBA')}</details>"

with open("index.html", "w") as f:
    print(open("template.html", "r").read().replace("####", s), file=f)
