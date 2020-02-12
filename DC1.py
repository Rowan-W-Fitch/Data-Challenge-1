import math
import glob
import string
import re
import nltk
from nltk.tokenize import word_tokenize
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

        self.words = math.log(words,10)

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
    def __init__(self, reviews, negations):
        self.reviews = reviews
        self.negations = negations

    #makes a review object
    def make_review(self, p, n, e, w):
        rev = review(p,n,e,w)
        return rev

    #checks if a word has been negated
    def is_negated(self,line,word):
        line = line.split()
        for i in range(len(line)-1):
            if(line[i+1] == word) and (line[i] in negations):
                return True
            elif(i+2 < len(line) -1) and (line[i+2] == word) and(line[i] in negations):
                return True
            else:
                return False

    #converts pos_tag t0 sentiNet pos
    def convert_pos(self, pos):
        if pos == "RB":
            return "r"
        elif pos == "JJ":
            return "a"
        elif pos[0] == "V":
            return "v"
        elif pos[0] == "N":
            return "n"

    #compares avg pos_score() and neg_score() from nltk sent_lists and determines if word is pos or neg
    def avg_senti(self, word,pos):
        pos = self.convert_pos(pos)
        sentis = list(swn.senti_synsets(word,pos))
        if len(sentis) == 0: return 2 #returning 2 means word is not pos or negative
        p_score = 0
        n_score = 0
        a_score = 0
        for set in sentis:
            if set != None:
                p_score += set.pos_score()
                n_score += set.neg_score()
                a_score += set.obj_score()
        p_score /= len(sentis)
        n_score /= len(sentis)
        a_score /= len(sentis)

        if max(p_score,n_score,a_score) == p_score:
            return 1
        elif max(p_score,n_score,a_score) == n_score:
            return 0
        else:
            return 2 #if avg objective score is higher than other two, should not be considered pos or neg

    def read_folder(self):
        exclamation = string.punctuation[0]
        path = input('enter path:')+'/*.txt'
        for file in glob.glob(path):
            #initializing review features
            pos = 0
            neg = 0
            exc = False
            wrds = 0
            #open file
            f = open(file)
            for line in f:
                #look for exclamation pt
                if exc:
                    continue
                elif exclamation in line and exc == False:
                    exc = True
                #get avg sentiment of each word from nltk senti_synsets, then add to either pos or neg
                #uses helper function avg_senti(x,y)
                line = line.lower()
                tokens = word_tokenize(line)
                tags = nltk.pos_tag(tokens)
                for x,y in tags:
                    if (self.avg_senti(x,y) == 1) and not(self.is_negated(line,x)):
                        pos += 1
                    elif self.avg_senti(x,y) == 1 and (self.is_negated(line,x)):
                        neg +=1
                    elif self.avg_senti(x,y) == 0 and not(self.is_negated(line,x)):
                        neg+=1
                    elif self.avg_senti(x,y) == 0 and (self.is_negated(line,x)):
                        pos += 1
                #get length of sentence
                line = re.sub(r'[^\w\s]','',line)
                line = line.split()
                wrds += len(line)

            #print all features to see data (remove after testing)
            print(pos)
            print(neg)
            print(exc)
            print(wrds)
            print("-----")
            r = review(pos,neg,exc,wrds)
            self.reviews.append(r)

negate = open("Negations.txt")
negations = [x.lower() for x in list(negate.read().split())]
FR = folder_reader([],negations)
FR.read_folder()
