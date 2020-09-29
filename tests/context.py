# see https://docs.python-guide.org/writing/structure/
import sys, os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROJECT_DIRS = [
    os.path.join(PROJECT_ROOT, 'tests'),
    os.path.join(PROJECT_ROOT, 'zettel'),
    PROJECT_ROOT
]
sys.path[:0] = PROJECT_DIRS

import zettel
import logging

logging.getLogger().setLevel(logging.DEBUG)

TEST_NOTEBOOK = "Test"

TEST_LABEL = "test"

def add_test_note(title,body):
    pass

def clear_test_notes():
    pass