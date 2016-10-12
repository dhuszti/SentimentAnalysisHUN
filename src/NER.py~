#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, getopt
import subprocess, tempfile
from os.path import expanduser

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'huntoken.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'huntoken.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   print 'Input file is "', inputfile
   print 'Output file is "', outputfile

   cmd_huntoken = "java -Xmx3G -jar /home/hd/Downloads/ner.jar -mode predicate -input "+inputfile+" -output " + outputfile
   p = subprocess.Popen(cmd_huntoken, stdout=subprocess.PIPE, shell=True)
   (output, err) = p.communicate()

if __name__ == "__main__":
   main(sys.argv[1:])
