# -*- coding: utf-8 -*-
import os, sys, getopt
import subprocess, linecache
import tempfile, csv

def stemmedform(posfile, morphfile, ofile):
	morphform(posfile, morphfile, ofile)
	tempfilename = '/tmp/tempfile.%s.txt' % os.getpid()
	tempfile = open(tempfilename, 'w+b')
	with open(ofile, 'r') as morph_results:
		csvreader = csv.reader(morph_results, delimiter='\t')
		for line in csvreader:
			if line[1] == 'UNKNOWN':
				tempfile.write(line[0] + '\t' + line[0] + '\n')
			else:
				tempfile.write(line[0] + '\t' + line[1].split('[')[0].split('<')[0] + '\n')

	tempfile.close()
	os.rename(tempfilename, ofile)	

def morphform(posfile, morphfile, ofile):
	# HunMorph Word Index
	IndexList_HunMorph = []
	i = 0
	with open(morphfile, 'r') as file1:
		for line in file1:
			if line != '\n':
				if line.startswith('> '):
					IndexList_HunMorph.append(i)
					i+=1
				else:
					i+=1

	Index_HunMorph_Length = len(IndexList_HunMorph)

	i = 0
	# Decision making part
	with open(ofile, 'w') as file_out:
	   with open(posfile, 'r') as file2:
		for line in file2:
			if line != '\n':
				file_out.write(line.split()[0] + '\t')
			  	# HunPos szofaj
			  	hunpos = line.split()[1]
		
				if i < (Index_HunMorph_Length-1):
					Start = IndexList_HunMorph[i]
					End = IndexList_HunMorph[i+1]
					i+=1

				HunMorph = []
				for num in range(Start+2,End+1):

					hunmorph = linecache.getline(morphfile, num)#.decode('utf8').encode('latin2')
					HunMorph.append(hunmorph)
			
				if len(HunMorph) == 1:					
					if hunpos == 'NUM':
						file_out.write(hunpos + '\n')
					else:	
						file_out.write(HunMorph[0])
				else:
					iterator = 0
					HunPosMorph = []
					# HunMorph results filter with HunPos
					for iterator in range(0,len(HunMorph)):
						if hunpos in HunMorph[iterator]:				
							HunPosMorph.append(HunMorph[iterator])
						iterator+=1
					# Filtered results' number is 0 - it can occur in case of no common det.
					if len(HunPosMorph) == 0:
						file_out.write(HunMorph[0] ) 
					# Filtered results' number is 1
					if len(HunPosMorph) == 1:	
						file_out.write(HunPosMorph[0] )
					# Filtered results' number is more than 1
					elif len(HunPosMorph) > 1:
						file_out.write(HunPosMorph[1] )

''' Options 
Argument values:
- 0: both POS and Morph applied, but stemmed form is used
- 1: both POS and Morph applied, but morhological analytics form is used
'''
def MorphologicalAnalysis(argument, posfile, morphfile, ofile):
	if argument == 0:
		stemmedform(posfile, morphfile, ofile)
	elif argument == 1:
		morphform(posfile, morphfile, ofile) 
	else:
		print "Please choose again"

def main():
	posfile='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunpos_ki.txt'
	morphfile='/home/osboxes/NLPtools/SentAnalysisHUN-master/hunmorph_ki.txt'
	outfile='/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'
	# Call this function to use morphological analysis
	MorphologicalAnalysis(0, posfile, morphfile, outfile)

if __name__ == '__main__':
	main()
