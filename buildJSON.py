#!/usr/bin/python3
# Name: buildJSON.py
# Version: R3.3
# Author: jvalentinpastrana at gmail
# Date: April 2020
#
# Usage: ./buildJSON [-d] [-f] <code1> <code2> <code3>...
#
# Function: Reads Filtered.url and Bookmarks and removes URLs not in
#           Filtered.url to Bookmarks.out
#           The strategy is to remove URLs list items as they are processed,
#           so duplicates entries won't be found and will be removed in exception
#           Iterating with while
#           Uses argparse
#
# Input: output/Bookmarks
#        output/Filtered.url
#
# Output: XXX.url
#         DDD.url
#         <code>.url
#         Bookmarks.out

DELETEFOLDERS = 0 # Delete folder if empty
DELETEDUPLICATES = 0 # Delete duplicated entries
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
import argparse

# Read input parameters and create corresponding files
parser = argparse.ArgumentParser(prog='./buildJSON.py', description="Reads Filtered.url and Bookmarks and removes specified return codes to Bookmarks.out")
parser.add_argument("-d", "--duplicates", dest='DELETEDUPLICATES', help="remove duplicated bookmarks", action="store_true")
parser.add_argument("-f", "--folders", dest='DELETEFOLDERS', help="remove empty folders", action="store_true")
parser.add_argument('params', metavar='code', type=int, nargs='+', help='http return code to be filtered', action='append')
args = parser.parse_args()
params = args.params[0]

nparams = len(params)

errorWatch = []
errorVarName = []
errorFile = []

# Parameter parsing
for iparam in params:
    if iparam > 99 and iparam < 1000:
        errorWatch.append(str(iparam))
        errorVarName.append("URL" + str(iparam))
        errorFile.append(DIRNAME + str(iparam) + '.url')
    else:
        print("Error: return code", iparam, "is out of bounds [100..999]\n")
        sys.exit()

# Parameter parsing
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
# Read Filtered.url to entry & code lists
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
#Create dictionay of URLs from entry & code
pairs = dict(zip(entry, code))

# Create output files
# For network error
urlXXX = open(URLXXX,"w")
for i in range(0, nparams):
    errorVarName[i] = open(errorFile[i], "w")
    print("Created", errorFile[i])
print()
# For duplicated bookmark
urlDDD = open(URLDDD,"w")

# Traverse the json tree and remove entries depending on its code in Filtered.url
def preorder(tree, depth):
    depth += 1
    if tree:
        numitems = len(tree)
# i: counter within folder
        i = 0
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
# Check status code of that URL in pairs
                    try:
                        status = pairs[url]
# Deleted, so next time won't be found => duplicated
                        if DELETEDUPLICATES == 1:
                            del pairs[url]
                        if status == "XXX":
                            print(RED + "    " + status + " " + id)
                            urlXXX.write(url + "\n")
                            tree.pop(i); i -= 1; numitems -= 1
                            print(NONE, end="")
                        elif status in errorWatch:
                            pos = errorWatch.index(status)
                            f = errorVarName[pos]
                            print(RED + "    " + status + " " + id)
                            f.write(url + "\n")
                            tree.pop(i); i -= 1; numitems -= 1
                            print(NONE, end="")
                        else: # looked for code not in list, entry remains
                            print("    " + status, '+')
                    except:
                        status = "DDD"
                        print(BLUE + "    " + status + " " + id)
                        urlDDD.write(url + "\n")
                        tree.pop(i); i -= 1; numitems -= 1
                        print(NONE, end="")
#
                elif type == "folder":
                    print(GREEN + "  Empty folder" + NONE)
                    if DELETEFOLDERS:
                        ret = tree.pop(i); i -= 1; numitems -= 1
                else:
                    print(BLUE + "   ???" + id + NONE)
            i += 1
        print()
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
