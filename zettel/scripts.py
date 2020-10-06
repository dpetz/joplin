"""Allows to trigger this library and review results from within Joplin notes via a simple
emoji based script language

:robot: `tag_report` :label: `Leben` 

"""

import server
import asyncio
import re
import markdown
from app import log, log_file

_emoji_code_pair = f"[ \t]*({markdown.emoji})[ \t]*({markdown.code})"

def find_command(doc):
    """Returns first command in doc as dict from emojis to code. None otherwise."""
    line = re.search(f"^({_emoji_code_pair})*[ \t]*$", doc, re.M)
    if line:
        line = line.group(0)
        cmd = {}
        while True:
            m = re.match(_emoji_code_pair, line)
            if m:
                if (not cmd) and (m.group(1) != ':robot:'):
                    return find_command(line[m.end(0)+1:])
                cmd[m.group(1)[1:-1]] = m.group(2)[1:-1]
                line = line[m.end(0)+1:]
            else:
                return cmd
            
async def tag_report(tag):
     notes = await server.notes_by_tag(tag)
     for n in notes:
        log.info(f"[{n['title']}](./{n['id']})")

async def find_scripts():
    notes_wo_body = (await server.api().search('/":robot:"'))
    notes_w_body = [(await server.api().get_note(s['id']))for s in notes_wo_body.json()]

    for note in notes_w_body:
        note = note.json()
        body = note['body']
        cmd = find_command(body)
        if cmd:
            if cmd['robot'] == 'tag_report':
                await tag_report(cmd['label'])
                with open(log_file) as file:  
                    note['body'] = note['body'] + '\n* * *\n' + file.read()
                    await server.update_note(note)
            else:
                log.warning(f"Unknown script: {cmd['robot']}")
    
    
    
    

def test_find_command(): # Intro\n
    doc = """Intro\n:robot:    `script_name`      :label:`tag_title`\nAppendix"""
    print(find_command(doc))


if __name__ == "__main__":
    asyncio.run(find_scripts())