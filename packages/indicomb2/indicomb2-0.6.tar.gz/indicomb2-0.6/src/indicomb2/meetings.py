import datetime
from dataclasses import dataclass
from pathlib import Path

from indicomb2.event import Event
from indicomb2.markdown import Markdown


@dataclass
class Meetings:
    meetings: list[Event]
    url: str
    start_date: str

    def __post_init__(self):
        self.meetings = sorted(self.meetings)

    def __add__(self, other):
        return Meetings(self.meetings + other.meetings, self.url, self.start_date)

    def meeting_list_md(self, name: str, when: str, target: Path | str):
        target = Path(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        md = Markdown()
        md += md.header(f"{name.capitalize()} Meetings", level=1)
        name = md.link(name, self.url)
        md += f"The {name} meetings take place every {when} CERN time."
        md += "\n\nYou can find a meeting overview below.\n\n"
        md += md.header("Meeting Overview", level=2)
        last_updated = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
        md += f"*last updated: {last_updated}*\n"
        md += "\n\n".join([str(m) for m in self.meetings])
        md += "\n\n"
        md += (
            f"*date cutoff: {self.start_date}, for older meetings please check "
            f"[indico]({self.url})*\n"
        )
        with target.open("w") as f:
            f.write(str(md))

    def minutes_md(self, name: str, target: Path):
        target = Path(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        md = Markdown()
        md += md.header(f"{name.capitalize()} Meetings Minutes", level=1)
        last_updated = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
        md += f"*last updated: {last_updated}*\n"
        md += "\n\n".join([m.minutes() for m in self.meetings])
        md += "\n\n"
        md += (
            f"*date cutoff: {self.start_date}, for older meetings please check "
            f"[indico]({self.url})*\n"
        )
        md += md.link("indico", self.url)
        with target.open("w") as f:
            f.write(str(md))

    def add_topic(
        self, target: Path, include: list[str] | None = None, exclude: list[str] | None = None
    ):
        if include is None:
            include = []
        if exclude is None:
            exclude = []
        data = {"Date": [], "Title": [], "Speakers": []}
        for e in self.meetings:
            for c in e.contributions:
                if any(x.lower() in c.title.lower() for x in include) and not any(
                    x.lower() in c.title.lower() for x in exclude
                ):
                    data["Date"].append(f"[{e.date}]({c.url})")
                    data["Title"].append(c.title)
                    data["Speakers"].append(c.speakers)

        md = Markdown()
        md += "\n"
        md += md.header("Meeting Contributions", level=2)
        md += md.table(data)
        md += "\n\n"
        md += f"*search terms: {include}*\n"
        md += (
            f"*date cutoff: {self.start_date}, for older meetings please check "
            f"[indico]({self.url})*\n"
        )
        target = Path(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a") as f:
            f.write(str(md))
