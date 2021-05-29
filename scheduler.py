'''
author: WoolenHat
title:  Scheduler for scrapper.py
Year:   2019

Description:
    A small script to keep the web_scraper running. All you have to do is
    leave it running in your dedicated web-server.

Usage:  python scheduler.py
'''

import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

try:
    import asyncio
except ImportError:
    import trollius as asyncio

def my_job():
    os.system('python3 scrapper.py')

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(my_job, 'interval', seconds=3)
    scheduler.start()
    print(f'Press Ctrl + {"Break" if os.name == "nt" else "C"} to exit')

    # Execution will block here until Ctrl+C is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

