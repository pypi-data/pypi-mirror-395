from pathlib import Path


class Markdown:
    """Class to write markdown for material for mkdocs."""

    def __init__(self, md: str = "", hide_toc=False) -> None:
        self.md = md
        if hide_toc:
            self.md += "\n".join(["---", "hide:", "  - toc", "---"])  # noqa: FLY002

    def __add__(self, other):
        if not other.startswith("\n") and self.md:
            other = "\n" + other
        self.md += other
        return self

    def __radd__(self, other):
        if not self.md.startswith("\n\n") and other:
            self.md = "\n\n" + self.md
        return other + str(self)

    def __str__(self) -> str:
        return self.md

    @staticmethod
    def indent(text):
        return "\t" + text.replace("\n", "\n\t")

    @staticmethod
    def header(text, level):
        return "#" * level + " " + text + "\n"

    @staticmethod
    def paragraph(text):
        return text + "\n\n"

    @staticmethod
    def code(text, language="", line_numbers=False):
        ln = ""
        if line_numbers:
            ln += ' linenums="1"'
        return "\n\n```" + language + ln + "\n" + text + "\n```\n\n"

    @staticmethod
    def link(text, url):
        return "[" + text + "](" + url + ")"

    @staticmethod
    def image(text, url):
        return "![" + text + "](" + url + ")"

    @staticmethod
    def table(data: dict[str, list], format_ints=True):
        assert len({len(row) for row in data.values()}) == 1
        text = "| "
        for header in data:
            text += header + " | "
        text += "\n| "
        for header in data:
            text += "-" * len(header) + " | "
        text += "\n"

        for row_idx in range(len(next(iter(data.values())))):
            text += "| "
            for col_idx in range(len(data.keys())):
                value = data[list(data.keys())[col_idx]][row_idx]
                if (format_ints and (isinstance(value, str) and value.isdigit())) or isinstance(
                    value, int
                ):
                    value = f"{int(value):,}"
                text += str(value) + " | "
            text += "\n"

        text += "\n\n"
        return text

    @staticmethod
    def list(items):
        text = ""
        for item in items:
            text += "- " + item + "\n"
        text += "\n\n"
        return text

    def admonition(self, style, header, body=None, expanded=False):
        if body is None:
            expanded = False
        md = "\n"
        md += "!!!" if body is None else "???"
        if expanded:
            md += "+"
        md += " "
        md += style + ' "' + header + '"\n\n'
        if body:
            md += self.indent(body) + "\n\n"
        return md

    def tabs(self, tabs: dict[str, str]):
        text = "\n"
        for header, body in tabs.items():
            text += "=== " + f'"{header}"' + " \n\n"
            text += self.indent(body) + "\n\n"
        return text

    @staticmethod
    def bold_text(text):
        return f"**{text}**"

    @staticmethod
    def italic_text(text):
        return f"*{text}*"

    def to_file(self, fname):
        with Path(fname).open("w") as f:
            f.write(self.md)
