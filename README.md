# Sentiment Analysis for Hungarian language

This is open-source sentiment analysis tool for Hungarian language, written in Python. The application has a REST API for easier access, and also accessible via Docker's container technology.

##Installation:
Docker container installation is suggested.
###1. Native way
- Prerequisite: linux Operation System
	- Ubuntu, tested for only 14.04 LTS
	- Debian, RHEL, CentOS done, but not yet tested for more distributions
- Launch `./install.sh` as root privileged user and accept every step of installation.					
- Takes about 20-30 minutes
	
###2. Docker 
- Install Docker for you Operation System: (https://docs.docker.com/engine/installation)
- Docker repo: (https://hub.docker.com/r/dhuszti/sentanalysis/)
- Download container: `docker pull dhuszti/sentanalysis`
- Run container: `docker run -d -it --privileged=true --net=host -e LANG=C.UTF-8 --name=sentanalysishun dhuszti/sentanalysis`

##Usage:
###1. Launch application with: 
- Native: `python $HOME/SentimentAnalysisHUN-master/src/Application.py`
- Docker: `docker exec -it sentanalysishun python $HOME/SentimentAnalysisHUN-master/src/Application.py`

###2. Usage of REST API:
- Based on a HTTP POST request.
- Receive an url (substitute to example): `http://ip_addr_of_docker:5000/sentiment`
- Please use sentence tag for adding input like this `{'sentence': '<write your input here>'}` to enter your input.
- Tool has two different HTTP POST requests:
	- `/sentiment`: 	for overall score
	- `/sentiment_verbose`: for more detailed scores
- Example usage on Linux/Mac with console curl: `curl -i -H "Content-Type: application/json" -X POST -d '{"sentence": "Budapest az egyik legszebb város."}' http://<ip_of_your_machine>:5000/sentiment`
- For Windows use a REST client like https://github.com/wiztools/rest-client

##Sources
Following external open-source tools were applied, some of their installer files are collected at /resources folder. All of their rights are owned by their creators.

1. NLP tools - HunToken, HunPoS, Ocamorph & HunMorph, Polyglot NER
2. OpinHUBank sentiment corpus
3. Python Flask REST API - http://flask.pocoo.org/
4. Python packages - NumPy, SciPy, Sklearn, NLTK
