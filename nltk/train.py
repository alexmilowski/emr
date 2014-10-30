import sys
import nltk
import sets
import pickle

# Local
import featureset

wordlistFilename = sys.argv[1]
rangeSpec = sys.argv[2].split(",")
wordStart = int(rangeSpec[0])
wordEnd = int(rangeSpec[1])
trainingDataFilename = sys.argv[3]
outputFilename = sys.argv[4]

stopWords = nltk.corpus.stopwords.words('english')
stemmer = nltk.stem.lancaster.LancasterStemmer()

featureWords = featureset.load(wordlistFilename,wordStart,wordEnd)
print featureWords

sys.stderr.write("Loading training data...");

reviews = []
trainingData = open(trainingDataFilename,"r")
# skip first line
trainingData.readline();

for line in trainingData:
   parts = line.split("\n")[0].split("\t")
   wordlist = [e.lower() for e in nltk.word_tokenize(parts[2]) if len(e) >= 3 and not e.lower() in stopWords]
   for i in range(len(wordlist)):
      wordlist[i] = stemmer.stem(wordlist[i])
   reviews.append((wordlist,parts[3]))

trainingData.close()

extractFeatures = featureset.makeExtractor(featureWords)

sys.stderr.write(" applying features ...");
trainingSet = nltk.classify.apply_features(extractFeatures, reviews)

sys.stderr.write(" training classifier ...");
classifier = nltk.NaiveBayesClassifier.train(trainingSet)
sys.stderr.write(" done\n");

f = open(outputFilename, 'wb')
pickle.dump(classifier, f)
f.close()
