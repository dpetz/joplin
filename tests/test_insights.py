from context import zettel
import insights
import re


doc_1 = """
Some Text
___
:link:<www.wikipedia.org>
:robot:`2020`

"""

def test_clear():
    md = insights.clear(doc_1)
    assert "\nSome Text\n" == md, md

def test_read():
    ins = insights.read(doc_1)
    assert len(ins) == 2, ins
    assert ins[0].marker == ':link:' and ins[0].content == '<www.wikipedia.org>', ins[0]
    assert ins[1].marker == ':robot:' and ins[1].content == '`2020`', ins[1]

def test_drop():
    doc = insights.drop(':link:', doc_1)
    ins = insights.read(doc)
    assert len(ins) == 1, ins
    assert ins[0].marker == ':robot:' and ins[0].content == '`2020`', ins[0]

def test_add():
    doc = insights.add(':panda_face:','Crowd','Zoo')
    ins = insights.read(doc)
    assert len(ins) == 1, doc


def test_drop_last():
    doc = """Hello\n___\n:smile:World"""
    drop = insights.drop(':smile:', doc)
    assert drop == "Hello", drop