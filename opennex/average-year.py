from mrjob.job import MRJob
import sys
import os
import json
import math




class AverageYear(MRJob):

   def configure_options(self):
      super(AverageYear, self).configure_options()
      self.add_passthrough_option('--resolution',help="The resolution.")
      self.add_passthrough_option('--data-dir',help="The directory where the data is stored.")
      
   def year_seq(self,_,line):

      yearMonth = line.rstrip()
   
      size = int(self.options.resolution) / 120.0
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
         for seq in range(s,s+width):
             yield yearMonth,seq
         s += lonMax
            
   def average_quadrangle(self, yearMonth, seq):
      fileName = self.options.data_dir+os.sep+yearMonth+"-"+self.options.resolution+"-"+str(seq)+".json"
      if os.path.exists(fileName):
         f = open(fileName,"r")
         obj = json.load(f)
         f.close()
         yield yearMonth,(1,sum(obj["data"])/len(obj["data"]))

   def sum_averages(self, yearMonth, countAverage):
      yield yearMonth, reduce(lambda x, y: map(sum, zip(x, y)), countAverage)
      
   def average(self,yearMonth,averageData):
      for count,averageSum in averageData:
         yield yearMonth,averageSum/count
      
   def steps(self):
        return [
            self.mr(mapper=self.year_seq),
            self.mr(mapper=self.average_quadrangle,
                    reducer=self.sum_averages),
            self.mr(reducer=self.average)
        ]      


if __name__ == '__main__':
   mr_job = AverageYear(args=sys.argv[1:])
   with mr_job.make_runner() as runner:
       runner.run()
       for line in runner.stream_output():
           key, value = mr_job.parse_output_line(line)
           print key,value

