from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class VectorDimensionError(Exception):
    def __init__(self, message, errors):
        super(Exception, self).__init__(message)
        self.errors = errors


def calculateSimilarity(x, y):
	if(len(x) != len(y)):
		raise VectorDimensionError("Vector must be the same size",None)
	return cosine_similarity(np.array(x).reshape(1,len(x)),np.array(y).reshape(1,len(y)))

def main():
	print calculateSimilarity([0,1,0,1,0],[1,2,5,4])


if __name__ == '__main__':
	main()