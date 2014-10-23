import sys
import json

f = open(sys.argv[1],"r")
data = json.load(f)
f.close()

for tweet in data["tweets"]:
   print json.dumps(tweet)
