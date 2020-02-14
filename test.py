import sklearn
import numpy as np
import os
import shutil
from nltk.corpus import stopwords as stp
from sklearn import datasets
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

#begin actual logistic regression model
path = r"C:\Users\Rowan Fitch\Desktop\NLP\Data\DC1\labeled"
#loads data, also shuffles it to randomize
reviews = load_files(path, shuffle = True, random_state = 31)
#splits training(70% of data) and testing data(30% of data)
review_train, review_test, sent_train, sent_test = train_test_split(reviews.data, reviews.target, test_size = 0.3)
"""for testing
print("number of docs in training: " + str(len(review_train)))
print("samples in training: " + str(np.bincount(sent_train)))"""
#vectorizer creates bucket of words for data
vectorizer = CountVectorizer(stop_words = stp.words("english"), ngram_range = (1,5), min_df = 3)
#apply vectorizer to training reviews
r_train = vectorizer.fit(review_train).transform(review_train)
#apply vectorizer to test reviews
r_test = vectorizer.transform(review_test)

""" ONLY FOR TESTING delete when done, prints size of vector created by vectorizer
features = vectorizer.get_feature_names()
print("number of features: " + str(len(features)))"""

p_grid = {'C': [0.001,0.01,0.1,1,10]}
grid = GridSearchCV(LogisticRegression(), p_grid, cv=5)
grid.fit(r_train,sent_train)

# print("best cv score: " + str(grid.best_score_)) -> test print statement
#print("best estimator: ", grid.best_estimator_) -> test print statement

logRes = grid.best_estimator_
logRes.fit(r_train,sent_train)
logRes.predict(r_test)

""" TEST prints accuracy of logistic regression on test data"""
print("score of logisitic regression: " + str(logRes.score(r_test,sent_test)))

""" Following code is for applying logRes model to the unlabeled data"""

source = r"C:\Users\Rowan Fitch\Desktop\NLP\Data\DC1\unlabeled"
pos_revs = r"C:\Users\Rowan Fitch\Desktop\NLP\Data\DC1\pos_labeled"
neg_reviews = r"C:\Users\Rowan Fitch\Desktop\NLP\Data\DC1\neg_labeled"
files = os.listdir(source)
for file in files:
    f = open(os.path.join(source,file))
    if str(logRes.predict(vectorizer.transform(f))) == "[1]":
        shutil.copy2(os.path.join(source,file), pos_revs)
    else:
        shutil.copy2(os.path.join(source,file), neg_reviews)

""" Following code is for flagging potential fake reviews"""
source1 = pos_revs
source2 = neg_reviews
ratings = r"C:\Users\Rowan Fitch\Desktop\NLP\Data\DC1\ratings\unlabeled"
fakes = r"C:\Users\Rowan Fitch\Desktop\NLP\Data\DC1\fakes"

for files in os.listdir(source1):
    print(files[len(files)-4])
