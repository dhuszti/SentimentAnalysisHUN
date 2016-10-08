# -*- coding: utf-8 -*-
from __future__ import division
import math

''' 
TF-IDF module

TF: raw frequency calculation 
IDF: smooth frequency calculation 

Parameters:
- word: a simple string
- sentence: a list of strings
- sentencelist: a list of "sentence"-s
'''

def tf(word, wordslist):
	return wordslist.count(word) / len(wordslist)

def idf(word, sentencelist):
	occuranceNum = 0
	for sentence in sentencelist:
    		if word in sentence:
			occuranceNum += 1
	return math.log(1 + len(sentencelist) / occuranceNum)

def calculate_tfidf(word, sentence, sentencelist):
	return tf(word, sentence) * idf(word, sentencelist)


def main():
	sentence = ['egy','kettő']
 	sentenceslist = [['egy','kettő'],['kettő','három','négy'],['három','négy','öt']]
 	print calculate_tfidf('egy', sentence, sentenceslist)

if __name__ == '__main__':
	main()
