# -*- coding: utf-8 -*-
import os, sys, getopt
import subprocess, linecache
import tempfile, csv

""" This python file contains some functions regarding to morphological diasmbiguation.
Functions:
- MorphologicalDisambiguation: can decide from PoS and morph results the proper morphologically analyzed form of each tokens.
	As input it takes pos and morph file, and gives a list as output.
- StemmedForm: can truncate morphological disambiguated form to use only its base form (stemmed form).
- SaveToFile: is only for test purposes, to save results to external file.
"""

def MorphologicalDisambiguation(posfilePath, morphfilePath):
	
	# HunPos outputs read into an array	
	posArray = []
	posList = []
	wordsArray = []
	wordsList = []
	
	posfile = open(posfilePath, 'r')
	posfilecsv = csv.reader(posfile, delimiter='\t')
	
	for line in posfilecsv:
		# Filter empty rows with this feature
		if len(line) > 0:
			if 'thisistheending' in line[0]:
				wordsArray.append(wordsList)
				posArray.append(posList)
				wordsList = []
				posList = []
			else:
				wordsList.append(line[0])
				posList.append(line[1])

	# HunMorph options read in a multidimensinal array
	morphfile = open(morphfilePath, 'r')
	
	morphArray = []
	morphSentList = []
	morphWordList = []
	
	# To skip sentence ending 'thisistheending' morph analysis
	sentenceEndFlag = 0

	for line in morphfile:
		if 'thisistheending' in line:
			morphSentList.append(morphWordList)
			morphArray.append(morphSentList)
			morphSentList = []
			morphWordList = []
			sentenceEndFlag = 1

		elif sentenceEndFlag == 1:
			sentenceEndFlag = 0

		else:	
			if line.startswith('> '):
				if len(morphWordList) > 0:
					morphSentList.append(morphWordList)
				morphWordList = []
			else:
				morphWordList.append(line.replace('\n',''))
	
	# Disambiguation
	disambiguatedArray = []	

	if len(posArray) == len(morphArray):
		for sentIter in range(0, len(morphArray)):
			disambiguatedSentence = []
			for wordIter in range(0, len(morphArray[sentIter])):
				# HunMorph has only one suggestion and it is not UNKNOWN
				if len(morphArray[sentIter][wordIter]) == 1 and morphArray[sentIter][wordIter][0] != 'UNKNOWN':
					disambiguatedSentence.append(morphArray[sentIter][wordIter][0])
				# Observe matching elements. If there is any then choose first one from HunMorph.
				else:
					matching = [s for s in morphArray[sentIter][wordIter] if posArray[sentIter][wordIter] in s]
					if len(matching) == 0:
						disambiguatedSentence.append(wordsArray[sentIter][wordIter])				
					else:
						disambiguatedSentence.append(matching[0])
			
			disambiguatedArray.append(disambiguatedSentence)
	
	else:
		# TODO: logger
		print "error"

	# Close files
	posfile.close()
	morphfile.close()
	
	return (wordsArray, disambiguatedArray)


# WithPOS to append POS to stemmed form with option "1" 
def StemmedForm(disambiguatedArray, withPOS):
	stemmedArray = []
	
	for sentence in disambiguatedArray:
		stemmedSentence = []
		for word in sentence:
			if withPOS == 0:
				stemmedSentence.append(word.split('/')[0])
			else:
				stemmedSentence.append(word.split('<')[0])
		stemmedArray.append(stemmedSentence)		 
	
	return stemmedArray


def SaveToFile(wordsArray, disambigutedArray, outputFilePath):
	outfile = open(outputFilePath, 'w')
	
	for sentences in range(0, len(disambigutedArray)):
		for words in range(0, len(disambigutedArray[sentences])):
			outfile.write(wordsArray[sentences][words] + '\t' + disambigutedArray[sentences][words] + '\n')
		outfile.write('\n')
	
	outfile.close()
	
