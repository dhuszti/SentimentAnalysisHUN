# -*- coding: utf-8 -*-
import netifaces, logging, subprocess, requests
from sklearn.externals import joblib

# Flask was used as REST API framework http://flask.pocoo.org/docs/0.11/
# Tutorial followed https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
from flask import Flask, jsonify, abort, make_response, request, url_for

from Morphological_Disambiguation import MorphologicalDisambiguation, StemmedForm
from Classifier import CountVectorizerTransform_input

# LOGGING INIT
logger = logging.getLogger('SentimentAnalysisHUN')
filehandler = logging.FileHandler('/var/tmp/SentimentAnalysisHUN.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)
logger.setLevel(logging.WARNING)

# GLOBAL VARIABLES
ML_model = joblib.load(open('SentAnalysisModel.pkl'))						# Load ML model file
xmlparserFilePath = '$HOME/Desktop/SentimentAnalysisHUN/src/xmlparser.py'
hunpostagFilePath = '$HOME/NLPtools/hunpos/hunpos-1.0-linux/hunpos-tag'
szegedmodelFilePath = '$HOME/NLPtools/hunpos/hu_szeged_kr.model'
ocamorphFilePath = '$HOME/NLPtools/HunMorph/ocamorph/adm/morphdb_hu.bin'
posFilePath = '/tmp/sentanalysis_pos.txt'
morphFilePath = '/tmp/sentanalysis_morph.txt'
githubUrl = 'https://raw.githubusercontent.com/dhuszti/SentimentAnalysisHUN/master/README'


# REST API creation
""" All rights are reserved by open-source Flask REST API framework. """
app = Flask(__name__)

# ERROR HANDLERS
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

# Overview page for sentiment analysis tool
@app.route('/', methods = ['GET'])
def description():
    return requests.get(githubUrl).text

# HTTP POST REQUEST FOR SENTIMENT ANALYSIS
@app.route('/sentiment', methods=['POST'])
def sentiment():
    if not request.json or not 'sentence' in request.json:
        abort(400)

    sentiment = {
        'sentence': request.json['sentence'].encode('utf8'),
        #'entity': 'Sando Chan',
		'sentiment': SentimentAnalysis(request.json['sentence'])
    }
  
    return jsonify({'sentiment': sentiment}), 201



""" Sentiment analysis function for incoming tuple """ 
def SentimentAnalysis(inputString):
	# Typoing
	#cmd = 'echo ' + inputString.encode('latin2') + ' | $HOME/NLPtools/typo/ekezo/ekito.run | $HOME/NLPtools/typo/p2iso '			
	#p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	#(typo_out, err) = p.communicate()

	# part-of-speech tagging 
	cmd = 'echo ' + inputString.encode('latin2') + ' | huntoken | ' + xmlparserFilePath + ' | ' + hunpostagFilePath + ' ' + szegedmodelFilePath + ' > ' + posFilePath			
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	(pos_out, err) = p.communicate()
	
	# morphological analysis
	cmd = 'echo ' + inputString.encode('latin2') + ' | huntoken | ' + xmlparserFilePath + ' | ocamorph --bin ' + ocamorphFilePath + ' > ' + morphFilePath			
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	(morph_out, err) = p.communicate()

	# morph disambiguation with stemmed form without POS tagging
	(wordsArray, disArray) = MorphologicalDisambiguation(posFilePath, morphFilePath)
	stemmedArray = StemmedForm(disArray, 0)
	
	# convert every word to lowercase
	stemmedArray = [[word.lower() for word in sent] for sent in stemmedArray]
	
	# convert to countvectorizer digestible format
	List = CountVectorizerTransform_input(stemmedArray)

	return ML_model.predict(List)[0]



""" Main function for Sentiment Analysis API access """
def main():
	# Network interfaces determination for IP address determination. 
	# source: http://stackoverflow.com/questions/11735821/python-get-localhost-ip
	interfaces = netifaces.interfaces()
	for i in interfaces:
	    if i == 'lo':
		continue
	    iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
	    if iface != None:
		for j in iface:
		    ip_addr = j['addr']

	# Run application with REST API
	print "\nThis is an open-source Sentiment Analysis tool created for Hungarian language.\n"
	print "Please use sentence tag for adding input\n"
	print "Usage example:\ncurl -i -H 'Content-Type: application/json' -X POST -d '{'sentence': 'Budapest az egyik legszebb város.'}' http://192.168.196.144:5000/sentiment\n"
	print "Please use url below to access API from other machine:"
	app.run(host=ip_addr, port=5000)
	
if __name__ == '__main__':
	main()
