import re
import os
import nltk
import pickle
import string
import wordnet
from os import listdir
from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.tag import DefaultTagger
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger

def get_steps(method):
	steps = []
	for line in method.split("\n"):
		if (not line.strip()==""):
			steps.append(line)
	return steps

def get_tokenised(text):
	allwords = (word_tokenize(text))
	#remove punctuation
	punctuation = {".", ",", "?"}
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
		
	#tagged[0][0] is word,  tagged[0][1] is tag
	#first index is word index, 2nd is word / tag
	tagged = postag(words)
	print tagged

	#analyze questions
	question = ""
	adj = ""
	subject = ""
	verb = ""
	for i in range(len(tagged)):
		tag = tagged[i]
		if not tag[1] is None:
			if (tag[1] == 'WRB' or tag[1]=='WP'):
				question = tag[0]
			if (tag[1] == 'JJ'):
				adj = tag[0]
			if (tag[1]=='VB'):
				verb = tag[0]
			if (tag[1]=='DT'):
				print "DT"
				#look for noun
				for j in range(i, len(tagged)):
					print ""
					if tagged[j][1] == 'NN':
						subject = tagged[j][0]
					if (tagged[j][1] is None and '.n.' in str(wordnet.get_full_meaning(tagged[j][0]))):
						subject=tagged[j][0]
						break
			if ('NN' in tag[1]):
				subject = tag[0]
		else:
			print wordnet.get_full_meaning(tag[0])

	# Now use wordnet
	#ORDER BY NUM WITH .v.
	if (subject==''):
		print "	USING WORDNET FOR SUBJECT HYPERNYMS"
		for word in words:
			hypers = wordnet.get_all_related(word)
			print word + ": " + str(hypers)
			if len(re.findall(r'food|kitchen|spice|cutlery', str(hypers))) > 0:
				subject = word

	if (verb==''):
		print "	USING WORDNET FOR VERB HYPERNYMS"
		for word in words:

			hypers = wordnet.get_full_meaning(word)
			print word + ": " + str(hypers)
			if ".v." in str(hypers):
				verb = word		

	#what is question???
	if (question==''):
		#Do I need
		if "need" in input:
			question="need"
			if verb =="need":
				verb="" 

	if (verb==subject):
		if (wordnet.noun_or_verb(subject)==True):
			print "removing verb " + subject
			verb = ""
		else:
			print "removing subject " + subject
			subject = ""

	if (adj==verb):
		if (wordnet.adj_or_verb(subject)==True):
			print "removing verb " + subject
			verb = ""
		else:
			print "removing adj " + subject
			adj = ""


	print (question, adj, subject, verb)

	return (question, adj, subject, verb)