# Bookmark cleansing R4.0

This are two simple **docker** images to weed your good old bookmark file. See code details in [README.md](README.md).

Scan image has been created with:

`$ docker build -f Dockerfile.scan -t solarix/scanjson .`

To run it create an empty directory and copy there Bookmarks file, also create there work_dir/. Then run docker:

`$ docker run --rm -v $(pwd)/work_dir:/app/work_dir solarix/scanjson`

ALL.urk will appear in work_dir/ in same folder, which contains a flat list of original URLs and their http returned status code.

A second image removes unwanted URLs from Bookmarks and will compose a new bookmarks new file, excluding those entries returning those codes.

Build image has been created with:

`$ docker build -f Dockerfile.build -t solarix/buildjson .`

Create a variable with the http codes to purge:

`$ export CODES="30. 404 406"`

Run then docker image:

`$ docker run -e CODES="$CODES" --rm -v $(pwd)/work_dir:/app/work_dir solarix/buildjson`

That will produce **Bookmarks.out** with Bookmarks format with entries gleaned from **ALL.url**. This script can be run several times using disctinct return codes. Both **Bookmrks** and **ALL.url** will be used as input.

&emsp;  `$ export CODES="30. 404 406"`

&emsp;will filter live bookmark file (for Ubuntu) so that invocation will remove http return codes `30.`, `404` & `406`. Those codes are parsed as Regexp, so character **.**  means any caharacter, so `30.` will actually filter `300`..`309`. This sample command will generate these 5 extra files in `work_dir` subdirectory. :

* **XXX.url**: list of inaccessible URLs

* **30..url**: list of 30. URLs

* **404.url**: list of 404 URLs

* **406.url**: list of 406 URLs

* **Bookmarks.out**: resulting json bookmarks with lame entries removed

If **buildjson** is run without http CODES it will just populate files for all http return codes found, and **Bookmarks.out** will hold original Bookmark file with no modifications. That dry run enables reviewing urls in files of specific return codes and decide whether actually removing them in next runs.

When it finishes all result files will appear in `work_dir` subdirectory. Original **Bookmarks** file can now be replaced with **Bookmarks.out**. Restart browser to reload them.

**Note**
Scripts deal with UTF-8 characters

Images available from [hub.docker.com](https://hub.docker.com).

```text
First backup original bookmark file !
```

## Input file

Use original chrome bookmark file or use a stored one.

## Output files

Script crawls the bookmark file using **requests.head** method to access each site and retrieve http return code. It has a hardcoded 10" timeout.

After processing all these files will be added to `work_dir`:

* entries failing due to sundry network errors in `XXX.url`.

* empty folders `Empty_folders.lst`.

* all https status codes specified will be rejected and entries logged in `<code>.url`.

* valid bookmarks in `Bookmarks.out`, to replace original `Bookmarks` with.

* return code and entry list in `ALL.url`

Find here more information [about files](work_dir/FILES.md) in `work_dir`.

## Sample screen dump

Here scripts are used to remove URLs returning 30., 404 & 406 codes. First `scanjson` launches parallel head requests to bookmarked sites. Next `buildjson` builds the json structure of the bookmark file and generates a replacement of original bookmark file filtered specified return codes (30., 404 & 406 in this example)

```bash
$ docker run --rm -v $(pwd)/work_dir:/app/work_dir solarix/scanjson
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

$ export CODES="30. 404 406"

$ docker run -e CODES="$CODES" --rm -v $(pwd)/work_dir:/app/work_dir solarix/buildjson
(Bookmarks from Bookmarks)
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

&nbsp;&nbsp;&nbsp;**return code** (200, 301, 404 & 406 in this sample run), + if preserved, entry id if rejected.

This sample run will filter out entries returning 30., 404, 406 & XXX. XXX code is caused by network errors and entry id is shown. These XXX entries are always removed, there is no need to specify it.

## Caveats

Running Chrome with a registered Google account may resynchronize bookmarks back, so applying this script to purge them won't show results.

## Status

Fully operational

## Change log

* R4.0 Available as docker images

* R3.9 Edited with PyCharm

* R3.8 Fixed bug so entries yielding XXX return code are not included in Bookmarks.out now

* R3.7 Fixed bug about deleting empty folders option, and renamed it to -e --empty

* R3.6 Intermediate file between scan and build renamed to ALL.url

* R3.5 http return codes can be specified using **dot** as a character wildcard (ie 4.4 means 404, 414...), codes allow dot wildcard and if no code is provided only classifies all bookmarks, yet Bookmark file remains unchanged

* R3.4 -i input_file and -w work_dir options

* R3.3 parses command line using argparse

* R3.2 remove duplicated entries option

* R3.1 handles UTF-8 characters and processes also "other" & "synced" bookmark folders. Output file is now Bookmarks.out

* R3 runs in two steps: scan and build

* R2 parallelization efforts

* R1.31 checks for valid http return codes

* R1.30 takes as parameters all the http return codes to be filtered out to files named as return codes.

## TODO

Gather other Chrome bookmark file locations for other Linux distributions

Provide it the format of a Chrome extension, like "Bookmarks clean up" one

## Author

* **Juan Valentín-Pastrana** (jvalentinpastrana at gmail)

Send feedback if you wish.

## License

This project is licensed under the MIT License

## Acknowledgments

* Joefrey who put me up to play in the open source arena

* Mario & Iñaki who are back to programming

* Antonio's hosting
