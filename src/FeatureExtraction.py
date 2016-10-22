# -*- coding: utf-8 -*-
import os, sys, getopt, csv, nltk, numpy
from sklearn.base import BaseEstimator, TransformerMixin

from Morphological_Disambiguation import StemmedForm
from Morphological_Disambiguation import MorphologicalDisambiguation
from Postprocess import StopWordFilter
from Postprocess import NumberFilter


# FEATURES, FUNCTIONS FOR SKLEARN.PIPELINE EXTENSION

class SentDictOccurancesFeature(BaseEstimator, TransformerMixin):
	""" This feature is used at next phase - "sklearn pipeline" - 
	to determine sentiment dictionary occurances by each tuple. """

	def __init__(self, posDict='', negDict=''):
		self.posDict = posDict
		self.negDict = negDict	
    	
	def fit(self, raw_documents, y=None):
       		return self
    	
	def fit_transform(self, raw_documents, y=None):
		return self.transform(raw_documents)

	def transform(self, raw_documents, y=None):
		PosNegOccurances = np.recarray(shape=(len(raw_documents),1), dtype=[('positive', int), ('negative', int)])		
		for i, sentence in enumerate(raw_documents):		
			PosOccurances = 0
			NegOccurances = 0	
			words = sentence.split()
			for word in words:
				if word in self.posDict:
					PosOccurances += 1
				elif word in self.negDict:
					NegOccurances += 1	

			PosNegOccurances['positive'][i]= PosOccurances
			PosNegOccurances['negative'][i]= NegOccurances	
		
		return PosNegOccurances


class ItemSelector(BaseEstimator, TransformerMixin):
	""" Itemselector is used at next phase at "sklearn pipeline". Its main role is
	to select positive or negative occurances in a tuple coming from
	'SentDictOccurancesFeature'.
	"""
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


class Densifier(BaseEstimator):
	""" Densifier is used at next phase at "sklearn pipeline" to be capable of 
	applying PCA as dimension reduction method. Basically it is quite simple, 
	only transforms input format into array, which is prerequisite incoming 
	format of PCA.
	"""
	def __init__(self):
		BaseEstimator.__init__(self)

	def fit(self, X, y=None):
		pass
		
	def fit_transform(self, X, y=None):
		return self.transform(X)

	def transform(self, X, y=None):
		return X.toarray()



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

def get_words_from_array(sentencesArray):
	all_words = []
	for words in sentencesArray:
		all_words.extend(words)
	return all_words


# FEATURE TO SUBSTITUTE RARE TOKENS/WORDS WITH A SPECIAL STRING 

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

def SentimentDictionary_Read(FilePath):
	SentDict = []
	
	sentdicfile = open(FilePath,'rb')
	for line in sentdicfile:
    		if not line.strip().startswith("#"):	
			SentDict.append(line.rstrip())

	return SentDict



def main():
	# EXAMPLE USAGE

	# Some info to apply morphological disambiguation and create stemmed form 
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	posfilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunpos_ki.txt'
	morphfilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunmorph_ki.txt'
	stopwordsFilePath='/home/osboxes/Desktop/SentimentAnalysisHUN/resources/StopwordLexicon/stopwords.txt'
	
	# Morphological disambiguation (wordsArray contains original words - for easier n-gram filtering, disArray for perfect output)
	(wordsArray, disArray) = MorphologicalDisambiguation(posfilePath, morphfilePath)
	stemmedArray = StemmedForm(disArray, 0)
	
	# Substitute rare words with specific label '_rare_'
	substArray = replace_if_occurances(stemmedArray, get_words_from_array(stemmedArray), 3, '_rare_')

	# 5-gram usage example
	n_Array = n_gram(wordsArray, substArray, PreprocessedCorpusPath, 5, 1)

	# Stopword filtering 
	stopwordfiltArray = StopWordFilter(n_Array, stopwordsFilePath)

	# Number filtering
	filtArray = NumberFilter(stopwordfiltArray)

	print SentimentDictionary_Read('/home/osboxes/Desktop/SentimentAnalysisHUN/resources/SentimentLexicons/PrecoNeg.txt')
	

if __name__ == '__main__':
	main()

