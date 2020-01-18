#!/usr/bin/python3
# Name: buildJSON.py
# Version: R3.2
# Author: jvalentinpastrana at gmail
# Date: January 2020
# Function: Reads Filtered.url and Bookmarks and removes URLs not in
#           Filtered.url to Bookmarks.out
#           The strategy is to remove URLs list items as they are processed,
#           so duplicates entries won't be found and will be removed in exception
#           Iterating with while
#           $ ./buildJSON.py -d 404 501 403
#
# Input: bookmark file in ./.config/BraveSoftware/Brave-Browser/Default/Bookmarks
#        File structure:
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
#           "children": [
#                    {
#                       "date_added": "13154093727000000",
#                       "guid": "fe8aac04-a71f-4645-b51e-dcfedddc855b",
#                       "id": "326",
#                       "name": "A Complete Guide to the MultiBit Bitcoin Wallet - Bitzuma",
#                       "type": "url",
#                       "url": "http://bitzuma.com/posts/a-complete-guide-to-the-multibit-bitcoin-wallet/"
#                    } ],
#           "date_added": "13198974830951405",
#           "date_modified": "13200950919336220",
#           "id": "2984",
#           "name": "Other bookmarks",
#           "type": "folder"
#        }
#        "synced": {
#           "children": [
#                    {
#                       "date_added": "13154093728000000",
#                       "guid": "49dc5d73-1001-4aed-a3d9-2fbc4cc39f62",
#                       "id": "335",
#                       "name": "(293,52EUR) RBEX buy and sell bitcoin",
#                       "type": "url",
#                       "url": "https://www.rbex.eu/"
#                    } ],
#           "date_added": "13198974830951420",
#           "date_modified": "0",
#           "id": "2985",
#           "name": "Mobile bookmarks",
#           "type": "folder"
#        }
#     }
#    "version": 1
#  }
#
# Output:

DELETEFOLDER = 1
DIRNAME = "output/"
URLIN = DIRNAME + "Filtered.url"
URLXXX = DIRNAME + "XXX.url"
URLDDD = DIRNAME + "DDD.url"
BOOK = DIRNAME + "Bookmarks"
JSONOUT = DIRNAME + "Bookmarks.out"

import json
from pprint import pprint
import sys
import http.client, sys
from que import *

# Read input parameters and create corresponding files
params = sys.argv[1:]
nparams = len(sys.argv)

errorWatch = []
errorVarName = []
errorFile = []
if nparams > 1:
    if params[0] == '--help':
        print("""
Usage:
    ./buildJSON.py <code1> <code2> <code3>

Parameters:
    http return <code> to be removed from filtered file . Code range [100..999].

Files:
    Input files 'output/Filtered.url' and 'output/Bookmarks'
    Output file will be written to 'output/Bookmarks.out'
        """)
        sys.exit()
    elif  not  params[0].isdigit():
        print("""
Error: code is not a valid number

See ./buildJSON.py --help
        """)
        sys.exit()
if nparams == 1:
    print("""
Usage: ./buildJSON.py <code1> <code2> <code3>
       ./buildJSON.py --help
    """)
    sys.exit()

# Parameter parsing
for param in params:
    if param.isdigit():
        iparam = int(param)
        if iparam > 99 and iparam < 1000:
            errorWatch.append(param)
            errorVarName.append("URL" + param)
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
    print("Directory" , DIRNAME , "didin't exist. Aborting.")
    sys.exit()
except:
    print("Directory" , DIRNAME , "Preserved.")

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
NONE = '\033[0m' # No Color

# Read source Bookmark file
with open(BOOK, "r") as f:
    Bookmarks = json.load(f)
f.close
# Read Filtered.url to code & entry lists
code = []
entry = []
nline = 0
f = open(URLIN, "r")
line = f.readline()
while line:
    nline += 1
    status, url = line.split(" ")
    url = url.strip('\n')
    code.append(status)
    entry.append(url)
    line = f.readline()
f.close

# Create output files
# For network error
urlXXX = open(URLXXX,"w")
for i in range(0, nparams-1):
    errorVarName[i] = open(errorFile[i], "w")
    print("Created", errorFile[i])
print()
# For duplicated bookmark
urlDDD = open(URLDDD,"w")

#Create dictionay of URLs
dictURL = dict((e, i) for i, e in enumerate(entry))

# Traverse the json tree and remove entries depending on its code in Filtered.url
def preorder(tree, depth):
    depth += 1
    if tree:
        numitems = len(tree)
# i: counter within folder
        i = d = 0
# This iteration fails when element is popped
# Tree should be copied to a new json
        while i < numitems:
            item = tree[i]
            name = item["name"]
            try:
                branches = len(item["children"])
                subtree = item["children"]
                print("[" + str(depth) + "] " + name + " (" + str(branches) + ")")
            except:
                branches = 0
            if branches > 0:
                preorder(subtree, depth)
                print()
            else:
                type = item["type"]
                id = item["id"]
                if type == "url":
# list element being checked is i
                    date_added = item["date_added"]
                    url = item["url"]
                    print(">>> " + url)
# Check status code of that URL in Filtered.url
#try:
#    ind = dictURL[url]
#    ...
#    remove from dictURL & code lists
#except:
#    it is duplicated, remove item from tree
                    ind = dictURL[url]
                    status = code[ind]
                    if status == "XXX":
                        print(RED + "  " + status + " " + id + " #" + str(i))
                        urlXXX.write(url + "\n")
                        ret = tree.pop(i); i -= 1; numitems -= 1
                        print(NONE, end="")
                    elif status in errorWatch:
                        pos = errorWatch.index(status)
                        f = errorVarName[pos]
                        print(RED + "  " + status + " " + id + " #" + str(i))
                        f.write(url + "\n")
                        ret = tree.pop(i); i -= 1; numitems -= 1
                        print(NONE, end="")
                    else: # looked for code not in list, entry remains
                        print(" ", status, '+' + " #" + str(i))
# Check status code of that URL in Filtered.url
                elif type == "folder":
                    print(GREEN + "  Empty folder" + NONE)
                    if DELETEFOLDER:
                        ret = tree.pop(i); i -= 1; numitems -= 1
                else:
                    print(BLUE + "   ???" + id + NONE)
            i += 1
            #d += 1
    return tree

# JSON structure
original = Bookmarks['roots']['other']['children']
nodes = preorder(original, 0)
other = {
    "children": nodes,
    "date_added": "13198974830951405",
    "date_modified": "13200950919336220",
    "id": "2",
    "name": "Other bookmarks",
    "type": "folder"
}

original = Bookmarks['roots']['synced']['children']
nodes = preorder(original, 0)
synced = {
    "children": nodes,
    "date_added": "13198974830951420",
    "date_modified": "0",
    "id": "3",
    "name": "Mobile bookmarks",
    "type": "folder"
}

original = Bookmarks['roots']['bookmark_bar']['children']
nodes = preorder(original, 0)
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
    json.dump(filtered , fout, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))

