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
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler

try:
    import asyncio
except ImportError:
    import trollius as asyncio

def start_scrapping():
    os.system('python3 scrapper.py')

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()

    interval_cycle = 3
    scheduler.add_job(start_scrapping, 'interval', seconds = interval_cycle)
    scheduler.start()

    # Execution will block here until Ctrl+C is pressed.
    print(f'Press Ctrl+{"Break" if sys.platform == "win32" else "C"} to exit')
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

