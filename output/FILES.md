# Files in this folder:

## Input
File to be copied here:
 - **Bookmarks**: Copy of source Bookmark file

`Don't forget to backup this file first !`

## Output
Files resulting after applying scripts:
 - **XXX.url**: listing of URLs that can't be reached (corresponding to XXX on screen dump)
 - **DDD.url**: listing of duplicated URLs
 - **5xx.url**: listing of URLs getting response code 5xx (corresponding to 5xx on screen dump)
 - **404.url**: listing of URLs getting response code 404 (corresponding to 404 on screen dump)
 - **...**: listing of other codes
 - **Filtered.url**: listing of all passed entries
 - **Bookmarks.out**: Result JSON file containing Chrome bookmarks filtered

You can copy Bookmarks.out back to Bookmark file.

## Reference
 - **format**: JSON bookmark file structure
