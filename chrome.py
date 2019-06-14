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

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
NC = '\033[0m' # No Color

# Read source bookmark file
with open(JSONIN, "r") as f:
    Bookmarks = json.load(f)

# Copy Bookmark list to Filtered list

############## delete from list
#for i, o in enumerate(obj_list):
#    if o.attr == known_value:
#        del obj_list[i]
#        break
#
############## remove() method
# x = open_list.pop(min_index) 
# node_list.remove(x)
#
# try:
#     node_list.remove(x)
# except:
#     pass
#

#checksum = Bookmarks['checksum']
#roots = Bookmarks['roots']
#version = Bookmarks['version']

# Define output files
jsonOK = open(JSONOUT,"w")
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
            try:
                branches = len(tree[i]["children"])
                subtree = tree[i]["children"]
                print("[" + str(depth) + "] " + name + " (" + str(branches) + ")")
            except:
                branches = 0
            if branches > 0:
                preorder(subtree, depth)
            else:
                type = tree[i]["type"]
                if type == "url":
                    id = tree[i]["id"]
# pop the list element
                    date_added = tree[i]["date_added"]
                    string = tree[i]["name"]
                    title = string.replace('"', '')
                    url = tree[i]["url"]
                    print(">>> " + url)
                    print("  T ", name)
                    try:
                        req = requests.head(url, timeout=10)
                    except:
                        print(RED + "  XXX " + id + NC)
                        urlError.write(url + "\n")
# Remove from Filtered list also
                    else:
                        status = req.status_code
                        if status == 404:
                            print(RED + "  404 " + id + NC)
                            url404.write(url + "\n")
# Remove from Filtered list also
                        else:
                            print(" ", status, '+')
                            urlOK.write(url + "\n")
                elif type == "folder":
                    print(GREEN + "  Empty folder" + NC)
                else:
                    print(BLUE + "   ???" + id + NC)
            
nodes = Bookmarks['roots']['bookmark_bar']['children']
preorder(nodes, 0)

url404.close()
# Write Filtered list to disk
urlOK.close()
urlError.close()
jsonOK.close()

