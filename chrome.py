# Name: chrome.py
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
#              "children": [ {
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
#              } ]
#           } ]
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

DIRNAME = "output/"
JSONIN = DIRNAME + "Bookmarks"
JSONOUT = DIRNAME + "OK.json"
URLERROR = DIRNAME + "error.url"
URL404 = DIRNAME + "404.url"
URLOK = DIRNAME + "OK.url"

# Create output/ directory if not exists
try:
    os.mkdir(DIRNAME)
    print("Directory" , DIRNAME , "created ") 
except:
    print("Directory" , DIRNAME , "preserved")

RED='\033[0;31m'
NC='\033[0m' # No Color

# Read source bookmark file
with open(JSONIN, "r") as f:
    Bookmarks = json.load(f)

# Define output files
jsonOK = open(JSONOUT,"w")
urlError = open(URLERROR,"w")
urlOK = open(URLOK,"w")
url404 = open(URL404,"w")

def preorder(tree, depth):
    depth += 1
    if tree:
        width = len(tree)
        #print("Checking", str(width), "entries in bookmark data at depth", depth)
        for i in range(width):
            name = tree[i]["name"]
            try:
                branches = len(tree[i]["children"])
                subtree = tree[i]["children"]
                print("[" + str(depth) + "] " + name + " (" + str(branches) + ")")
            except:
                branches = 0
            if branches > 0:
                preorder(subtree, depth)
            
checksum = Bookmarks['checksum']
roots = Bookmarks['roots']
version = Bookmarks['version']

nodes = Bookmarks['roots']['bookmark_bar']['children']
preorder(nodes, 0)

url404.close()
urlOK.close()
urlError.close()
jsonOK.close()

