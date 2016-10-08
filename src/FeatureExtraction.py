# -*- coding: utf-8 -*-
import os, sys, getopt, csv, nltk, numpy
from tfidf import calculate_tfidf
from Postprocess import PostFiltering

# Functions for word extraction, feature extraction

def get_words_from_array(sentencesArray):
    all_words = []
    for words in sentencesArray:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(sentencesArray, word_features):
    features = []  
    for array_element in sorted(sentencesArray):
	temp = []
	for it in sorted(word_features):
		if it not in array_element:
			temp.append(0)
		else:
			temp.append(1)
	features.append(temp)
    return features


def main():
	MorphResultsFilePath='/home/osboxes/NLPtools/SentAnalysisHUN-master/morph_ki.txt'
	PreprocessedCorpusPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv'
	StopwordsPath='/home/osboxes/NLPtools/SentAnalysisHUN-master/real_project/stopwords.csv'
	TFIDFthreshold=0.4	
	IntervalNumber=5
	OnOffFlag=1

	FilteredArray = PostFiltering(MorphResultsFilePath, PreprocessedCorpusPath, TFIDFthreshold, StopwordsPath, IntervalNumber, OnOffFlag)
	
	word_features = get_word_features(get_words_from_array(FilteredArray))
	extract_features(FilteredArray, word_features)
	

if __name__ == '__main__':
	main()

