""" Utility functions for working with markdown documents,
such as regular expressions for emojis and reading links into a data class.
"""

from dataclasses import dataclass
import commonmark
import re

# https://github.com/readthedocs/commonmark.py/blob/master/commonmark/blocks.py
reThematicBreak = re.compile(
    r'^(?:(?:\*[ \t]*){3,}|(?:_[ \t]*){3,}|(?:-[ \t]*){3,})[ \t]*$',re.MULTILINE)

thematicBreak = "* * *"

emoji = ":[a-z_]{3,}:"

code = "`.*?`"


def html(md):
    """ Render markdown into html. """
    parser = commonmark.Parser()
    return commonmark.HtmlRenderer().render(parser.parse(md))

@dataclass
class NoteLink:
    """Parses internal note links """
    id:str
    text:str

    # TODO: Support hints (see https://joplinapp.org/markdown/)

    def markdown(self) -> str:
        return f"[{self.text}](:/{self.id})"