from sklearn.neighbors import NearestNeighbors
import numpy as np
import random

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
	return np.array([generateJunkVector(5) for i in range(5)]).T

def tryKNN():
	X = createJunkData()
	test = [0,1,0,1,1]
	nbrs = NearestNeighbors(n_neighbors=2).fit(X)
	distances, indices = nbrs.kneighbors(np.array(test), n_neighbors=1)
	print "Nearest element of " + str(test) + " is:"
	print X[indices]





def generateJunkVector(n):
	return np.array([random.randrange(0,2) for i in range(n)])

if __name__ == '__main__':
	tryKNN()