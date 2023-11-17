from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import sqlite3
import csv


class Crawler():

    """
    given a county website, this class finds and stores the directory
    to the county's adopted building codes
    """

    def __init__(self, GovWebsite):
        self.countyUrl = [GovWebsite]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
            "Accept-Language": "en-US",
            'Referer': 'https://google.com',
            'DNT': '1',
        }

        # list of key words to loop thru
        self.kwords1 = [
            'Department',
            'department'
        ]
        self.kwords2 = [
            'Community',
            'community',
            'Planning',
            'planning',
            'Development',
            'development',
            'Building',
            'building',
        ]
        self.kwords3 = [
            'Building-Code',
            'building-codes',
            'Policy',
            'policy',
            'Policies',
            'policies',
            'Guide',
            'guide',
            'Amendments',
            'amendments',
            'Design',
            'design'
            'Code',
            'code'
        ]

        self.kwords = [
            self.kwords1,
            self.kwords2,
            self.kwords3
        ]

    def spider(self, urls):  # method to retrieve website source

        # instantiate a dictionary to hold url and source code
        sources = {}
        # iterate through urls
        for url in urls:
            # pass a static url header agent
            try:
                response = requests.get(url, headers=self.headers)
            except requests.exceptions.ConnectionError:
                print("Given URL: '%s' is not available!" % url)
                continue
            html = response.content
            # add source html to dictionary
            sources[url] = BeautifulSoup(html, features="html.parser")

        return(sources)

    def getLinks(self, sources):  # method that gathers all links on a web page

        # instantiate list to store links on page
        hrefs = []

        # Loop thru urls and only parse href websites
        for url, source in sources.items():
            for href in source.findAll('a', href=True):
                #temphref = href.get('href')
                temphref = (href.get('href'), href.string)

                # build a full link if href link is not a complete path
                # checks if contains "www."", "http", and "/" at begining of website
                if 'www.' not in temphref[0] and temphref[0].find('http') != 0 and temphref[0].find('/') == 0:
                    tempurl = url.split('/')
                    domain = tempurl[0]+'/'+tempurl[1]+'/'+tempurl[2]
                    hrefs.append(domain + temphref[0])
                # check if contains "www.", "http", and "/" symbol in the href
                elif temphref[0].find('www.') == -1 and temphref[0].find('http') != 0 and temphref[0].find('/') != 0:
                    tempurl = url.split('/')
                    domain = tempurl[0]+'/'+tempurl[1]+'/'+tempurl[2]+'/'
                    hrefs.append(domain + temphref[0])
                else:
                    hrefs.append(temphref[0])

        return(hrefs)

    def trimUrls(self, urls, kwords):  # filter urls for keywords

        # instantiate list to store urls with a keyword
        key_hrefs = []

        # finds urls that contains keywords
        for url in urls:
            for kword in kwords:
                # splits url by '/' and store as lists of string objects
                temp = url.split('/')
                # instantiate a variable to store the index with which keyword is found within the list of strings
                j = 0
                for i in range(len(temp)):
                    # gets the last index within the string
                    if temp[i].find(kword) != -1:
                        j = i

                # returns lists of url segments
                tempurlseg = temp[:j+1]

                # build a workable url link from list so url segments
                tempurl = ''
                if j != 0:
                    for seg in tempurlseg:
                        tempurl = tempurl+seg+'/'
                else:
                    continue
                # add to key-hrefs
                key_hrefs.append(tempurl)

        # remove duplicates
        key_hrefs = list(dict.fromkeys(key_hrefs))

        return(key_hrefs)

    def loop(self, websites=None):

        websites = self.countyUrl if websites == None else websites

        for count, kwords in enumerate(self.kwords):
            print("# in loop: ", count)
            sources = self.spider(websites)
            links = self.getLinks(sources)
            websites = self.trimUrls(links, kwords)

        return(websites)


'''--------- Searching thru Weld County Website - ----------'''

weld_county_home = 'https://www.weldgov.com/'

weld = Crawler(weld_county_home)
weld_temp_websites = weld.loop()

# writes the potential websites that contains code to a url
fw = open("weld_county_temp_code_websites.txt", "w")
for website in weld_temp_websites:
    fw.write(website + "\n")

fw.close()

# instantiate empty list to place
tempcode = []

# stores crawled
for item in weld_temp_websites:
    x = Crawler(item).spider([item])
    tempcode.append(x)

key_url = ''
"""
# writing
for count, item in enumerate(tempcode):
    filename = "Weld_url"+str(count+1)
    for url, soup in item.items():
        print(url)
        with open(filename, "w") as f:
            f.write("url :")
            f.write(url)
            f.write(soup.get_text())
            f.close()
"""
tempurl = {}

for count, item in enumerate(tempcode):
    for url, soup in item.items():
        tempurl[url] = soup.get_text()

for url, text in tempurl.items():
    if 'International Building Code' in text:
        key_url = url

print('the returning url is: %s' % key_url)

"""

'''--------- Searching thru Denver County Website -----------'''

denver_home = 'https://denvergov.org/'

denver = Crawler(denver_home)
denver_temp_website = denver.loop()

# writes the potential websites that contains code to a url
fw = open("denver_county_temp_code_websites.txt", "w")
for website in denver_temp_website:
    fw.write(website + "\n")

fw.close()

# instantiate empty list to place
tempcode = []

# stores crawled
for item in denver_temp_website:
    x = Crawler(item).spider([item])
    tempcode.append(x)

key_url = ''

# writing
for count, item in enumerate(tempcode):
    filename = "Denver_url"+str(count+1)
    for url, soup in item.items():
        with open(filename, "w") as f:
            f.write("url :")
            f.write(url)
            f.write(soup.get_text())
            f.close()

tempurl = {}

for count, item in enumerate(tempcode):
    for url, soup in item.items():
        tempurl[url] = soup.get_text()

for url, text in tempurl.items():
    if 'International Building Code' in text:
        key_url = url

print('the returning url is: %s' % key_url)

"""

"""

'''--------- Searching thru Monroe County Website -----------'''

monroe_home = 'https://www.monroecounty-fl.gov/'

monroe = Crawler(monroe_home)
monroe_temp_website = monroe.loop()

# writes the potential websites that contains code to a url
fw = open("monroe_county_temp_code_websites.txt", "w")
for website in monroe_temp_website:
    fw.write(website + "\n")

fw.close()

# instantiate empty list to place
tempcode = []

# stores crawled
for item in monroe_temp_website:
    x = Crawler(item).spider([item])
    tempcode.append(x)

key_url = ''

# writing
for count, item in enumerate(tempcode):
    filename = "Monroe_url"+str(count+1)
    for url, soup in item.items():
        print(url)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("url :")
            f.write(url)
            f.write(soup.get_text())
            f.close()

"""
