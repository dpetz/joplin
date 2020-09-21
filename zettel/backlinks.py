from zettel.util import api, notes_tagged
from asyncio import run, wait
from dataclasses import dataclass
from httpx import Response

import logging

import re


backlinks_regex = re.compile('\n\^:link:\^.*')

def write_backlinks_markdown(notelink_list):
    return f"\n^:link:^{', '.join([l.markdown() for l in notelink_list])}\n"

def remove_backlinks_markdown(markdown_string):
    match = backlinks_regex.search(markdown_string)
    if match:
        start = match.regs[0][0]
        end = match.regs[0][1]
        return some_markdown[: start] + some_markdown[end : ]
    else:
        return markdown_string 

@dataclass
class NoteLink:
    id:str
    text:str

    def markdown(self) -> str:
        return f"[{self.text}](:/{self.id})"

INTRO = "\n\n* * *\nBacklinks\n"

async def note_data(note):
    if isinstance(note, str):
         note = await api().get_note(note)
    if isinstance(note, Response):
        note = note.json()
    assert 'id' in note
    return note

async def add_backlinks(note):
    """Append backlinks to note and update at server """

    note = await note_data(note)
    logging.info(f"Adding backlinks: {note['id']}")
    linking_notes = (await api().search(note['id'])).json()
    links = [NoteLink(n['id'],n['title']) for n in linking_notes if n['id'] != note['id']]
    # remove old backlinks (if any)
    body = remove_backlinks_markdown(note['body'])
    # add backlinks and upload
    body += write_backlinks_markdown(links)
    await api().update_note(note['id'],note['title'],body, note['parent_id'])


async def main(tag):
    """ ... """

    # r = await api().get_note('9e830bc6530c416e950105834689cd63')
    # json = r.json

    notes = await notes_tagged(tag)
    add = [add_backlinks(n) for n in notes]
    await wait(add)


if __name__ == "__main__":
    run(main("test"))