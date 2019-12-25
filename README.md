# Bookmark cleansing R3.1
This is a simple command line utility to weed your good old bookmark file.

After gathering and classifying bookmarks for more than 20 years one may hit dead URLs just when expenting them work. In order to keep the bookmark list current I created this script.

Feed this python scripts with a Chrome bookmark file and a list of http return codes to be pruned and it will crawl through them and try to reach each entry. All successfull bookmarks will be copied to a _cleaner_ json file, and failing URLs will be copied to additional files named as the specified return code.

Due to the large number of agents involved in Internet traffic, results achieved have not been as reliable as to think about complete automation. It means that two consecutive runs with the same few thousands of bookmarks won't yield the exact same results. So far, the suggestion is to keep the original bookmark file for some time, load the clean one in your browser, and review the rejected entries for yet valuable ones. This is for the time being.

There is one script that crawls all entries included in the bookmarks and queues requests to workers that grab URLs in parallel performing these steps:
 - workers are created an listen to queue
 - main loop pushes entries to queue
 - workers reach URLs and store result
 - workers write results to file

A second script takes that file output plus a list of offending return codes and copies source bookmarks to a new file removing those affected.

## Requirements

* python 3

* *requests* module installed: `python3 -m pip install requests`

* *queue* module installed: `python3 -m pip install queue`

* *threading* module installed: `python3 -m pip install threading`

## Usage

Clone this repository into a directory

Copy json **Bookmarks** file in which Chrome stores bookmarks to a subdirectory named _output_ under this.

1. Run first `./scanJSON.py` to produce Filtered.url from Bookmarks. It includes bookmarks_bar, other and synced top folders

2. Run then `./buildJSON.py 301 404 406` to produce Bookmarks.out from Bookmarks and Filtered.url

This last sample commands will generate 6 files in _output_ subdirectory:

* **Filtered.url**: list of original URLs with their return code

* **XXX.url**: list of inaccessible URLs

* **301.url**: list of 301 URLs

* **404.url**: list of 404 URLs

* **406.url**: list of 406 URLs

* **Bookmarks.out**: resulting json bookmarks with stale entries removed

Allow it finish and all result files will appear in _output_ subdirectory. Replace original **Bookmarks** file with **Bookmarks.out**.

**Scripts deal with UTF-8 characters**

```
First backup original data !
```

## Input file
Place a copy of original chrome bookmark file, which may be found for Brave browser for Ubuntu in _~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks_.

## Output files
Script crawls the bookmark file using **requests.head** method to access each site. It is set a 10" timeout. It retrieves the http return code.

After processing all these files will be found in the _output_ subdirectory:

* return code and entry list in `Filtered.url`

* all https status codes specified will be rejected and entries logged in `<code>.url`.

* entries failing due to sundry network errors in `XXX.url`.

* valid bookmarks in `Bookmarks.out`, to replace original `Bookmarks`.

## Sample screen dump

Here scripts are used to remove 404 errors. First `scanJSON.py` launches parallel head requests to bookmarked sites. Next `buildJSON.py` builds the json structure of the bookmark file and generates a replacement of original bookmark file.

```
$ ./scanJSON.py
...
[3] MongoDB (21)
200 https://www.tutorialspoint.com/mongodb/index.htm
301 http://php.net/manual/en/mongo.tutorial.php
301 http://www.mongodb.org/display/DOCS/Querying
404 http://devzone.zend.com/1730/getting-started-with-mongodb-and-php/fake.html
XXX https://guides.codepath.com/android/Using-an-ArrayAdapter-with-ListView
...
$ ./buildJSON.py 404
...
[3] MongoDB (21)
>>> https://www.tutorialspoint.com/mongodb/index.htm
  200 + #0
>>> http://www.mongodb.org/display/DOCS/SQL+to+Mongo+Mapping+Chart
  301 + #1
>>> http://www.mongodb.org/display/DOCS/Querying
  301 + #2
>>> http://devzone.zend.com/1730/getting-started-with-mongodb-and-php/fake.html
  404 + #3
>>> https://guides.codepath.com/android/Using-an-ArrayAdapter-with-ListView
  XXX 1257 #4
...
```

Above, log entries for a folder and five processed bookmarks are shown:

**[depth] Folder name (entries)**  indicates the folder name, depth and number of entries in it

**code url** returned status (XXX, 200, 301, 404 in this sample run) *+* and entry #.

404 and XXX entries are removed. XXX code is caused by network errors and entry id is shown. XXX entries are always removed, there is no need to specify it.

## Change log

* R3.1 Handles UTF-8 characters and processes also "other" & "synced" bookmark folders. Output file is now Bookmarks.out

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

Send feedback if you wish.

## License

This project is licensed under the MIT License 

## Acknowledgments

* Joefrey who put me up to play in the open source arena

* Mario & Iñaki who are back to programming

* Antonio's hosting
 
