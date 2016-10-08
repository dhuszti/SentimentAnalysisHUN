#!/bin/bash

# Neccesseraly files
SentimentCorpusPath=$HOME/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv
HunTokenPath=$HOME/NLPtools/HunToken/huntoken-1.6/bin/huntoken
HunPosTagPath=$HOME/NLPtools/hunpos/hunpos-1.0-linux/hunpos-tag
SzegedModelPath=$HOME/NLPtools/hunpos/hu_szeged_kr.model
XmlParserPath=$HOME/NLPtools/SentAnalysisHUN-master/real_project/xmlparser.py
OcamorphBinPath=$HOME/NLPtools/HunMorph/ocamorph/adm/morphdb_hu.bin

# Output files
HunPosOutputPath=$HOME/NLPtools/SentAnalysisHUN-master/hunpos_ki.txt
HunMorphOutputPath=$HOME/NLPtools/SentAnalysisHUN-master/hunmorph_ki.txt
MorphAnalysisOuputPath=$HOME/NLPtools/SentAnalysisHUN-master/morph_ki.txt

# Hunpos
cat $SentimentCorpusPath | cut -f5 -d$'\t' | huntoken | $XmlParserPath | sed ':a;N;$!ba;s/\n\n/\n/g' | $HunPosTagPath $SzegedModelPath > $HunPosOutputPath

# Hunmorph
cat $SentimentCorpusPath | cut -f5 -d$'\t' | huntoken | $XmlParserPath | sed ':a;N;$!ba;s/\n\n/\n/g' | ocamorph --bin $OcamorphBinPath > $HunMorphOutputPath
