# Import sklearn functions
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.naive_bayes import MultinomialNB

# Import pipeline extension
import PipelineExtension

def pipeline_TFIDF_NaiveBayes(posLexicon, negLexicon):
	# create sklearn.pipeline for automated machine learning
	pipeline = Pipeline([
		
	    # Feature extraction part
	    ('features', FeatureUnion(
			transformer_list=[

			    # TF-IDF to have a more accurate overview on words, which have a huge influance on sentiment analysis
			    ('tfidf', Pipeline([
					('basic_cv', CountVectorizer(encoding='latin2')),
					('tfidf', TfidfTransformer()),
			    ])),

			    # Positive and negative sentiment dictionary occurances as a feature
			    ('sentdic_positive', Pipeline([
					('sentDicOcc', PipelineExtension.SentDictOccurancesFeature(posDict=posLexicon, negDict=negLexicon)),
					('posOcc', PipelineExtension.ItemSelector(key='positive'))
			    ])),
			    ('sentdic_negative', Pipeline([
					('sentDicOcc', PipelineExtension.SentDictOccurancesFeature(posDict=posLexicon, negDict=negLexicon)),
					('negOcc', PipelineExtension.ItemSelector(key='negative'))
			    ])),

			],

			# weight components in FeatureUnion
			transformer_weights={
			    'tfidf': 1.0,
			    'sentdic_positive': 0.5,
			    'sentdic_negative': 0.5,
			},
	    	)),
	   # Naive Bayes classifier
	   ('classifier', MultinomialNB()),

	])


	return pipeline

def getparams_TFIDF_NaiveBayes():
	# use gridsearchCV for automated machine learning with multiple options - "parameters"
	params = {
	    'classifier__alpha': [1.0], 		#[0.5, 0.75, 1.0, 1.25, 1.5],
	    'classifier__class_prior': [None],
	    'classifier__fit_prior': [True],
	}

	return params

