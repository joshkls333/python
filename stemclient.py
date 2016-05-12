import sys                       
import urllib.request

# Josh Klaus
# CS131A
# Python

# A client program for your stem CGI service which sends its command line argument 
# and gets the result back. This program works just as “stem” with a delay for the network
# operations between client and server. 

word = sys.argv[1]  # Command line argument

hostserver = "http://hills.ccsf.edu/"
path = "~jklaus1/cgi-bin/"
filename = "stemservice.py"
parameter = "stem"

# Reference to my stem service program has been hardcoded for testing purposes
url = hostserver + path + filename + "?" + parameter + "=" + word   

# request and response from URL
req = urllib.request.Request(url)

# Fetching the URL with Error handling as documented by Python HOWTO
try: response = urllib.request.urlopen(req)
except urllib.error.URLError as e:      
    if hasattr(e, 'reason'):            # handling URLError
        print('Unable to reach server.')  
        print('Reason: ', e.reason)
    elif hasattr(e, 'code'):            # handling HTTPError
        print('Server unable to fulfill the request.')
        print('Error code: ', e.code)

# decode the bytes object
clean_output = response.read().decode('utf-8')

print(clean_output)