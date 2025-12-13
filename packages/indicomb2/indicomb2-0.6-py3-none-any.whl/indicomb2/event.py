from dataclasses import dataclass

from indicomb2.contribution import Contribution
from indicomb2.markdown import Markdown


@dataclass
class Event:
    url: str
    date: str
    title: str
    contributions: list[dict] | list[Contribution]

    @classmethod
    def from_indico(cls, url: str, date: str, title: str, contributions: list[dict]):
        contributions_list = []
        for c in reversed(contributions):
            contribution = Contribution.from_indico(
                title=c["title"],
                url=c["url"],
                speakers=c["speakers"],
                minutes=c.get("note"),
                start_time=c["startDate"]["time"] if c["startDate"] else None,
            )
            contributions_list.append(contribution)
        contributions = sorted(contributions_list)
        return cls(url, date, title, contributions)

    @classmethod
    def from_json(cls, url: str, date: str, title: str, contributions: list[Contribution]):
        contributions = [Contribution(**c) for c in contributions]
        return cls(url, date, title, contributions)

    def __lt__(self, other):
        return self.date > other.date

    def __str__(self):
        md = Markdown()
        date = md.link(self.date, self.url)
        md += md.header(f"{date} - {self.title}", level=4)
        md += "\n".join([str(c) for c in self.contributions])
        return str(md)

    def minutes(self):
        md = Markdown()
        date = md.link(self.date, self.url)
        md += md.header(f"{date} - {self.title}", level=4)
        for c in self.contributions:
            if c.minutes:
                md += md.admonition("note", str(c)[3:], str(c.minutes["html"]))
        return str(md)
