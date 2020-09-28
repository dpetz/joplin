from util import api, notes_tagged, note_data
import markdown as md
import asyncio
from httpx import Response
import logging
import re
import difflib
import server

# INPUT PARAMETERS
TAG = 'test' # 'backlinks'

# OTHER GLOBAL VARS
_pattern = re.compile('\n\^:link:\^.*') # . matches until newline
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


async def add_backlinks(note):
    """Finds and appends backlinks to note and update at server. Returns Edit """

    logging.info(f"Adding backlinks: {note['id']}")

    # Find in-links from all other notes. Keep those not already contained
    linking_notes = (await api().search(note['id'])).json()
    links = [md.NoteLink(n['id'],n['title']) for n in linking_notes \
        if (n['id'] != note['id']) and (n['id'] not in body)]
    
    if not links:
        return None

    body = note['body']

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
    insights.add(':links:', '.'.join([l.markdown() for l in links]), body)

    body = md.normalize(body)

    return {'body' : body}




        
async def edit_notes(editor,filter):
    """ Applies function to every note and uploads changes.
    :param editor: function accepting a note data dict and returning those items that changed
    :param tag: notes with a tag of this title will be processed
    """
    notes = await fetch_notes(filter)
    edits = [await editor(n) for n in notes]

    differ = difflib.Differ()
    for edit, note in zip(notes, edits):

        # log diff
        for k,v in edit.items():
            logging.info(f"Updating '{k}' for note {note['id']}.")
            logging.info(differ.compare(note[k], edit[k])
        
        # update server
        # server.update_note(note.update(edit))


if __name__ == "__main__":
    tag = Filter(tag=["test"])
    asyncio.run(edit_notes(add_backlinks, tag)
