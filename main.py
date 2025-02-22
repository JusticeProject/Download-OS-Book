from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
import time
import subprocess
import os

####################################################################

BEGINNING_FILES = ["Preface", "TOC"]
ENDING_FILES = ["Virtual Machines", "Lab Tutorial"]
OUTPUT_FILE_NAME = "Operating_Systems_3_Easy_Pieces.pdf"

####################################################################

def doDownload():
    # Grab the HTML text from the main page
    BASE_URL = "https://pages.cs.wisc.edu/~remzi/OSTEP/"
    html = urlopen(BASE_URL)
    bs = BeautifulSoup(html.read(), "html.parser")

    chapterTags = {}

    # Look for all the table items that contain a chapter
    tableDataList = bs.find_all("td")
    for tableData in tableDataList:
        smallTags = tableData.find_all("small")
        if (len(smallTags) == 1):
            smallText = smallTags[0].text
            if (len(smallText) > 0) and (len(smallText) < 3):
                chapterTags[smallText] = smallTags[0]

    urls = {}

    # Collect the urls for each chapter
    for text, tag in chapterTags.items():
        aTag = tag.parent.find("a")
        href = aTag["href"]
        urls[text] = BASE_URL + href

    numChapters = len(urls)

    # Add the extra urls, join the two lists first
    for text in BEGINNING_FILES + ENDING_FILES:
        href = bs.find("a", string=text)["href"]
        urls[text] = BASE_URL + href

    # Download each url and save as .pdf
    for name, url in urls.items():
        filename = name + ".pdf"
        print(f"downloading {url} and saving as {filename}")
        urlretrieve(url, filename)
        time.sleep(5)

    return numChapters

####################################################################

def doPDFMerge(numChapters):
    cmd = "pdfunite"

    for name in BEGINNING_FILES:
        cmd = cmd + " '" + name + ".pdf'"

    for i in range(1, numChapters+1):
        cmd = cmd + " " + str(i) + ".pdf"
    
    for name in ENDING_FILES:
        cmd = cmd + " '" + name + ".pdf'"

    cmd = cmd + " " + OUTPUT_FILE_NAME

    print("running cmd:")
    print(cmd)
    subprocess.check_output(cmd, shell=True)

####################################################################

def doCleanup():
    files = os.listdir(".")
    for filename in files:
        if (".pdf" in filename) and (filename != OUTPUT_FILE_NAME):
            os.remove(filename)

####################################################################

numChapters = doDownload()
doPDFMerge(numChapters)
doCleanup()
