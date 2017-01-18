from hmm import *
import unittest


class HMM_TestCase(unittest.TestCase):
	def test_load_corpus(self):
		print " test_load_corpus "

		c = load_corpus("brown_corpus.txt")
		print c[1402]
		# [('It', 'PRON'), ('made', 'VERB'),('him', 'PRON'), ('human', 'NOUN'),('.', '.')]

		c = load_corpus("brown_corpus.txt")
		print c[1799]
		# [('The', 'DET'), ('prospects', 'NOUN'),('look', 'VERB'), ('great', 'ADJ'),('.', '.')]

		pass


	def test_most_probable_tags(self):
		print " test_most_probable_tags "

		c = load_corpus("brown_corpus.txt")
		t = Tagger(c)
		print t.most_probable_tags(["The", "man", "walks", "."])
		# ['DET', 'NOUN', 'VERB', '.']

		c = load_corpus("brown_corpus.txt")
		t = Tagger(c)
		print t.most_probable_tags(["The", "blue", "bird", "sings"])
		# ['DET', 'ADJ', 'NOUN', 'VERB']
		

		print 
		pass

	def test_viterbi_tags(self):
		print " test_viterbi_tags "

		c = load_corpus("brown_corpus.txt")
		t = Tagger(c)
		s = "I am waiting to reply".split()
		print t.most_probable_tags(s)
		# ['PRON', 'VERB', 'VERB', 'PRT', 'NOUN']
		print t.viterbi_tags(s)
		# ['PRON', 'VERB', 'VERB', 'PRT', 'VERB']
		print "----"
		c = load_corpus("brown_corpus.txt")
		t = Tagger(c)
		s = "I saw the play".split()
		print t.most_probable_tags(s)
		# ['PRON', 'VERB', 'DET', 'VERB']
		print t.viterbi_tags(s)
		# ['PRON', 'VERB', 'DET', 'NOUN']
		

		pass

if __name__ == '__main__':
	unittest.main()




	