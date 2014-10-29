import sys
import nltk
import sets
import pickle

# Local
import stopwords
import featureset

stopWordsFilename = sys.argv[1]
wordcountFilename = sys.argv[2]
rangeSpec = sys.argv[3].split(",")
wordStart = int(rangeSpec[0])
wordEnd = int(rangeSpec[1])
trainingDataFilename = sys.argv[4]
outputFilename = sys.argv[5]


stopWords = stopwords.load(stopWordsFilename)

featureWords = featureset.load(wordcountFilename,wordStart,wordEnd)
print featureWords

sys.stderr.write("Loading training data...");

reviews = []
trainingData = open(trainingDataFilename,"r")
# skip first line
trainingData.readline();

for line in trainingData:
   parts = line.split("\n")[0].split("\t")
   wordlist = [e.lower() for e in nltk.word_tokenize(parts[2]) if len(e) >= 3 and not e.lower() in stopWords]
   # putting data into your training set that doesn't exhibit your features doesn't hurt but it also doesn't help
   #rwordlist = reduce(lambda l,w: l+[w] if w in featureWords else l,wordlist,[])
   #if len(rwordlist)>0:
   reviews.append((wordlist,parts[3]))

trainingData.close()

#def extractFeatures(document):
#    words = set(document)
#    features = {}
#    for word in featureWords:
#        features['contains(%s)' % word] = (word in words)
#    return features

extractFeatures = featureset.makeExtractor(featureWords)

sys.stderr.write(" applying features ...");
trainingSet = nltk.classify.apply_features(extractFeatures, reviews)

sys.stderr.write(" training classifier ...");
classifier = nltk.NaiveBayesClassifier.train(trainingSet)
sys.stderr.write(" done\n");

f = open(outputFilename, 'wb')
pickle.dump(classifier, f)
f.close()
