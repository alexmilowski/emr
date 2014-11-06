from mrjob.job import MRJob
import re

class MRTweetWordCount(MRJob):

    def mapper(self, _, line):
        cline = re.sub("http[s]?:/\S+"," ",line)
        words = [word for word in re.split("[|'\",/\s.:?!~-]+",cline) if len(word)>=3]
        for word in words:
           yield word,1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRTweetWordCount.run()

