import re

def display_options():
	print "conversion options are:"
	print "tbsp - ml"
	print "tsp  - ml"
	print "tbsp - tsp"
	print "oz   - ml"
	print "g    - ml"
	print "cup  - ml"
	print "pint - ml"
	print "and vice versa"

def answer(input):
	input = re.sub("convert ", "", input)
	parts = input.split(" ")

	if (len(parts)==0):
		display_options()

	if (len(parts)==1):
		print "you need another unit to convert into"
		display_options()

	if (len(parts)==2):
		result = 0
		amount = int(re.findall(r'\d*', parts[0])[0])
		unit1 = re.findall(r'\D+', parts[0])[0]
		print unit1
		unit2= parts[1]
		print str(amount) + ":" + str(unit1) + "->" + str(unit2)
		if (unit1=='tbsp'):
			if (unit2=="tsp"):
				result =  tablespoon_teaspoon(amount)
			if (unit2=='ml'):
				result = tablespoon_ml(amount)
		elif (unit1=='tsp'):
			if (unit2=="tbsp"):
				result =  teaspoon_tablespoon(amount)
			if (unit2=='ml'):
				result = teaspoon_ml(amount)
		elif (unit1=='oz'):
			if (unit2=='ml'):
				result = oz_ml(amount)
		elif (unit1=='g'):	
			if (unit2=='ml'):
				result = g_ml(amount)
		elif (unit1=='cup'):
			if (unit2=='ml'):
				result = cup_ml(amount)
		elif (unit1=='pint'):
			if (unit2=='ml'):
				result = pint_ml(amount)
		elif (unit1=='ml'):
			if (unit2=='tbsp'):
				result = ml_tablespoon(amount)
			elif (unit2=='tsp'):
				result = ml_teaspoon(amount)
			elif (unit2=='oz'):
				result = ml_oz(amount)
			elif (unit2=='g'):	
				result = ml_g(amount)
			elif (unit2=='cup'):
				result = ml_cup(amount)
			elif (unit2=='pint'):
				result = ml_pint(amount)
		print parts[0] + " is " + str(result) + unit2
		#parse 1st
		#parse 2nd as unit

def tablespoon_ml(amount):
	return amount * 15
def ml_tablespoon(amount):
	return amount / 15

def teaspoon_ml(amount):
	return 5 * amount
def ml_teaspoon(amount):
	return amount / 5

def tablespoon_teaspoon(amount):
	return 3 * amount
def teaspoon_tablespoon(amount):
	return amount / 3

def oz_ml(amount):
	return amount*28.4131
def ml_oz(amount):
	return amount/28.4131

def g_oz(amount):
	return amount * 0.035274
def oz_g(amount):
	return amount / 0.035274

def cup_ml(amount):
	return amount * 250
def ml_cup(amount):
	return amount/250

def pint_ml(amount):
	return amount*600
def ml_pint(amount):
	return amount/600
