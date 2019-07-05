# Bookmark cleansing R3
This is a simple command line utility to weed your good old bookmark file.

After being gathering and classifying bookmarks for more than 20 years one may hit dead URLs just when accessing them. In order to keep the bookmark list current I created this script.

Feed this python scripts with a Chrome bookmark file and a list of http return codes to be pruned and it will crawl through it and try to reach each entry. All successfull bookmarks will be copied to a _cleaner_ json file, and failing URLs will be copied to additional named as the specified return code.

Due to the large number of agents involved in Internet traffic, results achieved have not been as reliable as to think about complete automation. So far, the suggestion is to keep the original bookmark file for some time, load the clean one in your browser, and review the rejected entries for yet valuable ones. This is for the time being.

There is one script that crawls all entries included in the bookmarks and generates a list with the status code of each entry.
 - workers reach URLs and store result
 - queue deliver tasks
 - main loop pushed to queue

A second script takes that output plus the source bookmark file plus a list of offending return codes and removes those bookmarks which returned that codes.

## Requirements

* python 3

* *requests* module installed: `python3 -m pip install requests`

* *queue* module installed: `python3 -m pip install queue`

* *threading* module installed: `python3 -m pip install threading`

## Usage

Clone this repository into a directory

Copy **Bookmarks** file in which Chrome stores bookmarks in json format to a subdirectory named _output_ under this.

1. Run first `./scanJSON.py` to produce Filtered.url from Bookmarks

2. Run then `./buildJSON 301 404 406` to produce Filtered.json from Bookmarks and Filtered.url

This two sample commands will generate 6 files in _output_ subdirectory:

* **Filtered.url**: list of return code and URL for each entry

* **XXX.url**: list of inaccessible URLs

* **301.url**: list of 301 URLs

* **404.url**: list of 404 URLs

* **406.url**: list of 406 URLs

* **Filtered.json**: resulting json bookmarks with stale entries removed

Allow it finish and all result files will appear in _output_ subdirectory. Replace original **Bookmarks** file with **Filtered.json**.

**The Title field of the bookmark could be defaced by non-ASCII characters, extra quotes or escape sequences found in the original entry.**

```
First backup original data !
```

## Input file
Copy original chrome bookmark file, which may be found for Brave browser in Ubuntu in _~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks_.

## Output files
Script crawls the bookmark file and uses **requests.head** method to access each site. It is set a 10" timeout. It retrieves the http return code.

After processing all these files will be found in the _output_ subdirectory:

* return code and entry list in `Filtered.url`

* all https status codes specified will be rejected and entries logged in `<code>.url`.

* entries failing due to sundry network errors in `XXX.url`.

* valid bookmarks in `Filtered.json`, to replace original `Bookmarks`.

## Sample screen dump

```
$ ./scanJSON.py
$ ./buildJSON.py 301 404 406
...
[3] MongoDB (21)
200 https://www.tutorialspoint.com/mongodb/index.htm
301 http://php.net/manual/en/mongo.tutorial.php
302 http://devzone.zend.com/1730/getting-started-with-mongodb-and-php/
XXX https://guides.codepath.com/android/Using-an-ArrayAdapter-with-ListView
...
```

Above, log entries for a folder and six processed bookmarks are shown:

**[depth] Folder name (entries)**  indicates the folder name, depth and number of entries in it

**code url** returned status (XXX, 200, 301 & 302 in this sample run) and URL (XXX entries are always removed, no need to specify it)

## Change log

* R3 runs in two steps: scan and build

* R2 parallelization efforts

* R1.31 checks for valid http return codes

* R1.30 takes as parameters all the http return codes to be filtered out to files named as return codes.

## Status

Fully operational

## TODO

Specify wildcards in http return codes so as **5xx** would filter 500, 501, 502...

## Author

* **Juan Valentín-Pastrana** (jvalentinpastrana at gmail)

## License

This project is licensed under the MIT License 

## Acknowledgments

* Joefrey who put me up to play in the open source arena

* Mario & Iñaki who are back to programming

* Antonio's hosting

