#!/usr/bin/python3
# Name: params.py
# Version: R1.30
# Date: July 2019
# Function: Parses original chrome Bookmarks file
#           Tries to reach each URL and removes it on error
#           Accepts return codes as parameters
#           $ python chrome.py 404 5xx 403
#

import json
from pprint import pprint
import sys
import requests

DELETEFOLDER = 0
DIRNAME = "../output/"
JSONIN = DIRNAME + "Bookmarks"
JSONOUT = DIRNAME + "Filtered.json"
URLXXX = DIRNAME + "XXX.url"
URLOK = DIRNAME + "OK.url"

# Read input parameters and create corresponding files
params = sys.argv
nparams = len(sys.argv)

errorNum = []
fileName = []
for param in params:
    errorNum.append("URL" + param)
    fileName.append(DIRNAME + param + '.url')
 
pprint(errorNum)
pprint(fileName)

# Create output/ directory if not exists

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
NONE = '\033[0m' # No Color

# Define output files
urlXXX = open(URLXXX,"w")
urlOK = open(URLOK,"w")
for i in range(1, nparams):
    errorNum[i] = open(fileName[i], "w")

# Recurrent function
