import json
import asyncio
from joplin_api import JoplinApi
from httpx import Response
import pprint
import difflib
import logging


async def new_folder(name):
    """Returns folder's id to be used as 'parent_id' for notes"""
    res = await joplin.create_folder(folder=name)
    return res.json()['id']
    
async def new_note(title, body, folder_id, tags=[]):

    assert title is str
    assert body is str
    assert folder_id is str
    assert tags is list

    kwargs = {}

    if tags:
        kwargs['tags'] = ', '.join(tags)

    await joplin.create_note(title="MY NOTE", body=body, parent_id=parent_id, **kwargs)

_joplin = None

def api():
    global _joplin
    if not _joplin:
        with open('.token') as f:
            _joplin = JoplinApi(f.readline())
    return _joplin


async def tag_id(title):
    "Fetches tags's Id given its title. "
    return (await api().search(title, item_type='tag')).json()[0]['id']


async def notes_by_tag(title):
    "Lists all note (as dics) for a given tags"
    return (await api().get_tags_notes(await tag_id(title))).json()


async def update_note(note,tags=None):
    """ Uploads note to serve.

    Required item or they will be erased: 'author', 'source_url', 'is_todo'
    if 'is_todo' in addition:  'todo_due', 'todo_completed'
    All other items are ignored.
    
    :param note: note data as dict

    :param tags: list of tag titles to replace current tags. If None current tags are kept

    """

    assert isinstance(note, dict), note

    id = note.pop('id')
    title = note.pop('title')
    body  = note.pop('body')
    pid = note.pop('parent_id')

    # fetch tags from server. There are note returned b which are not returned by `get_note`
    if tags:
        note['tags'] = ', '.join(tags)
    else:
        tags = (await api().get_notes_tags(id)).json()
        note['tags'] = ', '.join([t['title'] for t in tags])

    
        
    # see https://github.com/foxmask/joplin-api/blob/master/joplin_api/core.py
    res = await api().update_note(id,title, body, pid, **note)
    assert res.status_code == 200, res

async def edit_notes(editor,tag_title, logger):
    """ Applies function to every note with given tag and uploads changes.
    :param editor: function accepting a note data dict and returning those items that changed
    :param tag: notes with a tag of this title will be processed
    """
    notes = await notes_by_tag(tag_title)
    edits = [(await editor(n)) for n in notes]

    differ = difflib.Differ()
    for edit, note in zip(edits, notes):
        if edit:
            # log diff
            for k,v in edit.items():
                logger.info(f"Updating '{k}' for note {note['id']}.")
                diff = differ.compare(note[k].splitlines(), edit[k].splitlines())
                for d in diff: 
                    if not d.startswith(' '):
                        logger.info(d)
            
            # update server
            note.update(edit)
            await update_note(note)