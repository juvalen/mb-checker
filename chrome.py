#!/usr/bin/python
# Name: chrome.py
# Date: June 2019
# Function: Parses original chrome Bookmarks file
#           Tries to reach each URL and removes it on error
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

DELETEFOLDER = 0

DIRNAME = "output/"
JSONIN = DIRNAME + "Bookmarks"
JSONOUT = DIRNAME + "Filtered.json"
#NODEOUT = DIRNAME + "Nodes.json"
URLERROR = DIRNAME + "error.url"
URL404 = DIRNAME + "404.url"
URL500 = DIRNAME + "500.url"
URLOK = DIRNAME + "OK.url"

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

# Define output files
urlError = open(URLERROR,"w")
urlOK = open(URLOK,"w")
url404 = open(URL404,"w")
url500 = open(URL500,"w")

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
                    print("  N ", name)
                    try:
                        req = requests.head(url, timeout=10)
                    except:
                        print(RED + "  XXX " + id + " #" + str(i))
                        urlError.write(url + "\n")
                        ret = tree.pop(d); d -= 1
                        print(NONE, end="")
                    else:
                        status = req.status_code
                        if status == 404:
                            print(RED + "  404 " + id + " #" + str(i))
                            url404.write(url + "\n")
                            ret = tree.pop(d); d -= 1
                            print(NONE, end="")
                        elif status >= 500:
                            print(RED + "  500 " + id + " #" + str(i))
                            url500.write(url + "\n")
                            ret = tree.pop(d); d -= 1
                            print(NONE, end="")
                        else:
                            print(" ", status, '+' + " #" + str(i))
                            urlOK.write(url + "\n")
                elif type == "folder":
                    print(GREEN + "  Empty folder" + NONE + "\n")
                    if DELETEFOLDER:
                        ret = tree.pop(d); d -= 1
                else:
                    print(BLUE + "   ???" + id + NONE + "\n")
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

