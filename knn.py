from sklearn.neighbors import NearestNeighbors
import numpy as np
import random	
import os.path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.externals import joblib
from test_data import TestData

class Knn:

	def fit(self, train):
		self.train = train
		self.nbrs = NearestNeighbors(n_neighbors=10).fit(train) # choose the 5 nearest neighbors

	def predict(self, to_predict):
		indices,distances = self.getKNN(to_predict)
		return [self.train[i] for i in indices]

	def getKNN(self,to_predict):
		distances, indices = self.nbrs.kneighbors(test.reshape(1,-1) , n_neighbors=10) # but take only the closest
		return indices,distances
		# This is the proof that the best match is in the cluster

if __name__ == '__main__':
	knn = Knn()
	t = TestData()
	X, test = t.generateTrainData(3700,1000)
	knn = Knn()
	knn.fit(X)
	print knn.predict(test)
