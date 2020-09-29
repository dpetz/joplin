""" _Insights_ refer to note wide data created by this library and embedded within notes.
This module reads and writes insights to note markdown in a consistent and convenient way.
Each insights consists of a _marker_ and _content_.
The marker's are typically emojis such as `":robot:"` 
"""
import re
import markdown
import logging

from dataclasses import dataclass

# each line is empty or an insight starting with a marker 
_marker = "^:[a-z_]{3,}:"

# insights block starts with a thematic break
_opening = markdown.reThematicBreak.pattern

# insights block closes with end of string or thematic break
_closing =  r"\Z" 

reInsight = re.compile(f"^({_marker})(.*)$", re.M)

reInsights = re.compile(f"{_opening}\n+((?:^{_marker}.*\n*)+){_closing }", re.M)

@dataclass
class Insight:
    marker:str
    content:str
    start:int
    end:int

def add(marker, content, doc):
    """Add insight to note body markdown"""
    assert re.fullmatch(_marker, marker), marker
    edit = f"\n{marker}{content}"
    if not read(doc):
        doc += "\n* * *"
    return doc + edit
    
def read(markdown_string):
    """Lists insights found in note """
    block = reInsights.search(markdown_string)
    insights = []
    if block:
        offset = block.start(0)

        while True:
            match = reInsight.search(markdown_string, offset)
            if not match:
                break
            insights += [Insight(match.group(1), match.group(2).strip(), match.start(0), match.end(0))]
            offset = match.end(0) + 1

    return insights

def clear(doc):
    """Remove all insights. """
    match = reInsights.search(doc)
    return doc[:match.start(0)] if match else doc

def drop(marker, doc):
    """"Remove insights for given marker."""
    insights = read(doc)
    insights.reverse()
    for ins in insights:
        if ins.marker == marker:
            doc = doc[:ins.start] + doc[ins.end:]
    return doc


    

