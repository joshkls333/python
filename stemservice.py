#!/usr/local/bin/python3

# Josh Klaus
# CS131A
# Python

# A CGI program which serves up all the words from the dictionary which start with a given stem. 
# The stem was passed as an HTTP parameter called “stem”.

import cgi, cgitb, codecs
cgitb.enable()

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get value from the URL field
wordstem = form.getvalue('stem')

wordlen = len(wordstem)     # find length of argument

tempwordlist = []       # create temporary list to hold words
			
with codecs.open('/users/abrick/resources/american-english-insane-ascii', 'r', 'utf-8') as inFile:
 	for line in inFile:
	 	if wordstem in line[:wordlen]:
 			tempwordlist.append(line.strip())

cwd = ', '.join(tempwordlist)      # print list as a string

# Used for response to HTTP queries
print("Content-type: text/plain")
print()
print( 'these are the words in the dictionary with that stem: ' + cwd )
