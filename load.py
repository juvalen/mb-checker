import json
import os
import requests

DIRNAME = "output"
INPUTFILE = "./chrome_bookmarks.json"
FILEERROR = "output/error.log"
FILEOK = "output/OK.log"
FILE404 = "output/404.log"

input_filename = open(INPUTFILE, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Compute number of elements, including categories and end nodes
elements = len(bookmark_data)
print("Checking ", str(elements), " entries in bookmark data")

# Create output/ directory if not exists
try:
    os.mkdir(DIRNAME)
    print("Directory" , DIRNAME , "created ") 
except FileExistsError:
    print("Directory " , DIRNAME , " preserved")

# Defining output files
fileError = open(FILEERROR,"w")
fileOK = open(FILEOK,"w")
file404 = open(FILE404,"w")

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
                fileOK.write(str(url) + "\n")
# When it is only a bookmark folder
### Original json entries should be pasted here
    else:
        title = dict["title"]
        lastTitle = "[" + title + "]"
        print(lastTitle)
        fileOK.write(lastTitle + "\n") 

fileError.close()
fileOK.close()
