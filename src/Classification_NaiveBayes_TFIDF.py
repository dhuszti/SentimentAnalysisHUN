import matplotlib.pyplot as plt
import csv
import pandas
import sklearn
import cPickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split, learning_curve

from Morphological_Disambiguation import MorphologicalDisambiguation
from Morphological_Disambiguation import StemmedForm
from Postprocess import StopWordFilter
from Postprocess import NumberFilter
from FeatureExtraction import n_gram
from FeatureExtraction import replace_if_occurances
from FeatureExtraction import get_words_from_array

# Create a List containing all inputs in unicode encoding for CountVectorizer specific input purpose
def CountVectorizerTransform_input(inputList):
	outputList = []	
	for sentence in inputList:
		outputList.append(unicode(str(' '.join(sentence)),'latin2'))
	return outputList


# Get ratings from SentimentCorpus with an option to have category reduction ability
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
				ratings.append('positive')
			elif reviewScore < 0:
				ratings.append('negative')

	corpusfile.close()
	
	return ratings

# Save predictor model
def savePredictor(predictorName, predictorFilePath):
	with open(predictorFilePath, 'wb') as file_out:
    		cPickle.dump(predictorName, file_out)

	file_out.close()

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

	###################################################
	### Machine learning part with sklearn.pipeline ###
	###################################################

	# labels -  you can filter it to positive / negative as well
	labels = GetRatingsFromCorpus(PreprocessedCorpusPath, 1)

	# convert filtArray to new CountVect input format	
	new_filtArray = CountVectorizerTransform_input(filtArray)
	
	# create test and training set with divide corpus into two parts
	trainingSet, testSet, trainingLabel, testLabel = train_test_split(new_filtArray, labels, test_size=0.2)

	# create sklearn.pipeline for automated machine learning
	pipeline = Pipeline([
	    ('countVec', CountVectorizer()),  	# strings to token integer counts
	    ('tfidf', TfidfTransformer()),  	# integer counts to weighted TF-IDF scores
	    ('classifier', MultinomialNB()),  	# train on TF-IDF vectors w/ Naive Bayes classifier
	])

	# use gridsearchCV for automated machine learning with multiple options - "parameters"
	params = {
	    'tfidf__use_idf': (True, False),
	}

	grid = GridSearchCV(
	    pipeline,  				# pipeline from above
	    params,  				# parameters to tune via cross validation
	    refit=True,  			# fit using all available data at the end, on the best found param combination
	    n_jobs=-1,  			# number of cores to use for parallelization; -1 for "all cores"
	    scoring='accuracy',  		# what score are we optimizing?
	    cv=StratifiedKFold(n_splits=10).get_n_splits(trainingSet, trainingLabel),  # what type of cross validation to use
	)
	
	
	# predictive model training
	clf = grid.fit(trainingSet, trainingLabel)
	
	# predictive model results with different options determined at parameters
	means = clf.cv_results_['mean_test_score']
    	stds = clf.cv_results_['std_test_score']
	print means
	print stds

	# evaluation part with precision, recall, f-score
	predictions = clf.predict(testSet)			# predictions for test set
	print "ContegencyTableValues"
	print confusion_matrix(testLabel, predictions)		# TP, TF, ... values
	print "Evaluation scores"
	print classification_report(testLabel, predictions)	# precision, recall, f-score


if __name__ == '__main__':
	main()

