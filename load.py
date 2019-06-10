import json
import os
import requests

INPUTFILE = "./chrome_bookmarks.json"
FILEURLERROR = "output/URLerror.log"
FILEHTTPERROR = "output/HTTPerror.log"
FILEREACHABLE = "output/reachable.log"

input_filename = open(INPUTFILE, "r")
bookmark_data = json.load(input_filename)
input_filename.close()

# Compute number of elements, including categories and end nodes
elements = len(bookmark_data)
print("Checking" + str(elements) + "entries in bookmark data")

# Defining output files
fileURLError = open(FILEURLERROR,"w")
fileHTTPError = open(FILEHTTPERROR,"w")
fileReachable = open(FILEREACHABLE,"w")

for dict in bookmark_data:
    print(">  " + str(dict["id"]))
    if "url" in dict:
# Try here to access that URL
        print(' + ', dict["url"], end=" ")
        try:
            req = requests.get(dict["url"])
        except req.HTTPError:
            print(" H " + str(dict["url"]))
            fileHTTPError.write(lastTitle + "\n")
            fileHTTPError.write(str(dict["url"]) + "\n")
        except req.URLError:
            print(" X " + str(dict["url"]) + "\n")
            fileURLError.write(lastTitle + "\n") 
            fileURLError.write(str(dict["url"]) + "\n")
        except req.ConnectionRefusedError:
            print(" U " + str(dict["url"]) + "\n")
            fileReachable.write(lastTitle + "\n") 
            fileReachable.write(str(dict["url"]) + "\n")
        else:
            status = req.status_code
            print(str(status))
# When it is only a bookmark folder
    else:
        lastTitle = "[" + dict["title"] + "]"
        print(lastTitle)
        fileReachable.write(lastTitle) 

fileError.close()
fileReachable.close()
