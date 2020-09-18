import asyncio
from util import api, links_from_markdown, notes_tagged

TOC = '06b0454c00074d4da0141e4c865db701'


async def toc_dict(toc_note_id = TOC):
    """GETs note and returns links as a dict from urls to texts. """
    body = (await api().get_note(toc_note_id)).json()['body']
    return { link.url : link.text for link in links_from_markdown(body)}
    

async def replace_evernote_links(notes):
    url_to_text = await toc_dict()
    print(f"{len(url_to_text)} Table of Content entries read.")
    for note in notes:
        body = note['body']
        en_urls =  [l.url for l in links_from_markdown(body) \
            if l.url.startswith('evernote:')]
        for en_url in en_urls:
            if en_url in url_to_text:
                text = url_to_text[en_url]
                print(f"... found Evernote link: {text}")
                note_ids = await search_titles(text)
                if len(note_ids) == 1:
                    body = body.replace(en_url, f":/{note_ids[0]}")
                    await api().update_note(note['id'],note['title'],body, note['parent_id'])
                    print(f"... replaced  with :/{note_ids[0]}")
                else:
                    print(f"... cannot replace with: {note_ids}")
            else:
                print(f"... Link not in ToC: {en_url}")

async def search_titles(query):
    """Lists note ids with titles that equal query"""
    res = await api().search(query,'note')
    return [ r['id'] for r in res.json() if r['title'] == query ]


async def main(tag_name = 'links'):
    """ Replaces Evernotes links w/ Joplin links for all notes tagged TAG based on the TOC note
    containing a Table of Content of all Evernote notes as generated and exported from Evernote. """
    notes = await notes_tagged(tag_name)
    await replace_evernote_links(notes)

if __name__ == "__main__":
    asyncio.run(main())