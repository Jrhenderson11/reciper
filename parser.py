import re
import os
import nltk
import pickle
import string
#import Tagger
from os import listdir
from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.tag import DefaultTagger
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger
#brown.words()
#treebank.words()

def get_tokenised(text):
	allwords = (word_tokenize(text))
	#remove punctuation
	punctuation = {".", ","}
	words = []
	for word in allwords:
		if (word not in punctuation):
			words.append(word)
	return words

def postag(words):
	file = open("postagger.pickle", "rb")
	tagger = pickle.load(file)
	file.close()
	tagged = tagger.tag(words)
	return tagged

def parse_query(input):
	

	#split question into parts
	#lem and stem???
	words = get_tokenised(input)
	print words
	#remove punct

			
	#tagged[0][0] is word,  tagged[0][1] is tag
	#first index is word index, 2nd is word / tag
	tagged = postag(words)
	print tagged

	#analyze questions
	question = ""
	adj = ""
	subject = ""
	verb = ""
	for tag in tagged:
		if not tag[1] is None:
			if (tag[1] == 'WRB' or tag[1]=='WP'):
				question = tag[0]
			if (tag[1] == 'JJ'):
				adj = tag[0]
			if (tag[1]=='VB'):
				verb = tag[0]
			if ('NN' in tag[1]):
				subject = tag[0]

	print question
	print adj
	print subject
	print verb

	return (question, adj, subject, verb)

