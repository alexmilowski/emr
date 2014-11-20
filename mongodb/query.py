# coding=UTF-8

import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["test"]
collection = db["people"]

for person in collection.find({"familyName" : "Miłowski"},{"_id": 0, "givenName" : 1, "familyName" : "randomValueThatDoesNotReallyMatter"}):
   print person
   
   
