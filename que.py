#!/usr/bin/python3
# Name: que.py
# Version: R3.1
# Author: jvalentinpastrana at gmail
# Date: Jan 2021
# Function: Includes threading with queue
#
import requests
from threading import Thread
import queue

timeout = 5
concurrent = 4

# Threading functions
def do_work():
    while True:
        url = q.get()
        status, url = get_status(url)
        write_result(status, url)
        q.task_done()

def get_status(ourl):
    try:
        req = requests.head(ourl, timeout=timeout, proxies={'http':'','https':''})
        status = str(req.status_code)
        return status, ourl
    except:
        return "XXX", ourl

def write_result(status, ourl):
    urlFilter.write(status + ' ' + ourl + '\n')
    print(status + ' ' + ourl )

# Start the paralel queue
q = queue.Queue(concurrent)
for i in range(concurrent):
    t = Thread(target=do_work)
    t.daemon = True
    t.start()

