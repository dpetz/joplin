import server
import asyncio
import re
import markdown

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
            

async def find():
    notes_wo_body = (await server.api().search('/":robot:"'))
    notes_w_body = [(await server.api().get_note(s['id']))for s in notes_wo_body.json()]
    cmds = []
    for note in notes_w_body:
        note = note.json()
        body = note['body']
        cmd = find_command(body)
        if cmd:
            cmds.append(cmd)
    return cmds


def test_find_command(): # Intro\n
    doc = """Intro\n:robot:    `script_name`      :label:`tag_title`\nAppendix"""
    print(find_command(doc))