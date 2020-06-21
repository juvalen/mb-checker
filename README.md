# Bookmark cleansing R3.5
This is a simple command line utility to weed your good old bookmark file.

After gathering and classifying bookmarks for more than 20 years one may hit dead URLs just when expecting them work. In order to keep the bookmark list current I created this script.

Feed this python scripts with a Chrome bookmark file and a list of http return codes to be pruned and it will crawl through them and try to reach each entry. All successfull bookmarks will be copied to a _cleaner_ json file, and failing URLs will be copied to additional files named as the specified return code.

Duplicated bookmark entries can be optionally removed.

Due to the large number of agents involved in Internet traffic, results achieved have not been as reliable as to think about complete automation. It means that two consecutive runs with the same few thousands of bookmarks won't yield the exact same results. So far, the suggestion is to keep the original bookmark file for some time, load the clean one in your browser, and review the rejected entries for yet valuable ones. This is for the time being.

Tasks are divided between two scripts.

There is one script that crawls all entries included in the bookmarks and queues requests to workers that grab URLs in parallel performing these four steps:
 - workers are created an listen to queue
 - main loop pushes URLs to queue
 - workers read URLs from queue and try to reach them
 - workers write returned code to file

A second script reads that file output plus a list of return codes to discard, and composes a new bookmarks new file, excluding those entries returning those codes.

## Requirements

* python 3

* *requests* module installed: `python3 -m pip install requests`

* *queue* module installed: `python3 -m pip install queue`

* *threading* module installed: `python3 -m pip install threading`

## Usage

Clone this repository into a directory

1. Run first `./scanJSON.py [-w work_dir] [-i input_file]` to scan all present URLs in input Bookmarks file and produce **Filtered.url** which includes a list of URLs and their resulting return code. It scans bokmarks from bookmarks_bar, other and synced top folders. *concurrent* (32) parameter in que.py script defines the number of paralel threads. As this script crawls all bookmarks, it may take some time depending on the amount of original entries, about 10 entries per second.

 -i input_file: Bookmark file to use (defaults to live `/home/<user>/.config/google-chrome/Default/Bookmarks`)

 -o work_dir: Folder in which **Filtered.url** file will be stored (defaults to `./work_dir/`)

For instance:

  `./scanJSON`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Out original boormark file (for Ubuntu) it will generate **work_dir/Filtered.url**, which contains a flat list of URLs and their http returned status code.

2. Run then `./buildJSON.py [-w work_dir] [-i input_file] [-d] [-f] <code1> <code2>...` to produce <work_dir>/Bookmarks.out from Bookmarks and Filtered.url, removing duplicates (-d option) and removing empty folders (-f option). This script can be run several times with disctinct return codes. Both **input_file** and **work_dir/Filtered.url** will be read.

  `./buildJSON -h`

 -i input_file:	Bookmark file to use (defaults to live `/home/<user>/.config/google-chrome/Default/Bookmarks`)

 -o work_dir:	Folder in which **Filtered.url** file will be stored (defaults to `./work_dir/`)

 -d, --duplicates:	remove duplicated bookmarks

 -f, --folders:	remove empty folders

 <codeN>:	list of http return codes to filter out. If no codes are provided script will just classify all bookmarks to their code named file, and copy original Bookmarks unchanged. It is allowed the use of **dot** as a digit wildcard.

For instance:

  `./buildJSON -d 30. 404 406`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; will filter live bookmark file (for Ubuntu) to remove http return codes 30., 404 & 406 and removing duplicated entries. Regexp character **.** is allowed and means any caharacter, so 300..309 return codes will be filtered. This command will generate 7 files in _work_dir_ subdirectory. :

* **XXX.url**: list of inaccessible URLs

* **DDD.url**: list of duplicated URLs

* **30..url**: list of 30. URLs

* **404.url**: list of 404 URLs

* **406.url**: list of 406 URLs

* **Bookmarks.out**: resulting json bookmarks with lame entries removed

Allow it finish and all result files will appear in _work_dir_ subdirectory. Original **Bookmarks** file can now be replaced with **Bookmarks.out**. Restart browser to reload them.

**Scripts deal with UTF-8 characters**

