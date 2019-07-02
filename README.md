# Bookmark cleansing R1.31
This is a simple command line utility to weed your good old bookmark file.

After being gathering and classifying bookmarks for more than 20 years one may hit dead URLs just when accessing them. In order to keep the bookmark list current I created this script.

Feed this python script with a Chrome bookmark file and a list of http return codes to be pruned and it will crawl through it and try to reach each entry. All successfull bookmarks will be copied to a _cleaner_ json file, and failing URLs will be copied to additional named as the specified return code.

Due to the large number of agents involved in Internet traffic, results achieved have not been as reliable as to think about complete automation. So far, the suggestion is to keep the original bookmark file for some time, load the clean one in your browser, and review the rejected entries for yet valuable ones. This is for the time being.

## Requirements

* python 3

* *requests* module installed: `python3 -m pip install requests`

## Usage

Clone this repository into a directory

Copy **Bookmarks** file in which Chrome stores bookmarks in json format to a subdirectory named _output_ under this.

Run `./chrome.py 301 404 406`

This will generate 6 files in _output_ subdirectory:

* **XXX.url**: list of inaccessible URLs

* **OK.url**: list of successfull URLs

* **301.url**: list of 301 URLs

* **404.url**: list of 404 URLs

* **406.url**: list of 406 URLs

* **Filtered.json**: resulting json bookmarks with stale entries removed

Thus XXX.url & OK.url & 301.url & 404.url & 406.url altogether will contain all original bookmark entries.

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

* valid entry list in `OK.url`

* all https status codes spedified will be rejected and entries logged in `<code>.url`.

* those subject to some sundry network errors in `XXX.url`.

* Valid bookmarks in `Filtered.json`, to replace original `Bookmarks`.

## Sample screen dump

```
$ ./chrome.py 301 404 406
...
[2] Poesia (6)
>>> http://www.diccionariodesinonimos.es/
  T  Diccionario de Sinónimos
  404 4481 #13
>>> http://www.poemas-del-alma.com/mario-benedetti.htm
  T  Mario Benedetti - Poemas de Mario Benedetti
  301 1925 #11
>>> http://vademecum-poetico.blogspot.com.es/2009/10/acentuacion-ritmica-versal-ii-el.html
  T  VADEMECUM POETICO: ACENTUACIÓN RÍTMICA VERSAL: (II) EL ENDECASÍLABO
  302 + #8
>>> http://www.poesi.as/index43.htm
  T  Fábula de Polifemo y Galatea
  200 + #2
>>> http://www.foundalis.com/res/bps/bpidx.htm
  N  Index of Bongard Problems
  406 2973 #2
>>> http://www.phpeasystep.com/phptu/3.html
  T  PHP Limit upload file size
  XXX 5346 #3
```

Above, log entries for a folder and six processed bookmarks are shown:

**[depth] Folder name (entries)**  indicates the folder name, depth and number of entries in it

**>>>** URL under scrutiny

**T** original bookmark title

**NNN + #11** returned status (200 & 302 in this sample run, indicates bookmark entry is copied to __output/OK.url__ and bookmark preserved to `Filtered.json`) and list sequence # displayed

**301 1925 11** indicates site returned 301 and URL added to __output/301.url__, entry Id removed and list sequence # displayed

**404 4481 #13** indicates site returned 404 and URL added to __output/404.url__, entry Id removed and list sequence # displayed

**406 2973 #2** indicates site returned 406 and URL added to __output/406.url__, entry Id removed and list sequence # displayed

**XXX 5346 #3** means site unaccessible, so URL was copied to __output/XXX.url__, entry Id removed and list sequence # displayed

## Change log

* R1.31 checks for valid http return codes

* R1.30 takes as parameters all the http return codes to be filtered out to files named as return codes.

## Status

Fully operational

## TODO

Specify wildcards in http return codes so as **5xx** would filter 500, 501, 502...

Paralelize

## Author

* **Juan Valentín-Pastrana** (jvalentinpastrana at gmail)

## License

This project is licensed under the MIT License 

## Acknowledgments

* Joefrey who put me up to play in the open source arena

* Mario & Iñaki who are back to programming

* Antonio's hosting

