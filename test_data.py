import numpy as np

class TestData:

	def createJunkData(self,n_features,n_samples):
		return np.array([np.random.randint(2, size=n_features) for i in range(n_samples)])

	def generateJunkVector(self,n_features):
		return np.random.randint(2, size=n_features)
	
	def generateTrainData(self,n_features,n_samples):
		X = self.createJunkData(n_features,n_samples)
		test = self.generateJunkVector(n_features).reshape(1,n_features)
		return X,test