# Name: genOKurl.py
# Date: June 2019
# Function: reads chrome_bookmarks.json and just generates a URL list in OK.url
# Input: bookmark file in json format
# Output: a file with just the URL

import os
import ast

try:
    import json
except:
    # Python < 2.6
    try:
        import simplejson as json
    except:
        sys.stderr.write("%s: Please install the required module 'simplejson'.\n" % sys.argv[0])
        sys.exit(1)

DIRNAME = "output/"
INFILE = DIRNAME + "chrome_bookmarks.json"
URLOK = DIRNAME + "OK.url"

RED='\033[0;31m'
NC='\033[0m' # No Color

# Read source bookmark file
input_filename = open(INFILE, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Create output/ directory if not exists
try:
    os.mkdir(DIRNAME)
    print("Directory" , DIRNAME , "created ") 
except:
    print("Directory" , DIRNAME , "preserved")

# Defining output files
urlOK = open(URLOK,"w")

count = 1
for dict in bookmark_data:
# Shredding dict into variables
    id = str(dict["id"])
    dateAddedLocal = str(dict["dateAddedLocal"])
    dateAddedUTC = str(dict["dateAddedUTC"])
    index = str(dict["index"])
    parentId = dict["parentId"]
    string = str(dict["title"])
    try:
        url = dict["url"]
    except:
        url = ""
#
    print("@@@@@@@@@@@@", id)
# if there is something in url
    if url:
# Write url to file
        urlOK.write(url + '\n')

urlOK.close()

