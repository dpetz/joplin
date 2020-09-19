from context import zettel
from zettel.util import links_from_markdown

markup_example_3_links = """Table of Content

...

[siyach](evernote:///view/536854/s1/d9b2c4a8-9c77-4202-a6b0-1007f572754f/d9b2c4a8-9c77-4202-a6b0-1007f572754f/) bla

7193. [Predigt Vineyard Dirk: Freude](evernote:///view/536854/s1/a42586cd-3993-4827-8c1f-0e43f5e587a2/a42586cd-3993-4827-8c1f-0e43f5e587a2/)

7194. [Hauskreis (Apr'06)](evernote:///view/536854/s1/2a825cc7-b6d6-469d-95b8-11bf78ad2977/2a825cc7-b6d6-469d-95b8-11bf78ad2977/)
"""


def test_links_from_markdown():
    links = links_from_markdown(markup_example_3_links)
    print(links)
    assert len(links) == 3
    assert links[-1].url == 'evernote:///view/536854/s1/2a825cc7-b6d6-469d-95b8-11bf78ad2977/2a825cc7-b6d6-469d-95b8-11bf78ad2977/'
    assert links[-1].text == "Hauskreis (Apr'06)"