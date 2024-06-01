# Bookmark cleansing R4.1

This is a simple **python** script utility to weed your good old bookmark file.

After gathering and classifying bookmarks for more than 20 years one may hit dead URLs just when expecting them work. In order to keep the bookmark list current I created this script.

Feed this python scripts with a Chrome bookmark file and a list of http return codes to be pruned and it will crawl through them and try to reach each entry. All successfull bookmarks will be copied to a _cleaner_ json file, and failing URLs will be copied to additional files named as the specified return code.

Empty bookmark folders can be optionally removed.

Due to the large number of agents involved in Internet traffic, results achieved have not as reliable as to think about complete automation. Results may be inexact due to different redirect strategies, moved to https... So far, the suggestion is to keep the original bookmark file for some time, load the clean one in your browser, and review the excluded entries for yet valuable ones.

Tasks are divided between two scripts.

There is one script that runs on-line and crawls all entries included in the bookmarks and queues requests to workers that grab URLs in parallel performing these four steps:

- workers are created an listen to queue

- main loop pushes URLs to queue

- workers read URLs from queue and try to reach them

- workers write returned code to file

A second script may be run off-line that reads the previous script output plus and a list of return codes to discard, and composes a new **Bookmarks.out** new file, excluding those entries returning those codes.

| :warning: WARNING          |
|:---------------------------|
| Make sure bookmarks don't change between running both scripts, that may happen when it conflicts with some running bookmark synchronizer |

To run them in containers, check [DOCKER](DOCKER.md).

## Requirements

- python 3

- _requests_ module installed: `python3 -m pip install requests`

- _queue_ module installed: `python3 -m pip install queue`

- _threading_ module installed: `python3 -m pip install threading`

## Usage

Clone this repository into a directory

1. First copy your Bookmarks file to the directory and run `./scanJSON.py [-w work_dir] [-i input_file]` to scan all present URLs in input Bookmarks file and produce **ALL.url** which includes a list of URLs and their resulting return code. It scans bokmarks from **bookmarks_bar**, **other** and **synced** top folders. _concurrent_ (32) parameter in que.py script defines the number of paralel threads. As this script crawls all bookmarks, it is run on-line and may take some time depending on the connection speed and amount of original entries, typically about 10 entries per second.

 -i input_file: Bookmark file to use (defaults to `./Bookmarks`)

 -o work_dir: Folder in which **ALL.url** file will be stored (defaults to `./work_dir/`)

For instance:

  `./scanJSON`

&emsp;Out of original boormark file it will generate **ALL.url**, which contains a flat list of original URLs and their http returned status code.

1. Run then `./buildJSON.py [-w work_dir] [-i input_file] [-e] <code1> <code2>...` to produce **Bookmarks.out** with Bookmarks format with entries gleaned from **ALL.url**. This script can be run off-line and several times using disctinct return codes. Both **input_file** and **ALL.url** will be used as input.

  `./buildJSON -h`

 -i input_file: Original bookmark file to use (defaults to `./Bookmarks`)

 -o work_dir: Folder in which **ALL.url** file will be stored (defaults to `./work_dir/`)

 -e: remove empty folders flag

 \<codeN\>: list of http return codes to filter out. If no codes are provided script will just classify all bookmarks to their code named file, and copy original Bookmarks unchanged. It is allowed the use of **dot** as a digit wildcard.

&emsp;For instance:

&emsp;  `./buildJSON.py 30. 404 406`

&emsp;will filter bookmark file so that invocation will remove http return codes `30.`, `404` & `406`. Those codes are parsed as Regexp, so character **.**  means any caharacter, so `30.` will actually filter `300`..`309`. This sample command will generate these 5 extra files in `work_dir` subdirectory. :

- **XXX.url**: list of inaccessible URLs

- **30..url**: list of 30. URLs

- **404.url**: list of 404 URLs

- **406.url**: list of 406 URLs

- **Bookmarks.out**: resulting json bookmarks with lame entries removed

If **buildJSON.py** is run without parameters it will just populate files for all http return codes found, and **Bookmarks.out** will hold original Bookmark file with no modifications. That dry run enables reviewing urls in files of specific return codes and decide whether actually removing them in next runs.

When it finishes all result files will appear in `work_dir` subdirectory. Original **Bookmarks** file can now be replaced with **Bookmarks.out**. Restart browser to reload them.

**Note**
Scripts deal with UTF-8 characters

**Warning**
First backup original bookmark file !

## Input file

Copy of chrome Bookmarks file.

## Output files

Script crawls the bookmark file using **requests.head** method to access each site and retrieve http return code. It has a hardcoded 10" timeout.

