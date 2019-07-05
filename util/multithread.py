#!/usr/bin/python3
from threading import Thread
import http.client, sys
import queue
import requests

concurrent = 8

def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        req = requests.head(ourl, timeout=10, proxies={'http':'','https':''})
        status = str(req.status_code)
        return status, ourl
    except:
        return "error", ourl

def doSomethingWithResult(status, url):
    print(status, url)

q = queue.Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for url in open('output/OK.lst'):
        q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
