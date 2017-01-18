############################################################
# Markov Model
# @author: kevin_alcedo
# 
# more info: www.wikipedia.org/wiki/Markov_chain
# description: Markov Model used as a text generator 
############################################################

import re
import string
from collections import Counter,deque 
import random
import math

############################################################
# Markov Model
############################################################

def tokenize(text):
    # split by whitespaces, split words/numbers and punctuation
    return re.findall(r"[a-zA-Z0-9]+|[^\s]",text)

def ngrams(n, tokens):
        # pad the list of tokens with necessary number of 'starts' and 'ends' 
        pad_tokens = (n-1)*['<START>']+tokens+['<END>']
        # enumerate every token and if the index is >= to (n-1) then keep the (n-1) tokens in front of the current token
        return [ ( tuple(pad_tokens[abs(n-indx-1):indx]) ,token) for indx,token in enumerate(pad_tokens) if indx>=(n-1)]

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.count_dict_ngram = Counter()
        self.count_dict_context = Counter()
        self.context_to_word_dict = {}
        pass

    def update_vocabulary(self,new_ngram):

        # for each context,token pair in the new ngram add to the dictionary if exist, else create it
        for context, token in new_ngram:
            if context in (self.context_to_word_dict):
                (self.context_to_word_dict[context]).add(token)
            else: 
                (self.context_to_word_dict[context]) = set([token])

    def update(self, sentence):
        # tokenize incoming sentence
        tokenized = tokenize(sentence)
        # print tokenized
        # compute n-gram for sentence
        ngram = ngrams(self.n, tokenized)

        # update the vocabulary given the context
        # print ngram
        (self.update_vocabulary)(ngram)
        # (self.context_to_word_dict)( (self.context_to_word_dict[context]).add(token) for context, token in ngram )

        # update internal counts for ngram
        (self.count_dict_ngram).update(ngram)

        # update internal counts for context for each ngram
        (self.count_dict_context).update(elem[0] for elem in ngram)

    def prob(self, context, token):
        # calculate probability of the given context and ngram
        return 1.0*(self.count_dict_ngram[(context,token)])/(self.count_dict_context[(context)])

    def random_token(self, context):
        # return a random token from the probability distribution determined by incoming context

        # generate random number between [0.0,1.0)
        r = random.random()

        # for each token in the vocabulary for a given context 
        sum_p = 0
        # print self.context_to_word_dict[context]
        for token in sorted(self.context_to_word_dict[context]):
            # if the probability is > r then return it 
            if (self.prob(context,token)+sum_p > r) :
                return token
            # else sum up the next probability until its greater than r
            else: sum_p = sum_p + self.prob(context,token)

    def random_text(self, token_count):

        init_context = (self.n-1)*['<START>']
       
        context = deque(init_context)
        string = deque(context)
        for n in xrange(token_count):

            if self.n == 1: 
                context = init_context
            else: 
                # if the last token added was the special '<END>' then reset context to starting context
                if '<END>' == string[-1]:
                    context = deque(init_context)
                # else make the new context the last added (n-1) words + token
                else: 
                    context.popleft()
                    context.append(string[-1])

            string.append(self.random_token(tuple(context)))
        
        return ' '.join(string)

    def perplexity(self, sentence):
        # tokenize incoming sentence
        tokenized = tokenize(sentence)
        # compute n-gram for sentence
        ngram = ngrams(self.n, tokenized)
        return (1.0/(math.exp(sum(math.log(self.prob(context, token)) for context, token in ngram))))**(1.0/len(ngram))


def create_ngram_model(n, path):

    ngram_model = NgramModel(n)

    with open(path) as f:
        for line in f:
           ngram_model.update(line)

    return ngram_model
