import commonmark
import pprint
import json
import logging

from itertools import chain

from context import zettel

markdown_example = """
# My Title
* * *
Backlinks
- [Backlink 1](:/4083d03c95e042fb8da9176f9bb2a051)
"""

parser = commonmark.Parser()
ast = parser.parse(markdown_example)
pp = pprint.PrettyPrinter(indent=4, width=40, compact=False, sort_dicts=False)


def inspect_ast():
    #commonmark.dumpAST(ast)
    # see js doc: https://developer.aliyun.com/mirror/npm/package/commonmark
    for n in ast.walker():
        if n[1]: # entering
            n[0].pretty()
            print("\n\n")

def html(md):
    return commonmark.HtmlRenderer().render(parser.parse(md))
    
def deflist():
    md = "Term 1\n:   Def 1"
    print(html(md))

def test_markdown_to_html():
    assert renderer.render(ast) == \
        '<h1>My Title</h1>\n<hr />\n<p>Backlinks\n<a href=":/4083d03c95e042fb8da9176f9bb2a051">Backlink 1</a></p>\n'

def collect_values(json,key):
    """Recursively extracts all values of `key` from a json object as `list`."""
    if isinstance(json,list):
        return list(chain([collect_values(j,key) for j in json]))
    if isinstance(json,dict):
        vals = []
        for k,v in json.items():
            vals_recursive = collect_values(v,key)
            if vals_recursive:
                vals.append(vals_recursive)

        if len(vals) > 0:
            return {json.get(key, None) : vals}
        else:
            return json.get(key, None)
    return None
    

def test_types_in_json():
    json_dict = json.loads(commonmark.dumpJSON(ast))
    logging.info(pp.pprint(json_dict))
    tmp = list(collect_values(json_dict,'type'))
    assert tmp  == [ \
        {'document': [['heading', 'text']]}, \
        {'heading': [['thematic_break', 'paragraph', 'text']]}, \
        {'paragraph': [[{'list': ['bullet']}, {'item': ['bullet']}, 'paragraph', 'link', 'text']]}, \
        'link', \
        'paragraph', \
        {'item': ['bullet']}, \
        {'list': ['bullet']}, \
        'document'\
        ]

    
# inspect_ast()
deflist()