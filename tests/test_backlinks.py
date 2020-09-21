from context import zettel

from zettel.backlinks import remove_backlinks_markdown

some_markdown = """Some text
^:link:^[Test 2](:/736ab59b113e4ea4b09b24293dc2cba9), [Test 3](:/9e830bc6530c416e950105834689cd63) 
More text"""

def test_search():
    removed = remove_backlinks_markdown(some_markdown)
    print(removed)

test_search()