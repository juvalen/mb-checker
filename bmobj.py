#!/usr/bin/python
# Name: bmobj.py
# Date: June 2019
# Function: Parses original chrome Bookmarks file
#
# Input: bookmark file in ./.config/BraveSoftware/Brave-Browser/Default/Bookmarks
#        Bookmarks file structure:
#  {
#     "checksum": "79c9312bbeee61a5710117f00bc16ff8",
#     "roots": {
#        "bookmark_bar": {
#           "children": [ {
#              "date_added": "13187860085000000",
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
#                 'id': '6500',
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
#           "name": "Bookmarks bar",
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

class Url:
    'Contains end bookmark urls'
    count = 0
    def __init__(self, date_added, id, name, url):
        self.date_added = date_added
        self.id = id
        self.name = name
        self.type = "url"
        self.url = url

class Folder:
    'Holds bookmark folders'
    count = 0
    def __init__(self, date_added, date_modified, id, name):
        self.children = {}
        self.date_added = date_added
        self.date_modified = date_modified
        self.id = id
        self.name = name
        self.type = "folder"

DIRNAME = "output/"
JSONIN = DIRNAME + "Bookmarks"
JSONOUT = DIRNAME + "Filtered.json"
URLERROR = DIRNAME + "error.url"
URL404 = DIRNAME + "404.url"
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

# Copy Bookmark list to Filtered list
Filtered = Bookmarks.copy()

#checksum = Bookmarks['checksum']
#roots = Bookmarks['roots']
#version = Bookmarks['version']

# Define output files
urlError = open(URLERROR,"w")
urlOK = open(URLOK,"w")
url404 = open(URL404,"w")

# Recurrent function
def preorder(tree, depth):
    depth += 1
    if tree:
        width = len(tree)
        for i in range(width):
            name = tree[i]["name"]
            title = name.replace('"', '')
            id = tree[i]["id"]
            try:
                branches = len(tree[i]["children"])
                subtree = tree[i]["children"]
                date_added = tree[i]["date_added"]
                date_modified = tree[i]["date_modified"]
                print("[" + str(depth) + "] " + name + " (" + str(branches) + ")")
                BMFolder = Folder(subtree, date_added, date_modified, id, name)
            except:
                branches = 0
            if branches > 0:
                preorder(subtree, depth)
            else:
                type = tree[i]["type"]
                if type == "url":
# list element being checked is i
                    date_added = tree[i]["date_added"]
                    url = tree[i]["url"]
                    print(">>> " + url)
                    print("  T ", name)
                    try:
                        req = requests.head(url, timeout=10)
                    except:
                        print(RED + "  XXX " + id)
                        urlError.write(url + "\n")
                        BMError = Url(date_added, id, name, url)
# Remove from Filtered list also ???
                        #item = tree.pop(i)
                        #pprint(item)
#Filtered['roots']['bookmark_bar']['children'].remove(tree[i])
                        pprint(tree[i])
                        print(NONE, end="")
                        tree.remove(i)
                    else:
                        status = req.status_code
                        if status == 404:
                            print(RED + "  404 " + id)
                            url404.write(url + "\n")
                            BM404 = Url(date_added, id, name, url)
# Remove from Filtered list also ???
                            #item = tree.pop(i)
                            #pprint(item)
#Filtered['roots']['bookmark_bar']['children'].remove(tree[i])
                            print(NONE, end="")
                            tree.remove(i)
                        else:
                            print(" ", status, '+')
                            urlOK.write(url + "\n")
                            BMOK = Url(date_added, id, name, url)
                elif type == "folder":
                    print(GREEN + "  Empty folder" + NONE)
                else:
                    print(BLUE + "   ???" + id + NONE)
            
nodes = Bookmarks['roots']['bookmark_bar']['children']
preorder(nodes, 0)

url404.close()
# Write Filtered list to disk
with open(JSONOUT, 'w') as fout:
    json.dump(Filtered , fout, sort_keys=True, indent=4, separators=(',', ': '))
urlOK.close()
urlError.close()
