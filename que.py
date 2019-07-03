#!/usr/bin/python3
# Name: que.py
# Version: R2
# Date: July 2019
# Function: Includes threading with queue
#
import requests
from threading import Thread
import queue
concurrent = 2

# Threading functions
def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        #doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        req = requests.head(ourl, timeout=10)
        status = str(req.status_code)
        return status, ourl
    except:
        return "OOO", ourl

# Start the paralel queue
q = queue.Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
