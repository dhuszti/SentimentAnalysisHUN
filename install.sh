#!/bin/sh
# You must run this shell script as a root privilege user with following command
# sudo ./install.sh

# Get OS distribution for installer
OSdistribution=$(cat /etc/*release | grep '^NAME=' | sed -e 's/NAME=//g' | sed -e 's/"//g' )
# Remove white spaces
OSdistribution=${OSdistribution// /}

# -----------------------------------------------
# ----- Linux packages to download --------------
# -----------------------------------------------

# installer depends on OS distibution
if [[ "$OSdistribution" == 'CentOSLinux' ] || [ "$OSdistribution" == 'RedHat' ]]
then
	# Basic packages to install
	yum update
	yum -y groupinstall 'Development Tools'
	yum -y install cvs

	# Packages for HunMorph tool
	yum -y install ocaml
	yum -y install texinfo
	yum -y install ocaml-findlib
	yum -y install texlive

	# Packages for HunPos
	yum -y install glibc.i686
	dpkg-reconfigure dash

	# Install python pip
	yum -y install python-dev
	yum -y install python-setuptools
	easy_install pip

	# Python skearn prerequisites
	yum -y install libblas-dev liblapack-devel libatlas-base-dev gfortran

	# Polyglot prerequisite
	yum -y install libicu-dev
  
elif [[ "$OSdistribution" == 'Ubuntu' ] || [ "$OSdistribution" == 'Debian' ]]
then
	# Basic packages to install
	apt-get update
	apt-get --assume-yes install build-essential
	apt-get --assume-yes install cvs

	# Packages for HunMorph tool
	apt-get --assume-yes install ocaml
	apt-get --assume-yes install texinfo
	apt-get --assume-yes install ocaml-findlib
	apt-get --assume-yes install texlive

	# Packages for HunPos
	apt-get --assume-yes install --reinstall libc6-i386
	dpkg-reconfigure dash

	# Install python pip
	apt-get --assume-yes install python-dev
	apt-get --assume-yes install python-setuptools
	easy_install pip

	# Python skearn prerequisites
	apt-get --assume-yes install libblas-dev liblapack-devel libatlas-base-dev gfortran

	# Polyglot prerequisite
	apt-get --assume-yes install libicu-dev

else
	echo "OS distribution is not supported."
fi

# -----------------------------------------------
# ----- Downloading and installing tools --------
# -----------------------------------------------

# Change HOME directory where installation is going to be placed
cd $HOME

# Download code from github repo 
wget https://github.com/dhuszti/SentimentAnalysisHUN/archive/master.zip
unzip master.zip
rm master.zip

# Install HunMorph
cd $HOME/SentimentAnalysisHUN-master/resources
cd HunMorph
tar -xvzf morphdb.hu.tar.gz
tar -xvzf ocamorph.tar.gz
rm morphdb.hu.tar.gz
rm ocamorph.tar.gz
cd ocamorph
make clean
make
make install
echo " " >> ~/.bashrc
echo "# Ocamorph for HunMorph NLP tool" >> ~/.bashrc
echo "PATH=${PATH}:$HOME/NLPtools/HunMorph/ocamorph/adm" >> ~/.bashrc

# Install HunToken
cd $HOME/SentimentAnalysisHUN-master/resources
cd HunToken
tar -xvzf huntoken-1.6.tar.gz
rm huntoken-1.6.tar.gz
cd huntoken-1.6
make
make install

# Install HunPos
cd $HOME/SentimentAnalysisHUN-master/resources
mkdir HunPos
cd HunPos
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/hunpos/hu_szeged_kr.model.gz
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/hunpos/hunpos-1.0-linux.tgz
tar -xvzf hunpos-1.0-linux.tgz
rm hunpos-1.0-linux.tgz
gzip -d hu_szeged_kr.model.gz

# Install typoing for Hungarian language
cd $HOME/SentimentAnalysisHUN-master/resources
cd Typo
tar -xvzf ekezo.tar.gz
tar -xvzf p2iso.tar.gz
rm ekezo.tar.gz
rm p2iso.tar.gz

# Install python sklearn with prerequisites
pip install -U numpy
pip install -U scipy
pip install -U scikit-learn

# Install NLTK
pip install -U nltk

# Install NER from Polyglot http://polyglot.readthedocs.io/en/latest/NamedEntityRecognition.html
pip install polyglot
polyglot download embeddings2.hu ner2.hu ner2.cs embeddings2.cs

# Install REST API framework & extension for ip determination
pip install -U Flask
pip install -U netifaces
pip install -U requests

# -----------------------------------------------
# -------------- Test NLP tools  ----------------
# -----------------------------------------------

# Test NLP tools, whether there was any installation error
cd $HOME/SentimentAnalysisHUN-master/
mkdir tempfiles
cd tempfiles
echo "Teszteljük a következő nyelvi eszközöket, Kiss Géza." >> test.txt 
# HunMorph test
echo "ablakot" | ocamorph --aff $HOME/SentimentAnalysisHUN-master/resources/HunMorph/morphdb.hu/morphdb_hu.aff --dic $HOME/SentimentAnalysisHUN-master/resources/HunMorph/morphdb.hu/morphdb_hu.dic --bin $HOME/SentimentAnalysisHUN-master/resources/HunMorph/morphdb.hu/morphdb_hu.bin
# HunToken test
cat test.txt | huntoken > test_huntoken.xml
cat test_huntoken.xml
# HunPos test
echo "ablakot" | $HOME/SentimentAnalysisHUN-master/resources/HunPos/hunpos-1.0-linux/hunpos-tag  $HOME/SentimentAnalysisHUN-master/resources/HunPos/hu_szeged_kr.model
# Typoing test
echo "teszteles" | $HOME/SentimentAnalysisHUN-master/resources/Typo/ekezo/ekito.run | $HOME/SentimentAnalysisHUN-master/resources/Typo/p2iso
rm test.txt
rm test_huntoken.xml

# ---------------------------------------------------
# Set permissions to access files not only as root privilege user
# ---------------------------------------------------
chmod 777 -R $HOME/SentimentAnalysisHUN-master/*
