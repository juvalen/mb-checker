#!/usr/bin/python3
# Name: scanJSON.py
# Version: R3.9
# Author: jvalentinpastrana at gmail
# Date: Jan 2021
#
# Usage: ./scanJSON.py [-w work_dir] [-i input_file]
#
# Function: Parses original chrome Bookmarks file
#           Writes in ALL.url URLs from:
#            - bookmarks_bar
#            - other
#            - synced
#           tags
#
# Options:
#   input_file: bookmark file (defaults to ~/.config/google-chrome/Default/Bookmarks)
#   work_dir: output directory (defaults to ./work_dir/)
#
# Output: <work_dir>/ALL.url
#
import json
import os
import argparse
import sys
import que

# Read input parameters and create corresponding files
parser = argparse.ArgumentParser(prog='./scanJSON.py',
                                 description="Reaches each Bookmark entry and stores return code to <work_dir>/ALL.url")
parser.add_argument("-w", "--work-dir", dest='work_dir', type=str, help="Output directory, defaults to ./work_dir/",
                    action="store")
parser.add_argument("-i", "--input", dest='input_file', type=str,
                    help="Input bookmark file, defaults to ~/.config/google-chrome/Default/Bookmarks", action="store")
args = parser.parse_args()
#
try:
    JSONIN = os.path.expanduser(args.input_file)
except:
    JSONIN = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")
print("Reading bookmarks from " + JSONIN)
try:
    work_dir = os.path.expanduser(args.work_dir) + "/"
except:
    work_dir = os.path.expanduser("./work_dir/")

# Read input parameters and create corresponding files
errorWatch = []
errorName = []
errorFile = []
URLFILTER = work_dir + "ALL.url"

# Create <work_dir> directory if not exists
try:
    os.mkdir(work_dir)
    print("Output directory", work_dir, "created")
except:
    print("Output directory", work_dir, "preserved")
que.urlFilter = open(URLFILTER, "w")

# Read source bookmark file
try:
    with open(JSONIN, "r", encoding='utf-8') as f:
        Bookmarks = json.load(f)
except FileNotFoundError:
    print("> Input file ", JSONIN, " not found\n")
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
                if type == "url":
                    # list element being checked
                    url = item["url"]
                    # To parallelize
                    # Send request to queue
                    que.q.put(url.strip())
    que.q.join()
    return tree


# Main #####################################
print("[0] Bar")
original = Bookmarks['roots']['bookmark_bar']['children']
preorder(original, 0)
print("[0] Other")
original = Bookmarks['roots']['other']['children']
preorder(original, 0)
print("[0] Synced")
original = Bookmarks['roots']['synced']['children']
preorder(original, 0)

# Closes error#.url files
que.urlFilter.close()

print("Writing scan to " + work_dir)
