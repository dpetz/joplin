import commonmark
import pprint
import json

from itertools import chain

from context import zettel
parser = commonmark.Parser()

markdown_example= """
# My Title
---
Backlinks
[Backlink 1](:/4083d03c95e042fb8da9176f9bb2a051)
"""

def not_a_test_yet():
    
    print(html) # <p>Hello <em>World</em><p/>

    # inspecting the abstract syntax tree
    
    #commonmark.dumpAST(ast) # pretty print generated AST structure


def test_markdown_to_html():
    ast = parser.parse(markdown_example)
    json_dict = json.loads(commonmark.dumpJSON(ast))
    renderer = commonmark.HtmlRenderer()
    assert renderer.render(ast) == \
        '<h1>My Title</h1>\n<hr />\n<p>Backlinks\n<a href=":/4083d03c95e042fb8da9176f9bb2a051">Backlink 1</a></p>\n'

def collect_values(json,key):
    """Recursively extracts all values of `key` from a json object as `list`."""
    if isinstance(json,list):
        return chain(*[collect_values(j,key) for j in json])
    if isinstance(json,dict):
        vals = []
        if key in json:
            vals.append(json[key])
        for k,v in json.items():
            if k != key:
                vals += collect_values(v,key)
        return vals
    return []
    

def test_types_in_json():
    ast = parser.parse(markdown_example)
    json_dict = json.loads(commonmark.dumpJSON(ast))
    pp = pprint.PrettyPrinter(indent=4, width=40, compact=False, sort_dicts=False)
    #pp.pprint(json_dict)

            
    expected = ['document', 'heading', 'text', 'heading', 'thematic_break', \
        'paragraph', 'text', 'softbreak', 'link', 'text', 'link', 'paragraph', 'document']
    
    # assert collect_types(json_dict) == expected
    actual = list(collect_values(json_dict,'type'))
    print(actual)
    assert expected == actual

[{'children': [...], 'type': 'document'}, {'children': [...], 'type': 'heading'}, {'children': [...], 'destination': ':/4083d03c95e042fb8d...6f9bb2a051', 'type': 'link'}, {'children': [...], 'type': 'paragraph'}, {'children': [...], 'type': 'document'}]
test_types_in_json()