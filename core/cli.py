#!/usr/bin/env python
# see https://realpython.com/run-python-scripts/#using-the-script-filename

""" Entry point for application from 
"""

import logging, asyncio, sys
from datetime import datetime
import argparse # see https://docs.python.org/3/library/argparse.html#module-argparse
sys.path.insert(0, '/Users/dpetzoldt/git/home/joplin-api')
import server, markdown, scripts, backlinks

    
async def launch_command(args):
    if args.cmd == 'scripts':
        result = await scripts.find()
        logging.info(result)
    elif args.cmd == 'backlinks':
        await server.edit_notes(backlinks.add_backlinks, args.tag, logging.getLogger())
    elif args.cmd == 'notes':
        notes = await server.search(args.search)
        for n in notes:
            print(n)
        print(len(notes))   

def config_log(debug, log_file = 'app.log'):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(levelname)s:%(message)s' 
       #,handlers=[logging.FileHandler(log_file)]#, logging.StreamHandler()]
        )
    logging.debug(f"Zelda launching at {datetime.now()}.")

def config_args():
    parser = argparse.ArgumentParser(description='Turns Joplin into a Zettelkasten')
    parser.add_argument('cmd', help=f"The command Zelda will run", \
        choices=['scripts', 'backlinks', 'notes'])
    parser.add_argument('par', nargs='*', help=f"Command parameters (optional)")
    parser.add_argument("-d", "--debug", help="Print debug messages", action='store_true')
    parser.add_argument("-t", "--tag", help="Only process notes with this tag")
    parser.add_argument("-s", "--search", help="Only processes notes that match the search")
    return parser

def run_application():
    args = config_args().parse_args(sys.argv[1:])
    config_log(args.debug)
    #asyncio.run(launch_command(args))
    # file_handler.close()

if __name__ == '__main__':
    # if no parameters debug with following parameters
    if len(sys.argv) == 1:
        sys.argv = [sys.argv[0]] + 'notes -d -s data'.split()
    run_application()