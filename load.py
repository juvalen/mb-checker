import json
import os

FILENAME = "./chrome_bookmarks.json"

input_filename = open(FILENAME, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

elements = len(bookmark_data)
print(elements,"entries in bookmark_data") 
#print(json.dumps(bookmark_data, sort_keys=True, indent=4))

for i in bookmark_data:
    print('#',i["id"])
    try:
        url = i["url"]
    except NameError:
        print("No url")
    else:
        print(url)

