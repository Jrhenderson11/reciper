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
			print get_ingredient_lines(subject, ingredients)
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

def get_ingredient_lines(subject, ingredients):
	found = False
	lines = []
	for line in ingredients.split("\n"):
		if (subject in line):
			lines.append(line)
			utils.printgreen("found " + subject + " in " + line)
	return lines