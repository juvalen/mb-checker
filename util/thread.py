#!/usr/bin/python3
# Name: chrome.py
# Version: R2
# Date: July 2019
# Function: Parses original chrome Bookmarks file
#           Tries to reach each URL and removes it on error
#           Accepts return codes as parameters. chrome.py must be called as executable:
#           $ ./chrome.py --help
#           $ ./chrome.py 404 501 403
#           Threaded
#
# Input: bookmark file in ./.config/BraveSoftware/Brave-Browser/Default/Bookmarks
#        Bookmarks file structure:
#  {
#     "checksum": "79c9312bbeee61a5710117f00bc16ff8",
#     "roots": {
#        "bookmark_bar": {
#           "children": [ {
#              "date_added": "13187860084000000",
#                             ...
#           }, {
#                             ...
#           }],
#              "children": [ {
#                 "date_added": "13134043672000000",
#                             ...
#              }, {
#                             ...
#              }],
#                 "children": [ {
#                             ...
#                 }, {
#                    "date_added": "13154093672000000",
#                    "id": "4092",
#                    "name": "Servicio LG Electronics en Linea :: Drivers",
#                    "type": "url",
#                    "url": "http://es.lgservice.com/"
#                 }, {
#                             ...
#                 } ],
#                 'date_added': '13199527258944339',
#                 'date_modified': '0',
#                 'id': '6540',
#                 'name': 'Tuxedo',
#                 'type': 'folder'}
#              } ],
#              "date_added": "13199527258977344",
#              "date_modified": "13200493908840013",
#              "id": "7107",
#              "name": "unfiled",
#              "type": "folder"
#           } ],
#           "date_added": "13198974830896033",
#           "date_modified": "13200494087851454",
#           "id": "1",
#           "name": "Bookmark bar",
#           "type": "folder"
#        }
#        "other": {
#        }
#        "synced": {
#        }
#     }
#    "version": 1
#  }
#
# Output:

import requests
import json
from pprint import pprint
import sys
from threading import Thread
import http.client, sys
import queue

concurrent = 2

DELETEFOLDER = 0
DIRNAME = "output/"
JSONIN = DIRNAME + "Bookmarks"
JSONOUT = DIRNAME + "Filtered.json"
URLXXX = DIRNAME + "XXX.url"
URLOK = DIRNAME + "OK.url"

# Read input parameters and create corresponding files
params = sys.argv[1:]
nparams = len(sys.argv)
errorWatch = []
errorName = []
errorFile = []
if nparams > 1:
    if params[0] == '--help':
        print("""
Usage:
    ./thread.py <code1> <code2> <code3>

Parameters:
    http return <code> that will trigger not adding its URL to filtered file and writing its address to '<code>.url'. Code range [100..999].

Files:
    Input 'Bookmark' file
    Output will be written to 'output/'. These file will be created:
     - Filtered.json (purged file)
     - XXX.url (network errors)
     - OK.url (all passed)
     - One <code>.url file for each parameter
        """)
        sys.exit()
elif nparams == 1:
        print("""
Usage: ./chrome.py <code1> <code2> <code3>
        """)
        sys.exit()

# Parameter parsing
for param in params:
    if param.isdigit():
        iparam = int(param)
        if iparam > 99 and iparam < 1000:
            errorWatch.append(param)
            errorName.append("URL" + param)
            errorFile.append(DIRNAME + param + '.url')
        else:
            print("Error: return code", param, "is out of bounds [100..999]\n")
            sys.exit()
    else:
        print("Error: return code", param, "is not and integer\n")
        sys.exit()

# Create output/ directory if not exists
try:
    os.mkdir(DIRNAME)
    print("Directory" , DIRNAME , "created ")
except:
    print("Directory" , DIRNAME , "preserved")

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
NONE = '\033[0m' # No Color

# Read source bookmark file
with open(JSONIN, "r") as f:
    Bookmarks = json.load(f)

# Create output files
urlXXX = open(URLXXX,"w")
urlOK = open(URLOK,"w")
for i in range(0, nparams-1):
    errorName[i] = open(errorFile[i], "w")
    print("Created", errorName[i])

# Threading functions
def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        #doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        req = requests.head(ourl, timeout=10, proxies={'http':'','https':''})
        status = str(req.status_code)
        return status, ourl
    except:
        return "XXX", ourl

# Start the paralel queue
q = queue.Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

# Recurrent function
def preorder(tree, depth):
    depth += 1
    if tree:
        width = len(tree)
        i = d = 0
        for item in tree:
            name = item["name"]
            try:
                branches = len(item["children"])
                subtree = item["children"]
                print("[" + str(depth) + "] " + name + " (" + str(branches) + ")")
            except:
                branches = 0
            if branches > 0:
                preorder(subtree, depth)
            else:
                type = item["type"]
                id = item["id"]
                if type == "url":
# list element being checked is i
                    date_added = item["date_added"]
                    url = item["url"]
                    print(">>> " + url)
                    #print("  N ", name)
                    try:
# To paralelize
# Send request to queue
                        q.put(url.strip())
                        q.join()
# Read request from queue
                        status, url = getStatus(url)
# Old sequential
                        #req = requests.head(url, timeout=10)
                        #status = str(req.status_code)
                    except:
                        print(RED + "  XXX " + id + " #" + str(i))
                        urlXXX.write(url + "\n")
                        ret = tree.pop(d); d -= 1
                        print(NONE, end="")
                    else:
                        found = 0
                        for j, code in enumerate(errorWatch):
                            if status == code:
                                found = 1
                                print(RED + "  " + status + " " + id + " #" + str(i))
                                errorName[j].write(url + "\n")
                                ret = tree.pop(d); d -= 1
                                print(NONE, end="")
                        if not found: # looked for code not in list
                            print(" ", status, '+' + " #" + str(i))
                            urlOK.write(url + "\n")
                elif type == "folder":
                    print(GREEN + "  Empty folder" + NONE)
                    if DELETEFOLDER:
                        ret = tree.pop(d); d -= 1
                else:
                    print(BLUE + "   ???" + id + NONE)
            i += 1
            d += 1
    return tree

original = Bookmarks['roots']['bookmark_bar']['children']
nodes = preorder(original, 0)
# JSON structure
other = {
    "children": [  ],
    "date_added": "13198974830951405",
    "date_modified": "13200950919336220",
    "id": "2",
    "name": "Other bookmarks",
    "type": "folder"
}

synced = {
    "children": [  ],
    "date_added": "13198974830951420",
    "date_modified": "0",
    "id": "3",
    "name": "Mobile bookmarks",
    "type": "folder"
}

bookmarks_bar = {"children": nodes,
                 "date_added": "13198974830896033",
                 "date_modified": "13200494087851454",
                 "id": "1",
                 "name": "Bookmarks bar",
                 "type": "folder"
}

roots = {'bookmark_bar': bookmarks_bar,
         'other': other,
         'synced': synced}

# checksum entry is updated by Brave upon loading
filtered = {
    "checksum": "00000000000000000000000000000000",
    "roots": roots,
    "version": 1
}

# Write json list *filtered* to disk
with open(JSONOUT, 'w') as fout:
    json.dump(filtered , fout, sort_keys=True, indent=4, separators=(',', ': '))

