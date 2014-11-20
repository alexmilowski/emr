from mrjob.job import MRJob
import sys
import os
import json

class AverageMonth(MRJob):

   def configure_options(self):
      super(AverageMonth, self).configure_options()
      self.add_passthrough_option('--year-month',help="The year and month to process.")
      self.add_passthrough_option('--resolution',help="The resolution.")
      self.add_passthrough_option('--data-dir',help="The directory where the data is stored.")
            
   def average_quadrangle(self, _, line):
      seq = int(line)
      fileName = self.options.data_dir+os.sep+self.options.year_month+"-"+self.options.resolution+"-"+str(seq)+".json"
      if os.path.exists(fileName):
         f = open(fileName,"r")
         obj = json.load(f)
         f.close()
         yield self.options.year_month,(1,sum(obj["data"])/len(obj["data"]))

   def sum_averages(self, yearMonth, countAverage):
      yield yearMonth, reduce(lambda x, y: map(sum, zip(x, y)), countAverage)
      
   def average(self,_,averageData):
      for count,averageSum in averageData:
         yield self.options.year_month,averageSum/count
      
   def steps(self):
        return [
            self.mr(mapper=self.average_quadrangle,
                    reducer=self.sum_averages),
            self.mr(reducer=self.average)
        ]      


if __name__ == '__main__':
   mr_job = AverageMonth(args=sys.argv[1:])
   with mr_job.make_runner() as runner:
       runner.run()
       for line in runner.stream_output():
           key, value = mr_job.parse_output_line(line)
           print key,value

