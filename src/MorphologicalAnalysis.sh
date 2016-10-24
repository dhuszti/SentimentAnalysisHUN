#!/bin/bash

<<COMMENT  
Launching morhological analysis and part-of-speech tagging
with following parameters
-input: input parameter for preprocessed sentiment corpus path
-posfile: output parameter, determines a filepath to write part-of-speech tagging results
-morphfile: output parameter, determines a filepath to write morhological analysis results

Usage:
./MorphologicalAnalysis.sh -i <inputfile> -p <output_posfile> -m <output_morphfile>

Example usage:
./MorphologicalAnalysis.sh -i $HOME/SentimentAnalysisHUN-master/tempfiles/OpinHuBank_20130106_posneg.csv -p $HOME/SentimentAnalysisHUN-master/tempfiles/hunpos_posneg.txt -m $HOME/SentimentAnalysisHUN-master/tempfiles/hunmorph_posneg.txt

COMMENT


# Read inputs
while getopts ":i:p:m:" opt; do
  case $opt in
    i)
      echo "Sentiment corpus file: $OPTARG" >&2
	  SentimentCorpusPath=$OPTARG
      ;;
	p)
	  echo "PoS output file: $OPTARG" >&2
	  HunPosOutputPath=$OPTARG
	  ;;
	m)
	  echo "Morph output file: $OPTARG" >&2
	  HunMorphOutputPath=$OPTARG
	  ;; 
    \?)
      echo "Invalid option: -$OPTARG Please use -i <inputfile> -p <output_posfile> -m <output_morphfile>" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument. Please use -i <inputfile> -p <output_posfile> -m <output_morphfile>" >&2
      exit 1
      ;;
  esac
done

# Necesseraly files for launching analysis tasks. They are predifened by installation.
HunTokenPath=$HOME/SentimentAnalysisHUN-master/resources/HunToken/huntoken-1.6/bin/huntoken
HunPosTagPath=$HOME/SentimentAnalysisHUN-master/resources/HunPos/hunpos-1.0-linux/hunpos-tag
SzegedModelPath=$HOME/SentimentAnalysisHUN-master/resources/HunPos/hu_szeged_kr.model
XmlParserPath=$HOME/SentimentAnalysisHUN-master/src/xmlparser.py
OcamorphBinPath=$HOME/SentimentAnalysisHUN-master/resources/HunMorph/morphdb.hu/morphdb_hu.bin

# Hunpos analysis
cat $SentimentCorpusPath | cut -f5 -d$'\t' | huntoken | $XmlParserPath | sed ':a;N;$!ba;s/\n\n/\n/g' | $HunPosTagPath $SzegedModelPath > $HunPosOutputPath

# Hunmorph analysis
cat $SentimentCorpusPath | cut -f5 -d$'\t' | huntoken | $XmlParserPath | sed ':a;N;$!ba;s/\n\n/\n/g' | ocamorph --bin $OcamorphBinPath > $HunMorphOutputPath
