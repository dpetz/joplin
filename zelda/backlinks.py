import markdown as md
import asyncio
from httpx import Response
import logging
import re
import server
import insights
import rules


# OTHER GLOBAL VARS
_pattern = re.compile('\n:link:.*') # . matches until newline


async def add_backlinks(note):
    """Finds and appends backlinks to note and update at server. Returns Edit """

    logging.info(f"Collecting Backlinks: {note['id']}")

    body = note['body']

    # Find in-links from all other notes. Keep those not already contained
    linking_notes = (await server.api().search(note['id'])).json()
    links = [md.NoteLink(n['id'],n['title']) for n in linking_notes \
        if (n['id'] != note['id']) and (n['id'] not in body)]
    
    if links:    
        # remove old backlinks (if any)
        body = insights.drop(':link:',body)

        # append backlinks
        body = insights.add(':link:', ', '.join([l.markdown() for l in links]), body)

        return {'body' : body}



if __name__ == "__main__":
    asyncio.run(server.edit_notes(add_backlinks, "nobacklinks"))
