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

bs = BeautifulSoup(html, 'html.parser')
names = bs.find("section", {"class":"text-images"}).find_all("h2")
entries = bs.find("section", {"class":"text-images"}).find_all("p")

prof_names = []
for name in names:
    prof_names.append(name.get_text())

data = {}
prof_data = []
for entry in entries:
    temp = entry.get_text()
    prof_data.append(temp.split("  "))

for entry in prof_data:
    for i in range(len(entry)):
        if entry[i] == "Email:":
            entry[i] = entry[i] + " " + entry[i+1]
            entry.pop(i+1)
            break

for entry in prof_data:
    if len(entry) > 5:
        entry[4] = entry[4] + entry[5]
        entry.pop(5)

for entry in prof_data:
    for x in range(len(entry)):
        temp = entry[x].replace("\xa0", "")
        entry[x] = temp

for i in range(len(prof_data)):
    data_dict = {}
    for item in prof_data[i]:
        temp = item.split(":")
        data_dict.update({temp[0].lstrip():temp[1].lstrip()})
    data.update({prof_names[i].lstrip():data_dict})

for k, v in data.items():
    document = {
        "name":k,
        "title": v.get('Title'),
        "office": v.get('Office'),
        "email": v.get('Email'),
        "website": v.get('Web')
    }
    professors.insert_one(document)