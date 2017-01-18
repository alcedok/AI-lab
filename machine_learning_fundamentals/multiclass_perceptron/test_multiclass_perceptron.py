############################################################
# Unit Test of Multiclass Perceptron
############################################################

from multiclass_perceptron import *
import unittest
import cProfile
import multiclass_perceptron_data as data


class MulticlassPerceptron_TestCase(unittest.TestCase):
	def test_multiclass(self):
		print " test_multiclass "
		# Define the training data to be the corners and edge midpoints of the unit square
		train = [({"x1": 1}, 1), ({"x1": 1, "x2": 1}, 2), ({"x2": 1}, 3),({"x1": -1, "x2": 1}, 4), ({"x1": -1}, 5), ({"x1": -1, "x2": -1}, 6),({"x2": -1}, 7), ({"x1": 1, "x2": -1}, 8)]

		# Train the classifier for 10 iterations so that it can learn each class
		p = MulticlassPerceptron(train, 10)

		# Test whether the classifier correctly learned the training data
		print [p.predict(x) for x, y in train]
		# [1, 2, 3, 4, 5, 6, 7, 8]
		print 

		pass

	def test_iris(self):
		print " test_iris "
		c = IrisClassifier(data.iris)
		ans = c.classify((5.1, 3.5, 1.4, 0.2))
		print "My answer:" , ans
		print "Correct answer:" ,'iris-setosa'
		print
		c = IrisClassifier(data.iris)
		ans = c.classify((7.0, 3.2, 4.7, 1.4))
		print "My answer:" , ans
		print "Correct answer:" ,'iris-versicolor'
		print
		pass

	def test_dig(self):
		print " test_dig "
		c = DigitClassifier(data.digits)
		ans = c.classify((0,0,5,13,9,1,0,0,0,0,13,15,10,15,5,0,0,3,15,2,0,11,8,0,0,4,12,0,0,8,8,0,0,5,8,0,0,9,8,0,0,4,11,0,1,12,7,0,0,2,14,5,10,12,0,0,0,0,6,13,10,0,0,0))
		print "My answer:" , ans
		print "Correct answer:" ,0
		print 

		pass

if __name__ == '__main__':
	unittest.main()