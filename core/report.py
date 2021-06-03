"""Allows to trigger this library and review results from within Joplin notes via a simple
emoji based script language

:robot: `tag_report` :label: `Leben` 

"""

import server
import asyncio


async def tag_report(tag):
     notes = await server.notes_by_tag(tag)
     for n in notes:
        logging.info(f"[{n['title']}](:/{n['id']})")

if __name__ == "__main__":
    asyncio.run(find_scripts())