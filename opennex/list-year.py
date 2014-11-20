# coding=UTF-8

import sys
import json
import pymongo

slash = sys.argv[1].rindex('/')
dburi = sys.argv[1][0:slash+1]
dbname =  sys.argv[1][slash+1:]
dbcollection = sys.argv[2]
year = int(sys.argv[3])
 
client = pymongo.MongoClient(dburi)
db = client[dbname]
collection = db[dbcollection]

for data in collection.find({"year": year},{"month": 1, "average": 1}):
   print data["month"],"\t",data["average"]
   
   
