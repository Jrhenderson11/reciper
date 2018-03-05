# reciper
A natural language processing recipe based question answering system

## Description:

A system for interpreting and querying a knowledge base from a recipe
When the program is loaded it reads a file and starts a querying interface, which the 
user can ask questions to.

It uses several natural language processing techniques to analyse both the question and recipe text to come up with an answer, see the **Technical details** section for more info

Whilst this project is a question answering system it is only used on a very localised domain, this means lots of research on question answering / techniques used in the field are not relevant here, especially if they incorporate lots of Information Retreival methods. Here the problem is largely to do with disambiguating word meanings and preventing false positives.

-------------------------------------------------
## Usage:

	python reciper.py <RECIPE FILE>?

if no file is given it will prompt for one

	python wordnet.py

useful interface for querying wordnet synonym information


-------------------------------------------------
## Files:

### Main functionality:

**reciper.py**: main file that displays interface and answers very simple queries

**parser.py**: responsible for parsing questions and extracting other useful text information

**answerer.py**: part that is given a question and some recipe text and attempts to answer the question

**wordnet.py**: interfaces with nltk wordnet to find synonyms, hypernyms and hyponyms of words, this allows **parser** and **answerer** to explore different meanings of a word e.g cook and bake being similar, mix being a verb and a noun

### Other functionality:

**utils.py**: some useful output functions

**filehandling.py**: basic file io

**conversions.py**: handles unit conversion queries

### Other files:

**Recipe**: a BBC recipe for apple crumble (https://www.bbc.co.uk/food/recipes/applecrumble_2971)

**Kimichi**: a BBC recipe for quick kimichi (to test how well system generalises)

**DEMO QUESTIONS**: some example questions users have asked the system that I need to implement

**postagger.pickle**: a pre-trained part of speech tagger (uses trigrams but can't remember what i trained it on)

-------------------------------------------------

## TODO:

apply QA technique: Category specific transformation rules (hand crafted)
Where-Q insert "is" to all possible locations e.g

–"where is the louvre museum located" 

–is the louvre located

–the is louvre museum located 

–the louvre is museum located 

–the louvre museum is located

improve recognition of verbs and subjects with wordnet and reduce false positives

-------------------------------------------------
## Technical details:

reciper.py is the main interface to the program, when it is called it reads a specified recipe file and uses the split function to divide it into Description, Ingredients and Method section. It then presents a query prompt which the user can type questions into.

The user input first gets passed into simple_query() which will see if it matches some hard coded instructions which are:

 - description: displays description
 - ingredients: nicely displays ingredients
 - method / instructions: nicely displays method
 - current / current step / current instruction: displays current step in method
 - next / next step / next instruction: displays next step in method
 - step *i*: shows step number i
 - convert: displays available conversions
 - convert *x***unit1** **unit2**: converts x of unit 1 to unit 2

if none of these match the instruction then it passes the user input to **parser.parse_query()**

The aim of **parse_query()** is to extract a tuple of question word, adjective, subject and verb from the query. These 4 things roughly describe the query. 

This is done with a Part of Speech (POS) tagger, which uses a pre-trained model to decide the type of word (https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html).
 This will identify word types such as nouns, verbs, adjectives and question words quite well, however as we are interested in such a specific domain (food and cooking and kitchen utensils) this dataset is too general and doesn't always correctky identify words, especially nouns like oven / spoon. Additionally it frequently goes for the most obvious meaning of a word which can be problematic. For example:

	how much mix should I add?


is parsed correctly as 

```
	[('how', u'WRB'), ('much', u'JJ'), ('mix', u'NN'), ('should', u'MD'), ('i', None), ('add', u'VB'), ('?', u'.')]

	question parts: 
	question  adjective  subject  verb
	('how',   'much',    'mix',   'add')

```
 
(we can see that 'mix' is tagged as NN which means it is a noun) 

However the sentence:

	when do I mix the fruit
is interpreted as
```
	[('when', u'WRB'), ('do', u'VBP'), ('i', None), ('mix', u'NN'), ('the', u'DT'), ('fruit', None)]
```

see that 'mix' is still a noun and not correctly interpreted as a verb.

Therefore I have an additional layer of inference. When a question has no subject that it can find or no verb I use wordnet.
Wordnet is massive network of words, their semantics, synonyms, hypernyms and hyponyms.
This means that wordnet can very accurately tell the meaning of a word, all its additional interpretations, and words it is related to. So for example the full list of meanings, hypernyms and hyponyms for the word 'mix': 
	
	['mix.n.01', 'mix.n.02', 'mix.n.03', 'blend.v.03', 'desegregate.v.01', 'mix.v.03', 'mix.v.04', 'mix.v.05', 'shuffle.v.03']

So by looking at the letter in between the dots we can see that mix is sometimes a noun but also has lots of interpretations as a verb, so if we see no other verb then this is our verb.

This technique can also be applied to find missing nounx/subjects from a query. In the query

	how much flour do I add?

the parts of speech are:

	[('how', u'WRB'), ('much', u'JJ'), ('flour', None), ('do', u'VBP'), ('i', None), ('add', u'VB'), ('?', u'.')]

and we see 'flour' is not correctly identified as a noun. So now we take a look at the wordnet interpretations:

	['foodstuff', 'dredge', 'convert', 'plain_flour', 'semolina', 'soybean_meal', 'wheat_flour']

We can see that one of the hypernyms of flour is foodstuff, so we select it as our subject. More generally any hypernym / additional meaning that contains the word "food" is a probable subject.

Currently there is an issue with only having one subject / verb returned from parse_query(): curently if there is a definitive article in the query we use that to find which noun is the subject. However if there are multiple nouns in the query it will only ever know about one. This means more complex query types are not supported, such as asking about the relation between 2 things. I'm working on this at the moment, but it is tricky as it is very likely the other noun is not tagged as NN by the postagger, but adding any noun interpretation of any word in the sentence to the subjects would be very confusing.

Also, many user querieswill not actually have all the parts of the query we look for. for example if no verb is found the parser will switch to the backup synonym checking system to find a verb. This can be problematic:

	how long in the oven?

would be parsed as 

	('how', 'long', 'oven', 'long')

so long is identified first as an adjective, and then again as a verb, even though that is not its meaning. So at the end of parse_query() if an adjective and verb match, or a noun and verb match I try to choose which one it is.

at first I just looked at the number of meanings in wordnet.get_full_meaning() that were verbs as opposed to nouns or adjectives as opposed to nouns. This works in some situations but not others. For example the query

	how much flour?

is now parsed as 

	('how', 'much', '', 'flour')

because there are multiple interpretations for the verb flour but only one interpretation as a noun. This is because currently my wordnet interpretation gives no idea of confidence, or how frequentl it is used as a noun vs verb. The way I currently fix it is by not just choosing by number of interpretations in wordnet, but also saying that if its noun interpretation is a type of food this is more important than its verb meaning and the subject is preferred over the verb.

This still does not work for differentiation between the meaning of 'butter' in:

	when do I add the butter?

	when do I butter the dish?

possible remedies for this include looking at word embeddings to examine context, or to use actual parsing to see if butter is in the place of a VP or NP 


Once the query has been parsed **answerer.py** takes care of answering the question. This is done using simple regualr expressions and some hard coded if statements, for instance if the question is a 'how long' question then answerer looks through the steps for a combination of the questoin subject, verb and a regular expression matching an amount of time. Most other questions are answered this way, the complex NLP stuff is in the interpretation of the question, then it is answered by searching the recipe for answers more simply.
