# -*- coding: utf-8 -*-
from __future__ import division
import math, csv
from numpy import array

from Morphological_Disambiguation import MorphologicalDisambiguation
from Morphological_Disambiguation import StemmedForm
from Postprocess import StopWordFilter
from FeatureExtraction import n_gram
from FeatureExtraction import replace_if_occurances
from FeatureExtraction import get_words_from_array

''' 
TF-IDF module

TF: raw frequency calculation 
IDF: smooth frequency calculation 

Parameters:
- word: a simple string
- sentence: a list of strings
- sentencelist: a list of "sentence"-s
'''

def tf(word, wordslist):
	return wordslist.count(word) / len(wordslist)

def idf(word, sentencelist):
	occuranceNum = 0
	for sentence in sentencelist:
    		if word in sentence:
			occuranceNum += 1
	return math.log(1 + len(sentencelist) / occuranceNum)

def calculate_tfidf(word, sentence, sentencelist):
	return tf(word, sentence) * idf(word, sentencelist)


# returned List contains sentences "more exactly words in list" categorized into groups
# to retrieve dictionaries you need to do following
# [-5,-4,..., 5] -> to retrieve sentences with score -5 call createBlackWhiteLists(...)[0]
# to get 3 score call createBlackWhiteLists(...)[7]
def categorizeSentences(sentenceArray, sentimentCorpusPath):
	corpusfile = open(sentimentCorpusPath,'rb')
	csvreader = csv.reader(corpusfile, delimiter='\t')	

	# Ratings saved to list
	ratings = []	
	for line in csvreader:
		reviewScore = 0
		for i in range(6,11):
			if line[i] == '-1':
				reviewScore -= 1
			elif line[i] == '1':
				reviewScore += 1
		ratings.append(reviewScore)
	
	corpusfile.close()	
	
	# Create a list with possible categories and order ascending
	values = sorted(list(set(ratings)), key=int)
	
	# Organize sentences to categories
	categorizedSentences = []

	for element in values:
		sentences = []
		for iterator in range(0, len(ratings)):
			if element == ratings[iterator]:
				sentences.append(sentenceArray[iterator])
				#values.index(element)
	
		categorizedSentences.append(sentences)
	
	return categorizedSentences


# Blacklist if an incoming sentencelist contains only sentences with negative values
# Whitelist if opposite is true
def BlackWhiteList_with_TFIDF(sentencelist, TFIDFthreshold):
	filtered_wordlist = []	
	for sentence in sentencelist:
		for word in sentence:	
			if calculate_tfidf(word, sentence, sentencelist) > TFIDFthreshold:
				filtered_wordlist.append(word)

	return sorted(list(set(filtered_wordlist)))


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

	# Create black & white lists
	categorySentences = categorizeSentences(stopwordfiltArray, PreprocessedCorpusPath)
	
	''' Example Black/White list '''
	# Example determine most used words for -5 scores
	print BlackWhiteList_with_TFIDF(categorySentences[4], 1.5)

if __name__ == '__main__':
	main()
