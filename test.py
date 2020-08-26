my_token = "d71fffcded46c7385a1bf6a564e8e0d80ffc67d693e682131c3f4cba3ddb896aaf3210dd09a783e460c303cca61d3132b5dd2a5a6566b7b696972347b0f45cb9"

import asyncio
from joplin_api import JoplinApi
joplin = JoplinApi(token=my_token)



async def get_toc(id = 'f25dd640fb8f43dab90f9652e30b6a20'):
    res = await joplin.get_note(id)
    print(res.json()['body'])

#asyncio.run(get_toc())


example = """Table of Content

...

[siyach](evernote:///view/536854/s1/d9b2c4a8-9c77-4202-a6b0-1007f572754f/d9b2c4a8-9c77-4202-a6b0-1007f572754f/) bla

7193. [Predigt Vineyard Dirk: Freude](evernote:///view/536854/s1/a42586cd-3993-4827-8c1f-0e43f5e587a2/a42586cd-3993-4827-8c1f-0e43f5e587a2/)

7194. [Hauskreis (Apr'06)](evernote:///view/536854/s1/2a825cc7-b6d6-469d-95b8-11bf78ad2977/2a825cc7-b6d6-469d-95b8-11bf78ad2977/)
"""

def regexpr():
    # https://stackoverflow.com/questions/25109307/how-can-i-find-all-markdown-links-using-regular-expressions
    import regex
    q = regex.compile('(?|(?<txt>(?<url>(?:ht|f)tps?://\S+(?<=\P{P})))|\(([^)]+)\)\[(\g<url>)\])')
    print(regex.findall(q,example))

def __collect_links(data,links):

    # if list recurse all elements
    if isinstance(data,list):
        for d in data:
            collect_links(d,links)

    # if dict recurse 'children' element
    elif isinstance(data,dict):

        if 'children' in data:
            collect_links(data['children'],links)
        
        if data['type'] == 'link':
            links.append(Link(link=data['destination'],text=''))

        if data['type'] == 'text':
            links[-1] = Link(links[-1].link, links[-1].text + data['literal'])

    return links

def parse_as_json(s):
    import commonmark, json
    parser = commonmark.Parser()
    ast = parser.parse(s)
    return commonmark.dumpJSON(ast)
    

def extract_links(s):
    data = json.loads(parse_as_json(s))
    links = __collect_links(data, [])
    return [link for link in links if link.text] 




print(parse_as_json(example))