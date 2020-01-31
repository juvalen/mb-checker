#!/usr/bin/python3
# Name: scanJSON.py
# Version: R3.2
# Author: jvalentinpastrana at gmail
# Date: January 2020
#
# Usage: ./scanJSON.py
#
# Function: Parses original chrome Bookmarks file
#           Writes in Filtered.url URLs from:
#            - bookmarks_bar
#            - other
#            - synced
#           tags
#
# Input: bookmark file in output/Bookmarks
#        copied from ~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks
#        See file structure in output/format
#
# Output: output/Filtered.url

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
# To paralelize
# Send request to queue
                    que.q.put(url.strip())
    que.q.join()
    return tree

original = Bookmarks['roots']['bookmark_bar']['children']
nodes = preorder(original, 0)
original = Bookmarks['roots']['other']['children']
nodes = preorder(original, 0)
original = Bookmarks['roots']['synced']['children']
nodes = preorder(original, 0)

# Closes error#.url files
que.urlFilter.close()
