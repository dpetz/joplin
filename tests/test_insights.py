from context import zettel
import insights
import re

markdown_01 = """
Some Text
___
:link:<www.wikipedia.org>
:robot:`2020`

"""

def test_remove():
    md = insights.remove(markdown_01)
    assert re.match("\n*Some Text\n*",md), md

def test_read():
    
    assert insights.read(markdown_01) == \
        {':link:': '<www.wikipedia.org>', ':robot:': '`2020`'}


test_remove() 
