import math
import glob
import string
import re
import nltk
from nltk.corpus import sentiwordnet as swn

"""
review class acts as a node, holds all data
and has all features of logistic regression model
"""
class review:
    def __init__(self,pos,neg,exc,words):
        self.pos = pos
        self.neg = neg

        if exc:
            self.exc = 1
        else:
            self.exc = 0

        self.words = log(words,10)

    def get_pos_count(self):
        return len(self.pos)

    def get_neg_count(self):
        return len(self.neg)

    def has_exc(self):
        if self.exc == True:
            return 1
        else:
            return 0

    def get_wrds(self):
        return self.words

"""
folder reader class opens folder of txt files, and creates a review class for each txt file
has a list of reviews
"""

class folder_reader:
    def __init__(self, reviews):
        self.reviews = reviews

    def make_review(self, p, n, e, w):
        rev = review(p,n,e,w)
        return rev

    def convert_pos(tag):
        if tag.startswith('J'):
            return "a"
        elif tag.startswith('N'):
            return "n"
        elif tag.startswith('R'):
            return "r"
        elif tag.startswith('V'):
            return "v"
        return None

    def get_sentiment(word,tag):
        tag = self.convert_pos(tag)
        sentis = swn.senti_synsets(word, tag)[0]
        return [sentis.pos_score(),sentis.neg_score()]

    def read_folder(self):
        exclamation = string.punctuation[0]
        path = input('enter path:')+'/*.txt'
        for file in glob.glob(path):
            #initializing review features
            pos = 0
            neg = 0
            exc = False
            wrds = 0

            f = open(file)
            for line in f:
                #look for exclamation pt
                if exclamation in line:
                    exc = True
                #get negative an positive sentiment values
                token = nltk.word_tokenize(line)
                tagged = nltk.pos_tag(token)
                for x,y in tagged:
                    print(x)
                    print(y)
                    print("------")
                senti_val = [self.get_sentiment(x,y) for x,y in tagged]
                for sent in senti_val:
                    if len(sent) > 0:
                        print(sent[0])
                        print(sent[1])
                        pos += sent[0]
                        neg += sent[1]
                #get length of sentence
                line = re.sub(r'[^\w\s]','',line)
                wrds += len(line)

            print(pos)
            print(neg)
            print(exc)
            print(wrds)




FR = folder_reader([])
FR.read_folder()
