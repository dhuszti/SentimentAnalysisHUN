# -*- coding: utf-8 -*-
import os, sys, getopt, csv, nltk, numpy



# FEATURE IS FOR N-GRAM EXTRACT AROUND ENTITIES
""" There is some functions for determining n-gram around entities in corpus. 

Variables: 
	- wordsArray: an input array without any morhological analysis launched in it. It is used to detect entity in Corpus.
	- Array_to_N_Gram: launch this function on a morphological disambiguated input
	- PreprocessedCorpusPath: path of preprocessed OpinHuBank corpus
	- n_gram_number: integer number for plus/minus n-gram around entity
	- n_gram_onoff: turn on (1) or off (0) n-gram function
	
Usage example:
	n_gram(wordsArray, substArray, PreprocessedCorpusPath, 5, 1)
"""

def ReadCorpusIntoArray(PreprocessedCorpusPath):
	corpusfile = open(PreprocessedCorpusPath,'rb')
	csvreader = csv.reader(corpusfile, delimiter='\t')
	return csvreader

def n_gram_indexes_by_line(List, ListElement, EntityStart, EntityEnd, n_gram_number, n_gram_onoff):
	if n_gram_onoff == 1:
		# Determine +/- n-grams around entity
		if (EntityStart - n_gram_number) < 0:
			Start = 0
		else:
			Start = EntityStart-n_gram_number

		if (EntityEnd + n_gram_number) > len(List[ListElement]):		
			End = len(List[ListElement])
		else:
			End = EntityEnd + n_gram_number
	else:
		Start = 0
		End = len(List[ListElement])
		
	return (Start, End)


def n_gram_intervals(wordsArray, PreprocessedCorpusPath, n_gram_number, n_gram_onoff):
	corpusfile = ReadCorpusIntoArray(PreprocessedCorpusPath)
	# Determine entity place in corpus - find word in a list
	EntityStartList = []
	EntityEndList = []
	StartList = []
	EndList = []

	iterator = 0

	for line in corpusfile:	
	# Determine EntityStart & End position, furthermore exceptions are needed to be handled. If exact match not exist, then a shortened form is searched.
		if line[3].split()[0] in wordsArray[iterator]:
			EntityStart = wordsArray[iterator].index(line[3].split()[0])
			EntityStartList.append(EntityStart)
			EntityEnd = EntityStart + int(line[2])
			EntityEndList.append(EntityEnd)
		
		elif any(line[3].split()[0][:-1] in s for s in wordsArray[iterator]):
			matching_temp = [s for s in wordsArray[iterator] if line[3].split()[0][:-1] in s]
			EntityStart = wordsArray[iterator].index(matching_temp[0])
			EntityStartList.append(EntityStart)
			EntityEnd = EntityStart + int(line[2])
			EntityEndList.append(EntityEnd)
			
		elif str(line[3].split()[0]).lower() in wordsArray[iterator]:
			# in case of capital letter would mean a problem
			EntityStart = wordsArray[iterator].index(str(line[3].split()[0]).lower())
			EntityStartList.append(EntityStart)
			EntityEnd = EntityStart + int(line[2])
			EntityEndList.append(EntityEnd)
			
		else:
			print "Problem with entity match"
			# TODO: logger setup
	
		
		(Start, End) = n_gram_indexes_by_line(wordsArray, iterator, EntityStart, EntityEnd, n_gram_number, n_gram_onoff)
		StartList.append(Start)
		EndList.append(End)

		iterator += 1
	
	return (EntityStartList, EntityEndList, StartList, EndList)
	

def n_gram(wordsArray, Array_to_N_Gram, PreprocessedCorpusPath, n_gram_number, n_gram_onoff):
	# Leave it so, it is needed for Span Interval determination
	(EntityStartList, EntityEndList, StartList, EndList) = n_gram_intervals(wordsArray, PreprocessedCorpusPath, n_gram_number, n_gram_onoff)
	
	# Filter out Entity from SpanInterval, in order not to be in training set
	n_gram_Array = []
	
	iterator = 0
	for line in Array_to_N_Gram:
		elements = []
	
		for element in line[StartList[iterator]:EntityStartList[iterator]]:
			elements.append(element)
		for element in line[EntityEndList[iterator]:EndList[iterator]]:
			elements.append(element)
			
		n_gram_Array.append(elements)
		iterator += 1

	return n_gram_Array


# FUNCTION FOR WORD EXTRACTION TO HAVE A LIST OF POSSIBLE WORDS
""" It is used for determining a list of possible words. """
def get_words_from_array(sentencesArray):
	all_words = []
	for words in sentencesArray:
		all_words.extend(words)
	return all_words


# FEATURE TO SUBSTITUTE RARE TOKENS/WORDS WITH A SPECIAL STRING 
""" Rare tokens are really a huge problem for machine learning tasks, so they 
are substituted with a unique token. Now applying this function machine learning 
results are going to be more realistic. """
def replace_if_occurances(sentencesArray, wordlist, occurance_threshold, substString):
	words_with_occurances = nltk.FreqDist(wordlist)
	words = words_with_occurances.keys()
	occurances = words_with_occurances.values()

	# Determine words to substitute with a new _rare_ string
	wordsToReplace = []
	for i in range(0, len(occurances)):
		if occurances[i] < occurance_threshold:
			wordsToReplace.append(words[i])	
	
	# Create new array with _rare_ values	
	substArray = []
	for sentence in sentencesArray:
		substSentence = [] 
		for word in sentence:
			if word not in wordsToReplace:
				substSentence.append(word)
			else:
				substSentence.append(substString)			 			
		substArray.append(substSentence)
		
	return substArray


# SENTIMENT DICTIONARY READ FROM FILE
""" Read values from external sentiment dictionaries into a list """
def SentimentDictionary_Read(FilePath):
	SentDict = []
	
	sentdicfile = open(FilePath,'rb')
	for line in sentdicfile:
    		if not line.strip().startswith("#"):	
			SentDict.append(line.rstrip())

	return SentDict

