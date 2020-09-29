from dataclasses import dataclass
import commonmark
import re

# https://github.com/readthedocs/commonmark.py/blob/master/commonmark/blocks.py
reThematicBreak = re.compile(
    r'^(?:(?:\*[ \t]*){3,}|(?:_[ \t]*){3,}|(?:-[ \t]*){3,})[ \t]*$',re.MULTILINE)

thematicBreak = "* * *"

def html(md):
    parser = commonmark.Parser()
    return commonmark.HtmlRenderer().render(parser.parse(md))

@dataclass
class NoteLink:
    id:str
    text:str

    def markdown(self) -> str:
        return f"[{self.text}](:/{self.id})"

@dataclass
class Edit:
    original:str
    revision:str = None

def lines_changed(edit):
    pass

def diff(edit):
    pass