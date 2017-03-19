from sklearn.neighbors import NearestNeighbors
import numpy as np
import random	
from sklearn.metrics.pairwise import cosine_similarity

n_features = 10
n_samples = 1000

'''
class VectorDimensionError(Exception):
    def __init__(self, message, errors):
        super(Exception, self).__init__(message)
        self.errors = errors


def calculateSimilarity(x, y):
	if(len(x) != len(y)):
		raise VectorDimensionError("Vector must be the same size",None)
	return cosine_similarity(np.array(x).reshape(1,len(x)),np.array(y).reshape(1,len(y)))
'''

def createJunkData():
	return np.array([generateJunkVector(n_features) for i in range(n_samples)])

def tryKNN():
	X = createJunkData()
	test = generateJunkVector(n_features)
	nbrs = NearestNeighbors(n_neighbors=5).fit(X)
	distances, indices = nbrs.kneighbors(test.reshape(1,-1) , n_neighbors=1)
	print "Nearest element of " + str(test) + " is:"
	print X[indices]
	print "The distance between the two values: "
	print distances





def generateJunkVector(n):
	return np.array([random.randrange(0,2) for i in range(n)])

if __name__ == '__main__':
	tryKNN()