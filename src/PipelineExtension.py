# Import libs
from numpy import array, recarray

# Import sklearn base classes
from sklearn.base import BaseEstimator, TransformerMixin


# FEATURES FOR SKLEARN.PIPELINE EXTENSION
""" There are some classes which are especially dedicated to
sklearn.pipeline's toolkit extension. """
 
class SentDictOccurancesFeature(BaseEstimator, TransformerMixin):
	""" This feature is used at next phase - "sklearn pipeline" - 
	to determine sentiment dictionary occurances by each tuple. """

	def __init__(self, posDict='', negDict=''):
		self.posDict = posDict
		self.negDict = negDict	
    	
	def fit(self, raw_documents, y=None):
       		return self
    	
	def fit_transform(self, raw_documents, y=None):
		return self.transform(raw_documents)

	def transform(self, raw_documents, y=None):
		PosNegOccurances = recarray(shape=(len(raw_documents),1), dtype=[('positive', int), ('negative', int)])		
		for i, sentence in enumerate(raw_documents):		
			PosOccurances = 0
			NegOccurances = 0	
			words = sentence.split()
			for word in words:
				if word in self.posDict:
					PosOccurances += 1
				elif word in self.negDict:
					NegOccurances += 1	

			PosNegOccurances['positive'][i]= PosOccurances
			PosNegOccurances['negative'][i]= NegOccurances	
		
		return PosNegOccurances


class ItemSelector(BaseEstimator, TransformerMixin):
	""" Itemselector is used at next phase at "sklearn pipeline". Its main role is
	to select positive or negative occurances in a tuple coming from
	'SentDictOccurancesFeature'.
	"""
	def __init__(self, key):
		self.key = key

	def fit(self, x, y=None):
		return self

	def transform(self, data_dict):
		return data_dict[self.key]


class Densifier(BaseEstimator):
	""" Densifier is used at next phase at "sklearn pipeline" to be capable of 
	applying PCA as dimension reduction method. Basically it is quite simple, 
	only transforms input format into array, which is prerequisite incoming 
	format of PCA.
	"""
	def __init__(self):
		BaseEstimator.__init__(self)

	def fit(self, X, y=None):
		pass
		
	def fit_transform(self, X, y=None):
		return self.transform(X)

	def transform(self, X, y=None):
		return X.toarray()


