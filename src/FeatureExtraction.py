# -*- coding: utf-8 -*-
import os, sys, getopt, csv, nltk, numpy
from tfidf import calculate_tfidf
from Morphological_Disambiguation import StemmedForm
from Morphological_Disambiguation import MorphologicalDisambiguation

#
# Functions for n-gram usage
# n_gram_onoff 1/0
# n_gram_number integer
#
def ReadCorpusIntoArray(PreprocessedCorpusPath):
	#'/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
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


def n_gram_intervals(disambiguatedArray, PreprocessedCorpusPath, n_gram_number, n_gram_onoff):
	corpusfile = ReadCorpusIntoArray(PreprocessedCorpusPath)
	# Determine entity place in corpus - find word in a list
	EntityStartList = []
	EntityEndList = []
	StartList = []
	EndList = []

	iterator = 0

	for line in corpusfile:	
	# Determine EntityStart & End position, furthermore exceptions are needed to be handled. If exact match not exist, then a shortened form is searched.
		if line[3].split()[0] in disambiguatedArray[iterator]:
			EntityStart = disambiguatedArray[iterator].index(line[3].split()[0])
			EntityStartList.append(EntityStart)
			EntityEnd = EntityStart + int(line[2])
			EntityEndList.append(EntityEnd)
		elif any(line[3].split()[0][:-1] in s for s in disambiguatedArray[iterator]):
			matching_temp = [s for s in disambiguatedArray[iterator] if line[3].split()[0][:-1] in s]
			EntityStart = disambiguatedArray[iterator].index(matching_temp[0])
			EntityStartList.append(EntityStart)
			EntityEnd = EntityStart + int(line[2])
			EntityEndList.append(EntityEnd)
		else:
			break
		
		(Start, End) = n_gram_indexes_by_line(disambiguatedArray, iterator, EntityStart, EntityEnd, n_gram_number, n_gram_onoff)
		StartList.append(Start)
		EndList.append(End)

		iterator += 1

	return (EntityStartList, EntityEndList, StartList, EndList)
	

def n_gram(disambiguatedArray, PreprocessedCorpusPath, n_gram_number, n_gram_onoff):
	# Leave it so, it is needed for Span Interval determination
	(EntityStartList, EntityEndList, StartList, EndList) = n_gram_intervals(disambiguatedArray, PreprocessedCorpusPath, n_gram_number, n_gram_onoff)
	
	# Filter out Entity from SpanInterval, in order not to be in training set
	n_gram_Array = []
	
	iterator = 0
	for line in disambiguatedArray:
		elements = []
		for element in line[StartList[iterator]:EntityStartList[iterator]]:
			elements.append(element)
		for element in line[EntityEndList[iterator]:EndList[iterator]]:
			elements.append(element)
		print elements
		n_gram_Array.append(elements)
		
		iterator += 1

	return n_gram_Array




#
# Functions for word extraction, feature extraction
def get_words_from_array(sentencesArray):
    all_words = []
    for words in sentencesArray:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
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



# Main
def main():
	MorphResultsFilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	StopwordsPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/real_project/stopwords.csv'
	TFIDFthreshold=0.4	
	IntervalNumber=5
	OnOffFlag=1


	posfilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunpos_ki.txt'
	morphfilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunmorph_ki.txt'

	(wordsArray, disArray) = MorphologicalDisambiguation(posfilePath, morphfilePath)
	array = StemmedForm(disArray, 0)
	#print array
	print n_gram(array, PreprocessedCorpusPath, 5, 1)

	#print n_gram_intervals_by_line(array, PreprocessedCorpusPath, 5, 1)

	#FilteredArray = PostFiltering(MorphResultsFilePath, PreprocessedCorpusPath, TFIDFthreshold, StopwordsPath, IntervalNumber, OnOffFlag)
	
	#word_features = get_word_features(get_words_from_array(FilteredArray))
	#extract_features(FilteredArray, word_features)
	

if __name__ == '__main__':
	main()

