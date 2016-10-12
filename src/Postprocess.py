# -*- coding: utf-8 -*-
import os, sys, getopt, csv
import subprocess, linecache
from stop_words import get_stop_words
from Morphological_Disambiguation import StemmedForm
from Morphological_Disambiguation import MorphologicalDisambiguation


def StopWordFilter(sentencesArray):
	# Stopwords in unicode format	
	stopwords = get_stop_words('hu')
	
	# These words are missing from stopwords
	stopwords.append('is')
	stopwords.append('le')

	filteredArray = []
	for sentence in sentencesArray:
		filteredSentence = []
		for word in sentence:
			# Decode word to unicode to be capable of doing comparison with same encoding
			if word.decode('latin2') not in stopwords:
				filteredSentence.append(word)
		filteredArray.append(filteredSentence)
				
	return filteredArray


def NERFilter(sentencesArray):
	
	return NER

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

def main():
	MorphResultsFilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	TFIDFthreshold=0.4	
	#StopwordsPath='/home/osboxes/Desktop/SentimentAnalysisHUN/resources/stopwords.txt'
	IntervalNumber=5
	OnOffFlag=1
	
	posfilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunpos_ki.txt'
	morphfilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunmorph_ki.txt'
	
	# Morphological disambiguation
	(wordsArray, disArray) = MorphologicalDisambiguation(posfilePath, morphfilePath)
	Array = StemmedForm(disArray, 0)
	
	# Stopword filtering
	filtArray = StopWordFilter(Array)
	
	# Number character filtering
	print NumberFilter(filtArray)	
	

if __name__ == '__main__':
	main()

