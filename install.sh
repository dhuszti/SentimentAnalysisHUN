#!/bin/sh
# You must run this shell script as a root privilege user with following command
# sudo ./install.sh

# -----------------------------------------------
# ----- Linux packages to download --------------
# -----------------------------------------------

# Basic packages to install
apt-get update
apt-get --assume-yes install build-essential
apt-get --assume-yes install cvs

# Packages for HunMorph tool
apt-get --assume-yes install ocaml
apt-get --assume-yes install texinfo
apt-get --assume-yes install ocaml-findlib
apt-get --assume-yes install texlive

# Packages for SzegedNER
apt-get update
apt-get --assume-yes install default-jre
apt-get --assume-yes install default-jdk

# Packages for HunPos
apt-get --assume-yes install --reinstall libc6-i386
dpkg-reconfigure dash


# -----------------------------------------------
# ----- Downloading and installing tools --------
# -----------------------------------------------

# Creating basic directory 
cd $HOME
mkdir SentimentAnalysisHUN
cd SentimentAnalysisHUN

# Download code and NLP tools' files from github repo 
wget https://github.com/dhuszti/SentimentAnalysisHUN/archive/master.zip
unzip SentimentAnalysisHUN-master.zip
rm SentimentAnalysisHUN-master.zip


# Install HunMorph
cd $HOME/SentimentAnalysisHUN/SentimentAnalysisHUN-master/resources
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
cd $HOME/SentimentAnalysisHUN/SentimentAnalysisHUN-master/resources
cd HunToken
tar -xvzf huntoken-1.6.tar.gz
rm huntoken-1.6.tar.gz
cd huntoken-1.6
make
make install

# Install HunPos
cd $HOME/SentimentAnalysisHUN/SentimentAnalysisHUN-master/resources
mkdir HunPos
cd HunPos
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/hunpos/hu_szeged_kr.model.gz
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/hunpos/hunpos-1.0-linux.tgz
tar -xvzf hunpos-1.0-linux.tgz
rm hunpos-1.0-linux.tgz
gzip -d hu_szeged_kr.model.gz

# Install typoing for Hungarian language
cd $HOME/SentimentAnalysisHUN/SentimentAnalysisHUN-master/resources
cd Typo
tar -xvzf ekezo.tar.gz
tar -xvzf p2iso.tar.gz
rm ekezo.tar.gz
rm p2iso.tar.gz

# Install NER from Polyglot http://polyglot.readthedocs.io/en/latest/NamedEntityRecognition.html
apt-get --assume-yes install python-numpy libicu-dev
pip install polyglot
polyglot download embeddings2.hu ner2.hu

# Install REST API framework & extension for ip determination
pip install Flask
pip install netifaces
pip install requests

# Set permissions to access files not only as root privilege user
chmod -R +r $HOME/SentimentAnalysisHUN

# -----------------------------------------------
# -------------- Test NLP tools  ----------------
# -----------------------------------------------

# Test NLP tools, whether there was any installation error
cd $HOME/SentimentAnalysisHUN
mkdir tempfiles
cd tempfiles
echo "Teszteljük a következő nyelvi eszközöket, Kiss Géza." >> test.txt 
# HunMorph test
echo "ablakot" | ocamorph --aff $HOME/SentimentAnalysisHUN/SentimentAnalysisHUN-master/resources/HunMorph/morphdb.hu/morphdb_hu.aff --dic $HOME/SentimentAnalysisHUN/SentimentAnalysisHUN-master/resources/HunMorph/morphdb.hu/morphdb_hu.dic
# HunToken test
cat test.txt | huntoken > test_huntoken.xml
cat test_huntoken.xml
# HunPos test
echo "ablakot" | $HOME/NLPtools/hunpos/hunpos-1.0-linux/hunpos-tag  $HOME/NLPtools/hunpos/hu_szeged_kr.model
# Typoing test
echo "teszteles" | $HOME/SentimentAnalysisHUN/SentimentAnalysisHUN-master/resources/Typo/ekezo/ekito.run | $HOME/SentimentAnalysisHUN/SentimentAnalysisHUN-master/resources/Typo/p2iso
rm test.txt
rm test_huntoken.xml
