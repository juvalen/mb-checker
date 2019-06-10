import json
import os
import urllib2

INPUTFILE = "./chrome_bookmarks.json"
FILEURLERROR = "output/URLerror.log"
FILEHTTPERROR = "output/HTTPerror.log"
FILEREACHABLE = "output/reachable.log"

input_filename = open(INPUTFILE, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Compute number of elements, including categories and end nodes
elements = len(bookmark_data)
print "Checking" + str(elements) + "entries in bookmark data"

# Defining output files
fileURLError = open(FILEURLERROR,"w")
fileHTTPError = open(FILEHTTPERROR,"w")
fileReachable = open(FILEREACHABLE,"w")

for dict in bookmark_data:
    print ">  " + str(dict["id"])
    if "url" in dict:
# Try here to access that URL
#        print " U " + str(dict["url"])
        try:
            webUrl = urllib2.urlopen(str(dict["url"]))
        except urllib2.HTTPError:
            print " X " + str(dict["url"]) 
            fileHTTPError.write(lastTitle + "\n")
            fileHTTPError.write(str(dict["url"]) + "\n")
        except urllib2.URLError:
            print " X " + str(dict["url"] + "\n") 
            fileURLError.write(lastTitle + "\n") 
            fileURLError.write(str(dict["url"]) + "\n")
        else:
            result = webUrl.getcode()
            print " + " + webUrl.url + " " + str(result)
            fileReachable.write(str(dict["url"]) + "\n")
            webUrl.close()
# It is only a bookmark folder
    else:
        lastTitle = "[" + dict["title"] + "]"
        print  "\n" + lastTitle
        fileReachable.write("\n" + lastTitle) 
# Bookmark is just a folder

fileError.close()
fileReachable.close()
