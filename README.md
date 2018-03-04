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

stop confusion between priority of alternate meanings in wordnet e.g

	how long in the oven

is interpreted as

	('how', 'long', 'oven', 'long')

but actually long should not be used as a verb here

one way to fix this is to look at the number of meanings of 'long' that are verbs vs nouns
or do not allow word to appear in 2 different parts of sentence (beware of mix!)

OR: if at the end of parsing a word does appear twice use the most probable form (using wordnet synonyms) to distinguish

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

currently there is an issue with only having one subject / verb returned from parse_query(): curently if there is a definitive article in the query we use that to find which noun is the subject. However if there are multiple nouns in the query it will only ever know about one. This means more complex query types are not supported, such as asking about the relation between 2 things. I'm working on this at the moment, but it is tricky as it is very likely the other noun is not tagged as NN by the postagger, but adding any noun interpretation of any word in the sentence to the subjects would be very confusing.
