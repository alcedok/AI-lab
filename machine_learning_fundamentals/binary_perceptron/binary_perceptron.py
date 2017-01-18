############################################################
# Binary Perceptron
# @author: kevin_alcedo
# 
# more info: www.wikipedia.org/wiki/Perceptron
# description: algorithm for supervised learning 
#              of binary classifiers 
############################################################

from collections import defaultdict

############################################################
# Model Class
############################################################

class BinaryPerceptron(object):
    # input: list of training examples in the form of a tuple (x,y)
    #       x: feature vector
    #       y: binary label for given feature 

    def dot(self,x):
        # compute the dot product of the weight and the feature vector
        return sum(self.weights[x_i] * x[x_i] for x_i in x )

    def sign(self,value):
        # compute the sign of the prediction
        if value >= 0: return True
        else: return False

    def update_weights(self,y,x):
        # given the prediction label update the weights
        if y: 
            for x_i in x:
                self.weights[x_i] = self.weights[x_i] + x[x_i]
        else:
            for x_i in x:
                self.weights[x_i] = self.weights[x_i] - x[x_i]

    def __init__(self, examples, iterations):
        # initialize weight vector to zero
        # an integer defaultdict data structure is chosen so that a value of zero is default
        # this allows for efficient storage of sparse high-dimensional vectors
        self.weights =  defaultdict(int)

        # loop thru training data and adjust weight vector when missclassification
        for i in xrange(iterations):

            # go through all samples
            for x,y in examples:

                # for the given feature predict label
                y_pred = self.sign(self.dot(x))
                # if misclassified then update weights
                if y_pred != y:
                    # depending on the label update the weights
                    self.update_weights(y,x)
    
    def predict(self, x):
        # output: True or False
        # True  if dot(w,x) >  0
        # False if dot(w,x) =< 0 
        return self.sign(self.dot(x))

############################################################
# Implementation of Binary Perceptron with bias 
############################################################

class BiasClassifier(object):

    def __init__(self, data):
        # load and parse data
        # features will be kept as keys-value pairs
        # add a bias term of 1.0
        train_data = [({'x0':1.0,'x1':x } ,y) for x,y in data]

        # train multiclass perceptron given with the parsed data
        self.multi_percep =  BinaryPerceptron(train_data, 10)

    def classify(self, instance):
        # load and parse test instance
        # add a bias term of 1.0
        test_data = {'x0':1.0,'x1':instance}
        # classify
        return (self.multi_percep).predict(test_data)

############################################################
# Implementation of Binary Perceptron using 
# feature expansion and bias
############################################################

class MysteryClassifier1(object):

    def __init__(self, data):
        # load and parse data
        # features will be kept as keys-value pairs

        # by plotting the 2D data we found that a feature composed of 
        # x1*x1+x2*x2 can discriminate between labels
        # we also added a bias term
        train_data = [({'x0':1.0,'x1':x1,'x2':x2,'x3':x1*x1+x2*x2} ,y) for (x1,x2),y in data]

        # train binary perceptron given with the parsed data
        self.multi_percep =  BinaryPerceptron(train_data, 10)

    def classify(self, instance):
        # load and parse test instance
        x1 = instance[0]
        x2 = instance[1]
        x3 = instance[0]*instance[0]+instance[1]*instance[1]
        # test_data = {'x0':1.0,'x1':x1,'x2':x2,'x3':x3}
        test_data = {'x0':1.0,'x1':x1,'x2':x2,'x3':x3}

        # classify
        return (self.multi_percep).predict(test_data)

############################################################
# Implementation of Binary Perceptron using 
# feature expansion and bias
############################################################

class MysteryClassifier2(object):

    def __init__(self, data):
        # load and parse data
        # features will be kept as keys-value pairs
        # we chose our features by vizualizing the 3D data 
        # we also added a bias term
        train_data = [({'x0':1.0,'x1':x1*x2*x3} ,y) for (x1,x2,x3),y in data]

        # train binary perceptron given with the parsed data
        self.multi_percep =  BinaryPerceptron(train_data, 10)

    def classify(self, instance):
        # load and parse test instance
        x1 = instance[0]*instance[1]*instance[2]
        test_data = {'x0':1.0,'x1':x1}

        # classify
        return (self.multi_percep).predict(test_data)
