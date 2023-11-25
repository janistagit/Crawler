from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient

frontier = []
frontier.append("https://www.cpp.edu/sci/computer-science/")

def crawlerThread(frontier):
    while len(frontier) != 0:
        url = frontier.pop()
        try:
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        except URLError as e:
            print("Server could not be found.")
        else:
            pass
