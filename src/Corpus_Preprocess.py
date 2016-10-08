# -*- coding: utf-8 -*-
import csv

'''
Sentiment corpus preprocessing - only for OpinHuBank corpus

Parameters:
- in_file: whole url of source file
- out_file: whole url of sink
'''

def CorpusPreprocess(in_file, out_file):
	
	# Open input and output file
	inputfile = open(in_file,'rb')
	reader = csv.reader(inputfile, delimiter=',')

	outputfile = open(out_file,'wb')
	writer = csv.writer(outputfile, delimiter='\t')

	# Iterate through lines of original corpus
	for line in reader:
		# Calculate reviewScore for every row	
		reviewScore = 0

		for i in range(7,11):
			if line[i] == '-1':
				reviewScore -= 1
			elif line[i] == '1':
				reviewScore += 1
	
		# Filter rows to positive/negative reviews
		if reviewScore != 0:
			''' 
			There are two main modifications, that are need to have operater in order to achieve equal element number after 	  		tokenization. Otherwise some entities were compromised.
			- start every sentence with a capital letter
			- add plus sentence closure marks to avoid mistakes caused by shortened forms
			- it won't have an effect on modell
			'''
			line[4] = line[4][0:1].title() + line[4][1:] + '. '
			writer.writerow(line)	
	# Close files
	inputfile.close()
	outputfile.close()

def main():
	inputfile = '/home/osboxes/Downloads/archive/OpinHuBank_20130106.csv' 
	outputfile = '/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	CorpusPreprocess(inputfile, outputfile)

if __name__ == '__main__':
	main()

