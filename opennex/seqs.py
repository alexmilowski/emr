import sys,math

resolution = int(sys.argv[1])

size = resolution / 120.0
latMax = int(180 / size)
lonMax = int(360 / size)

def sequenceNumber(lat,lon):
   nlat = 90 - lat
   nlon = 360 + lon if lon < 0 else lon
   s = int(math.floor(nlat/size)) * int(lonMax) + int(nlon / size) + 1
   return s

quad = [ sequenceNumber(49.5,-126.0), sequenceNumber(49.5,-67.0),
         sequenceNumber(25.0,-126.0), sequenceNumber(25.0,-67.0) ]
width = int(quad[1] - quad[0] + 1)

s = quad[0]
while s<quad[3]:
   print s
   for seq in range(s,s+width):
       print seq
   s += lonMax
