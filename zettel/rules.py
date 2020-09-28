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
    r'^(?:(?:\*[ \t]*){3,}|(?:_[ \t]*){3,}|(?:-[ \t]*){3,})[ \t]*$',re.MULTILINE)

rules = [
    Rule('Trailing Line Break', re.compile(r'\n\Z'), ''),
    Rule('Repeated Empty Lines', re.compile(r'\n{3,}'), '\n\n'),
    Rule('Thematic Break * * *', reThematicBreak, '* * *'),
    Rule('Repated Thematic Break', re.compile(r'\* \* \*\n+\* \* \*'), '* * *')
    ]

def normalize(body):
    nextLoop = True
    while nextLoop:
        nextLoop = False
        for r in rules:
            if r.pattern.search(body) != None:
                logging.debug(f"Rule match: {r.name}")
                body_old = body
                body = r.pattern.sub(r.substitution,body)
                nextLoop = (body != body_old)
    return body