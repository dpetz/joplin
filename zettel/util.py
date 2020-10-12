from dataclasses import dataclass
import commonmark
import json
import pprint


@dataclass
class Link:
    url:str
    text:str

def pretty(json):
    pp = pprint.PrettyPrinter(indent=4, width=40, compact=False, sort_dicts=False)
    return pp.pprint(json)


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