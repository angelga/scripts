from bs4 import BeautifulSoup

import requests
import os
import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = raw_input("4chan thread link (full): ")

threadpage = BeautifulSoup(requests.get(url).text)
try:
    threadid = threadpage.find("div", class_="file").get("id")[1:]
except:
    print "Thread seems to be gone: ", sys.exc_info()[0]
    sys.exit()

threadFiles = threadpage.find_all("a", class_="fileThumb")

for fileThumb in threadFiles:
    if "4archive.org" in url:
        fileHref = fileThumb.get("href")
        if fileHref == "/images/image-404.png":
            print "Skipping empty image"
            continue
    elif "4chan.org" in url:
        fileHref = "http:" + fileThumb.get("href")

    fileName = fileHref.split("/")[-1]
    filePath = threadid + "/" + fileName

    if os.path.exists(filePath):
            print "Skipped existing file."
            continue

    if not os.path.exists(os.path.dirname(filePath)):
            os.makedirs(os.path.dirname(filePath))

    print "Downloading %s." % fileHref,

    try:
        with open(filePath, "wb") as saveFile:
                saveFile.write(requests.get(fileHref).content)
                saveFile.close()
        print "Done."
    except:
        print "Unexpected error downloading: ", sys.exc_info()[0]
        pass