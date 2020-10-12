#!/usr/bin/env python
# see https://realpython.com/run-python-scripts/#using-the-script-filename

import logging
import os
from datetime import datetime
import argparse # see https://docs.python.org/3/library/argparse.html#module-argparse


log_file = 'zettel.log'

def init_log():
    log = logging.getLogger('zettel')
    log.setLevel(logging.DEBUG)
    os.remove(log_file)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(levelname)s %(message)s') # %(asctime)s - %(name)s - 
    handler.setFormatter(formatter) 
    log.addHandler(handler)

    log.info(f"Zettel App launched at {datetime.now()}.")

    return log

log = init_log()



parser = argparse.ArgumentParser(description='Turn Joplin into a Zettelkasten')
parser.add_argument('script', help='Name of script to run')
parser.add_argument("-d", "--debug", help="Print debug messages", action="store_true")
parser.add_argument("-l", "--label", help="Only process notes with this tag")

args = parser.parse_args()

logging.basicConfig(
    level=logging.DEBUG if args.debug else logging.INFO,
    format='%(levelname)s:%(message)s', 
    handlers=[logging.FileHandler('app.log','w'), logging.StreamHandler()]
    )



logging.info(args.script)
logging.debug(args.label)
