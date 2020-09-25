from util import api, notes_tagged, note_data
import markdown as md
import asyncio
from httpx import Response
import logging
import re
import difflib

# INPUT PARAMETERS
TAG = 'test' # 'backlinks'

# OTHER GLOBAL VARS
_pattern = re.compile('\n\^:link:\^.*') # . matches until newline
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


async def add_backlinks_note(note, update_server=True):
    """Finds and appends backlinks to note and update at server. Returns Edit """

    note = await note_data(note)
    nid = note.pop('id')
    body = note.pop('body')
    edit = md.Edit(body)
    logging.info(f"Adding backlinks: {nid}")

    # Find in-links from all other notes. Keep those not already contained
    linking_notes = (await api().search(nid)).json()
    links = [md.NoteLink(n['id'],n['title']) for n in linking_notes \
        if (n['id'] != nid) and (n['id'] not in body)]
    
    if not links:
        return None

    # remove old backlinks (if any)
    match = _pattern.search(body)
    if match:
        body =  markdown_string[: match.start()] + markdown_string[match.end() : ]
    
    # Temporary code to clean up deprecated backlinks
    match = re.search("\n---\nBacklinks\n", body)
    if match:
        start = match.regs[0][0]
        body = body[:start]

    # append backlinks
    body += f"\n* * *\n:link:{', '.join([l.markdown() for l in links])}"

    body = md.normalize(body)

    # upload changed body and confirm all other fields
    if update_server:

        # make sure to pass all fields again or they are erased by server
        # requires to fetch tags from server which are not returned by `get_note`
        title = note.pop('title')
        pid = note.pop('parent_id')
        tags = (await api().get_notes_tags(nid)).json()
        note['tags'] = ', '.join([t['title'] for t in tags])

        await api().update_note(nid, title, body, pid, **note)

    edit.revision = body

    return edit


async def add_backlinks_tag():
    """ Adds backlinks to all notes tagged TAG and updates server """
    notes = await notes_tagged(TAG)
    edits = [await add_backlinks_note(note=n, update_server=True) for n in notes]
    edits = list(filter(None, edits))
    print(f"Edits: {len(edits)}")


if __name__ == "__main__":
    asyncio.run(add_backlinks_tag())
