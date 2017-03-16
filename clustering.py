from sklearn.cluster import MiniBatchKMeans
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
	km = MiniBatchKMeans(n_clusters=100)
	km.fit(X)
	prediction = km.predict(test)
	print X[prediction]
	cluster_elements =  ClusterIndicesNumpy(prediction,km.labels_)
	print [X[c] for c in cluster_elements]
	

if __name__ == '__main__':
	clustering()