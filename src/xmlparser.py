#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, fileinput

""" A light xml parser application which is good for transforming HunToken's xml based output into plain lines, 
which is necesseraly for input data form of HunPoS (part-of-speech tagging) and HunMorph (morphological analysis).
It is embedded in MorphologicalAnalysis.sh file's shell pipeline. """

def main():
	# Parse incoming XML file
	try:	
		for line in fileinput.input():
			if line.startswith("<w>"):
				print line.replace("<w>","").replace("</w>","").replace("\n","")
			if line.startswith("</s>"):
				print "thisistheending"
	except:
		print "ERROR at xmlparser.py file"			
	
if __name__ == '__main__':
	main()
