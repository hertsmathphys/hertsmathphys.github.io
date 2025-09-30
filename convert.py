import tomllib
import datetime
import re


def make_current_entry(date, location, name, institution, title, abstract):
    time = f"<time datetime='{date}'>{date.strftime("%-d %B, %H:%M")}</time>"
    summary = f"{time}, {location}: {name} ({institution}), {title}"
    return (f"<details><summary>{summary}</summary>{abstract}</details>")


def make_past_entry(date, name, institution, title, abstract):
    time = f"<time datetime='{date}'>{date.strftime("%-d %B %Y, %H:%M")}</time>"
    summary = f"{time}: {name} ({institution}), {title}"
    return (f"<details><summary>{summary}</summary>{abstract}</details>")


def strip_html(html_string):
    """ Remove HTML tags from string """
    return re.sub("<[^>]*>", "", html_string)


hour = datetime.timedelta(hours=1)

stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
with open("calendar.ics", "w") as calendar_file:
    calendar_file.writelines([
            "BEGIN:VCALENDAR\n",
            "VERSION:2.0\n",
            "PRODID:-//hertsmathphys.github.io//calendar//EN\n",
            "CALSCALE:GREGORIAN\n",
            "METHOD:PUBLISHn\n",
        ])
    with open("data.toml", "rb") as f:
        for entry in tomllib.load(f).values():
            date = entry['date'].strftime("%Y%m%d")
            time_begin = entry['date'].strftime("%H%M%S")
            time_end = (entry['date'] + hour).strftime("%H%M%S")

            calendar_file.writelines([
                "BEGIN:VEVENT\n",
                f"DTSTART;VALUE=DATE:{date}T{time_begin}\n",
                f"DTEND;VALUE=DATE:{date}T{time_end}\n",
                f"SUMMARY:{strip_html(entry['name'])} ({strip_html(entry['institution'])}), {strip_html(entry.get('title','TBA'))}\n",
                f"DESCRIPTION:{strip_html(entry.get('abstract', 'TBA'))}\n",
                f"UID:{strip_html(entry['name']).replace(' ', '')+date}@hertsmathphys.github.io\n",
                f"DTSTAMP:{stamp}\n"
                "STATUS:CONFIRMED\n",
                "TRANSP:TRANSPARENT\n",
                "SEQUENCE:0\n",
                "END:VEVENT\n",
            ])

        calendar_file.write("END:VCALENDAR\n")


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
    with open("template.html", "r") as template_file:
        template = template_file.read()
        index = template.replace("$current_year", current_year_entries).replace("$past_years", past_year_entries) + "\n"
        f.write(index)
