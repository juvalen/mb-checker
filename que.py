#!/usr/bin/python3
# Name: que.py
# Version: R3.1
# Author: jvalentinpastrana at gmail
# Date: January 2020
# Function: Includes threading with queue
#
import requests
from threading import Thread
import queue
DIRNAME = "output/"
TIMEOUT = 5

concurrent = 32

# Threading functions
def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        writeResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        req = requests.head(ourl, timeout=TIMEOUT, proxies={'http':'','https':''})
        status = str(req.status_code)
        return status, ourl
    except:
        return "XXX", ourl

def writeResult(status, ourl):
    urlFilter.write(status + ' ' + ourl + '\n')
    print(status + ' ' + ourl )

# Start the paralel queue
q = queue.Queue(concurrent)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

