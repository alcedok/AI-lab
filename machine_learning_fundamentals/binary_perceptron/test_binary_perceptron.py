############################################################
# Unit Test of Binary Perceptron
############################################################

from binary_perceptron import *
import unittest
import cProfile
import binary_perceptron_data as data


class BinaryPerceptron_TestCase(unittest.TestCase):
	def test_binary_perceptron(self):
		print " test_binary_perceptron "
		# Define the training and test data
		train = [({"x1": 1}, True), ({"x2": 1}, True), ({"x1": -1}, False),({"x2": -1}, False)]
		test = [{"x1": 1}, {"x1": 1, "x2": 1}, {"x1": -1, "x2": 1.5},{"x1": -0.5, "x2": -2}]

		# Train the classifier for one iteration
		p = BinaryPerceptron(train, 1)

		# Make predictions on the test data
		print [p.predict(x) for x in test]
		# [True, True, True, False]
		print 
		pass

	def test_bias(self):
		print " test_bias "
		c = BiasClassifier(data.bias)
		ans = [c.classify(x) for x in (-1, 0, 0.5, 1.5, 2)]
		print "My answer:" , ans
		print "Correct answer:" ,[False, False, False, True, True]
		print ans == [False, False, False, True, True]
		print
		pass

	def test_mistery1(self):
		print " test_mistery1 "
		c = MysteryClassifier1(data.mystery1)
		print [False, False, False, True, True] == [c.classify(x) for x in ((0, 0), (0, 1), (-1, 0), (1, 2), (-3, -4))]
		
		pass

	def test_mistery2(self):
		print " test_mistery2 "
		c = MysteryClassifier2(data.mystery2)
		print [True, False, False, True] == [c.classify(x) for x in ((1, 1, 1), (-1, -1, -1), (1, 2, -3), (-1, -2, 3))]
		
		pass
if __name__ == '__main__':
	unittest.main()