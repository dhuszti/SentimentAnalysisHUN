# -*- coding: utf-8 -*-
import os, sys, getopt, csv
from polyglot.text import Text
from itertools import chain

""" This python file contains functions for postprocessing phase of morphological and PoS analyzed data.
Functions:
- StopwordFilter: uses external stopword list to filter them out from input list.
- NumberFilter: uses a very light filtering of number characters out from input list. 
- NER_Dictionary: is a function for creating 3 Named Entity Recognition dictionaries (location, names, organizations) as return lists.
- NERFilter: uses dictionaries mainly created by NER_Dictionary to filter entities from input list.
"""

def StopWordFilter(sentencesArray, stopwordsFilePath):
	stopwords = []
	stopfile = open(stopwordsFilePath,'rb')
	for line in stopfile:
    		if not line.strip().startswith("#"):
        		stopwords.append(line.rstrip().decode('utf8'))

	filteredArray = []
	for sentence in sentencesArray:
		filteredSentence = []
		for word in sentence:
			# Decode word to unicode to be capable of doing comparison with same encoding
			if word.decode('latin2') not in stopwords:
				filteredSentence.append(word)
		filteredArray.append(filteredSentence)
		
	return filteredArray


def NumberFilter(sentencesArray):
	filteredArray = []
	for sentence in sentencesArray:
		filteredSentence = []
		for word in sentence:
			characters = set('0123456789')
			if not any((c in characters) for c in word):
				filteredSentence.append(word)
		filteredArray.append(filteredSentence)

	return filteredArray

# This function creates 3 dictionaries for location, person and organization. Important, every result set is in UNICODE encoding! 
def NER_Dictionary(CorpusFilePath):
	corpusfile = open(CorpusFilePath, 'rb')
	csvreader = csv.reader(corpusfile, delimiter='\t')

	locationList = []
	personList = []
	organizationList = []

	for line in csvreader:
		try:
			blob = str(line[4]).decode('latin2')
			text = Text(blob)
			for sent in text.sentences:
				for entity in sent.entities:
					tag = entity.tag
					for element in entity:
						if element.encode('latin2') not in chain(personList, locationList, organizationList):
							if 'PER' in tag:
								personList.append(element.encode('latin2'))
							elif 'LOC' in tag:
								locationList.append(element.encode('latin2'))
							elif 'ORG' in tag:
								organizationList.append(element.encode('latin2'))
		except:
			pass
	
	# Filter out some mistaken nouns
	person = []
	for word in personList:
		if word[0].isupper():
			person.append(word)

	# Sort them to make it more understandable for human beings
	locationList = sorted(locationList)
	personList = sorted(person)
	organizationList = sorted(organizationList)	

	return (locationList, personList, organizationList)

def NERfilter(sentencesArray, filterList):
	filteredArray = []
	for sentence in sentencesArray:
		filteredSentence = []
		for word in sentence:
			if word not in filterList:			
				filteredSentence.append(word)
			
		filteredArray.append(filteredSentence)

	return filteredArray

