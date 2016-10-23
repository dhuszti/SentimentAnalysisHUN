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
./MorphologicalAnalysis.sh -i $HOME/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new_with_posneg.csv -p $HOME/NLPtools/SentAnalysisHUN-master/hunpos_ki_with_posneg1.txt -m $HOME/NLPtools/SentAnalysisHUN-master/hunmorph_ki_with_posneg1.txt

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
HunTokenPath=$HOME/NLPtools/HunToken/huntoken-1.6/bin/huntoken
HunPosTagPath=$HOME/NLPtools/hunpos/hunpos-1.0-linux/hunpos-tag
SzegedModelPath=$HOME/NLPtools/hunpos/hu_szeged_kr.model
XmlParserPath=$HOME/Desktop/SentimentAnalysisHUN/src/xmlparser.py
OcamorphBinPath=$HOME/NLPtools/HunMorph/ocamorph/adm/morphdb_hu.bin

# Hunpos analysis
cat $SentimentCorpusPath | cut -f5 -d$'\t' | huntoken | $XmlParserPath | sed ':a;N;$!ba;s/\n\n/\n/g' | $HunPosTagPath $SzegedModelPath > $HunPosOutputPath

# Hunmorph analysis
cat $SentimentCorpusPath | cut -f5 -d$'\t' | huntoken | $XmlParserPath | sed ':a;N;$!ba;s/\n\n/\n/g' | ocamorph --bin $OcamorphBinPath > $HunMorphOutputPath
