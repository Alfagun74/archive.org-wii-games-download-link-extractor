from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

links = [
    "https://archive.org/download/WiiRedumpNKitPart1/",
    "https://archive.org/download/WiiRedumpNKitPart2/",
    "https://archive.org/download/WiiRedumpNKitPart3/",
    "https://archive.org/download/WiiRedumpNKitPart4/",
    "https://archive.org/download/WiiRedumpNKitPart5/",
    "https://archive.org/download/WiiRedumpNKitPart6/",
    "https://archive.org/download/WiiRedumpNKitPart7/",
    "https://archive.org/download/WiiRedumpNKitPart8/",
]
ShallowExtractedLinks = []
DeepExtractedLinks = []

print("[+] Starting Shallow Extraction...")
# Go through each archive dump link
for index, link in enumerate(links, start=1):
    print("[+] Shallow Extraction: " + str(index) + " of " + str(len(links)))
    soup = BeautifulSoup(urlopen(Request(link)), "lxml")
# Get all the sublinks
    for extract in soup.select('td a'):
        extractedName = extract.getText()
# Get German/European Titles
        match = re.search(",de|de,|german|europe",
                          extractedName, re.IGNORECASE)
        if match == None:
            continue
# Get German/European Titles
        extractedLink = extract.get('href')
        if extractedLink == None:
            continue
        extractedLink = link + extractedLink
        if re.search("\.nkit\.gcz", extractedLink, re.IGNORECASE):
            DeepExtractedLinks.append(extractedLink)
        else:
            ShallowExtractedLinks.append(extractedLink)

print("[+] Shallow Extraction Complete!")
print("[+] Saving Progress...")
f = open("shallowextract.txt", "w")
for link in ShallowExtractedLinks:
    f.write(link + "\n")
f.close()
print("[+] Progress saved.")
print("[+] Starting Deep Extraction...")
f = open("deepextract.txt", "w")
for index, link in enumerate(ShallowExtractedLinks, start=1):
    print("[+] Deep Extraction: " + str(index) +
          " of " + str(len(ShallowExtractedLinks)))
    goodsoup = BeautifulSoup(urlopen(Request(link)), "lxml")
    for extract in goodsoup.select('td a'):
        extractedName = extract.getText()
        match = re.search("nkit", extractedName, re.IGNORECASE)
        if match == None:
            continue
        extractedLink = extract.get('href')
        if extractedLink == None:
            continue
        extractedLink = link + extractedLink
        print("Added: " + extractedLink)
        DeepExtractedLinks.append(extractedLink)
        f.write(extractedLink + "\n")
print("[+] Deep Extraction Complete!")
print("[+] Saving Progress...")
f.close()
print("[+] Progress saved.")
print("[+] Done!")
