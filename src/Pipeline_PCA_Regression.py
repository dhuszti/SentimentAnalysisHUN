# Import sklearn functions
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion

# Import pipeline extension
import PipelineExtension


def pipeline_PCA_Regression(posLexicon, negLexicon):
	# create sklearn.pipeline for automated machine learning
	pipeline = Pipeline([
		
	    # Feature extraction part
	    ('features', FeatureUnion(
			transformer_list=[

			    # Dimension reduction with pca
			    ('pca', Pipeline([
					('countVec', CountVectorizer(encoding='latin2')),					
					('densify', PipelineExtension.Densifier()),		# densifier to apply toarray() transformation
					('pca', PCA(n_components=2)),			# this is called otherwise LSA, n_components need to have same number as input label category number
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
			    'pca': 1.0,
			    'sentdic_positive': 0.5,
			    'sentdic_negative': 0.5,
			},
	    	)),

	   # Regression
	   ('regression', LogisticRegression()),

	])


	return pipeline

def getparams_PCA_Regression():
	# use gridsearchCV for automated machine learning with multiple options - "parameters"
	params = {
	    'regression__solver': ['liblinear'],
	}

	return params

