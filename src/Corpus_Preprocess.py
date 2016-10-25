# -*- coding: utf-8 -*-
import csv, re
from os.path import expanduser

''' The function CorpusPreprocess can transform OpinHuBank sentiment coprus into
digestable format for next process phrases. It can take corpus with every value
(positive/neutral/negative) or able to filter it to positive/negative ones.
This can be made with small modifications on "if reviewScore ..." if it is "!=0"
then later mentioned corpus is going to be created.

Parameters:
- in_file: whole url of source file
- out_file: whole url of sink
'''

def CorpusPreprocess(in_file, out_file):
	
	# Open input and output file
	inputfile = open(in_file,'rb')
	reader = csv.reader(inputfile, delimiter=',')
	# Skip header	
	next(reader, None)

	outputfile = open(out_file,'wb')
	writer = csv.writer(outputfile, delimiter='\t')

	# Iterate through lines of original corpus
	for line in reader:
		pass
		# Calculate reviewScore for every row	
		reviewScore = 0

		for i in range(6,11):
			if line[i] == '-1':
				reviewScore -= 1
			elif line[i] == '1':
				reviewScore += 1
		
		# Special letters to cleanse data at points where sentence not starts with capital one
		HunSpecLetters = str('ÁáÉéÍíÓóÖöŐőÚúÜüŰŰ').decode('utf8').encode('latin2')		
		
		# Filter rows to positive/negative reviews
		# CHANGE IT TO: 
		#	- reviewScore!=0 for only positive/negative entities
		#	- reviewScore<6 for both positive/negative/neutral entities
		if reviewScore != 0:
			''' Check for letter and make it uppercase later. '''
			firstLetter = 1
			for char in line[4][0:5]:
				if char.isalpha() or char in HunSpecLetters:
					break
				else:
					firstLetter += 1			
			''' 
			There are two main modifications, that are need to have operater in order to achieve equal element number after 	  		tokenization. Otherwise some entities were compromised.
			- start every sentence with a capital letter
			- if no	t first letter is the starting, then
			- add plus sentence closure marks to avoid mistakes caused by shortened forms
			- it won't have an effect on modell
			- treat sentences staring with special character "..." or "4. " with custom regulations
			'''
			if '...' in line[4][0:4]:
				line[4] = line[4][3:firstLetter].title() + line[4][firstLetter:] + '. '
			elif '4.' in line[4][0:4]:
				line[4] = line[4][3:firstLetter].title() + line[4][firstLetter:] + '. '			
			else:
				line[4] = line[4][0:firstLetter].title() + line[4][firstLetter:] + '. '
			writer.writerow(line)	
					
	# Close files
	inputfile.close()
	outputfile.close()

def main():
	# Get home folder
	homeFolder = expanduser('~')
	
	# Launch corpus preprocess function
	inputfile = homeFolder + '/SentimentAnalysisHUN-master/resources/SentimentCorpus/OpinHuBank_20130106.csv' 
	outputfile = homeFolder + '/SentimentAnalysisHUN-master/tempfiles/OpinHuBank_20130106_posneg.csv'
	CorpusPreprocess(inputfile, outputfile)

if __name__ == '__main__':
	main()
