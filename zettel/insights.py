""" _Insights_ refer to note wide data created by this library and embedded within notes.
This module reads and writes insights to note markdown in a consistent and convenient way.
Each insights consists of a _marker_ and _content_.
The marker's are typically emojis such as `":robot:"` 
"""

import re
import markdown

# each line is empty or an insight starting with a marker 
_marker = "^:[a-z]{3,}:"

_content = ".*"

# insights block starts with a thematic break
_opening = markdown.reThematicBreak.pattern

# insights block closes with end of string or thematic break
_closing =  "\Z"  # r"[(?:" + _opening + r")\Z]"

_insight = f"^(?P<marker>{_marker})(?P<content>{_content})$"

# 
_insights = f"(?:{_insight}\n+)+"

_block = f"{_opening}\n+(?P<insights>{_insights})" #\n+{_closing}


def add(insight_marker, insight_content, note_body):
    """Add insight to note body markdown"""
    assert re.match(marker + '$', insight_marker), insight_marker
    note_body += f"\n{_opening}\n{insight_marker}{insight_content}"

def read(markdown_string):
    """Extracts all note insights as dict from markers to content,
    with same order as in the markup."""
    m = re.search(_block, markdown_string, re.M)
    print(f"INSIGHTS:\n{m.group('insights')}\n---------------")
    return re.findall(_insights + '?', m.group('insights'), re.M)

def drop(insight_marker, note_body):
    """"Remove insight for given marker."""
    pass


def test_read():
    body = """
Some Text
___
:link:<www.wikipedia.org>
:robot:`2020`
"""
    matches = read(body)
    print(matches)
    #for m in matches:
    #    print(m)

test_read()


