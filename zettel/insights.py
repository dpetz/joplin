""" _Insights_ refer to note wide data created by this library and embedded within notes.
This module reads and writes insights to note markdown in a consistent and convenient way.
Each insights consists of a _marker_ and _content_.
The marker's are typically emojis such as `":robot:"` 
"""
import re
import markdown
import logging

# each line is empty or an insight starting with a marker 
_marker = "^:[a-z]{3,}:"

# insights block starts with a thematic break
_opening = markdown.reThematicBreak.pattern

# insights block closes with end of string or thematic break
_closing =  "\Z" 

_insight = f"^({_marker})(.*)$"

_insights = f"{_opening}\n+((?:^{_marker}.*\n*)+){_closing }"

def add(insight_marker, insight_content, note_body):
    """Add insight to note body markdown"""
    assert re.match(marker + '$', insight_marker), insight_marker
    note_body += f"\n{_opening}\n{insight_marker}{insight_content}"

def read(markdown_string):
    """Extracts all note insights as dict from markers to content,
    with same order as in the markup. None if no insights found. """
    block = re.search(_insights, markdown_string, re.M)
    if block:
        insights = {}
        for line in block.group(1).split("\n"):
            if line:
                m = re.match(_insight,line)
                insights[m.group(1)] = m.group(2).strip()

        return insights

def remove(markdown_string):
    """Remove all insights. Returns new modified string or None of no insights found."""
    m = re.search(_insights, markdown_string, re.M)
    if m:
        return markdown_string[:m.start(0)] + markdown_string[m.end(0):]

def drop(insight_marker, note_body):
    """"Remove insights for given marker."""
    raise Exception("Not Implemented")

