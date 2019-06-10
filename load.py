import json
import os

FILENAME = "./chrome_bookmarks.json"

input_filename = open(FILENAME, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Compute number of elements, including categories and end nodes
elements = len(bookmark_data)
print(elements,"entries in bookmark_data") 
#print(json.dumps(bookmark_data, sort_keys=True, indent=4))

for dict in bookmark_data:
    print('#',dict["id"], end="")
    if "url" in dict:
        print(' ->',dict["url"])
    else:
        print(':',dict["title"])

