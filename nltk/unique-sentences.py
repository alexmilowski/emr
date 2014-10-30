import sys
import nltk
# skip first line
sys.stdout.write(sys.stdin.readline())

lastSentence = ""
for line in sys.stdin:
   parts = line.split("\n")[0].split("\t")
   if parts[1] != lastSentence:
      sys.stdout.write(line)
      lastSentence = parts[1]
