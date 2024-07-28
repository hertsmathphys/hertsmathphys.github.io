import tomllib
print("""BEGIN:VCALENDAR
VERSION:2.0""")

with open("data.toml", "rb") as f:
    for entry in tomllib.load(f).values():
        print("BEGIN:VEVENT")
        date = entry['date'].strftime("%Y%m%d")
        print(f"DTSTART;VALUE=DATE:{date}T150000")
        print(f"DTEND;VALUE=DATE:{date}T160000")
        print(f"SUMMARY:{entry['name']} ({entry['institution']}), {entry.get('title','TBA')}")
        print(f"DESCRIPTION:{entry.get('abstract','TBA')}")
        print("END:VEVENT")
print("END:VCALENDAR")
