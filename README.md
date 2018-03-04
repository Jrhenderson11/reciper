# reciper
A natural language processing recipe based question answering system

## Description:

A system for interpreting and querying a knowledge base from a recipe
When the program is loaded it reads a file and starts a querying interface, which the 
user can ask questions to.

It uses several natural language processing techniques to analyse both the question and recipe text to come up with an answer, see the **Technical details** section for more info

-------------------------------------------------
## Usage:

	python reciper.py <RECIPE FILE>?

if no file is given it will prompt for one

	python wordnet.py

useful interface for querying wordnet synonym information


-------------------------------------------------
## Files:

#### Main functionality:

**reciper.py**: main file that displays interface and answers very simple queries

**parser.py**: responsible for parsing questions and extracting other useful text information

**answerer.py**: part that is given a question and some recipe text and attempts to answer the question

**wordnet.py**: interfaces with nltk wordnet to find synonyms, hypernyms and hyponyms of words, this allows **parser** and **answerer** to explore different meanings of a word e.g cook and bake being similar, mix being a verb and a noun

#### Other functionality:

**utils.py**: some useful output functions

**filehandling.py**: basic file io

**conversions.py**: handles unit conversion queries

#### Other files:

**Recipe**: a BBC recipe for apple crumble (https://www.bbc.co.uk/food/recipes/applecrumble_2971)

**Kimichi**: a BBC recipe for quick kimichi (to test how well system generalises)

**DEMO QUESTIONS**: some example questions users have asked the system that I need to implement

**postagger.pickle**: a pre-trained part of speech tagger (uses trigrams but can't remember what i trained it on)
-------------------------------------------------