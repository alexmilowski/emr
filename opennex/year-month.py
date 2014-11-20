import sys

startYear = int(sys.argv[1])
monthCount = int(sys.argv[2])

for m in range(0,monthCount):
   year = startYear+m/12
   month = m % 12 + 1
   yearMonth = "{0}-{1:02d}".format(year,month)
   print yearMonth
