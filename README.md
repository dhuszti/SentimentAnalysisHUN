# Sentiment Analysis for Hungarian language

This is open-source sentiment analysis tool for Hungarian language, written in Python. The application has a REST API for easier access, and also accessible via Docker's container technology.

##Installation:
Docker container installation is suggested.
###1. Native way
	- Prerequisite: linux Operation System
		- Ubuntu 14.04 or plus is supported
		- Support for Debian, RHEL, CentOS coming very soon
	- Launch ./install.sh as root privileged user and accept every step of installation.					
	- Takes about 20-30 minutes
	
###2. Docker 
	- Install Docker for you Operation System: (https://docs.docker.com/engine/installation)
	- Docker repo: (https://hub.docker.com/r/dhuszti/sentanalysis/)
	- Download container: **docker pull dhuszti/sentanalysis:v1.0.0**
	- Run container: **docker run -d -it --privileged=true --net=host dhuszti/sentanalysis**

##Usage:
###1. Launch application with: 
	Native: **python $HOME/SentimentAnalysisHUN/src/Application.py**
	Docker: **docker exec -it dhuszti/sentanalysis python $HOME/SentimentAnalysisHUN/src/Application.py**

###2. Usage of REST API:
- Based on a HTTP POST request.
- Receive an url as launch: **http://<ip_addr_of_docker>:5000/sentiment**
- Please use sentence tag for adding input like this **{'sentence': '<write your input here>'}** to enter your input.
- Example: **curl -i -H "Content-Type: application/json" -X POST -d '{"sentence": "Budapest az egyik legszebb város."}' http://192.168.196.144:5000/sentiment**

##Sources
Following external open-source tools were applied, some of their installer files are collected at /resources folder. All of their rights are owned by their creators.

1. NLP tools - HunToken, HunPoS, Ocamorph & HunMorph, Polyglot NER
2. OpinHUBank sentiment corpus
3. Python Flask REST API - http://flask.pocoo.org/
4. Python packages - NumPy, SciPy, Sklearn, NLTK
