import re
import sys
import parser
import answerer
import conversions
import filehandling

step = 0


def split(text):
	description_text = ""
	ingredient_text = ""
	method_text = ""

	if ("ingredients" in text):
		description_text = text.split("description")[1].split("ingredients")[0].strip()
		text = text.split("ingredients")[1]
	if ("method" in text):
		ingredient_text = text.split("method")[0]
		method_text = text.split("method")[1]
	return (description_text, ingredient_text, method_text)


def simple_query(input, text, step):
	(desc, ingredients, method) = text
	steps = parser.get_steps(method)


	if len(re.findall(r'next( instruction| step)?', input)) > 0:
		if (not step==len(steps)):
			print steps[step+1]
			step = step + 1
		return True
	elif len(re.findall(r'current( instruction| step)?', input))>0:
		print "	- " + steps[step]
		return True
	elif ('description' in input):
		print "	< DESCRIPTION >"
		for line in desc.split("\n"): 
			print "  " + line
		print "--------------------------"

		return True
	elif ('ingredient' in input):
		print "		< INGREDIENTS LIST >"
		for line in ingredients.split("\n"): 
			print " - " + line
		print "--------------------------"
		return True
	elif ('method' in input or input.lower()=='instructions'):
		print "		< INSTRUCTIONS >"
		i=0
		for line in method.split("\n"):
			if (not line.strip()==""): 
				print str(i) + ") " + line
				i=i+1
			else:
				print line
		print "--------------------------"

		return True
	elif (re.match(r'step \d*', input)):
		num = int(re.sub("step ", "", input))
		print "	" + parser.get_steps(method)[num]
		return True
	elif ("convert" in input):
		conversions.answer(input)
		return True
	else:
		return False

def query_loop(text):
	step=0
	input = ""
	#quantity name
	lastinput = ""
	while (not (input == "quit" or input=="exit")):
		print "\033[93m"
		print "enter a query:\033[0m"
		input = raw_input()
		if not input.strip()=="":
			if ('\x1b' in input):
				input = lastinput
			input = input.lower()

			if (not simple_query(input, text, step)):
				query_type = parser.parse_query(input)
				answerer.answer_question(query_type, text)
			lastinput = input

if __name__ == '__main__':
	step = 0
	if len(sys.argv) >1:
		fname= sys.argv[1]
	else:
		print "enter recipe file to process:"
		fname = raw_input()
	text = filehandling.readfile(fname).lower()
	(desc, ingredients, method) = split(text)

	print "ready for queries"
	try:
		query_loop((desc, ingredients, method))
	except KeyboardInterrupt:
		print "done"