After processing all these files will be added to `work_dir`:

- entries failing due to sundry network errors in `XXX.url`.

- empty folders `Empty_folders.lst`.

- all https status codes specified will be rejected and entries logged in `<code>.url`.

- valid bookmarks in **Bookmarks.out**, to replace original `Bookmarks` with.

- return code and entry list in `ALL.url`

Find here more information [about files](work_dir/FILES.md) in `work_dir`.

## Sample screen dump

Here scripts are used to remove URLs returning 30., 404 & 406 codes. First `scanJSON.py` launches parallel head requests to bookmarked sites. Next `buildJSON.py` builds the json structure of the bookmark file and generates a replacement of original Bookmarks file filtered specified return codes (30., 404 & 406 in this example)

```bash
$ ./scanJSON.py
(Bookmarks from /home/juan/.config/google-chrome/Default/Bookmarks)
...
[3] MongoDB (21)
200 https://www.tutorialspoint.com/mongodb/index.htm
301 http://php.net/manual/en/mongo.tutorial.php
200 http://www.mongodb.org/display/DOCS/Querying
404 http://devzone.zend.com/1730/getting-started-with-mongodb-and-php/fake.html
XXX https://guides.codepath.com/android/Using-an-ArrayAdapter-with-ListView
406 http://www.tokutek.com/
...
(Scanned to ./work_dir/ALL.url)

$ ./buildJSON.py -e 30. 404 406
(Bookmarks from /home/juan/.config/google-chrome/Default/Bookmarks)
(Scanned from ./work_dir/ALL.url)
...
[3] MongoDB (21)
>>> https://www.tutorialspoint.com/mongodb/index.htm
    200 +
>>> http://php.net/manual/en/mongo.tutorial.php
    301 1345
>>> http://www.mongodb.org/display/DOCS/Querying
    200 +
>>> http://devzone.zend.com/1730/getting-started-with-mongodb-and-php/fake.html
    404 1348
>>> https://guides.codepath.com/android/Using-an-ArrayAdapter-with-ListView
    XXX 1349
>>> http://www.tokutek.com/
    406 1350
...
```

And output files will be stored in `work_dir`.

Above, log entries for a folder and six processed bookmarks are shown where four are filtered out:

**[depth] Folder name (entries)**  indicates the folder name, depth and number of entries in it

&gt;&gt;&gt; **url**

&nbsp;&nbsp;&nbsp;**return code** (200, 301, 404 & 406 shown in this sample run), + if preserved, entry id if rejected.

This sample run will filter out entries returning 30., 404, 406 & XXX. XXX code is caused by network errors and entry id is shown. These XXX entries are always removed, there is no need to specify it.

## Sample recording

Here is a sample screen recording, an i5 box with 16 GB and 300 Mb/s scans at 5 entries/s.

https://user-images.githubusercontent.com/7460694/233157006-b294ed35-dc25-427f-a3a4-6807fafe9897.mp4

## Caveats

Running Chrome with a registered Google account may resynchronize bookmarks back, so applying this script to purge them won't show results.

## Status

Fully operational

## Change log

- R4.1 docker images generated with Jenkins

- R4.0 To run as docker images, see [DOCKER](DOCKER.md) and [JENKINS](JENKINS.md)

- R3.9 Edited with PyCharm

- R3.8 Fixed bug so entries yielding XXX return code are not included in Bookmarks.out now

- R3.7 Fixed bug about deleting empty folders option, and renamed it to -e --empty

- R3.6 Intermediate file between scan and build renamed to ALL.url

- R3.5 http return codes can be specified using **dot** as a character wildcard (ie 4.4 means 404, 414...), codes allow dot wildcard and if no code is provided only classifies all bookmarks, yet output Bookmarks file remains unchanged

- R3.4 -i input_file and -w work_dir options

- R3.3 parses command line using argparse

- R3.2 remove duplicated entries option

- R3.1 handles UTF-8 characters and processes also "other" & "synced" bookmark folders. Output file is now Bookmarks.out

- R3 runs in two steps: scan and build

- R2 parallelization efforts

- R1.31 checks for valid http return codes

- R1.30 takes as parameters all the http return codes to be filtered out to files named as return codes.

## TODO

Use it as the core for developing a Chrome extension, like "Bookmarks clean up" one

## Author

- **Juan Valentín-Pastrana** (jvalentinpastrana at gmail)

Send feedback if you wish.

## License

This project is licensed under the MIT License

## Acknowledgments

- Joefrey who put me up to play in the open source arena

- Mario & Iñaki who are back to programming

- Antonio's hosting
