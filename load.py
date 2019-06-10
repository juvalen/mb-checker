import json
import os
import urllib2

INPUTFILE = "./chrome_bookmarks.json"
OUT404 = "output/404.json"
OUTFILE = "output/filtered.json"

input_filename = open(INPUTFILE, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Compute number of elements, including categories and end nodes
elements = len(bookmark_data)
print "Checking" + str(elements) + "entries in bookmark data"

for dict in bookmark_data:
    print "#  " + str(dict["id"])
    if "url" in dict:
# Try here to access that URL
#        print " U " + str(dict["url"])
        try:
            webUrl = urllib2.urlopen(str(dict["url"]))
        except urllib2.HTTPError:
            print " X " + str(dict["url"]) 
        else:
            result = webUrl.getcode()
            print " + " + str(dict["url"]) + str(result)
# It is only a bookmark folder
    else:
        print "[" + dict["title"] + "]"
# Bookmark is just a folder
