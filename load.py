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
INFILE = DIRNAME + "chrome_bookmarks.json"
OUTFILE = DIRNAME + "OK.json"
FILEERROR = DIRNAME + "error.url"
FILE404 = DIRNAME + "404.url"

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

fileOK.write("[\n")

count = 0
for dict in bookmark_data:
# Shredding dict into variables
    id = str(dict["id"])
    dateAddedLocal = str(dict["dateAddedLocal"])
    dateAddedUTC = str(dict["dateAddedUTC"])
    index = str(dict["index"])
    parentId = dict["parentId"]
    title = str(dict["title"])
    try:
        url = dict["url"]
    except:
        url = ""
# Tweak title here
#
    print("@@@@@@@@@", id)
    #print(" L ", dateAddedLocal)
    #print(" U ", dateAddedUTC)
    #print(" I ", index)
    #print(" P ", parentId)
    print(" T ", title)
# if there is something in url
    if url:
# Try here to access that URL
        try:
            folder = parent[parentId]
            print(" > [", folder, "] ", url)
            req = requests.head(url, timeout=10)
# Attends all & timeout
        except:
            print("XXX")
            fileError.write(url + "\n")
        else:
            status = req.status_code
            if status == 404:
                print(" 4 ")
                file404.write(url + "\n")
            else:
                print(" + ", status)
# Original json entries pasted here
# Approach from scratch
# Write to file
                fileOK.write('{\n')
                fileOK.write('    "id" = "' + id + '",\n')
                fileOK.write('    "dateAddedLocal" = "' + dateAddedLocal + '",\n')
                fileOK.write('    "dateAddedUTC" = "' + dateAddedUTC + '",\n')
                fileOK.write('    "index" = "' + index + '",\n')
                fileOK.write('    "parentId" = "' + parentId + '",\n')
                fileOK.write('    "title" = "' + title + '"\n')
                fileOK.write('    "url" = "' + url + '"\n')
                fileOK.write('},\n')
# When it is only a bookmark folder
# Original json entries be pasted here
    else:
        lastTitle = "[" + title + "]"
        print(lastTitle)
# Create parent dictionary
        parent = {}
        parent[id] = title
# Write to file
        fileOK.write('{\n')
        fileOK.write('    "id" = "' + id + '",\n')
        fileOK.write('    "dateAddedLocal" = "' + dateAddedLocal + '",\n')
        fileOK.write('    "dateAddedUTC" = "' + dateAddedUTC + '",\n')
        fileOK.write('    "index" = "' + index + '",\n')
        fileOK.write('    "parentId" = "' + parentId + '",\n')
        fileOK.write('    "title" = "' + title + '"\n')
        fileOK.write('},\n')
        #dquotes = str(eval(dquotes))
        #dquotes = dquotes.replace('\\x', '\\u00')
        #dquotes = dquotes.replace('\\"', '')
        #dquotes = dquotes.replace("\\'", "'")
        #dquotes = dquotes.replace("{'", '{"')
        #dquotes = dquotes.replace(" '", ' "')
        #dquotes = dquotes.replace("':", '":')
        #dquotes = dquotes.replace("',", '",')
        #dquotes = dquotes.replace("'}", '"}')
    count += 1

fileOK.write("]\n")

fileError.close()
fileOK.close()
file404.close()

