from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from pymongo import MongoClient

frontier = []
frontier.append("https://www.cpp.edu/sci/computer-science/")

def crawlerThread(frontier):
    while len(frontier) != 0:
        pass
