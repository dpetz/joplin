from __future__ import absolute_import, unicode_literals
from dataclasses import dataclass
import re
import logging
import markdown
import asyncio
import server


@dataclass
class Rule:
    name:str
    pattern:re.Pattern
    substitution:str
    

rules = [
    Rule('Trailing Line Break', re.compile(r'\n\Z',re.MULTILINE), ''),
    Rule('Repeated Empty Lines', re.compile(r'\n{3,}'), '\n\n'),
    Rule('Thematic Break * * *', markdown.reThematicBreak, '* * *'),
    Rule('Repated Thematic Break', re.compile(r'\* \* \*\n+\* \* \*'), '* * *')
    #Rule('Old Backlinks', re.compile(':link:'), ':robot:')
    #Rule('Old Backlinks', re.compile(r':robot:'), '* * *\n:link:')
    ]

async def normalize(note):

    body = note['body']

    nextLoop = True
    while nextLoop:
        nextLoop = False
        for r in rules:
            if r.pattern.search(body) != None:
                logging.debug(f"Rule match: {r.name}")
                body_old = body
                body = r.pattern.sub(r.substitution,body)
                nextLoop = (body != body_old)
    
    return {'body':body}


if __name__ == "__main__":
    asyncio.run(server.edit_notes(normalize, "china"))
    print('Done')