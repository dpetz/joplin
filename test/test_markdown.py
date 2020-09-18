import commonmark
import pprint
import json
parser = commonmark.Parser()

markdown_example= """
# Empty Note
---
Backlinks
[Test 1](:/4083d03c95e042fb8da9176f9bb2a051)
"""

def tes():

    renderer = commonmark.HtmlRenderer()
    html = renderer.render(ast)
    #print(html) # <p>Hello <em>World</em><p/>

    # inspecting the abstract syntax tree
    
    commonmark.dumpAST(ast) # pretty print generated AST structure


def test_mk_to_json():
    ast = parser.parse(markdown_example)
    json_dict = json.loads(commonmark.dumpJSON(ast))
    pp = pprint.PrettyPrinter(indent=4, width=40, compact=False, sort_dicts=False)
    #pp.pprint(json_dict)
    
    def collect_types(json, types=[]):
        for child in json.get('children',[]):
            collect_types(child,types)
        types.append(json['type'])
    
    print(collect_types())


