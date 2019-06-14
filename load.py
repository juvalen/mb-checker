# Name: load.py
# Date: June 2019
# Function: goes trough a bookmark file checking the status of each URL
# Input: bookmark file in json format
# Output: new text and json files including those URLs according with their status

import os
import ast

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

DIRNAME = "output/"
JSONIN = DIRNAME + "chrome_bookmarks.json"
JSONOK = DIRNAME + "OK.json"
URLERROR = DIRNAME + "error.url"
URL404 = DIRNAME + "404.url"
URLOK = DIRNAME + "OK.url"

RED='\033[0;31m'
NC='\033[0m' # No Color

# Read source bookmark file
input_filename = open(JSONIN, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Compute number of elements, including categories and end nodes
elements = len(bookmark_data)
print("Checking", str(elements), "entries in bookmark data")

# Create output/ directory if not exists
try:
    os.mkdir(DIRNAME)
    print("Directory" , DIRNAME , "created ") 
except:
    print("Directory" , DIRNAME , "preserved")

# Defining output files
urlError = open(URLERROR,"w")
jsonOK = open(JSONOK,"w")
urlOK = open(URLOK,"w")
url404 = open(URL404,"w")

jsonOK.write("[")

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
# Tweak title here
    title = string.replace('"', '')
#
    print("@@@@@@@@@@@@", id)
    #print(" L ", dateAddedLocal)
    #print(" U ", dateAddedUTC)
    #print(" I ", index)
    #print(" P ", parentId)
# if there is something in url
    if url:
        print(" T ", title)
# Try here to access that URL
        try:
            try:
                folder = parent[parentId]
            except:
                folder = "1"
            print(" > [", folder, "] ", url)
            req = requests.head(url, timeout=10)
# Attends all & timeout
        except:
            print(RED + "XXX" + NC)
            urlError.write(url + "\n")
        else:
            status = req.status_code
            if status == 404:
                print(RED + "404" + NC)
                url404.write(url + "\n")
            else:
                print(" + ", status)
# Original json entries pasted here
# Approach from scratch
# Write to file
                jsonOK.write('{\n')
                jsonOK.write('    "id": ' + id + ',\n')
                jsonOK.write('    "dateAddedLocal": "' + dateAddedLocal + '",\n')
                jsonOK.write('    "dateAddedUTC": "' + dateAddedUTC + '",\n')
                jsonOK.write('    "index": ' + index + ',\n')
                jsonOK.write('    "parentId": ' + parentId + ',\n')
                jsonOK.write('    "title": "' + title + '",\n')
                jsonOK.write('    "url": "' + url + '"\n')
                if count<elements:
                    jsonOK.write('},\n')
                else:
                    jsonOK.write('}]\n')
                urlOK.write(url + '\n')
# When it is only a bookmark folder
# Original json entries be pasted here
    else:
        lastTitle = "[" + title + "]"
        print(lastTitle)
# Create parent dictionary
        parent = {}
        parent[id] = title
# Write to file
        jsonOK.write('{\n')
        jsonOK.write('    "id": ' + id + ',\n')
        jsonOK.write('    "dateAddedLocal": "' + dateAddedLocal + '",\n')
        jsonOK.write('    "dateAddedUTC": "' + dateAddedUTC + '",\n')
        jsonOK.write('    "index": ' + index + ',\n')
        jsonOK.write('    "parentId": ' + parentId + ',\n')
        jsonOK.write('    "title": "' + title + '"\n')
        if count<elements:
            jsonOK.write('},\n')
        else:
            jsonOK.write('}]\n')
        urlOK.write(url + '\n')
    count += 1

jsonOK.close()
urlError.close()
url404.close()
urlOK.close()

