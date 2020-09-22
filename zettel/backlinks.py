from util import api, notes_tagged
from asyncio import run, wait
from dataclasses import dataclass
from httpx import Response

import logging

import re


backlinks_regex = re.compile('\n\^:link:\^.*') # . matches until newline

def write_backlinks_markdown(notelink_list):
    return f"\n\n^:link:^{', '.join([l.markdown() for l in notelink_list])}\n"

def remove_backlinks_markdown(markdown_string):
    match = backlinks_regex.search(markdown_string)
    if match:
        start = match.regs[0][0]
        end = match.regs[0][1]
        return markdown_string[: start] + markdown_string[end : ]
    else:
        return markdown_string

def trim_newlines(body):
    while body and body[-1] == '\n':
        body = body[:-1]
    return body

@dataclass
class NoteLink:
    id:str
    text:str

    def markdown(self) -> str:
        return f"[{self.text}](:/{self.id})"


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
    nid = note.pop('id')
    body = note.pop('body')
    logging.info(f"Adding backlinks: {nid}")

    # Temporary code to clean up deprecated backlinks
    match = re.search("\n---\nBacklinks\n", body)
    if match:
        start = match.regs[0][0]
        body = body[:start]

    # remove old backlinks (if any)
    body = remove_backlinks_markdown(body)
    body = trim_newlines(body)

    # Find in-links from all other notes. Keep those not already contained
    linking_notes = (await api().search(nid)).json()
    links = [NoteLink(n['id'],n['title']) for n in linking_notes \
        if (n['id'] != nid) and (n['id'] not in body)]
    
    if links:

        # add backlinks and upload
        body += write_backlinks_markdown(links)[:-1] # drop closing newline

        # fields not passed (again) into `update_note` are lost
        title = note.pop('title')
        pid = note.pop('parent_id')
        tags = (await api().get_notes_tags(nid)).json()
        
        # tags were not returned by `get_note` but required during update
        note['tags'] = ', '.join([t['title'] for t in tags])
        
        # upload changed body and confirm all other fields
        await api().update_note(nid, title, body, pid, **note)


async def add_backlinks_tagged(tag):
    """ ... """
    notes = await notes_tagged(tag)
    await wait([add_backlinks(n) for n in notes])


if __name__ == "__main__":
    run(add_backlinks_tagged("test")) #backlinks
