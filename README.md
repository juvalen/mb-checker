# Bookmark checker
I have been gathering and classifying bookmarks for more than 20 years. Some out of those bookmarks -a few thousand- actually outdated. When this python script is fed with a Chrome bookmark file it crawls it and tries to reach each one. As a result it generates a file with all the 404 http errors and another with the successfull ones.

## Input file
File is exported from Chrome using Export History/Bookmarks to JSON extension with name `chrome_bookmarks.json`

## Output files
After processing, valid bookmar files are copied to *filetered.json*.

Those bookmarks rejected due to a 404 http error are put in *404.json*.

The classification structure is preserved.

