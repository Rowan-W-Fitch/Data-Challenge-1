from DC1 import review
from DC1 import folder_reader as fr
import math
import random

weights = [0,0,0,0,0]
learn_rate = 0.1
#puts dot product result thru sigmoid function
def sigmoid(number):
    e = math.exp(-number)
    denominator = 1 + e
    return 1/denominator

#dot products review w/ weights and adds bias term
def dot_product(review):
    dp = 0
    for i in range(len(review.features)):
        dp += review.features[i] * weights[i]
    dp += weights[len(weights) -1] #for bias value
    return sigmoid(dp)

#performs dot product and classifys review, 1 -> pos, 0 -> neg
def classify(review):
    if dot_product(review) > 0.5:
        return 1
    else:
        return 0

#performs gradient descent
def gradient_descent(review, exp_val):
    #exp_val is the expected value
    val = dot_product(review) - exp_val
    gradient = []
    for f in review.features:
        gradient.append(val*f)
    gradient.append(val) #for the bias term
    for i in range(len(weights)):
        weights[i] -= (learn_rate*gradient[i])
    return weights

#performs batch graident, ie, returns avg of the gradients of every review
def batch_gradient(reviews):
    #reviews is a dictionary of reviews and their expected value
    #g_avg is a list of all the gradient components summed together, ie, g_avg[0] = SUM(weights[0] from 1 to n)
    #initializing g_avg with all zeros
    g_avg = []
    for i in range(len(weights)):
        g_avg.append(0)
    #getting avg gradient for all data points
    for r,e in reviews:
        gd = gradient_descent(r,e)
        for i in range(len(gd)):
            g_avg[i] += gd[i]
    for gr in g_avg:
        gr /= len(reviews)
    return gr

def main():
    path1 = input("enter negative reviews dir: ")+'/*.txt'
    path2 = input("enter pos review dir: ")+'/*.txt'
    fr.read_folder(fr,path1,0)
    fr.read_folder(fr,path2,1)
    keys = list(fr.reviews.keys())
    random.shuffle(keys)
    random.shuffle(keys)
    data = keys[0:int(len(keys) * 0.75)]
    incorrect = 0
    for key in keys:
        c = classify(key)
        if c != fr.reviews[key]:
            incorrect +=1
        weights = gradient_descent(key, fr.reviews[key])
        """ THIS IS FOR TESTING, DELETE WHEN FINISHED
        print("original classification: " + (str)(fr.reviews[key]))
        print("machine classification: " + (str)(c))
        print(weights)
        """
    print("reviews misclassified: "+str(incorrect))
    print("percentage misclassified: " + str(incorrect/len(data)))
main()
