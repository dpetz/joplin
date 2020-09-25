from __future__ import absolute_import, unicode_literals
from dataclasses import dataclass
import re
import logging


@dataclass
class Rule:
    name:str
    pattern:re.Pattern
    substitution:str
    
# https://github.com/readthedocs/commonmark.py/blob/master/commonmark/blocks.py
reThematicBreak = re.compile(
    r'^(?:(?:\*[ \t]*){3,}|(?:_[ \t]*){3,}|(?:-[ \t]*){3,})[ \t]*$')

rules = [
    Rule('Ends Newline', re.compile(r'\n\Z'), ''),
    Rule('Thematic Break to * * *', reThematicBreak, '* * *'),
    Rule('Repated Thematic Break', re.compile(r'\* \* \*\n\* \* \*'), '* * *')
    ]

def normalize(body):
    nextLoop = True
    while nextLoop:
        nextLoop = False
        for r in rules:
            if r.pattern.search(body) != None:
                logging.debug(f"Rule match: {r.name}")
                body = r.pattern.sub(r.substitution,body)
                nextLoop = True
    return body

def test_normalize():
    norm = normalize("Hello\n\n****\n---\nWorld\n\n")
    assert norm == "Hello\n* * *\nWorld", norm

test_normalize()

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