```
First backup original bookmark file !
```

See usage details at `./buildJSON.py -h`

## Input file
Use original chrome bookmark file or use a stored one.

## Output files
Script crawls the bookmark file using **requests.head** method to access each site. It has a hardcoded 10" timeout. It retrieves the http return code.

After processing all these files will be added to work_dir:

* entries failing due to sundry network errors in `XXX.url`.

* duplicated entries in `DDD.url`. (if option d specified)

* all https status codes specified will be rejected and entries logged in `<code>.url`.

* valid bookmarks in `Bookmarks.out`, to replace original `Bookmarks`.

* return code and entry list in `Filtered.url`

## Sample screen dump

Here scripts are used to remove URLs returning 30., 404 & 406 codes. First `scanJSON.py` launches parallel head requests to bookmarked sites. Next `buildJSON.py` builds the json structure of the bookmark file and generates a replacement of original bookmark file filtered specified return codes (30., 404 & 406 in this example)

```
$ ./scanJSON.py
(Bookmarks from /home/juan/.config/google-chrome/Default/Bookmarks)
...
[3] MongoDB (21)
200 https://www.tutorialspoint.com/mongodb/index.htm
301 http://php.net/manual/en/mongo.tutorial.php
200 http://www.mongodb.org/display/DOCS/Querying
200 http://www.mongodb.org/display/DOCS/Querying
404 http://devzone.zend.com/1730/getting-started-with-mongodb-and-php/fake.html
XXX https://guides.codepath.com/android/Using-an-ArrayAdapter-with-ListView
406 http://www.tokutek.com/
...
(Scanned to ./work_dir/Filtered.url)

$ ./buildJSON.py -d 30. 404 406
(Bookmarks from /home/juan/.config/google-chrome/Default/Bookmarks)
(Scanned from ./work_dir/Filtered.url)
...
[3] MongoDB (21)
>>> https://www.tutorialspoint.com/mongodb/index.htm
    200 +
>>> http://php.net/manual/en/mongo.tutorial.php
    301 1345
>>> http://www.mongodb.org/display/DOCS/Querying
    200 +
>>> http://www.mongodb.org/display/DOCS/Querying
    DDD 1347
>>> http://devzone.zend.com/1730/getting-started-with-mongodb-and-php/fake.html
    404 1348
>>> https://guides.codepath.com/android/Using-an-ArrayAdapter-with-ListView
    XXX 1349
>>> http://www.tokutek.com/
    406 1350
...
```

And output files will be stored in work_dir.

Above, log entries for a folder and seven processed bookmarks are shown where five are filtered out:

**[depth] Folder name (entries)**  indicates the folder name, depth and number of entries in it

**>>> url**

&nbsp;&nbsp;&nbsp;**return code** (200, 301, 404 & 406 in this sample run), + if preserved, entry id if rejected.

This sample run will filter out entries returning 30., 404, 406, DDD & XXX. XXX code is caused by network errors and entry id is shown. These XXX entries are always removed, there is no need to specify it. DDD means a duplicated entry that will be removed -first occurrence will be preserved- showing its id.

## Change log

* R3.5 http return codes can be specified using **dot** as a character wildcard (ie 4.4 means 404, 414...), codes allow dot wildcard and if no code is provided only classifies all bookmarks, yet Bookmark file remains unchanged

* R3.4 -i input_file and -w work_dir options

* R3.3 parses command line using argparse

* R3.2 remove duplicated entries option

* R3.1 handles UTF-8 characters and processes also "other" & "synced" bookmark folders. Output file is now Bookmarks.out

* R3 runs in two steps: scan and build

* R2 parallelization efforts

* R1.31 checks for valid http return codes

* R1.30 takes as parameters all the http return codes to be filtered out to files named as return codes.

## Status

Fully operational

## TODO

Gather other Chrome bookmark file locations for other Linux distributions

## Author

* **Juan Valentín-Pastrana** (jvalentinpastrana at gmail)

Send feedback if you wish.

## License

This project is licensed under the MIT License 

## Acknowledgments

* Joefrey who put me up to play in the open source arena

* Mario & Iñaki who are back to programming

* Antonio's hosting
 
