# -*- coding: utf-8 -*-
import os, sys, getopt, csv, nltk, numpy
from Morphological_Disambiguation import StemmedForm
from Morphological_Disambiguation import MorphologicalDisambiguation
from Postprocess import StopWordFilter
from Postprocess import NumberFilter

#
# Functions for n-gram usage
# n_gram_onoff 1/0
# n_gram_number integer
#
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
		else:
			break
		
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




#
# Functions for word extraction, feature extraction
#
def get_words_from_array(sentencesArray):
	all_words = []
	for words in sentencesArray:
		all_words.extend(words)
	return all_words

def get_word_features(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	word_occ = wordlist.values()
	return word_features

def extract_features(sentencesArray, word_features):
	features = []  
	for array_element in sorted(sentencesArray):
		temp = []
		for it in sorted(word_features):
			if it not in array_element:
				temp.append(0)
			else:
				temp.append(1)
		features.append(temp)
	return features


#
# Substitute tokens if occurance is more than determined variable
#
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


# Main
def main():
	# Some info to apply morphological disambiguation and create stemmed form 
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	posfilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunpos_ki.txt'
	morphfilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunmorph_ki.txt'
	
	# Morphological disambiguation (wordsArray contains original words - for easier n-gram filtering, disArray for perfect output)
	(wordsArray, disArray) = MorphologicalDisambiguation(posfilePath, morphfilePath)
	stemmedArray = StemmedForm(disArray, 0)
	
	# Substitute rare words with specific label '_rare_'
	substArray = replace_if_occurances(stemmedArray, get_words_from_array(stemmedArray), 3, '_rare_')

	# 5-gram usage example
	n_Array = n_gram(wordsArray, substArray, PreprocessedCorpusPath, 5, 1)

	# Stopword filtering 
	stopwordfiltArray = StopWordFilter(n_Array)

	# Number filtering
	filtArray = NumberFilter(stopwordfiltArray)
		
	# Feature extraction and frequency list
	word_features = get_word_features(get_words_from_array(filtArray))
	extract_features(filtArray, word_features)
	


if __name__ == '__main__':
	main()

