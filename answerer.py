import re
import utils
import parser
import wordnet

def answer_question(query, text):
	(desc, ingredients, method) = text
	(question, adj, subject, verb) = query

	if (question=='why'):
		print "because " + subject + " is " + adj
	if (question == 'how'):

		if (adj=='much' or adj=='many'):
			#basic: look in ingredients for subj
			if (not subject == ""):
				quantity_of(subject, ingredients)
		elif (adj=='hot'):
			#query temp
			print "temp query"
			find_temperature(method)
		elif (adj=='long'):
			#look through steps for time using FOR __ MINUTES / HOURS or UNTIL
			#get steps with verb same as when
			found = False
			for step in parser.get_steps(method):
				
				if (subject in step and (verb + " " in step)):
					found = True
					matches =re.findall(r'.* (min(ute)?|hour|second)s?' , step) 
					if (len(matches) > 0):
						utils.printgreen(step)
			if (found==False):
				print "LOOKING AT SYNONYMS"
				#start searching synonyms
				for step in parser.get_steps(method):
					synonyms = wordnet.get_all_related(verb)
					if not synonyms is None:
						for synonym in synonyms:
							if (subject in step and (synonym in step)):
								found = True
								
								if (len(re.findall(r'.* (min(ute)?|hour|second)s?' , step)) > 0):
									utils.printgreen(step)
									break
					if found==True:
						break
			if found==False:
				find_times(desc)

		elif (not verb == ""):
			#look for verb
			print "looking for adverb for " + verb
			#look for adverb (RB, RBR, RBS)
			#print "method:" + method
			for line in method.split("\n"):
				if (verb in line):
					#print "found " + verb + " in " + line
					utils.printgreen(line)
					words = parser.get_tokenised(line)
					for taggedword in parser.postag(words):
						tag = taggedword[1]
						word = taggedword[0]
						if (not tag is None):
							if (tag[0]=='R'):
								utils.printgreen("ADVERB: " + word)
	elif (question == 'when'):
		#look for subject and verb combo in a step
		i=0
		for step in parser.get_steps(method):
			if (verb in step) and subject in step:
				utils.printgreen("	< STEP " + str(i) + ">")
				utils.printgreen(step)
				utils.printgreen("--------------------------")
				break
			i = i+1
	elif (question=='what'):
		#synonyms temp
		if (subject=='temperature' or 'temperature' in wordnet.get_all_related(subject) or 'heat' in wordnet.get_all_related(adj) or 'hot' in wordnet.get_all_related(adj)):
			find_temperature(method)
	elif (question=="need"):
		#look through inredients for subj
		if not subject == '':
			quantity_of(subject, ingredients)

def get_ingredient_lines(subject, ingredients):
	found = False
	lines = []
	for line in ingredients.split("\n"):
		if (subject in line):
			lines.append(line)
			#print "found " + subject + " in " + line
			#print "TRYING TO PARSE"
	
	return lines

def quantity_of(subject, ingredients):
	quantity = ""
	forchunks = ingredients.split("\n\n")
	#print forchunks
	for part in forchunks:
		if (not (part.strip() == "")):
			useful = get_ingredient_lines(subject, part)
			if len(useful) > 0:
				print part.strip().split("\n")[0]
			for line in useful:
				utils.printgreen(line)
				if ('of' in line):
					quantity = line.split("of")[0].strip()

				#print "quantity: " + quantity			

def find_temperature(method):
	#oven to
	#bake at
	# ___ at ___C
	for step in parser.get_steps(method):
		if (len(re.findall("oven to", step))>0) or (len(re.findall("bake at", step))>0) or (len(re.findall(r"Gas\s?\d", step))>0) or(len(re.findall(r"\d*c\W", step))>0) or (len(re.findall(r"\df", step))>0):
			utils.printgreen(step)

def find_times(text):
	for line in text.split("\n"):
		if (len(re.findall(r'.* (min(ute)?|hour|second)s?', line)) > 0):
			utils.printgreen(line)