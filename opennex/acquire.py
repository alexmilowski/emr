import urllib2, gzip, StringIO
from xml.dom import pulldom
from xml import sax
import json
import math

import sys

serviceURI = "http://data.pantabular.org/opennex/data/"

def fetchQuadrangle(dataset,yearMonth,resolution,sequence):
   url = serviceURI+dataset+"/"+yearMonth+"/"+str(resolution)+"/"+str(sequence);
   print url
   response = None
   try:
      response = urllib2.urlopen(url)
   except urllib2.HTTPError as e:
      return None
      
   html = None
   
   if response.headers.get('content-encoding', '') == 'gzip':
      data = response.read()
      compressedstream = StringIO.StringIO(data)
      gzipper = gzip.GzipFile(fileobj=compressedstream)
      html = gzipper.read()
   else:
      html = response.read()
      
   parser = sax.make_parser()
   parser.setFeature(sax.handler.feature_namespaces, 1)
   doc = pulldom.parseString(html,parser)
   
   inTable = False
   
   def textContent(parent):
      s = "";
      for n in parent.childNodes:
         if n.data != None:
            s += n.data
      return s
   
   data = []
   for event, node in doc:
       if event == pulldom.START_ELEMENT and node.tagName == 'table':
          if node.getAttribute("typeof") == "IndexedTable":
             inTable = True
       if event == pulldom.END_ELEMENT and node.tagName == 'table':
          inTable = False
       if inTable and event == pulldom.START_ELEMENT and node.tagName == 'td':
          doc.expandNode(node)
          if len(node.childNodes) > 0:
             data.append(float(textContent(node)))
             
   if len(data) == 0:
      return None
   
   return {"dataset": dataset, "yearMonth": yearMonth, "resolution" : resolution, "sequence": sequence, "data": data }

dataset = sys.argv[1]   
resolution = int(sys.argv[2])
year = sys.argv[3]

size = resolution / 120.0
latMax = int(180 / size)
lonMax = int(360 / size)
seqMax = int(latMax * lonMax)

def sequenceNumber(lat,lon):
   nlat = 90 - lat
   nlon = 360 + lon if lon < 0 else lon
   s = int(math.floor(nlat/size)) * int(lonMax) + int(nlon / size) + 1
   return s

quad = [ sequenceNumber(49.5,-126.0), sequenceNumber(49.5,-67.0),
         sequenceNumber(25.0,-126.0), sequenceNumber(25.0,-67.0) ]
width = int(quad[1] - quad[0] + 1)

print quad
for m in sys.argv[4:]:
   yearMonth = "{}-{:02d}".format(year,int(m))
   print yearMonth
   s = quad[0]
   while s<quad[3]:
      for seq in range(s,s+width):
          print seq
          obj = fetchQuadrangle(dataset,yearMonth,resolution,seq)
          if obj != None:
             fileName = yearMonth+"-"+str(resolution)+"-"+str(seq)+".json"
             f = open(fileName,"w")
             json.dump(obj,f)
             f.close()
      s += lonMax

#print json.dumps(fetchQuadrangle("avg-rcp85","2014-10",resolution,1))
#print json.dumps(fetchQuadrangle("avg-rcp85","2014-10",resolution,58798))