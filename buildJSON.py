#!/usr/bin/python3
# Name: buildJSON.py
# Version: R4.1
# Author: jvalentinpastrana at gmail
# Date: Dec 2022
#
# Usage: ./buildJSON [-w work_dir] [-i input_file] [-e] <code1> <code2> <code3>...
#
# Function: Reads ALL.url and original input Bookmarks file and removes entries returning
#           any of <codeN> to Bookmarks.out
#           The strategy is to remove URLs list items as they are processed,
#           so duplicates entries won't be found and will be removed in exception
#           Iterating with while
#           Uses argparse
#
# Input:
#        input_file, Bookmarks
#        work_dir, where **ALL.url** will be stored
#
# Output files in working_directory: 
#         XXX.url
#         Empty_folders.lst
#         <code>.url
#         Bookmarks.out

import json
import os, glob
import re
import sys
import argparse

# Read input parameters and create corresponding files
parser = argparse.ArgumentParser(prog='./buildJSON.py', description="Reads ALL.url and Bookmarks to removes specific return codes to Bookmarks.out")
parser.add_argument("-w", "--work-dir", dest='work_dir', help="Working directory, defaults to ./work_dir/", action="store")
parser.add_argument("-i", "--input", dest='input_file', type=str, help="Input bookmark file, defaults to ~/Bookmarks", action="store")
parser.add_argument("-e", "--empty", dest='DELETEFOLDERS', help="remove empty folders", action="store_true")
parser.add_argument('params', metavar='code', type=str, nargs='*', help='http return code to be filtered, if none only classifies', action='append')
args = parser.parse_args()
params = args.params[0]
nparams = len(params)
try:
    work_dir = os.path.expanduser(args.work_dir) + "/"
except:
    work_dir = "./work_dir/"
print("Reading scan results from", work_dir)
try:
    input_file = os.path.expanduser(args.input_file)
except:
    input_file = os.path.expanduser("Bookmarks")
print("Reading bookmarks from", input_file)
#
DELETEFOLDERS = args.DELETEFOLDERS
URLIN = work_dir + "ALL.url"
URLXXX = work_dir + "XXX.url"
URLEEE = work_dir + "Empty_folders.lst"
JSONOUT = work_dir + "Bookmarks.out"

errorWatch = []
errorVarName = []
errorFile = []

# parsing http codes in params
if nparams:
    for iparam in params:
        if re.match("[0-9.]{3}", iparam):
            errorWatch.append(iparam)
            errorVarName.append("URL" + iparam)
            errorFile.append(work_dir + iparam + '.url')
        else:
            print("  Error: return code", iparam, "malformed, should contain three digits or dots\n")
            sys.exit()
else:
    print("Code list is empty, return codes will be kust classified to files")
    for f in glob.glob(work_dir + "[0-9][0-9][0-9].url"):
        os.remove(f)

# ASCII color codes
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
NONE = '\033[0m' # No Color

# Read source Bookmark file
with open(input_file, "r") as f:
    Bookmarks = json.load(f)
f.close()
# Read ALL.url to entry & code lists
code = []
entry = []
nline = 0
try:
    f = open(URLIN, "r")
except:
    print("Error: ", URLIN, "not found\n")
    sys.exit()
line = f.readline()
while line:
    print(line)
    nline += 1
    status, url = line.split(" ")
    url = url.strip('\n')
    code.append(status)
    entry.append(url)
    line = f.readline()
f.close()
# Create dictionay of URLs from entry & code
pairs = dict(zip(entry, code))

# Create output files
# For network error
urlXXX = open(URLXXX,"w")
for i in range(0, nparams):
    errorVarName[i] = open(errorFile[i], "w")
    print("Created", errorFile[i])
print()
# For duplicated bookmark
urlEEE = open(URLEEE,"w")

# Traverse the json tree and remove entries with its code in ALL.url
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
                    status = pairs[url]
                    combined = "(" + ")|(".join(errorWatch) + ")"
# Deleted, so next time won't be found => duplicated
                    if status == "XXX":
                        print(RED + "    " + status + " " + id)
                        urlXXX.write(url + "\n")
                        tree.pop(i); i -= 1; numitems -= 1
                        print(NONE, end="")
                    if nparams:
# Check status code of that URL in pairs
                        try:
                            if re.match(combined, status): # look if some codes to be filtered match the actual status
                                for http_code in errorWatch:
                                    if re.match(http_code, status):
                                        pos = errorWatch.index(http_code)
                                        f = errorVarName[pos]
                                        print(RED + "    " + status + " " + id)
                                        f.write(url + "\n")
                                        tree.pop(i); i -= 1; numitems -= 1
                                        print(NONE, end="")
                            else: # looked up code not in list, entry remains
                                print("    " + status, '+')
                        except:
                            pass
                    else:
# No return codes were specified
                        if status != "XXX":
                            status = pairs[url]
                            ef = work_dir + status + '.url'
                            ev = open(ef, "a+")
                            print(GREEN + "    " + status + " " + id)
                            ev.write(url + "\n")
                            ev.close()
                            print(NONE, end="")
                elif type == "folder":
                    print(BLUE + "    EEE " + id, end="")
                    urlEEE.write("[" + str(depth) + "] " + name + " (" + str(branches) + ")\n")
                    if DELETEFOLDERS:
                        tree.pop(i); i -= 1; numitems -= 1
                        print(RED + " Deleted ")
                    print(NONE)
                else:
                    print(BLUE + "   ???" + id + NONE)
            i += 1
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
