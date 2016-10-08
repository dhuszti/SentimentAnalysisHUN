# -*- coding: utf-8 -*-

import logging, subprocess
from SentimentCorpusPreprocess import CorpusPreprocess
from morph_decision import MorphologicalAnalysis
from SpanFilterMorphResults import TrainingSetReady
from SentimentAnalysis_Training_SVM import 

# Logging initialization
logger = logging.getLogger('HunSA')
filehandler = logging.FileHandler('/var/tmp/HunSA.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)
logger.setLevel(logging.WARNING)

# Logger usage
#logger.error()
#logger.warning()

def main():
	#
	# Sentiment corpus preprocessing
	#	
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

	#
	# Create Training Set
	#
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

if __name__ == '__main__':
	main()


