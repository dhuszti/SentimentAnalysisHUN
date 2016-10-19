#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, getopt, csv
from polyglot.text import Text
from itertools import chain

# This function creates 3 dictionaries for location, person and organization. Important, every result set is in UNICODE encoding! 
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
					tag = entity.tag
					for element in entity:
						if element not in chain(personList, locationList, organizationList):
					    		if 'PER' in tag:
								personList.append(element)
							elif 'LOC' in tag:
								locationList.append(element)
							elif 'ORG' in tag:
								organizationList.append(element)
		except:
			pass
	
	# Filter out some mistaken nouns
	person = []
	for word in personList:
    		if word[0].isupper():
        		person.append(word)

	# Sort them to make it more understandable for human beings
	locationList = sorted(locationList)
	personList = sorted(person)
	organizationList = sorted(organizationList)	

	return (locationList, personList, organizationList)
	

def main():
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	(locationList, personList, organizationList) = NER_Dictionary(PreprocessedCorpusPath)

	print personList


if __name__ == "__main__":
   	main()
