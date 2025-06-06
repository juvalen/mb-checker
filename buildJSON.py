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
number_of_params = len(params)
#
try:
    jsonin = os.path.expanduser(args.input_file)
except:
    jsonin = os.path.expanduser("Bookmarks")
print(f"Using bookmarks name {jsonin}")

try:
    work_dir = os.path.expanduser(args.work_dir) + "/"
except:
    work_dir = "./work_dir/"
print(f"Reading scan results from {work_dir}")
#
DELETEFOLDERS = args.DELETEFOLDERS
URLIN = work_dir + "ALL.url"
URLXXX = work_dir + "XXX.url"
URLEEE = work_dir + "Empty_folders.lst"
jsonout = work_dir + "Bookmarks.out"

error_watch = []
error_var_name = []
errorFile = []

# parsing http codes in params
if number_of_params:
    for iparam in params:
        if re.match("[0-9.]{3}", iparam):
            error_watch.append(iparam)
            error_var_name.append("URL" + iparam)
            errorFile.append(work_dir + iparam + '.url')
        else:
            print("  Error: return code", iparam, "malformed, should contain three digits or dots\n")
            sys.exit()
else:
    print("Code list is empty, return codes will be just classified to files")
    for f in glob.glob(work_dir + "[0-9][0-9][0-9].url"):
        os.remove(f)

# ASCII color codes
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
NONE = '\033[0m' # No Color

# Read source bookmark file (paramater, Bookmarks, /data/Bookmarks)
try:
    print("> Trying input file", jsonin, "\n")
    with open(jsonin, "r", encoding='utf-8') as f:
        Bookmarks = json.load(f)
except FileNotFoundError:
    try:
        print(">", jsonin, "not found, looking for /tmp/Bookmarks\n")
        jsonin = "/tmp/Bookmarks"
        with open(jsonin, "r", encoding='utf-8') as f:
            Bookmarks = json.load(f)
    except FileNotFoundError:
        print("> Input file", jsonin, "not found either /tmp\n")
        sys.exit()
f.close()

# Read ALL.url to entry & code lists
print("Read ", URLIN, "\n")
code = []
entry = []
try:
    f = open(URLIN, "r")
except:
    print("Error: ", URLIN, "not found\n")
    sys.exit()
for line in f:
    line = line.strip('\n')
    status, url = line.split(" ")
    code.append(status)
    entry.append(url)
f.close()
# Create dictionay of URLs from entry & code
pairs = dict(zip(entry, code))

# Create output files for network error
urlXXX = open(URLXXX,"w")
for i in range(0, number_of_params):
    error_var_name[i] = open(errorFile[i], "w")
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
                print(f"[{depth}] {name} ({branches})")
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
                    combined = "(" + ")|(".join(error_watch) + ")"
# Deleted, so next time won't be found => duplicated
                    if status == "XXX":
                        print(RED + "    " + status + " " + id)
                        urlXXX.write(url + "\n")
                        tree.pop(i); i -= 1; numitems -= 1
                        print(NONE, end="")
                    if number_of_params:
# Check status code of that URL in pairs
                        try:
                            if re.match(combined, status): # look if some codes to be filtered match the actual status
                                for http_code in error_watch:
                                    if re.match(http_code, status):
                                        pos = error_watch.index(http_code)
                                        f = error_var_name[pos]
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
with open(jsonout, 'w') as fout:
    json.dump(filtered , fout, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
