from context import zettel
from zettel import rules


def test_normalize():
    norm = rules.normalize("Hello\n\n\n\n****\n---\nWorld\n\n")
    assert norm == "Hello\n\n* * *\nWorld", norm
    print('Done')


def test_thematic_break():
    assert rules.reThematicBreak.search(f"hi\n___") != None