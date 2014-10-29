import sets

def load(filename,start,end):
   featureWords = sets.Set()
   input = open(filename,"r")
   count = 0
   for line in input:
      count += 1
      if count < start:
         continue
      if count > end:
         break
      parts = line.split("\n")[0].split("\t")
      featureWords.add(parts[0])
   input.close()
   return featureWords
   
def makeExtractor(featureWords):
   def extractFeatures(document):
       words = set(document)
       features = {}
       for word in featureWords:
           features['contains(%s)' % word] = (word in words)
       return features
   return extractFeatures
