# Bookmark checker
I have been gathering and classifying bookmarks for more than 20 years. Some out of those bookmarks -a few thousand- actually outdated. When this python script is fed with a Chrome bookmark file it crawls it and tries to reach each one. As a result it generates a file with all the 404 http errors and another with the successfull ones.

## Requirements
python 2

Having *urllib2* module installed:

`pip install requests`

## Input file
File is exported from Chrome using Export History/Bookmarks to JSON extension with name `chrome_bookmarks.json`

## Output files
After processing, valid bookmark files are copied to `filtered.json`.

Those bookmarks rejected due to a 404 http error are copied to `404.json`.

The classification structure is preserved.

## Screen output

`
#  3607
[International]
#  3608
 + http://www.discoverthenetworks.org/group.asp 200
#  3609
 X http://www.frontpagemag.com/
`

Above three entries in the bookmark file are shown:

# indicates the id in the bookmark input file

+ indicates site responded (200 code here)

X means site is unreachable

