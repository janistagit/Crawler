from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

frontier = []
frontier.append("https://www.cpp.edu/sci/computer-science/")
target = "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"

client = MongoClient(host="localhost", port=27017)
db = client.crawler
pages = db.pages

def crawlerThread(frontier):
    while len(frontier) != 0:
        url = frontier.pop()

        if (re.match("^https://www.cpp.edu", url) == None):
             url = "https://www.cpp.edu" + url

        try:
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        except URLError as e:
            print("Server could not be found.")
        else:
            data = html.read().decode(encoding="iso-8859-1")
            document = {
                "url":url,
                "html":data
            }
            pages.insert_one(document)

            bs = BeautifulSoup(html.read(), 'html.parser')
            if bs.find("h1", string="Permanent Faculty"):
                frontier.clear()

crawlerThread(frontier)