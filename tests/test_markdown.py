import commonmark
import logging

from itertools import chain
from zettel.util import pretty
from context import zettel
from zettel import markdown

markdown_example = """
# My Title
* * *
Backlinks
- [Backlink 1](:/4083d03c95e042fb8da9176f9bb2a051)
"""

def inspect_ast():
    #commonmark.dumpAST(ast)
    # see js doc: https://developer.aliyun.com/mirror/npm/package/commonmark
    ast = parser.parse(markdown_example)
    for n in ast.walker():
        if n[1]: # entering
            n[0].pretty()
            print("\n\n")

    
def deflist():
    md = "Term 1\n:   Def 1"
    print(markdown.html(md))


def _test_html():
    result = html(markdown_example)
    print (result)
    assert result == \
        '<h1>My Title</h1>\n<hr />\n<p>Backlinks</p>\n<ul>\n<li><a href=":/4083d03c95e042fb8da9176f9bb2a051">Backlink 1</a></li>\n</ul>\n'

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



def _test_types_in_json():
    json_dict = json.loads(commonmark.dumpJSON(ast))
    logging.info(pretty(json_dict))
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