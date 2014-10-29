import sys
import pickle
import sets
import nltk

# Local
import stopwords
import featureset

classifierFilename = sys.argv[1]
stopWordsFilename = sys.argv[2]
wordcountFilename = sys.argv[3]
rangeSpec = sys.argv[4].split(",")
wordStart = int(rangeSpec[0])
wordEnd = int(rangeSpec[1])
dataFilename = sys.argv[5]

f = open(classifierFilename,"rb")
classifier = pickle.load(f)
f.close()

stopWords = stopwords.load(stopWordsFilename)

featureWords = featureset.load(wordcountFilename,wordStart,wordEnd)

reviews = []
data = open(dataFilename,"r")
# skip first line
data.readline()

extractFeatures = featureset.makeExtractor(featureWords)

count = 0
missed = 0
for line in data:
   parts = line.split("\n")[0].split("\t")
   wordlist = [e.lower() for e in nltk.word_tokenize(parts[2]) if len(e) >= 3 and not e.lower() in stopWords]
   c = int(classifier.classify(extractFeatures(wordlist)))
   if len(parts) > 3:
      a = int(parts[3])
      count += 1
      if c != a:
         missed += 1
         print parts[0]+"\t"+(",".join(reduce(lambda l,w: l+[w] if w in featureWords else l,wordlist,[])))+"\t"+parts[2]+"\t"+str(a)+"\t"+str(c)
   else:
      print parts[0]+"\t"+str(c)

data.close()

if count>0:
   print "{0} % missed ".format(100* (missed*1.0 / count))