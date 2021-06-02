#!/usr/bin/env python
# see https://realpython.com/run-python-scripts/#using-the-script-filename

import logging
import os
from datetime import datetime
import argparse # see https://docs.python.org/3/library/argparse.html#module-argparse
import server
import asyncio
import re
import markdown
import scripts


log_file = 'app.log'
commands = ['scripts']
    

async def launch(args):
    """
        if cmd:
            if cmd['robot'] == 'tag_report':
                await tag_report(cmd['label'])
                with open(log_file) as file:  
                    note['body'] = note['body'] + '\n* * *\n' + file.read()
                    await server.update_note(note)
            else:
                logging.warning(f"Unknown script: {cmd['robot']}")
    """

    if args.command == 'scripts':
        result = await scripts.find()
        logging.info(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Turns Joplin into a Zettelkasten')
    parser.add_argument('command', help=f"Command to run", choices=commands)
    parser.add_argument("-d", "--debug", help="Print debug messages", action="store_true")
    parser.add_argument("-l", "--label", help="Only process notes with this tag")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(levelname)s:%(message)s', 
        handlers=[logging.FileHandler(log_file,'w'), logging.StreamHandler()]
        )

    logging.debug(f"Zelda App launched at {datetime.now()}.")

    asyncio.run(launch(args))