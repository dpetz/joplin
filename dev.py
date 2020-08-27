import commonmark
import json
import asyncio
from joplin_api import JoplinApi


def read_token():
    with open('.token') as f:
        return f.readline()
    
joplin = JoplinApi(read_token())




async def get_toc(id = 'f25dd640fb8f43dab90f9652e30b6a20'):
    res = await joplin.get_note(id)
    print(res.json()['body'])

#asyncio.run(get_toc())




from dataclasses import dataclass

@dataclass
class Link:
    url:str
    text:str

def regexpr():
    # https://stackoverflow.com/questions/25109307/how-can-i-find-all-markdown-links-using-regular-expressions
    import regex
    q = regex.compile('(?|(?<txt>(?<url>(?:ht|f)tps?://\S+(?<=\P{P})))|\(([^)]+)\)\[(\g<url>)\])')
    print(regex.findall(q,example))



    

def markup_to_json(s):
    parser = commonmark.Parser()
    ast = parser.parse(s)
    return commonmark.dumpJSON(ast)
    

def extract_links(md):

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
                
            elif data['type'] == 'link':
                link = Link(data['destination'],'')
                links.append(link)
                
            elif (data['type'] == 'text') and link:
                    link.text += data['literal']
                
        return link


    data = json.loads(markup_to_json(md))
    links = []
    __collect_links(data, links, None)
    return [link for link in links if link.text] 