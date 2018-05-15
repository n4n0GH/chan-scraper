#! /usr/bin/python
#
# coding: utf-8

# chan-scraper.py is a standalone mass downloader for any arbitrary
# chan or website in general. It looks for links that point to media
# files and downloads them accordingly.

# TODO: make script compatible with Python 2.7 and Python 3.x
# TODO: make downloader handle unicode characters (i.e. cyrillic)
# TODO: have only a hrefs in array if the a has an img child (line 60)

# import some libraries
from bs4 import BeautifulSoup
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
import sys
import os

# print ASCII intro
print("""
      _
     | |
  ___| |__   __ _ _ __    ___  ___ _ __ __ _ _ __   ___ _ __
 / __| '_ \ / _` | '_ \  / __|/ __| '__/ _` | '_ \ / _ \ '__|
| (__| | | | (_| | | | | \__ \ (__| | | (_| | |_) |  __/ |
 \___|_| |_|\__,_|_| |_| |___/\___|_|  \__,_| .__/ \___|_|
                                            | |
  Download picrelated from any chan         |_|       v0.1

""")

# set up UA so *chan accepts the request
ua = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
      'AppleWebKit/537.11 (KHTML, like Gecko)'
      'Chrome/23.0.1271.64 Safari/537.11'}

# get URL from user
if sys.version_info[:2] <= (2,7):
    user_input = raw_input
else:
    user_input = input
url = user_input("Input URL to scrape: \n > ")

# make some soup
req = urllib2.Request(url, headers=ua)
soup = BeautifulSoup(urllib2.urlopen(req), "lxml")

# split the url into parts
parse = url.split('/')
base = parse[2]
path = parse[3]
thread = parse[-1]

# fetch all files and append to array
scrape = []

for img in soup.select('a[href$=jpg],'
                       'a[href$=jpeg],'
                       'a[href$=png],'
                       'a[href$=gif],'
                       'a[href$=webm]'):
    img_url = urlparse.urljoin(url, img['href'])
    if img_url not in scrape:
        scrape.append(img_url)

# set up path names for downloads
home = os.path.expanduser("~")
fpath = os.path.join(home, "chanscraper", base, path, thread)

# create directory if necessary
if not os.path.exists(fpath):
    os.makedirs(fpath)

# download array to disk
for img in scrape:
    file_name = img.split('/')[-1]
    full_path = os.path.join(fpath, file_name)
    if not os.path.exists(full_path):
        filedata = urllib2.urlopen(img)
        print("Grabbing " + img + "...")
        with open(full_path, 'wb') as f:
            f.write(filedata.read())
        print("OK!")
    else:
        print("File already exists, skipping...")

print("\nDownloaded " + str(len(scrape)) + " files!")