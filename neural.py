import numpy as np


class OneLayerNeuralNetwork:
    def __init__(self, weights):
        """weights must be numpy matrix (dtype=float), which sets the weights of the neural netwrok
        dimensionality determines the number of neurons in each layer (including constant 1 in input layer, but not including constant 1 in output)
        so far 3 input neurons and 2 output neurons the shape must be 2x4"""
        assert len(weights.shape)==2
        self.weights=weights

    def compute(self,input):
        assert input.shape == tuple((self.weights.shape[1]-1,)) , f"wrong input dimension, required dimensions are {self.weights.shape[1]-1}"

        extended_input=np.insert(input,0,1,0) #insert constant 1 in zero place

        NextLayerInput= np.matmul(self.weights,extended_input)
        #for one layer thats the output
        return NextLayerInput
