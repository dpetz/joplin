from dataclasses import dataclass
import commonmark
import json
import asyncio
from joplin_api import JoplinApi

@dataclass
class Link:
    url:str
    text:str

joplin = None
def api():
    global joplin
    if not joplin:
        with open('.token') as f:
            joplin = JoplinApi(f.readline())
    return joplin


async def tag_titled(tag_title):
    tags = await api().get_tags()
    for t in tags.json():
         if t['title'] == tag_title:
             return t['id']
    raise Exception(f"No such tag: {tag_title}")


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