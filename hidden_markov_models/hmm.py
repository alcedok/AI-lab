############################################################
# POS-tagger Hidden Markov Models
# @author: kevin_alcedo
# 
# more info: www.wikipedia.org/wiki/Hidden_Markov_model
# description: an HMM is trained using the brown corpus 
#              to create a part-of-speech tagger.
#              this is particularly useful in computational
#              linguistics. 
############################################################

from collections import defaultdict,deque,Counter
import math
import operator

############################################################
# Hidden Markov Models
############################################################

def load_corpus(path):

	with open(path,'r') as txtfile:
		 POS_tagged_sentences = [[tuple(word.split('=')) for word in sentence.split()] for sentence in  txtfile]
	return POS_tagged_sentences

class Tagger(object):

	def init_tag_probs_calc(self,sentences,smoothing):
		# calculate probaility of a tag given that its the first word of a sentence 
		# count number of times tag occurs at the beginning of sentence
		# count number of sentences

		# collect first tag in sentence
		collect_firsts = [ sentence[0][1] for sentence in sentences]

		# count number of times tag occurs at the beginning of sentence 
		init_tag_counts = defaultdict(int)
		for tag in collect_firsts:
			init_tag_counts[tag]+=1

		num_sentences = len(sentences)
		num_tags = len(self.unique_POS)
		# probaility that sentence begins with tag
		init_tag_probs = {tag: math.log(1.0*count / (num_sentences)) for tag, count in init_tag_counts.items()}

		return init_tag_probs

	def trans_probs_calc(self,sentences,smoothing):
		# calculate probability of a tag sequence occurs , bigram of tags: i,e (DET,NOUN)
		# count number of times a particular tag sequence occurs at the beginning of sentence
		# count number of total sequences

		# create dictionary that maps POS_i -> POS_j
		# go thru every sentence, and every element in the sentence
		POSi_POSj_counts = {POS:deque() for POS in self.unique_POS}
		# print POSi_POSj_counts
		{(POSi_POSj_counts[sentence[i][1]]).append(sentence[i+1][1]) for sentence in sentences for i in xrange(len(sentence)-1)}

		# go through dictionary and create a counter of POS in order to calculate probabilities
		for POS in POSi_POSj_counts:
			POSi_POSj_counts[POS] = Counter(POSi_POSj_counts[POS])

		num_tag_per_tag = {tag: (sum(POSi_POSj_counts[tag][word] for word in POSi_POSj_counts[tag]),len(POSi_POSj_counts[tag])) for tag in POSi_POSj_counts }
		# emission probability of tagi given tagj
		trans_tag_probs = {}
		for tag in POSi_POSj_counts:
			trans_tag_probs[tag] = { word: math.log((count + 1.0*smoothing)/ (num_tag_per_tag[tag][0] + smoothing*(num_tag_per_tag[tag][1]+1))) for word,count in POSi_POSj_counts[tag].items()}
		
		# add UNK and it's Laplace-smooted log probability to dictionary 
		for tag in POSi_POSj_counts:
			trans_tag_probs[tag]['<UNK>'] = math.log((1.0*smoothing)/ (num_tag_per_tag[tag][0] + smoothing*(num_tag_per_tag[tag][1])+1))
		
		return trans_tag_probs

	def emission_probs_calc(self,sentences,smoothing):
		# calculate probaility of a word given a tag
		# count number of times a particular word occurs for a given tag
		# count number of total words in a given tag

		# create dictionary that maps POS -> words
		# go thru every sentence, and every element in the sentnce
		POS_word_counts = {POS:deque() for POS in self.unique_POS}
		{(POS_word_counts[POS]).append(word) for sentence in sentences for word,POS in sentence}

		# go through dictionary and create a counter of words in order to calculate probabilities
		for POS in POS_word_counts:
			POS_word_counts[POS] = Counter(POS_word_counts[POS])
		# tuple of : total number of words per tag , unique words per tag
		num_words_per_tag = {tag: (sum(POS_word_counts[tag][word] for word in POS_word_counts[tag]),len(POS_word_counts[tag])) for tag in POS_word_counts }

		# emission probability of word given a tag
		emission_probs = {}
		for tag in POS_word_counts:
			emission_probs[tag] = { word: math.log((count + 1.0*smoothing)/ (num_words_per_tag[tag][0] + smoothing*(num_words_per_tag[tag][1]+1))) for word,count in POS_word_counts[tag].items()}
		
		# add UNK and it's Laplace-smooted log probability to dictionary 
		for tag in POS_word_counts:
			emission_probs[tag]['<UNK>'] = math.log((1.0*smoothing)		/ (num_words_per_tag[tag][0] + smoothing*(num_words_per_tag[tag][1])+1))
		
		return emission_probs

	def __init__(self, sentences):
		smoothing = 1e-3
		self.unique_POS = ['ADJ','VERB','ADP','NOUN','DET','.','ADV','PRON','NUM','CONJ','PRT','X']
		self.init_tag_probs = self.init_tag_probs_calc(sentences,smoothing)
		self.trans_probs 	= self.trans_probs_calc(sentences,smoothing)
		self.emission_probs = self.emission_probs_calc(sentences,smoothing)

		pass

	def most_probable_tags(self, tokens):
		# returns a list of the most probable tags for each input token
		# collect all (tag,word_probability) for each tag and choose the tag of maximum probaility
		most_probable_tags = []
		for token in tokens:
			current_possibilities = []
			for tag in self.emission_probs:
				current_token = token
				if token not in self.emission_probs[tag]:
					current_token = '<UNK>'
				current_possibilities.append((tag,self.emission_probs[tag][current_token]))
			most_probable_tags.append(max(current_possibilities,key=operator.itemgetter(1))[0])

		return most_probable_tags

	def viterbi_tags(self, tokens):
		Viterbi = [{}]
		# calculate probability of initial tag given first word
		for tag in self.unique_POS:
			current_token = tokens[0]
			if current_token not in self.emission_probs[tag]:
				current_token = '<UNK>'
			Viterbi[0][tag] = self.init_tag_probs[tag] + self.emission_probs[tag][current_token]
		
		# go through Viterbi Algorithm Decoding
		for n in xrange(1,len(tokens)):
			Viterbi.append({})
			for current_tag in self.unique_POS:
				current_probabilities = []
				for prev_tag in self.unique_POS:				
					current_token = tokens[n]
					if current_token not in self.emission_probs[current_tag]:
						current_token = '<UNK>'

					current_probabilities.append(Viterbi[n-1][prev_tag]+self.trans_probs[prev_tag][current_tag]+self.emission_probs[current_tag][current_token])
				# choose max
				Viterbi[n][current_tag] = max(current_probabilities)

		tag_seq = []
		for column in Viterbi:
			tag_seq.append( (max(column.iteritems(),key=operator.itemgetter(1)))[0])
		return tag_seq