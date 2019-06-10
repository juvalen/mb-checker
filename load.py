import json
import os
import requests

INPUTFILE = "./chrome_bookmarks.json"
OUT404 = "output/404.json"
OUTFILE = "output/filtered.json"

input_filename = open(INPUTFILE, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Compute number of elements, including categories and end nodes
elements = len(bookmark_data)
print("Checking", elements, "entries in bookmark data") 
#print(json.dumps(bookmark_data, sort_keys=True, indent=4))

for dict in bookmark_data:
    print('#', dict["id"], end="")
    if "url" in dict:
# Try here to access that URL
        print(' ->', dict["url"], end=": ")
        req = requests.get(dict["url"])
        print(req.status_code)
# It is only a bookmark folder
    else:
        print(':', dict["title"])
