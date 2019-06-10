# Bookmark cleansing
I have been gathering and classifying bookmarks for more than 20 years. From time to time I hit some outdated bookmark. In order to have that file updated there is this script. When this python script is fed with a Chrome bookmark file it crawls it and tries to reach each bookmark. As a result it generates files with different kind of errors and another file with the successfull ones.

## Requirements
python 3

Having *requests* module installed:

`pip install requests`

## Usage

Clone this repository into a directory

Export your bookmarks in **json** format to a file named `chrome_bookmarks.json` in same directory

Run `python3 load.py`

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

 ` H http://www.frontpagemag.com/`

`>  3695`

 ` X https://porandalucialibre.es/ [Errno 111] Connection refused`

Above log for four bookmark entries are shown:

**>** indicates the id in the bookmark input file

**+** indicates what site responded (200 code here)

**H** means site has some HTTP error

**X** means content unaccessible

