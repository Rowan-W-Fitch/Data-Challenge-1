import math
import glob
import string

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

    def read_folder(self):
        exclamation = string.punctuation[0]
        path = input('enter path:')+'/*.txt'
        for file in glob.glob(path):
            #initializing review features
            pos = []
            neg = []
            exc = False
            wrds = 0
            #search for exclamation pts
            f = open(file, 'rU')
            for line in f:
                if exclamation in line:
                    exc = True



FR = folder_reader([])
FR.read_folder()
