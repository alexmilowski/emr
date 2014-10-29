
def load(filename):

   # stop words from http://www.textfixer.com/resources/common-english-words.txt (via Wikipedia)
   stopWordsFile = open(filename,"r")
   stopWords = stopWordsFile.readline().split("\n")[0].split(",")
   stopWordsFile.close()

   return stopWords + ["...", "-rrb-", "-lrb-","n't"]