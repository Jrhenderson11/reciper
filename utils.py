		#green: '\033[92m'
		# default: "\033[0m"
		#red: "\033[31m"
		#underlined \e[4m
		#Bold \e[1m
		#yellow \e[93m

def printgreen(text):
	print '\033[92m' + text + '\033[0m'


def get_steps(method):
	steps = []
	for line in method.split("\n"):
		if (not line.strip()==""):
			steps.append(line)
	return steps
