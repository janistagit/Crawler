from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

#Set up database connection, create database and collection
client = MongoClient(host="localhost", port=27017)
db = client.crawler
professors = db.professors