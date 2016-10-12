# -*- coding: utf-8 -*-
import os, sys, getopt, csv
import subprocess, linecache
from tfidf import calculate_tfidf
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
			# Decode word to unicode to capable of doing comparison
			if word.decode('latin2') not in stopwords:
				filteredSentence.append(word)
		filteredArray.append(filteredSentence)
				
	return filteredArray

'''
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
	#TFIDF_array = StopWordFilterTFIDF(SentencesArray, TFIDFthreshold)

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
'''

def NER_filtering():
	
	return NER
	

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
	print StopWordFilter(Array)	
	

if __name__ == '__main__':
	main()

