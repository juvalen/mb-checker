from twisted.internet import reactor, threads
from urllib.parse import urlparse
import http.client
import itertools


concurrent = 200
finished=itertools.count(1)
reactor.suggestThreadPoolSize(concurrent)

def getStatus(ourl):
    url = urlparse(ourl)
    conn = httplib.HTTPConnection(url.netloc)   
    conn.request("HEAD", url.path)
    res = conn.getresponse()
    return res.status

def processResponse(response, url):
    print(response, url)
    processedOne()

def processError(error, url):
    print("error", url, error)
    processedOne()

def processedOne():
    if finished.next()==added:
        reactor.stop()

def addTask(url):
    req = threads.deferToThread(getStatus, url)
    req.addCallback(processResponse, url)
    req.addErrback(processError, url)   

added=0
for url in open('OK.url'):
    added+=1
    addTask(url.strip())

try:
    reactor.run()
except KeyboardInterrupt:
    reactor.stop()
