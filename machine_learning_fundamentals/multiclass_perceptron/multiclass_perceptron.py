############################################################
# Multiclass Perceptron
# @author: kevin_alcedo
# 
# more info: www.wikipedia.org/wiki/Perceptron
# description: algorithm for supervised learning 
#              of multiclass classifiers 
############################################################

from collections import defaultdict
from operator import itemgetter

############################################################
# Model Class
############################################################

class MulticlassPerceptron(object):
    # input: list of training examples in the form of a tuple (x,y)
    #       x: feature vector
    #       y: multiclass label for given feature 

    def dot(self,x,y_i):
        # compute the dot product of the weight and the feature vector
        return sum(self.weights[y_i][x_i] * x[x_i] for x_i in x )

    def argmax(self,values):
        # return the max of the incoming list of feature-label pair
        return max(values,key=itemgetter(1))[0]

    def update_weights(self,y,y_pred,x):
        # given the prediction label update the weights
        for x_i in x:
            self.weights[y][x_i]      = self.weights[y][x_i]      + x[x_i]
            self.weights[y_pred][x_i] = self.weights[y_pred][x_i] - x[x_i] 

    def __init__(self, examples, iterations):
        # extract unique labels from training data
        unique_ys = list(set([y for x,y in examples]))

        # initialize weight vector to zero for each label
        # an integer defaultdict data structure is chosen so that a value of zero is default
        # this allows for efficient storage of sparse high-dimensional vectors
        self.weights =  {y:defaultdict(int) for y in unique_ys}

        # loop thru training data and adjust weight vector when missclassification
        for i in xrange(iterations):

            # go through all samples
            for x,y in examples:

                # predict the label with maximum values for a given feature*label
                y_pred = self.argmax( [ (y_i,self.dot(x,y_i)) for y_i in self.weights] )

                # if misclassified then update weights
                if y_pred != y:
                   self.update_weights(y,y_pred,x)

    def predict(self, x):
        # output: True or False
        # True  if dot(w,x) >  0
        # False if dot(w,x) <= 0 
        return self.argmax( [(y_i,self.dot(x,y_i)) for y_i in self.weights] )

############################################################
# Implementation of Multiclass Perceptron using Iris data
############################################################

class IrisClassifier(object):
    def __init__(self, data):
        # load and parse data
        # features will be kept as keys-value pairs
        train_data = [({x_i:value for x_i,value in enumerate(x) if x_i!=0.0} ,y) for x,y in data]

        # train multiclass perceptron given with the parsed data
        self.multi_percep =  MulticlassPerceptron(train_data, 10)
    
    def classify(self, instance):
        # load and parse test instance
        test_data = {x_i:value for x_i,value in enumerate(instance) if x_i!=0.0}
        # classify
        return (self.multi_percep).predict(test_data)

############################################################
# Implementation of Multiclass Perceptron using Digits data
############################################################

class DigitClassifier(object):

    def __init__(self, data):
        # load and parse data
        # features will be kept as keys-value pairs
        train_data = [({x_i:value for x_i,value in enumerate(x) if x_i!=0.0} ,y) for x,y in data]

        # train multiclass perceptron given with the parsed data
        self.multi_percep =  MulticlassPerceptron(train_data, 10)

    def classify(self, instance):
        # load and parse test instance
        test_data = {x_i:value for x_i,value in enumerate(instance) if x_i!=0.0}
        # classify
        return (self.multi_percep).predict(test_data)