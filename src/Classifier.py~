# -*- coding: utf-8 -*-
import os, sys, nltk, numpy, csv, pickle, re, tempfile, subprocess
from Morphological_Disambiguation import MorphologicalDisambiguation
from Morphological_Disambiguation import StemmedForm
from Postprocess import StopWordFilter
from Postprocess import NumberFilter
from FeatureExtraction import n_gram
from FeatureExtraction import replace_if_occurances
from FeatureExtraction import get_word_features
from FeatureExtraction import extract_features
from FeatureExtraction import get_words_from_array

from sklearn.cross_validation import KFold
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest

from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

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
		for i in range(6,11):
			if row[i] == '-1':
				reviewScore -= 1
			elif row[i] == '1':
				reviewScore += 1

		# RatingsReduction with option except 1: 1 (pos) and 0 (neg) or not
		if RatingsReduction == 0:			
			ratings.append(reviewScore)
		else:
			if reviewScore > 0:
				ratings.append('1')
			elif reviewScore < 0:
				ratings.append('0')

	corpusfile.close()
	
	return ratings

def FeatureReduction():
	features = []
	features.append(('pca', PCA(n_components=10)))
	#features.append(('select_best', SelectKBest(k=6)))
	feature_union = FeatureUnion(features)
	return feature_union

def Classifier_with_Evaluation(X, Y, feature, InstanceNum, CrossValidationNum, Seed):
	estimators = []
	estimators.append(('feature_union', feature))
	estimators.append(('logistic', LogisticRegression()))
	model = Pipeline(estimators)
	
	kfold = KFold(n=InstanceNum, n_folds=CrossValidationNum, random_state=Seed)
	results = cross_val_score(model, X, Y, cv=kfold)
	
	return results.mean()

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
	
	''' Classification starts here '''
	# Feature reduction determination
	feature = FeatureReduction()

	X = numpy.array(extract_features(filtArray, word_features))
	Y = numpy.array(GetRatingsFromCorpus(PreprocessedCorpusPath, 0))

	# Classifier with evaluation - everything in a sklearn.pipeline
	print Classifier_with_Evaluation(X, Y, feature, len(X), 3, 7)

	

if __name__ == '__main__':
	main()

