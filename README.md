# Bookmark cleansing
I have been gathering and classifying bookmarks for more than 20 years. Some out of those bookmarks -a few thousand- actually outdated. When this python script is fed with a Chrome bookmark file it crawls it and tries to reach each one. As a result it generates a file with all the 404 http errors and another with the successfull ones.

## Requirements
python 2

Having *urllib2* module installed:

`pip install urllib2`

## Usage

Clone this repository into a directory

Export your bookmarks in **json** format to a file named `chrome_bookmarks.json` in same directory

Run `python2 load.py`

let it finish and result files will appear in _output_ directory

## Input file
File has to be exported from Chrome using Export History/Bookmarks plugin to a file with JSON extension and name `chrome_bookmarks.json`

## Output files
After processing, valid bookmark files are copied to `filtered.json`.

Those bookmarks rejected due to a 404 http error are copied to `404.json`.

The classification structure is preserved.

## Screen output

`>  3607`

`[International]`

`>  3608`

 ` + http://www.discoverthenetworks.org/group.asp 200`

`>  3609`

 ` X http://www.frontpagemag.com/`

Above three entries in the bookmark file are shown:

**>** indicates the id in the bookmark input file

**+** indicates what site responded (200 code here)

**X** means site is unreachable

