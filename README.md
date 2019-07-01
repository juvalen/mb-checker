# Bookmark cleansing R1.2.
This is a simple command line utility to weed your good old bookmark file.

After being gathering and classifying bookmarks for more than 20 years one may hit dead URLs just when accessing them. In order to keep the bookmark list current I created this script.

Feed this python script with a Chrome bookmark file and it will crawl through it and try to reach each entry. All successfull bookmarks will be copied to a _cleaner_ file, plus additional files classifying the failing URLs.

Due to the large number of agents involved in Internet traffic, results achieved have not been as reliable as to think about complete automation. So far, the suggestion is to keep the original bookmark file for some time, load the clean one in your browser, and review the rejected entries for yet valuable ones. This is for the time being.

## Requirements

* python 3

* *requests* module installed: `python3 -m pip install requests`

## Usage

Clone this repository into a directory

Copy **Bookmarks** file in which Chrome stores bookmarks in json format to a subdirectory named _output_ under this.

Run `python3 chrome.py`

It generates 5 files in _output_ subdirectory:

* **error.url**: list of not accessible URLs

* **404.url**: list of 404 URLs

* **500.url**: list of 500+ URLs

* **OK.url**: list of successfull URLs

* **Filtered.json**: resulting json bookmarks with stale entries removed

So error.url & 404.url && 500.url && OK.url altogether will contain all original bookmark entries.

Allow it finish and all result files will appear in _output_ subdirectory. Replace original **Bookmarks** file with **Filtered.json**.

**The Title field of the bookmark could be defaced by non-ASCII characters, extra quotes or escape sequences found in the original entry.**

```
First backup original data !
```

## Input file
Copy original chrome bookmark file, which may be found for Brave browser in Ubuntu in _~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks_.

## Output files
Script crawls the bookmark file and uses **requests.head** method to access the site. It is set a 10" timeout. It retrieves the http return code.

After processing all these files will be found in the _output_ subdirectory:

* valid entry list in `OK.url`

* rejected entries due to a 404 http error in `404.url`.

* rejected entries due to a 5xx http error in `500.url`.

* those subject to some sundry network errors in `error.url`.

* Valid bookmarks in `Filtered.json`, which can overwrite original `Bookmarks`.

## Sample screen dump

```
[2] Poesia (6)
>>> http://www.diccionariodesinonimos.es/
  T  Diccionario de Sinónimos
  404 4481 #13
>>> http://www.poemas-del-alma.com/mario-benedetti.htm
  T  Mario Benedetti - Poemas de Mario Benedetti
  301 + 11
>>> http://vademecum-poetico.blogspot.com.es/2009/10/acentuacion-ritmica-versal-ii-el.html
  T  VADEMECUM POETICO: ACENTUACIÓN RÍTMICA VERSAL: (II) EL ENDECASÍLABO
  302 + 8
>>> http://www.poesi.as/index43.htm
  T  Fábula de Polifemo y Galatea
  200 + 2
>>> http://www.nxtcrypto.org/
  T  Nxt • Next Generation of Cryptocurrency • NxtCoin • Nextcoin
  500 2933 #5
>>> http://www.phpeasystep.com/phptu/3.html
  T  PHP Limit upload file size
  XXX 5346 #3
```

Above, log entries for a folder and six bookmarks are shown:

**[depth] Folder name (entries)**  indicates the folder name, depth and number of entries in it

**>>>** URL under scrutiny

**T** original bookmark title

**NNN + #11** returned code (301 in this sample, so bookmark entry is copied to __output/OK.url__ and bookmark preserved to `Filtered.json`) and list sequence # displayed

**404 Id #13** indicates site returned 404 and URL added to __output/404.url__, entry Id removed and list sequence # displayed

**500 Id #5** indicates site returned 500 and URL added to __output/500.url__, entry Id removed and list sequence # displayed

**XXX Id #3** means site unaccessible, so URL was copied to __output/error.url__, entry Id removed and list sequence # displayed

# Status

Fully operational

# Author

* **Juan Valentín-Pastrana** (jvalentinpastrana at gmail)

# License

This project is licensed under the MIT License 

# Acknowledgments

* Joefrey who put me up to play in the open source arena

* Mario & Iñaki who are back to programming

* Antonio's hosting

