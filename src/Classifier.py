# Import basics libs
import csv
from numpy import array
from numpy import recarray
from math import sqrt
from scipy.stats import pearsonr
from os.path import expanduser

# Import sklearn functions
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix, mean_squared_error, mean_absolute_error
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split, learning_curve
from sklearn.externals import joblib

# Import functions from project files
from Morphological_Disambiguation import MorphologicalDisambiguation, StemmedForm
from Postprocess import StopWordFilter, NumberFilter, NER_Dictionary, NERfilter
from FeatureExtraction import SentimentDictionary_Read, n_gram, replace_if_occurances, get_words_from_array

# Import pipelines from external project files
from Pipeline_PCA_SVM import pipeline_PCA_SVM, getparams_PCA_SVM 
from Pipeline_PCA_Regression import pipeline_PCA_Regression, getparams_PCA_Regression
from Pipeline_TFIDF_NaiveBayes import pipeline_TFIDF_NaiveBayes, getparams_TFIDF_NaiveBayes


# GLOBAL FUNCTIONS FOR CLASSIFICATION
""" These functions are useful for every single classification task,
so it is worth collecting them at one single place for reusability. 

Functions:
- CountVectorizerTransform_input: transforming list to perfect match Countvectorizer input
	Variables:
		- inputList: incoming list with morph analyzed and filtered values

- GetRatingsFromCorpus: gets human annotated ratings from sentiment corpus, with option 'RatingsReduction' reduces its [-5,5] values to positive/neutral/negative ones
	Variables:
		- FilePath: preprocessed sentiment corpus filepath
		- RatingsReduction: option (0) [-5,5] discret values, with (1) positive/neutral/negative scores

- savePredictor: save machine learning model to a file
	Variables:
		- predictorName: name of predictor 
		- predictorFilePath: where to save model
"""

def CountVectorizerTransform_input(inputList):
	outputList = []	
	for sentence in inputList:
		outputList.append(str(' '.join(sentence)))
	return outputList


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

		if RatingsReduction == 0:			
			ratings.append(reviewScore)
		else:
			if reviewScore > 0:
				ratings.append('positive')
			elif reviewScore < 0:
				ratings.append('negative')
			else:
				ratings.append('neutral')

	corpusfile.close()
	
	return ratings


def savePredictor(predictorName, predictorFilePath):
	joblib.dump(predictorName, predictorFilePath, compress = 1)	


# MORPHOLOGICAL ANALYSIS, DISAMBIGUATION AND FILTERING
"""
This function contains every single step to process 

Variables:
	- pos_onoff: switch on (1) or off (0) POS as an added feature
	- n_gram_onoff: switch on (1) or off (0) n-gram around entities as an added feature
	- n_gram_value: int value, determines plus/minus n-gram around entities

Return value:
	- two dimensional list with morphological analyzed, disambiguated and filtered tokens

Usage example:
	# POS off, N-GRAM on, N-GRAM value is +/- 5 tokens
	morphAnalysis_and_filtering(0, 1, 5)
"""
def morphAnalysis_and_filtering(pos_onoff, n_gram_onoff, n_gram_value):	
	# Morphological disambiguation (wordsArray contains original words - for easier n-gram filtering, disArray for perfect output)
	(wordsArray, disArray) = MorphologicalDisambiguation(posfilePath, morphfilePath)
	stemmedArray = StemmedForm(disArray, 0)
	
	# Substitute rare words with specific label '_rare_'
	substArray = replace_if_occurances(stemmedArray, get_words_from_array(stemmedArray), 3, '_rare_')

	# 5-gram usage example
	n_Array = n_gram(wordsArray, substArray, preprocessedCorpusPath, 5, 0)
	
	# Stopword filtering 
	stopwordfiltArray = StopWordFilter(n_Array, stopwordsFilePath)

	# Number filtering
	numfiltArray = NumberFilter(stopwordfiltArray)

	# NER filtering can be applied
	#(locationList, personList, organizationList) = NER_Dictionary(preprocessedCorpusPath)
	#NERArray = NERfilter(numfiltArray, personList)
	#NERArray = NERfilter(NERArray, locationList)
	#NERArray = NERfilter(NERArray, organizationList)
	#numfiltArray = NERArray

	# convert filtArray to new CountVect input format	
	filtArray = CountVectorizerTransform_input(numfiltArray)

	return filtArray


# Get home folder
homeFolder = expanduser('~')

