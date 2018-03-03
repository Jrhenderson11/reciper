import utils
import parser

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
		elif (not verb == ""):
			#look for verb
			print "looking for adj for " + verb
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
				print "	< STEP " + str(i) + ">"
				print step
				print "--------------------------"
				break
			i = i+1


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