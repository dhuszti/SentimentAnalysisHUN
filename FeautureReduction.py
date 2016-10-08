# -*- coding: utf-8 -*-


def sentdic(FilePath):
	SentDic = []
	# "/home/osboxes/NLPtools/SentAnalysisHUN-master/hu_pos_morph.txt" & hu_neg_morph.txt
	dic_file = open(FilePath,'rb')
	for line in dic_file:
		SentDic.append(line.replace('\n','').replace('\r',''))
	return SentDic

def featureReduction():
	
	return TrainingSet

def main():


if __name__ == '__main__':
	main()
