import json
import asyncio
from joplin_api import JoplinApi
from httpx import Response
from util import Filter

import pprint


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


async def tag_titled(tag_title):
    tags = await api().get_tags()
    for t in tags.json():
         if t['title'] == tag_title:
             return t['id']
    raise Exception(f"No such tag: {tag_title}")


async def note_data(note):
    if isinstance(note, str):
         note = await api().get_note(note)
    if isinstance(note, Response):
        note = note.json()
    assert 'id' in note
    return note

async def fetch_notes(filter_values filter_type):
    """ Convenience method to get notes by tag, notebook or query. Returns list
    of note data dicts.
    :param filter_type: 't' for tag, 'n' for notebook or 'q' for 
    """
    assert filter.notebooks == [], 'Notebook filter not implemented'
    assert filter.query == '', 'Query filter not implemented'
    assert len(filter.tags) == 1, 'Expect single tag. (multiple tags filter not implemented) '

    return (await api().get_tags_notes(await tag_titled(ilter.tags[0]))).json()

async def update_note(note,tags=None):
    """ Uploads note to serve.

    Required item or they will be erased: 'author', 'source_url', 'is_todo'
    if 'is_todo' in addition:  'todo_due', 'todo_completed'
    All other items are ignored.
    
    :param note: note data as dict

    :param tags: list of tag titles to replace current tags. If None current tags are kept

    """

    # fetch tags from server. There are note returned b which are not returned by `get_note`
    if tags:
        note['tags'] = ', '.join(tags)
    else:
        tags = (await api().get_notes_tags(nid)).json()
        note['tags'] = ', '.join([t['title'] for t in tags])
        
    # see https://github.com/foxmask/joplin-api/blob/master/joplin_api/core.py
    res = await api().update_note(note['id'], note['title'], note['body'], note['parent_id'], **note)
    assert res.status_code == 200, res