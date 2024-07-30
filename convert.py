import tomllib

with open("calendar.ics", "w") as c: 
    print("BEGIN:VCALENDAR\nVERSION:2.0", file=c)
    with open("data.toml", "rb") as f:
        for entry in tomllib.load(f).values():
            print("BEGIN:VEVENT", file=c)
            date = entry['date'].strftime("%Y%m%d")
            print(f"DTSTART;VALUE=DATE:{date}T150000", file=c)
            print(f"DTEND;VALUE=DATE:{date}T160000", file=c)
            print(f"SUMMARY:{entry['name']} ({entry['institution']}), {entry.get('title','TBA')}", file=c)
            print(f"DESCRIPTION:{entry.get('abstract','TBA')}", file=c)
            print("END:VEVENT", file=c)
    print("END:VCALENDAR", file=c)

s = ""
with open("data.toml", "rb") as f:
    for entry in sorted(tomllib.load(f).values(), key=lambda e: e['date']):
        s += f"<details><summary>{entry['date']}: {entry['name']} ({entry['institution']}), {entry.get('title','TBA')}</summary>{entry.get('abstract','TBA')}</details>"

with open("index.html", "w") as f:
    print(open("template.html", "r").read().replace("####", s), file=f)
