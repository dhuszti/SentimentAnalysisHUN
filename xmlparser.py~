#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, fileinput

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
