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

	for line in csvreader:
		try:
			blob = str(line[4]).decode('latin2')
			text = Text(blob)
			for sent in text.sentences:
				for entity in sent.entities:
			    		if 'PER' in entity.tag and entity not in personList:
						personList.append(entity)
					elif 'LOC' in entity.tag and entity not in locationList:
						locationList.append(entity)
					elif 'ORG' in entity.tag and entity not in organizationList:
						organizationList.append(entity)
		except:
			pass
	
	return (locationList, personList, organizationList)
	

def main():
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	(locationList, personList, organizationList) = NER_Dictionary(PreprocessedCorpusPath)

	print locationList


if __name__ == "__main__":
   	main()
