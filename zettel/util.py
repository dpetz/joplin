from dataclasses import dataclass
import commonmark
import json
import asyncio
from joplin_api import JoplinApi
from httpx import Response


@dataclass
class Link:
    url:str
    text:str

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

async def notes_tagged(tag_title):
    return (await api().get_tags_notes(await tag_titled(tag_title))).json()


def markup_to_json(s):
    parser = commonmark.Parser()
    ast = parser.parse(s)
    return commonmark.dumpJSON(ast)
    

def links_from_markdown(md):
    """ Returns all links found in Markdowen string md as a list of Link objects. """

    def __collect_links(data,links,link):
        """
        data -- deserialized json of parsed markup
        links -- all links collected so far
        link -- last parsed link; set / reset within each level to match terxt w/ urls.

        """

        # if list recurse all elements
        if isinstance(data,list):
            for d in data:
                link = __collect_links(d,links,link)
            return None

        # if dict recurse 'children' element
        elif isinstance(data,dict):

            if ('children' in data) and data['children']:
                    __collect_links(data['children'],links,None)
                
            elif 'destination' in data: # data['type'] == 'link':
                link = Link(data['destination'],'')
                links.append(link)
                
            elif (data['type'] == 'text') and link:
                    link.text += data['literal']
                
        return link


    data = json.loads(markup_to_json(md))
    links = []
    __collect_links(data, links, None)
    return [link for link in links if link.text] 