from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random

class VectorDimensionError(Exception):
    def __init__(self, message, errors):
        super(Exception, self).__init__(message)
        self.errors = errors


def calculateSimilarity(x, y):
	if(len(x) != len(y)):
		raise VectorDimensionError("Vector must be the same size",None)
	return cosine_similarity(np.array(x).reshape(1,len(x)),np.array(y).reshape(1,len(y)))

def createJunkData():
	return np.array([generateJunkVector(5) for i in range(5)]).T

def tryKNN():
	from sklearn.neighbors import NearestNeighbors
	import numpy as np
	X = createJunkData()
	nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
	distances, indices = nbrs.kneighbors([0,1,2,1,5], n_neighbors=1)
	print distances
	print X[indices]


def generateJunkVector(n):
	return [random.random() for i in range(n)]

if __name__ == '__main__':
	tryKNN()