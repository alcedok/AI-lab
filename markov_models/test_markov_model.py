############################################################
# Unit Test of Markov Model
############################################################

from markov_model import *
import unittest

class MM_TestCase(unittest.TestCase):
	def test_tokenize(self):
		print " test_tokenize "
		text1 = "  This is an_example.  "
		# ['This', 'is', 'an', 'example', '.']
		text2 = "'Medium-rare.'' she_said!."
		# ["'", 'Medium', '-', 'rare', ',', "'", 'she', 'said', '.']
		print tokenize(text2)
		print 

		pass


	def test_ngrams(self):
		print " test_ngrams "
		ngrams(1, ["a", "b", "c"])
		# [((), 'a'), ((), 'b'), ((), 'c'),((), '<END>')]
		ngrams(2, ["a", "b", "c"])
		# [(('<START>',), 'a'), (('a',), 'b'),(('b',), 'c'), (('c',), '<END>')]
		ngrams(3, ["a", "b", "c"])
		# [(('<START>', '<START>'), 'a'),(('<START>', 'a'), 'b'),(('a', 'b'), 'c'),(('b', 'c'), '<END>')]
		ngrams(4, ["a", "b", "c"])
		print 

		pass
	def test_update(self):
		print " test_update "
		m = NgramModel(1)
		m.update("a b c d")
		print m.count_dict_ngram
		print m.count_dict_context
		print
		m.update("a b a b")
		print m.count_dict_ngram
		print m.count_dict_context
		print 

		pass

	def test_prob(self):
		print " test_prob "
		m = NgramModel(1)
		m.update("a b c d")
		m.update("a b a b")
		print m.prob((), "a")
		# 0.3
		print m.prob((), "c")
		# 0.1
		print m.prob((), "<END>")
		# 0.2		
		m = NgramModel(2)
		m.update("a b c d")
		m.update("a b a b")
		print m.prob(("<START>",), "a")
		# 1.0
		print m.prob(("b",), "c")
		# 0.3333333333333333
		print m.prob(("a",), "x")
		# 0.0
		print 

		pass
	def test_random(self):
		print " test_random "
		m = NgramModel(1)
		m.update("a b c d")
		m.update("a b a b")
		random.seed(1)
		print [m.random_token(()) for i in range(25)]
		# ['<END>', 'c', 'b', 'a', 'a', 'a', 'b',
		# 'b', '<END>', '<END>', 'c', 'a', 'b',
		# '<END>', 'a', 'b', 'a', 'd', 'd',
		# '<END>', '<END>', 'b', 'd', 'a', 'a']	
		print
		m = NgramModel(2)
		m.update("a b c d")
		m.update("a b a b")
		random.seed(2)
		print [m.random_token(("<START>",)) for i in range(6)]
		# ['a', 'a', 'a', 'a', 'a', 'a']
		print [m.random_token(("b",)) for i in range(6)]
		# ['c', '<END>', 'a', 'a', 'a', '<END>']
		print 

		pass
	def test_random_text(self):
		print " test_random_text "
		m = NgramModel(1)
		m.update("a b c d")
		m.update("a b a b")
		random.seed(1)
		print m.random_text(13)
		# '<END> c b a a a b b <END> <END> c a b'
		print 
		# print
		m = NgramModel(3)
		m.update("a b c d")
		m.update("a b a b")
		random.seed(3)
		print m.random_text(15)
		# 'a b <END> a b c d <END> a b a b a b c'
		print
		pass

	def test_perplex(self):
		print " test_perplex "
		m = NgramModel(1)
		m.update("a b c d")
		m.update("a b a b")
		print m.perplexity("a b")
		# 3.815714141844439

		m = NgramModel(2)
		m.update("a b c d")
		m.update("a b a b")
		print m.perplexity("a b")
		# 1.4422495703074083
		print
		pass

	def test_create_ngram_model(self):
		print " test_create_ngram_model "
		# No random seeds, so your results may vary
		m = create_ngram_model(1, "frankenstein.txt"); 
		print m.random_text(15)
		# 'beat astonishment brought his for how , door <END> his . pertinacity to I felt'
		m = create_ngram_model(2, "frankenstein.txt"); 
		print m.random_text(15)
		# 'As the great was extreme during the end of being . <END> Fortunately the sun'
		m = create_ngram_model(3, "frankenstein.txt"); 
		print m.random_text(15)
		# 'I had so long inhabited . <END> You were thrown , by returning with greater'
		m = create_ngram_model(1, "frankenstein.txt");
		random.seed(2)
		print m.random_text(15)
		m = create_ngram_model(2, "frankenstein.txt");
		random.seed(2)
		print m.random_text(15)
		# 'We were soon joined by Elizabeth . <END> At these moments I wept bitterly and'
		print 


		pass
if __name__ == '__main__':
	unittest.main()

