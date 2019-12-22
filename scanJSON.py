#!/usr/bin/python3
# Name: scanJSON.py
# Version: R2
# Date: July 2019
# Function: Parses original chrome Bookmarks file
#           Writes Filtered.url file with (status url) in each line
#           Runs threaded
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

DIRNAME = "output/"
JSONIN = DIRNAME + "Bookmarks"
URLFILTER = DIRNAME + "Filtered.url"

import json
from pprint import pprint
import sys
import http.client, sys
import que
que.urlFilter = open(URLFILTER,"w")

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
    ./scanJSON.py

Files:
    Input 'output/Bookmark' file
    Output 'output/Filtered.url' (status & url) in each line
        """)
        sys.exit()
    else:
        print("""
Usage: ./scanJSON.py

See ./scanJSON.py --help
        """)
        sys.exit()

# Create output/ directory if not exists
try:
    os.mkdir(DIRNAME)
    print("Directory" , DIRNAME , "created ")
except:
    print("Directory" , DIRNAME , "preserved")

# Read source bookmark file
with open(JSONIN, "r", encoding='utf-8') as f:
    Bookmarks = json.load(f)

import que

# Recurrent function
def preorder(tree, depth):
    depth += 1
    if tree:
        width = len(tree)
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
# list element being checked
                    url = item["url"]
                    #print(">>> " + url)
# To paralelize
# Send request to queue
                    que.q.put(url.strip())
    que.q.join()
    return tree

original = Bookmarks['roots']['bookmark_bar']['children']
nodes = preorder(original, 0)
que.urlFilter.close()
