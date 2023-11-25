from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

target = "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"

# Set up database connection, create database and collection
client = MongoClient(host="localhost", port=27017)
db = client.crawler
professors = db.professors
pages = db.pages

# Retrieve html from pages collection using target url
result = pages.find(filter={"url":target}, projection={"html":1, "_id":0})
html = result[0]["html"]

bs = BeautifulSoup(html, 'html.parser')
names = bs.find("section", {"class":"text-images"}).find_all("h2")
entries = bs.find("section", {"class":"text-images"}).find_all("p")

# Store professor names in list
prof_names = []
for name in names:
    prof_names.append(name.get_text())

# Split professors' data and store as separate lists inside prof_data
data = {}
prof_data = []
for entry in entries:
    temp = entry.get_text()
    prof_data.append(temp.split("  "))

# Fix inconsistent formatting in email entries
for entry in prof_data:
    for i in range(len(entry)):
        if entry[i] == "Email:":
            entry[i] = entry[i] + " " + entry[i+1]
            entry.pop(i+1)
            break

# Fix inconsistent formatting in web entries
for entry in prof_data:
    if len(entry) > 5:
        entry[4] = entry[4] + entry[5]
        entry.pop(5)

# Remove tags remaining in strings
for entry in prof_data:
    for x in range(len(entry)):
        temp = entry[x].replace("\xa0", "")
        entry[x] = temp

# Split fields of professor data and store as dictionaries
# Then store all data as a dictionary of dictionaries with professor name as the key
for i in range(len(prof_data)):
    data_dict = {}
    for item in prof_data[i]:
        temp = item.split(":")
        data_dict.update({temp[0].lstrip():temp[1].lstrip()})
    data.update({prof_names[i].lstrip():data_dict})

# Insert professor data into MongoDB collection
for k, v in data.items():
    document = {
        "name":k,
        "title": v.get('Title'),
        "office": v.get('Office'),
        "email": v.get('Email'),
        "website": v.get('Web')
    }
    professors.insert_one(document)