# Name: load.py
# Date: June 2019
# Function: goes trough a bookmark file checking the status of each URL
# Input: bookmark file in json format
# Output: new text and json files including those URLs according with their status

import os

try:
    import requests
except:
    sys.stderr.write("%s: Please install the required module 'requests'.\n" % sys.argv[0])
    sys.exit(1)

try:
    import json
except:
    # Python < 2.6
    try:
        import simplejson as json
    except:
        sys.stderr.write("%s: Please install the required module 'simplejson'.\n" % sys.argv[0])
        sys.exit(1)

DIRNAME = "output"
INFILE = "./chrome_bookmarks.json"
OUTFILE = "output/OK.json"
FILEERROR = "output/error.url"
FILE404 = "output/404.url"

# Read source bookmark file
input_filename = open(INFILE, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Compute number of elements, including categories and end nodes
elements = len(bookmark_data)
print("Checking", str(elements), "entries in bookmark data")

# Create output/ directory if not exists
try:
    os.mkdir(DIRNAME)
    print("Directory" , DIRNAME , "created ") 
except FileExistsError:
    print("Directory" , DIRNAME , "preserved")

# Defining output files
fileError = open(FILEERROR,"w")
fileOK = open(OUTFILE,"w")
file404 = open(FILE404,"w")

fileOK.write("[")

for dict in bookmark_data:
    id = str(dict["id"])
    print(">>>", id)
    if "url" in dict:
# Try here to access that URL
        url = dict["url"]
        try:
            req = requests.head(url, timeout=10)
# Attends all & timeout
        except:
            print(" X ", str(url))
            fileError.write(str(url) + "\n")
        else:
            print(" + ", str(url), end=" ")
            status = req.status_code
            print(str(status))
            if status == 404:
                file404.write(str(url) + "\n")
            else:
### Original json entries should be pasted here
                fileOK.write(str(dict) + ",\n")
# When it is only a bookmark folder
### Original json entries should be pasted here
    else:
        title = dict["title"]
        lastTitle = "[" + title + "]"
        print(lastTitle)
        fileOK.write(str(dict) + ",\n")

fileOK.write("]")

fileError.close()
fileOK.close()
file404.close()

