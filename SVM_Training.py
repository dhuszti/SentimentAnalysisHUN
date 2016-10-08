# -*- coding: utf-8 -*-
import os, sys, nltk, numpy, csv, pickle, re, tempfile, subprocess
from Postprocess import PostFiltering
from FeatureExtraction import get_word_features
from FeatureExtraction import extract_features
from FeatureExtraction import get_words_from_array
from sklearn import svm

def save(classifier, name):
	f = open(name, 'wb')
	pickle.dump(classifier, f, -1)
	f.close()

def GetRatingsFromCorpus(FilePath, RatingsReduction):
	ratings = []
	corpusfile = open(FilePath,'rb')
	csvreader = csv.reader(corpusfile, delimiter='\t')
	
	for row in csvreader:
		reviewScore = 0
		for i in range(7,11):
			if row[i] == '-1':
				reviewScore -= 1
			elif row[i] == '1':
				reviewScore += 1

		# RatingsReduction with option except 1: 1 (pos) and 0 (neg) or not
		if RatingsReduction == 1:			
			ratings.append(reviewScore)
		else:
			if reviewScore > 0:
				ratings.append('1')
			elif reviewScore < 0:
				ratings.append('0')

	corpusfile.close()
	
	return ratings


def SVM_classification(TrainingSetArray, Ratings, WordFeaturesOutputPath, ClassifierOutputPath):
	# Word features extractor
	word_features = get_word_features(get_words_from_array(TrainingSetArray))

	# Save word features
	save(word_features, WordFeaturesOutputPath)

	# SVM classifier
	clf = svm.SVR()
	classification = clf.fit(extract_features(TrainingSetArray, word_features), Ratings)

	# SVM classifier save
	save(classification, ClassifierOutputPath)


def main():
	# Here is a sample Test application how to launch SVM classifier
	MorphResultsFilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	TFIDFthreshold=0.4	
	StopwordsPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/real_project/stopwords.csv'
	IntervalNumber=5
	OnOffFlag=1
	
	Ratings = GetRatingsFromCorpus(PreprocessedCorpusPath, 0)
	
	TrainingSet = PostFiltering(MorphResultsFilePath, PreprocessedCorpusPath, TFIDFthreshold, StopwordsPath, IntervalNumber, OnOffFlag)
	
	SVM_classification(TrainingSet, Ratings, 'SVM_wordfeatures', 'SVM_classfier')	

if __name__ == '__main__':
	main()

