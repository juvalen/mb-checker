# Bookmark cleansing R1
This is a simple command line utility to weed your good old bookmark file.

After one has been gathering and classifying bookmarks for more than 20 years one may hit dead URLs just when accessing them. In order to keep the bookmark list current I created this script.

Feed this python script with a Chrome bookmark file and it will crawl through it and try to reach each bookmark. As a result it generates a *cleaner* bookmark file, plus additional files including the failing URLs.

Due to the large number of agents involved in Internet traffic, results achieved have not been as reliable as to think about complete automation. So far, the suggestion is to keep the original bookmark file for some time, load the clean one in your browser, and review the rejected entries for valuable ones. This for the time being.

## Requirements

* python 3

* *requests* module installed: `python3 -m pip install requests`

## Usage

Clone this repository into a directory

Copy **Bookmarks** file in which Chrome stores bookmarks in json format to directory _output_ under this.

Run `python3 chrome.py`

It generates four files:

* **error.url**: list of not accessible URLs

* **404.url**: list of 404 URLs

* **OK.url**: list of successfull URLs

* **Filtered.json**: original json bookmarks purged

So error.url & 404.url && OK.url will contain all original URLs altogether.

Allow it finish and result files will appear in _output_ directory. Replace original **Bookmarks** file with **Filtered.json**.

**The Title field of the bookmark could be defaced by non-ASCII characters, extra quotes or escape sequences found in the original.**

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

## Sample screen dump

```
[2] Poesia (6)
>>> http://www.diccionariodesinonimos.es/
  T  Diccionario de Sinónimos
  406+
>>> http://www.poemas-del-alma.com/mario-benedetti.htm
  T  Mario Benedetti - Poemas de Mario Benedetti
  301+
>>> http://vademecum-poetico.blogspot.com.es/2009/10/acentuacion-ritmica-versal-ii-el.html
  T  VADEMECUM POETICO: ACENTUACIÓN RÍTMICA VERSAL: (II) EL ENDECASÍLABO
  302+
>>> http://www.poesi.as/index43.htm
  T  Fábula de Polifemo y Galatea
  200+
>>> http://www.nxtcrypto.org/
  T  Nxt • Next Generation of Cryptocurrency • NxtCoin • Nextcoin
  404 2933
>>> http://www.phpeasystep.com/phptu/3.html
  T  PHP Limit upload file size
  XXX 5346
```

Above, log entries for a folder and four bookmarks are shown:

**[depth] Folder name (entries)**  indicates the folder, depth and number of entries

**>>>** URL being reached

**T** original bookmark title

**NNN +** added entry and returned code (301 in this sample), bookmark entry copied to __output/OK.json__

**404 Id** indicates site returned 404 and URL added to __output/404.url__ and entry Id to be removed

**XXX Id** means site unaccessible, so URL was copied to __output/error.url__ and entry Id to be removed

# Author

* **Juan Valentín-Pastrana** (jvalentinpastrana at gmail)

# License

This project is licensed under the MIT License 

# Acknowledgments

* Joefrey who put me up to play in the open source arena

* Mario & Iñaqui who are back to programming

* Antonio's hosting

