from context import zettel
from zettel import rules
from zettel import markdown


async def test_normalize():
    norm = await rules.normalize("Hello\n\n\n\n****\n---\nWorld\n\n")
    assert norm == "Hello\n\n* * *\nWorld", norm


def test_thematic_break():
    assert markdown.reThematicBreak.search(f"hi\n___") != None