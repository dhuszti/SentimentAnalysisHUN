#!/bin/bash

# Neccesseraly files
SentimentCorpusPath=$HOME/NLPtools/SentAnalysisHUN-master/OpinHuBank_20130106_new.csv
HunTokenPath=$HOME/NLPtools/HunToken/huntoken-1.6/bin/huntoken
HunPosTagPath=$HOME/NLPtools/hunpos/hunpos-1.0-linux/hunpos-tag
SzegedModelPath=$HOME/NLPtools/hunpos/hu_szeged_kr.model
XmlParserPath=$HOME/Desktop/SentimentAnalysisHUN/src/xmlparser.py
OcamorphBinPath=$HOME/NLPtools/HunMorph/ocamorph/adm/morphdb_hu.bin
SzegedNERPath=$HOME/NLPtools/SzegedNER/ner.jar
SzegedNERInputPath=$HOME/NLPtools/SentAnalysisHUN-master/NER_input.txt

# Output files
HunPosOutputPath=$HOME/NLPtools/SentAnalysisHUN-master/hunpos_ki.txt
HunMorphOutputPath=$HOME/NLPtools/SentAnalysisHUN-master/hunmorph_ki.txt
SzegedNERPath=$HOME/NLPtools/SentAnalysisHUN-master/SzegedNER.txt

# Hunpos
#cat $SentimentCorpusPath | cut -f5 -d$'\t' | huntoken | $XmlParserPath | sed ':a;N;$!ba;s/\n\n/\n/g' | $HunPosTagPath $SzegedModelPath > $HunPosOutputPath

# Hunmorph
#cat $SentimentCorpusPath | cut -f5 -d$'\t' | huntoken | $XmlParserPath | sed ':a;N;$!ba;s/\n\n/\n/g' | ocamorph --bin $OcamorphBinPath > $HunMorphOutputPath

# SzegedNER
cat $SentimentCorpusPath | cut -f5 -d$'\t' > $SzegedNERInputPath
java -Xmx3G -jar /home/osboxes/NLPtools/SzegedNER/ner.jar -mode predicate -input $SzegedNERInputPath -output $SzegedNERPath
