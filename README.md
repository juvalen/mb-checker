# Bookmark cleansing R1
This is a simple command line utility to weed your good old bookmark file.

After one has been gathering and classifying bookmarks for more than 20 years one may hit dead URLs just when accessing them. In order to keep the bookmark list current I created this script.

Feed this python script with a Chrome bookmark file and it will crawl through it and try to reach each bookmark. As a result it generates a *cleaner* bookmark file, plus additional files including the failing URLs.

Due to the unsteady nature of Internet traffic, results achieved have not been as reliable as to think about complete automation. So far, the suggestion is to keep the original bookmark file for some time, load the clean one in your browser, and review the rejected entries for valuable ones. This for the time being.

## Requirements

* python 3

* *requests* module installed: `pip install requests`

## Usage

Clone this repository into a directory

Export your bookmarks in **json** format to a file named `chrome_bookmarks.json` in same directory

Run `python3 load.py`

Allow it finish and result files will appear in _output_ directory

## Input file
File has to be exported from Chrome using _Export History/Bookmarks_ plugin to a file with JSON extension and name `chrome_bookmarks.json`

## Output files
Script crawls the bookmark file and uses **requests.head** to access the site. It is set a 10" timeout. It retrieves the http return code.

After processing there will be these files in the _output_ directory:

* valid bookmarks files in `OK.json`

* rejected entries due to a 404 http error in `404.url`.

* those subject to some sundry network errors in `error.url`.

`OK.json` has to be converted to html before importing it back. For that https://github.com/andreax79/json2html-bookmarks.git can be used.

File can be imported back to browser.

To tr

## Sample screen dump

```
>>> 6195
[WiMax]
>>> 6196
 +  http://www.wimax.com/education/wimax/wimax_overview 302
>>> 6197
 X  http://www.iec.org/online/tutorials/ofdm/index.html
```

Above, log entries for a folder and two bookmark are shown:

**>>>** indicates the internal id in the bookmark input file

**+** indicates what site responded (with 302 code in this sample)

**X** means sites unaccessible

# Author

* **Juan Valentín-Pastrana** (jvalentinpastrana at gmail)

# License

This project is licensed under the MIT License 

# Acknowledgments

* Joefrey who put me up to play in the open source arena

* Mario & Iñaqui who are back to programming

* Antonio's hosting

