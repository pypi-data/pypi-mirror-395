import datetime
from dataclasses import dataclass


@dataclass
class Contribution:
    title: str
    url: str
    speakers: list[dict] | str
    minutes: str
    start_time: str = None  # HH:MM:SS

    @classmethod
    def from_indico(cls, start_time: str | None, speakers: list[dict], **kwargs):
        if start_time is None:
            start_time = "00:00:00"
        start_time = datetime.datetime.strptime(start_time, "%H:%M:%S").replace(
            tzinfo=datetime.timezone.utc
        )
        speakers = ", ".join(
            [f"{s['first_name']} {s['last_name']}" for s in speakers],
        )
        return cls(speakers=speakers, start_time=start_time, **kwargs)

    def __str__(self):
        # Define the replacements for brackets
        replacements = {
            "[": r"\[",
            "]": r"\]",
            "(": r"\(",
            ")": r"\)",
        }

        # Replace the brackets with the escaped version to be ok with markdown
        for iter_bracket, iter_escaped in replacements.items():
            self.title = self.title.replace(iter_bracket, iter_escaped)

        return f" - [{self.title}]({self.url}) - {self.speakers}"

    def __lt__(self, other):
        return self.start_time < other.start_time
