""" _Insights_ refer to note wide data created by this library and embedded within notes.
This module reads and writes insights to note markdown in a consistent and convenient way.
Each insights consists of a _marker_ and _content_.
The marker's are typically emojis such as `":robot:"` 
"""

def add(insight_marker, insight_content, note_body):
    """Add insight to note body markdown"""
    pass

def read(note_body):
    """Extracts all note insights as dict from markers to content."""
    pass

def drop(insight_marker, note_body):
    """"Remove insight for given marker."""
    pass

