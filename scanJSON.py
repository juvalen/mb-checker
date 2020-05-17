#!/usr/bin/python3
# Name: scanJSON.py
# Version: R3.3
# Author: jvalentinpastrana at gmail
# Date: May 2020
#
# Usage: ./scanJSON.py [-i input_file]
#
# Function: Parses original chrome Bookmarks file
#           Writes in Filtered.url URLs from:
#            - bookmarks_bar
#            - other
#            - synced
#           tags
#
# Options:
#   input_file: bookmark file (defaults to ~/.config/google-chrome/Default/Bookmarks)
#
# Output: output/Filtered.url
#

DIRNAME = "output/"
URLFILTER = DIRNAME + "Filtered.url"

import json
import os
import argparse
from pprint import pprint
import sys
import http.client
import que
que.urlFilter = open(URLFILTER,"w")
from pathlib import Path
#
# Read input parameters and create corresponding files
parser = argparse.ArgumentParser(prog='./scanJSON.py', description="Tries to reach each Bookmarks entry and stores return code to output/Filtered.url")
parser.add_argument("-i", "--input", dest='input_file', type=str, help="Input bookmark file, defaults to ~/config/google-chrome/Default/Bookmarks", action="store")
args = parser.parse_args()
#
try:
    JSONIN = os.path.expanduser(args.input_file)
except:
    JSONIN = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")
#
# Read input parameters and create corresponding files
errorWatch = []
errorName = []
errorFile = []

# Create output/ directory if not exists
try:
    os.mkdir(DIRNAME)
    print("Directory" , DIRNAME , "created")
except:
    print("Directory" , DIRNAME , "preserved")

# Read source bookmark file
try:
    print("Reading bookmarks from " + JSONIN)
    with open(JSONIN, "r", encoding='utf-8') as f:
        Bookmarks = json.load(f)
except FileNotFoundError:
    print("> Input file " + JSONIN + " not found\n")
    sys.exit()

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

############### Main #######################
original = Bookmarks['roots']['bookmark_bar']['children']
nodes = preorder(original, 0)
original = Bookmarks['roots']['other']['children']
nodes = preorder(original, 0)
original = Bookmarks['roots']['synced']['children']
nodes = preorder(original, 0)

# Closes error#.url files
que.urlFilter.close()
