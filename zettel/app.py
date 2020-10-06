import logging
import os
from datetime import datetime


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

if __name__ == "__main__":
    pass


