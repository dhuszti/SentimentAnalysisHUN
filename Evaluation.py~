# -*- coding: utf-8 -*-
# For handling float numbers at division. Needs to be at first line.
from __future__ import division

import logging, subprocess, csv, pickle, numpy
from Postprocess import PostFiltering
from SVM_Training import SVM_classification
from SVM_Training import get_word_features
from SVM_Training import extract_features
from SVM_Training import get_words_from_array
from itertools import izip
from sklearn import svm


# Load function for classification matrix & word features
def load(name):
	f = open(name, 'rb')
	word_features = pickle.load(f)
	f.close()
	return word_features

# Determine classified labels
def ClassifiedLabels(sentencesArray):
	# Load classifier & word features file
	clf = load('SVM_classfier')
	word_features = load('SVM_wordfeatures')

	# Call classifier
	SVM_results = numpy.array(clf.predict(extract_features(sentencesArray, word_features)))	
	return SVM_results


# Read correctLabels from corpus
def CorrectLabels(filePath, RatingsReduction):
	corpusfile = open(filePath,'rb')
	csvreader = csv.reader(corpusfile, delimiter='\t')
	correctlabels = []
	for line in csvreader:
		reviewScore = 0
		for i in range(7,11):
			if line[i] == '-1':
				reviewScore -= 1
			elif line[i] == '1':
				reviewScore += 1

		# RatingsReduction to with option except 1: 1 (pos) and 0 (neg) or not
		if RatingsReduction == 1:			
			correctlabels.append(reviewScore)
		else:
			if reviewScore > 0:
				correctlabels.append('1')
			elif reviewScore < 0:
				correctlabels.append('0')

	return correctlabels


# Determine necesseraly contengency table values for evaluation
def ContegencyTableValues(correctLabels, classifiedLabels, trueLabel, falseLabel):
	(TP, FP, FN, TN) = (0, 0, 0, 0)
	try:
		for correct, classified in zip(correctLabels, classifiedLabels):
			if correct is trueLabel and classified is trueLabel:
				TP += 1
			elif correct is falseLabel and classified is trueLabel:
				FP += 1
			elif correct is trueLabel and classified is falseLabel:
				FN += 1
			elif correct is falseLabel and classified is falseLabel:
				TN += 1			
	except:
		print "ERROR entity number not equal"	
		
	return (TP, FP, FN, TN)
	

def Accuracy(TP, FP, FN, TN):
	accuracy = (TP + TN) / (TP + TN + FP + FN)	
	return accuracy

def Precision(TP, FP):
	precision = TP / (TP + FP)
	return precision

def Recall(TP, FN):
	recall = TP / (TP + FN)
	return recall

def Fscore(TP, FP, FN, TN):
	fscore = (2 * Accuracy(TP, FP, FN, TN) * Recall(TP, FN)) / (Precision(TP, FP) + Recall(TP, FN)) 
	return fscore

def main():
	MorphResultsFilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	TFIDFthreshold=0.4	
	StopwordsPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/real_project/stopwords.csv'
	IntervalNumber=5
	OnOffFlag=1
	
	FilteredArray = PostFiltering(MorphResultsFilePath, PreprocessedCorpusPath, TFIDFthreshold, StopwordsPath, IntervalNumber, OnOffFlag)
	
	ClassifiedResults = []
	for element in ClassifiedLabels(FilteredArray):
		if int(element) < 0.098:
			ClassifiedResults.append('1')
		else:
			ClassifiedResults.append('0')

	CorrectResults = CorrectLabels(PreprocessedCorpusPath, 0)
	
	print ClassifiedResults[1:10]
	print CorrectResults[1:10]
	
	(TP, FP, FN, TN) = ContegencyTableValues(CorrectResults, ClassifiedResults, '1', '0')
	print (TP, FP, FN, TN)
	print Accuracy(TP, FP, FN, TN)
	print Precision(TP, FP)
	print Recall(TP, FN)
	print Fscore(TP, FP, FN, TN)

	
'''
	try:
		CorpusPreprocess('/home/osboxes/Downloads/archive/OpinHuBank_20130106.csv', '/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv')
	except:
		logger.error('Sentiment corpus may not exist or at wrong place. Please doublecheck it!')

	#
	# Launch Morphological Analysis parameters: 0 or 1 at first phase
	#
	posfile='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunpos_ki.txt'
	morphfile='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunmorph_ki.txt'
	ofile='/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'

	try:
		subprocess.call(['./SHELL_SCRIPT_SENTIMENT_DICTIONARY_MORPH.sh'])
		MorphologicalAnalysis(0, posfile, morphfile, ofile)
	except:
		logger.error('Morphological Analysis problem.')


	MorphResultsFilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	IntervalNumber=5
	OnOffFlag=1

	try:
		print TrainingSetReady(MorphResultsFilePath, PreprocessedCorpusPath, IntervalNumber, OnOffFlag)		
	except:
		logger.error('Training Set filtering problem.')
	
	#
	# Launch machine learning algorithm SVM for training purpose 
	#
	try:
		Ratings = GetRatingsFromCorpus(PreprocessedCorpusPath)
		TrainingSetArray = SpanFilterMorphResults.TrainingSetReady(MorphResultsFilePath, PreprocessedCorpusPath, IntervalNumber, OnOffFlag)	SVM_classification(TrainingSetArray, Ratings, 'SVM_wordfeatures', 'SVM_classfier')
	except:
		logger.error('Training Set filtering problem.')
'''


if __name__ == '__main__':
	main()

