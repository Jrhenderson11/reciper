def readfile(fname):
	file = open(fname)
	text = file.read()
	file.close()
	return text

