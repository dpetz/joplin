#!/usr/bin/env python
# see https://realpython.com/run-python-scripts/#using-the-script-filename

""" Application accessible as Command Line Interface """

import logging, asyncio, sys
from datetime import datetime
from argparse import ArgumentParser # see https://docs.python.org/3/library/argparse.html#module-argparse
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

def config_log(debug_flag, log_file = '.log'):
    logging.basicConfig(
        level=logging.DEBUG if debug_flag else logging.INFO,
        format='%(levelname)s:%(message)s' 
        ,handler = logging.FileHandler(log_file)#, logging.StreamHandler()]
        )
    logging.debug(f"Zelda launching at {datetime.now()}.")

def config_args():
    p = ArgumentParser(description='Turns Joplin into a Zettelkasten')
    add = p.add_argument
    add(
        'cmd', help=f"The command Zelda will run", \
        choices=['scripts', 'backlinks', 'notes'])    
    add('par', nargs='*', help=f"Command parameters (optional)")
    add("-d", "--debug",  help="Print debug messages", action='store_true')
    add("-t", "--tag",    help="Only process notes with this tag")
    add("-s", "--search", help="Only processes notes that match the search")
    return p

def run_client():
    """ Entry point when starting the application. """
    args = config_args().parse_args(sys.argv[1:])
    config_log(args.debug)
    #asyncio.run(launch_command(args))
    # file_handler.close()

if __name__ == '__main__':
    # if no parameters (except path to script) debug with some hardcoded parameters
    if len(sys.argv) <= 1:
        sys.argv += 'notes -d -s data'.split()
    run_client()