from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
import numpy as np
import random	
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
	n_features = 5
	n_samples = 1000

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

	def trainModel(self,X):
		km = MiniBatchKMeans(n_clusters=10)
		km.fit(X)
		return km

	def predictAndGetElements(self,km,elements,to_predict):
		prediction = km.predict(to_predict) # prediction is the label of the cluster
		print to_predict # print the test vector for visual comparing
		cluster_elements =  self.ClusterIndicesNumpy(prediction,km.labels_)
		res = np.array([elements[c] for c in cluster_elements]) # All the elements that belongs to the predicted cluster
		return res

	def clustering(self):
		X, test = self.generateTrainData()
		km = self.trainModel(X)
		res = self.predictAndGetElements(km,X,test)
		self.getKNN(res,test) # Apply KNN to the result cluster to get the best result
		
	def getKNN(self,X,test):
		nbrs = NearestNeighbors(n_neighbors=5).fit(X) # choose the 5 nearest neighbors
		distances, indices = nbrs.kneighbors(test.reshape(1,-1) , n_neighbors=1) # but take only the closest
		print "Nearest element of " + str(test) + " is:"
		print X[indices]
		# This is the proof that the best match is in the cluster


if __name__ == '__main__':
	r = Recommender()
	r.clustering()