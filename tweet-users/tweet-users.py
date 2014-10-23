import sys
import json

for line in sys.stdin:
   tweet = json.loads(line)
   username = "?"
   print "LongValueSum:{0}\t1".format(username)
