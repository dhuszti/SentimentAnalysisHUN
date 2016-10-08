# -*- coding: utf-8 -*-
import os, sys, getopt, csv
import subprocess, linecache
from tfidf import calculate_tfidf

''' This file is responsible for
	- span interval determination around entity 
	- filter sentence to this span interval
	- stop word filtering
'''

def SpanIntervalPositions(List, ListElement, Line, IntervalNumber, EntityStart, EntityEnd, OnOffFlag):
	if OnOffFlag == 1:
		# Determine +/- words around entity
		if (EntityStart-IntervalNumber) < 0:
			Start = 0
		else:
			Start = EntityStart-IntervalNumber

		if (EntityEnd+IntervalNumber) > len(List[ListElement]):		
			End = len(List[ListElement])
		else:
			End = EntityEnd + IntervalNumber
	else:
		Start = 0
		End = len(List[ListElement])
		
	return (Start, End)


def SpanInterval(SentencesArray, PreprocessedCorpusPath, IntervalNumber, OnOffFlag):
	csvreader = ReadCorpusIntoArray(PreprocessedCorpusPath)
	# Determine entity place in corpus - find word in a list
	iterator = 0
	for line in csvreader:	
	# Determine EntityStart&End position, exceptions are needed to be handled. If exact match not exist, then a shortened form is searched.
		if line[3].split()[0] in SentencesArray[iterator]:
			EntityStart = SentencesArray[iterator].index(line[3].split()[0])
			EntityEnd = EntityStart + int(line[2])
		elif any(line[3].split()[0][:-1] in s for s in SentencesArray[iterator]):
			matching_temp = [s for s in SentencesArray[iterator] if line[3].split()[0][:-1] in s]
			EntityStart = SentencesArray[iterator].index(matching_temp[0])
			EntityEnd = EntityStart + int(line[2])	
		else:
			break

		(Start, End) = SpanIntervalPositions(SentencesArray, iterator, line, IntervalNumber, EntityStart, EntityEnd, OnOffFlag)
	
		iterator += 1

	return (EntityStart, EntityEnd, Start, End)
		

# original word (0) or morphological analyzed (1)
def ReadMorphResultsIntoArray(MorphResultsFilePath, Column):
	#'/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'
	morphfile = open(MorphResultsFilePath, 'rb') 
	csvreader = csv.reader(morphfile, delimiter='\t')
	sentences = []
	words = []	
	for line in csvreader:
		if 'thisistheending' in line[0]:
			sentences.append(words)
			words = []
		else:
			words.append(line[Column])
	return sentences


def ReadCorpusIntoArray(PreprocessedCorpusPath):
	#'/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	corpusfile = open(PreprocessedCorpusPath,'rb')
	csvreader = csv.reader(corpusfile, delimiter='\t')
	return csvreader


def StopWordFilterTFIDF(sentencelist, TFIDFthreshold):
	filtered_sentlist = []	
	for sentence in sentencelist:
		filtered_sentence = []
		for word in sentence:	
			if calculate_tfidf(word, sentence, sentencelist) > TFIDFthreshold:
				filtered_sentence.append(word)	
		filtered_sentlist.append(filtered_sentence)
	return filtered_sentlist


def StopWordFilter(SentencesArray, TFIDFthreshold, stopwordsFilePath):
	
	# Apply TF-IDF to filter basic stopwords
	TFIDF_array = StopWordFilterTFIDF(SentencesArray, TFIDFthreshold)

	# Apply some additional stopword filtering with a dictionary
	stopwords = []
	stopwordsfile = open(stopwordsFilePath,'rb')
	for line in stopwordsfile:
		stopwords.append(line.replace('\n',''))

	# Apply some other filter
	filteredArray = []
	for elements in TFIDF_array:
		filteredElements = []
		
		for element in elements:
			if element != 'UNKNOWN' and '/ART' not in element and '/CONJ' not in element and '/PREV' not in element and 'NUM' not in element and '/POSTP' not in element:
				if element not in stopwords:				
					filteredElements.append(element)

		filteredArray.append(filteredElements)

	return filteredArray


def PostFiltering(MorphResultsFilePath, PreprocessedCorpusPath, TFIDFthreshold, StopwordsPath, IntervalNumber, OnOffFlag):
	# Leave it so, it is needed for Span Interval determination
	SentencesArray = ReadMorphResultsIntoArray(MorphResultsFilePath, 0)
	(EntityStart, EntityEnd, Start, End) = SpanInterval(SentencesArray, PreprocessedCorpusPath, IntervalNumber, OnOffFlag)
	
	# Read morphological analyzed words	
	SentencesArray = ReadMorphResultsIntoArray(MorphResultsFilePath, 1)
	
	# Filter out Entity from SpanInterval, in order not to be in training set
	SentencesForTraining = []
	iterator = 0
	for line in SentencesArray:
		elements = []
		for element in line[Start:EntityStart]:
			elements.append(element)
		for element in line[EntityEnd:End]:
			elements.append(element)

		SentencesForTraining.append(elements)

	FilteredTrainingSet = StopWordFilter(SentencesForTraining, TFIDFthreshold, StopwordsPath)
	return FilteredTrainingSet
	#return SentencesForTraining
	

def main():
	MorphResultsFilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	TFIDFthreshold=0.4	
	StopwordsPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/real_project/stopwords.csv'
	IntervalNumber=5
	OnOffFlag=1
	
	
	print PostFiltering(MorphResultsFilePath, PreprocessedCorpusPath, TFIDFthreshold, StopwordsPath, IntervalNumber, OnOffFlag)
		

if __name__ == '__main__':
	main()

