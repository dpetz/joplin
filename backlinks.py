from util import api, notes_tagged
from asyncio import run, wait
from dataclasses import dataclass
from httpx import Response

import logging

logging.set

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
    """Append backlinksd to note and update at server """

    note = await note_data(note)
    logging.info(f"Adding backlinks: {note['id']}")
    linking_notes = (await api().search(note['id'])).json()
    links = [NoteLink(n['id'],n['title']) for n in linking_notes if n['id'] != note['id']]

    body = note['body']

    insertion = "\n".join([l.markdown() for l in links if l.id not in body])

    if len(insertion) > 2:
        if INTRO in body:
            body += '\n'
        else:
            body += INTRO
        
        body += insertion
        
        await api().update_note(note['id'],note['title'],body, note['parent_id'])


async def main(tag = "test"):
    """ ... """

    # r = await api().get_note('9e830bc6530c416e950105834689cd63')
    # json = r.json

    notes = await notes_tagged(tag)
    add = [add_backlinks(n) for n in notes]
    await wait(add)



if __name__ == "__main__":
    run(main())