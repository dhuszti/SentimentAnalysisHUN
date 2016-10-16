#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, getopt, csv
from polyglot.text import Text

# This function creates 3 dictionaries for location, person and organization. Important, both ones are in UNICODE encoding! 
def NER_Dictionary(CorpusFilePath):
	corpusfile = open(CorpusFilePath, 'rb')
	csvreader = csv.reader(corpusfile, delimiter='\t')

	locationList = []
	personList = []
	organizationList = []

	tempList = []

	for line in csvreader:
		try:
			blob = str(line[4]).decode('latin2')
			text = Text(blob)
			for sent in text.sentences:
				for entity in sent.entities:
					if entity not in tempList:
				    		if 'PER' in entity.tag:
							personList.extend(entity)
						elif 'LOC' in entity.tag:
							locationList.extend(entity)
						elif 'ORG' in entity.tag:
							organizationList.extend(entity)

					tempList.extend(entity)
		except:
			pass
	
	return (locationList, personList, organizationList)
	

def main():
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	(locationList, personList, organizationList) = NER_Dictionary(PreprocessedCorpusPath)

	print locationList


if __name__ == "__main__":
   	main()