# GLOBAL VARIABLES
""" These are used everywhere """ 
preprocessedCorpusPath = homeFolder + '/SentimentAnalysisHUN-master/tempfiles/OpinHuBank_20130106_posneg.csv'
posfilePath = homeFolder + '/SentimentAnalysisHUN-master/tempfiles/hunpos_posneg.txt'
morphfilePath = homeFolder + '/SentimentAnalysisHUN-master/tempfiles/hunmorph_posneg.txt'
stopwordsFilePath = homeFolder + '/SentimentAnalysisHUN-master/resources/StopwordLexicon/stopwords.txt'
posLexiconPath = homeFolder + '/SentimentAnalysisHUN-master/resources/SentimentLexicons/PrecoPos.txt'
negLexiconPath = homeFolder + '/SentimentAnalysisHUN-master/resources/SentimentLexicons/PrecoNeg.txt'
MLmodelPath = homeFolder + '/SentimentAnalysisHUN-master/src/SentAnalysisModel.pkl'

# MAIN FUNCTION FOR CREATING CLASSIFICATION ON TOP OF MORPHOLOGICAL ANALYSIS AND FILTERING
""" 
"""
def main():
	""" Change here parameters """
	# POS off, N-GRAM on, N-GRAM value is +/- 5 tokens
	allSet = morphAnalysis_and_filtering(0, 1, 5)
		
	# labels -  you can filter it to positive / negative as well
	allLabels = GetRatingsFromCorpus(preprocessedCorpusPath, 1)
	
	# create test and training set with divide corpus into two parts
	trainingSet, testSet, trainingLabel, testLabel = train_test_split(allSet, allLabels, test_size=0.2)
	
	# load sentiment lexicons from external files
	posLexicon = SentimentDictionary_Read(posLexiconPath)
	negLexicon = SentimentDictionary_Read(negLexiconPath)
	
	""" Load functions written in 'Pipeline*.py' files """	
	# pipeline and its parameters	
	pipeline = pipeline_TFIDF_NaiveBayes(posLexicon, negLexicon)
	params = getparams_TFIDF_NaiveBayes()

	# gridsearch for automated machine learning with cross validation	
	grid = GridSearchCV(
	    pipeline,					# pipeline from above
	    params, 					# parameters to tune via cross validation
	    refit=True,					# fit using all available data at the end, on the best found param combination
	    n_jobs=-1, 					# number of cores to use for parallelization; -1 for "all cores"
	    scoring='accuracy',				# what score are we optimizing?
	    cv=StratifiedKFold(n_splits=10).get_n_splits(trainingSet, trainingLabel),  	# what type of cross validation to use
	)

	# predictive model training
	clf = grid.fit(trainingSet, trainingLabel)

	# save model to file
	savePredictor(grid.best_estimator_, MLmodelPath)

	# evaluation part with precision, recall, f-score
	predictions = clf.predict(testSet)					# predictions for test set
	print "\nContegency table"
	print confusion_matrix(testLabel, predictions)		# TP, TF, ... values
	print "\nEvaluation scores"
	print classification_report(testLabel, predictions)	# precision, recall, f-score
	
	# Pearson correlation - if possible
	try:
		pearson = pearsonr(testLabel, predictions)
		print "Pearson correlation"
		print pearson
	except:
		pass

	# MSE, MAE, RMSE, MAE^2 error scores - if possible
	try:
		mse = mean_squared_error(testLabel, predictions)
		rmse = sqrt(mean_squared_error(testLabel, predictions))
		mae = mean_absolute_error(testLabel, predictions)
		print "MSE \t MAE \t RMSE \t MAE_square"
		print str(mse) + '\t' + str(mae) + '\t' + str(rmse) + '\t' + str(mae*mae)
	except:
		pass

	# MAE < RMSE < MAE2
	# MAE < RMSE < MAE2 (for regression)
	# if RMSERMSE is close to MAEMAE, the model makes many relatively small errors
	# if RMSERMSE is close to MAE2MAE2, the model makes few but large errors

	# Test some sentences
	print "\nTest:"	
	testSent1 = ["ez egy nagyon rossz nap"]
	print testSent1
	print clf.predict(testSent1)
	testSent2 = ["hihetetlen boldog vagyok nagyon szuper"]
	print testSent2
	print clf.predict(testSent2)
	testSent3 = ["az alma angolul apple"]
	print testSent3
	print clf.predict(testSent3)
	

if __name__ == '__main__':
	main()
