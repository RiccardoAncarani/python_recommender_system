from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
import numpy as np
import random	
import os.path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.externals import joblib
import pickle

class Recommender:
	n_features = 10
	n_samples = 500
	model_name = 'model.pkl'
	train_object = 'train.pkl'

	def saveModel(self,km,X):
		'''
		Save the current model
		'''
		joblib.dump(X, self.train_object)
		joblib.dump(km, self.model_name) 
		

	def restoreModel(self):
		'''
		Restore the model
		'''
		self.km = joblib.load(self.model_name)
		self.X = joblib.load(self.train_object)

	def createJunkData(self):
		return np.array([self.generateJunkVector(self.n_features) for i in range(self.n_samples)])

	def generateJunkVector(self,n):
		return np.array([random.randrange(0,2) for i in range(n)])

	# Print all elements that belong to a particular cluster
	def ClusterIndicesNumpy(self,clustNum, labels_array): 
	    return np.where(labels_array == clustNum)[0]

	def generateTrainData(self):
		X = self.createJunkData()
		test = self.generateJunkVector(self.n_features).reshape(1,self.n_features)
		return X,test

	def fit(self,X):
		km = MiniBatchKMeans(n_clusters=10)
		km.fit(X)
		self.saveModel(km,X)
		return km

	def predictAndGetElements(self,elements,to_predict):
		'''
		Predict a value and returns all elements that beongs
		to the predicted cluster
		elements = the train data, where to extract elements
		to_predict = the vector to be predicted
		'''
		prediction = self.km.predict(to_predict) # prediction is the label of the cluster
		print to_predict # print the test vector for visual comparing
		cluster_elements =  self.ClusterIndicesNumpy(prediction,self.km.labels_)
		res = np.array([elements[c] for c in cluster_elements]) # All the elements that belongs to the predicted cluster
		return res

	def predict(self,to_predict):
		to_predict = np.array(to_predict)
		res = self.predictAndGetElements(self.X,to_predict)
		return self.getKNN(res,to_predict) # Apply KNN to the result cluster to get the best result


	def buildCluster(self, X = None, isTest = True ):
		# Check if this is a test run or not
		if isTest:
			self.X, self.test = self.generateTrainData()
		else:
			self.X = X

		# Check if a model is already present
		if not os.path.isfile(self.model_name):
			self.km = self.fit(self.X) # train k mean model 
		else:
			self.restoreModel()
		
	def getKNN(self,X,test):
		nbrs = NearestNeighbors(n_neighbors=5).fit(X) # choose the 5 nearest neighbors
		distances, indices = nbrs.kneighbors(test.reshape(1,-1) , n_neighbors=1) # but take only the closest
		#print "Nearest element of " + str(test) + " is:"
		return X[indices]
		# This is the proof that the best match is in the cluster


if __name__ == '__main__':
	r = Recommender()
	X, test = r.generateTrainData()

	r.buildCluster(X, isTest = False)
	print r.predict(test)