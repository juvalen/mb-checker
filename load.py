import json
import os
import urllib2

INPUTFILE = "./chrome_bookmarks.json"
FILEERROR = "output/error.log"
FILEREACHABLE = "output/reachable.log"

input_filename = open(INPUTFILE, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Compute number of elements, including categories and end nodes
elements = len(bookmark_data)
print "Checking" + str(elements) + "entries in bookmark data"

# Defining output files
fileError = open(FILEERROR,"w")
fileReachable = open(FILEREACHABLE,"w")

for dict in bookmark_data:
    print "#  " + str(dict["id"])
    if "url" in dict:
# Try here to access that URL
#        print " U " + str(dict["url"])
        try:
            webUrl = urllib2.urlopen(str(dict["url"]))
        except urllib2.HTTPError:
            print " X " + str(dict["url"]) 
            fileError.write(lastTitle) 
            fileError.write(str(dict["url"]))
        else:
            result = webUrl.getcode()
            print " + " + webUrl.url + " " + str(result)
            fileReachable.write(str(dict["url"]))
            webUrl.close()
# It is only a bookmark folder
    else:
        lastTitle = "[" + dict["title"] + "]"
        print lastTitle
        fileReachable.write(lastTitle) 
# Bookmark is just a folder
