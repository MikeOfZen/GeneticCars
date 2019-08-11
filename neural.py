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


class SymmetricalNeuralNetwork:
    def __init__(self, weights, symmetry_mat):
        """weights must be numpy matrix (dtype=float), which sets the weights of the neural netwrok
        dimensionality determines the number of neurons in each layer (including constant 1 in input layer, but not including constant 1 in output)
        so far 3 input neurons and 2 output neurons the shape must be 2x4"""
        assert symmetry_mat.shape==weights.shape, "symmetry and weights must match in shape"
        self._symmetry_mat = symmetry_mat
        self.weights = weights

    def compute(self, input):
        assert input.shape == tuple((self.weights.shape[1] - 1,)), f"wrong input dimension, required dimensions are {self.weights.shape[1] - 1}"

        extended_input = np.insert(input, 0, 1, 0)  # insert constant 1 in zero place

        NextLayerInput = np.matmul(self.weights, extended_input)
        # for one layer thats the output
        return NextLayerInput

    def apply_symetry(self, weights_mat):
        for i in np.unique(self._symmetry_mat[self._symmetry_mat>0]):
            original = weights_mat[self._symmetry_mat == i]
            if not original.size:
                continue
            original_value = original[0]
            weights_mat[self._symmetry_mat == -i] = -original_value
            weights_mat[self._symmetry_mat == i] = original_value
        return weights_mat

    def _mutable_weights(self):
        self.mutables=np.zeros(self._symmetry_mat.shape,dtype=np.bool)
        for i in np.unique(self._symmetry_mat[self._symmetry_mat > 0]):
            first=np.where(self._symmetry_mat==i)[0]
            self.mutables[first]=True

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, new_weights):
        assert len(new_weights.shape) == 2
        assert new_weights.shape == self._symmetry_mat.shape
        self._weights = self.apply_symetry(new_weights).copy()
        self._mutable_weights()

class NeuralNetwork():
