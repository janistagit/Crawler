from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

target = "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"

#Set up database connection, create database and collection
client = MongoClient(host="localhost", port=27017)
db = client.crawler
professors = db.professors
pages = db.pages

#Retrieve html from pages collection using target url
result = pages.find(filter={"url":target}, projection={"html":1, "_id":0})
html = result[0]["html"]