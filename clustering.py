from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
import numpy as np
import random	
from sklearn.metrics.pairwise import cosine_similarity

n_features = 10
n_samples = 1000

def createJunkData():
	return np.array([generateJunkVector(n_features) for i in range(n_samples)])

def generateJunkVector(n):
	return np.array([random.randrange(0,2) for i in range(n)])

def ClusterIndicesNumpy(clustNum, labels_array): #numpy 
    return np.where(labels_array == clustNum)[0]

def clustering():
	X = createJunkData()
	test = generateJunkVector(n_features).reshape(1,n_features)
	km = MiniBatchKMeans(n_clusters=10)
	km.fit(X)
	prediction = km.predict(test)
	print test
	cluster_elements =  ClusterIndicesNumpy(prediction,km.labels_)
	res = np.array([X[c] for c in cluster_elements])
	#print np.bitwise_xor(res,X[prediction])
	getKNN(res,test)
	
def getKNN(X,test):
	nbrs = NearestNeighbors(n_neighbors=5).fit(X)
	distances, indices = nbrs.kneighbors(test.reshape(1,-1) , n_neighbors=1)
	print "Nearest element of " + str(test) + " is:"
	print X[indices]
	print "The distance between the two values: "
	print distances

if __name__ == '__main__':
	clustering()