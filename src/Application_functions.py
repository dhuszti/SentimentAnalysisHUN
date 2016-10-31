# -*- coding: utf-8 -*-
import subprocess
from os.path import expanduser
from sklearn.externals import joblib
from polyglot.text import Text
from itertools import chain

from Morphological_Disambiguation import MorphologicalDisambiguation, StemmedForm
from Classifier import CountVectorizerTransform_input

'''
Functions:
- MorphAnalysis: morhological analysis and disambiguation task with a multidimensional list as output
- NER: creates three dictionaries as output, containing locations, person and organization names with extraction from input text
- SentimentScore: calls sentiment scoring machine learning model's prediction function for morphological analyzed data 
- OverallSentiment: function creates an overall sentiment for whole input text
- EntitySentimentScore: function determines entities' index and start/end position and calculates sentiment for this restricted interval
- NERsentiment: creates json format for EntitySentimentScore function
'''


# get user's home folder
homeFolder = expanduser('~')
# load machine learning model file
ML_model = joblib.load(open( homeFolder + '/SentimentAnalysisHUN-master/src/SentAnalysisModel.pkl'))
# file pathes for morhological analysis
xmlparserFilePath = homeFolder + '/SentimentAnalysisHUN-master/src/xmlparser.py'
hunpostagFilePath = homeFolder + '/SentimentAnalysisHUN-master/resources/HunPos/hunpos-1.0-linux/hunpos-tag'
szegedmodelFilePath = homeFolder + '/SentimentAnalysisHUN-master/resources/HunPos/hu_szeged_kr.model'
ocamorphFilePath = homeFolder + '/SentimentAnalysisHUN-master/resources/HunMorph/morphdb.hu/morphdb_hu.bin'
posFilePath = '/tmp/SentimentAnalysis_pos.txt'
morphFilePath = '/tmp/SentimentAnalysis_morph.txt'


def MorphAnalysis(inputString):
	# part-of-speech tagging on input
	cmd = 'echo ' + inputString.encode('latin2') + ' | huntoken | ' + xmlparserFilePath + ' | ' + hunpostagFilePath + ' ' + szegedmodelFilePath + ' > ' + posFilePath
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	(pos_out, err) = p.communicate()
	
	# morphological analysis on input
	cmd = 'echo ' + inputString.encode('latin2') + ' | huntoken | ' + xmlparserFilePath + ' | ocamorph --bin ' + ocamorphFilePath + ' > ' + morphFilePath			
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	(morph_out, err) = p.communicate()

	# morph disambiguation with stemmed form without POS tagging
	(wordsArray, disArray) = MorphologicalDisambiguation(posFilePath, morphFilePath)
	stemmedArray = StemmedForm(disArray, 0)
	
	# convert every word to lowercase
	stemmedArray = [[word.lower() for word in sent] for sent in stemmedArray]

	return stemmedArray


def NER(inputString):
	locationList = []
	personList = []
	organizationList = []

	text = Text(inputString)

	# select entities into categories
	for sent in text.sentences:
		for entity in sent.entities:
			if 'PER' in entity.tag:
				personList.append(entity)
			elif 'LOC' in entity.tag:
				locationList.append(entity)
			elif 'ORG' in entity.tag:
				organizationList.append(entity)

	return (locationList, personList, organizationList)


def SentimentScore(stemmedArray):
	# convert to countvectorizer digestible format
	List = CountVectorizerTransform_input(stemmedArray)

	# get sentiment probabilities
	negProb, posProb = ML_model.predict_proba(List)[0]
	
	# calculate neutral if difference is small
	if abs(negProb-posProb) < 0.15:
		sentiment = 'neutral'
	elif posProb > negProb:
		sentiment = 'positive'
	else:
		sentiment = 'negative'	

	# return sentiment category and probalities
	return (sentiment, negProb, posProb)


def OverallSentiment(inputString, morphAnalyzed, sentimentList):
	# get sentiment scores for overall
	(sent, negProb, posProb) = SentimentScore(morphAnalyzed)
	
	overallScore = {
		'input sentence': inputString,
		'sentiment': sent,
		'negative probability': negProb,
		'positive probalitiy': posProb,
    }

	sentimentList.append(overallScore)

	
def EntitySentimentScore(stemmedArray, entity, span):
	for i in range(0,int(len(stemmedArray))):
		try:
			# determine boundaries for entity
			EntityStart = stemmedArray[i].index(entity[0].encode('latin2').lower())
			EntityEnd = EntityStart + int(len(entity))
			Start = EntityStart-span if EntityStart>span else 0
			End = EntityEnd+span if EntityEnd<(len(stemmedArray[i])-span) else len(stemmedArray[0])
	
			# get score for entity
			return SentimentScore([stemmedArray[i][Start:EntityStart] + stemmedArray[i][EntityEnd:End]])
		except:
			pass


def NERsentiment(stemmedArray, entityList, entityType, sentimentList):
	for i in range(0,len(entityList)):
		# get sentiment score for every entity		
		(sentiment, negProb, posProb) = EntitySentimentScore(stemmedArray, entityList[i], 3)

		entity = {
			'entity': ' '.join(entityList[i]),
			'entity type': entityType,
			'sentiment': sentiment,
			'negative prob': negProb,
			'positive prob': posProb
		}

		sentimentList.append(entity)
