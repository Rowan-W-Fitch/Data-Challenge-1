import math
import glob
import string
import re
import nltk

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
    def __init__(self, reviews, good_words, bad_words, negations):
        self.reviews = reviews
        self.good_words = good_words
        self.bad_words = bad_words
        self.negations = negations


    def make_review(self, p, n, e, w):
        rev = review(p,n,e,w)
        return rev

    def is_negated(self,line,word):
        for i in range(len(line)-1):
            if(line[i+1] == word) and (line[i] in negations):
                return True
            elif(i+2 < len(line) -1) and (line[i+2] == word) and(line[i] in negations):
                return True
            else:
                return False

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
                if exc:
                    continue
                elif exclamation in line and exc == False:
                    exc = True
                #get length of sentence
                line = re.sub(r'[^\w\s]','',line)
                line = line.split()
                wrds += len(line)
                #get number of positive and negative words
                for word in line:
                    if word in good_words and self.is_negated(line,word):
                        neg +=1
                    elif word in good_words and not(self.is_negated(line,word)):
                        pos +=1
                    elif word in bad_words and self.is_negated(line,word):
                        pos +=1
                    elif word in bad_words and not(self.is_negated(line,word)):
                        neg+=1

            review r = review(pos,neg,exc,wrds)
            reviews.append(r)


bad = open("negative-words.txt")
good = open("positive-words.txt")
negate = open("Negations.txt")
bad_words = [x.lower() for x in list(bad.read().split())]
good_words = [x.lower() for x in list(good.read().split())]
negations = [x.lower() for x in list(negate.read().split())]
FR = folder_reader([],good_words,bad_words,negations)
FR.read_folder()
