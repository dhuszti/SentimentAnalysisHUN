# -*- coding: utf-8 -*-
import netifaces, logging, requests

# Flask was used as REST API framework http://flask.pocoo.org/docs/0.11/
# Tutorial https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
from flask import Flask, jsonify, abort, make_response, request, url_for

from Application_functions import OverallSentiment
from Application_functions import NERsentiment
from Application_functions import MorphAnalysis
from Application_functions import NER

# Initialization of logger
logger = logging.getLogger('SentimentAnalysisHUN')
filehandler = logging.FileHandler('/var/tmp/SentimentAnalysisHUN.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)
logger.setLevel(logging.WARNING)

# Github Read
githubUrl = 'https://github.com/dhuszti/SentimentAnalysisHUN/blob/master/README.md'


""" This is a REST API for easier user interface access to the sentiment analysis tool

Defined functions:
- GET for /: overview page contains usage example
- POST for /sentiment: request for an overall sentiment score
- POST for /sentiment_verbose: request for more detailed (entity focused) sentiment scores

*** All rights are reserved by open-source Flask REST API framework. *** """

app = Flask(__name__)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/', methods = ['GET'])
def description():
    return requests.get(githubUrl).text

@app.route('/sentiment', methods=['POST'])
def sentiment():
	if not request.json or not 'sentence' in request.json:
		abort(400)
	try:
		# get morphological analyzed output
		morphAnalyzed = MorphAnalysis(request.json['sentence'])

		# get NER dictionaries extracted from input text		
		(locationList, personList, organizationList) = NER(request.json['sentence'])

		sentimentList = []

		# call sentiment for overall scores
		OverallSentiment(request.json['sentence'], morphAnalyzed, sentimentList)
	except Exception:
		logger.error("Exception occurred at http post request for /sentiment")
		logger.exception("Sentiment_exception")

	# return output as jsonify
	return jsonify(results = sentimentList), 201

@app.route('/sentiment_verbose', methods=['POST'])
def sentiment_verbose():
	if not request.json or not 'sentence' in request.json:
		abort(400)

	try:
		# get morphological analyzed output
		morphAnalyzed = MorphAnalysis(request.json['sentence'])
	
		# get NER dictionaries extracted from input text		
		(locationList, personList, organizationList) = NER(request.json['sentence'])

		sentimentList = []

		# call sentiment for overall scores
		OverallSentiment(request.json['sentence'], morphAnalyzed, sentimentList)

		# call sentiment for named-entity related scores
		NERsentiment(morphAnalyzed, locationList, 'location', sentimentList)
		NERsentiment(morphAnalyzed, personList, 'person', sentimentList)
		NERsentiment(morphAnalyzed, organizationList, 'organization', sentimentList)

	except Exception:
		logger.error("Exception occurred at http post request for /sentiment_verbose")
		logger.exception("Sentiment_verbose_exception")

	# return output as jsonify
	return jsonify(results = sentimentList), 201



""" Main function for Sentiment Analysis API access """
def main():
	# Network interfaces determination for IP address determination. 
	# source: http://stackoverflow.com/questions/11735821/python-get-localhost-ip
	try:	
		interfaces = netifaces.interfaces()
		for i in interfaces:
			if i == 'lo':
				continue
			iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
			if iface != None:
				for j in iface:
					ip_addr = j['addr']
	except Exception:
		logger.error("Exception occurred while determining IP address")
		logger.exception("IP_Address_exception")

	# short user guide
	print "\033[0;32m ****************************************************************************** \033[0m"
	print "\033[0;32m This is an open-source Sentiment Analysis tool created for Hungarian language. \033[0m"
	print ""
	print "\033[0;32m Please use sentence tag for adding user input. Example {\"sentence\": \"Teszt mondat\"} \033[0m"
	print ""
	print "\033[0;32m Tool has two different HTTP POST request:\033[0m"
	print "\033[0;32m	/sentiment: 	for overall score  \033[0m"
	print "\033[0;32m	/sentiment_verbose: for more detailed scores \033[0m"
	print ""
	print "\033[0;32m Usage example from Linux/Mac console with curl: \033[0m"
	print "\033[0;32m curl -i -H 'Content-Type: application/json' -X POST -d '{\"sentence\": \"Budapest az egyik legszebb város.\"}' http://"+ip_addr+":5000/sentiment \033[0m"
	print ""
	print "\033[0;32m For Windows use an REST client like https://github.com/wiztools/rest-client \033[0m"
	print "\033[0;32m ****************************************************************************** \033[0m"
	print "\033[0;32m This tool is running on: \033[0m"

	# run application
	try:
		app.config['JSON_AS_ASCII'] = False
		app.run(host=ip_addr, port=5000)
	except Exception:
		logger.error("Exception occurred while started running application")
		logger.exception("App_run_exception")

if __name__ == '__main__':
	main()
