# coding=UTF-8

import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test"]
collection = db["people"]

people = [
      {
         "@id" : "http://milowski.com/#alex",
         "givenName" : "Alex",
         "familyName" : "Miłowski",
         "url" : "http://www.milowski.com/",
         "email" : "alex@milowski.com"
      },
      {
         "@id" : "http://nwalsh.com/#ndw",
         "givenName" : "Norman",
         "familyName" : "Walsh",
         "url" : "http://nwalsh.com",
         "email" : "norman.walsh@marklogic.com"
      },
      {
         "@id" : "http://ltg.ed.ac.uk/#henry",
         "givenName" : "Henry",
         "familyName" : "Thompson",
         "url" : "http://www.ltg.ed.ac.uk/~ht/",
         "email" : "ht@inf.ed.ac.uk"
      }
]

collection.create_index([("familyName",pymongo.ASCENDING)])

for person in people:
   id = collection.insert(person)
   print id
   
   
   
