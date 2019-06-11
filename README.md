# Bookmark cleansing
I have been gathering and classifying bookmarks for more than 20 years. From time to time I hit some outdated bookmark. In order to have that file updated there is this script. When this python script is fed with a Chrome bookmark file it crawls it and tries to reach each bookmark. As a result it filters original bookmark file, clasifying its entries into files by different kind of errors and also the successfull ones.

Due to the unsteady nature of Internet traffic, results have not been as reliable as to think about complete automation. So far, original bookmark file is splitted into several bookmark files depending on the error found to be manually examined and removed. For the time being.

## Requirements
python 3

Having *requests* module installed:

`pip install requests`

## Usage

Clone this repository into a directory

Export your bookmarks in **json** format to a file named `chrome_bookmarks.json` in same directory

Run `python3 load.py`

Allow it finish and result files will appear in _output_ directory

## Input file
File has to be exported from Chrome using Export History/Bookmarks plugin to a file with JSON extension and name `chrome_bookmarks.json`

## Output files
Script crawls the bookmark file and uses **requests.head** to access the site. It is set a 10" timeout. It retrieves the http return code.

After processing, valid bookmark files are fed to `OK.json`.

Those bookmarks rejected due to a 404 http error are fed to `404.json`.

Those subject to some different network errors are fed to `error.json`.

The classification structure is preserved.

## Sample screen output

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

**+** indicates what site responded (302 code in this sample)

**X** means content unaccessible

# Author

* **Juan Valentín-Pastrana** (jvalentinpastrana at gmail)

# License

This project is licensed under the MIT License 

# Acknowledgments

* Joefrey who prodded me to write open source code

* Mario & Iñaqui who are back to programming

