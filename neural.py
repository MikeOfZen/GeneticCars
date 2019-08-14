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
        self.mutables[self._symmetry_mat == 0]=True

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
    def __init__(self,shape_v,weights,symmetry_mat=None,intensity_if_new=0.1):
        """

        :param shape_v: one dimensional array, first element is the number of inputs, last is the number of outputs,
        and anything in between is the hidden layers
        so (5,4,2) would describe a network of 5 inputs 4 hidden neurons and 2 outpus
        :param weights is a list of weight matrices, length of shape_v -1, each matrix must be of shape
        (layer_i)X((layer_i+1)+1) so the first matrix for the previous shape_v would be
        4x6 and the second 2x5.
        weights must be numpy matrix (dtype=float)
        :param symmetry_mat applies to the first layer only, and describes the symmetries in the weights matrix to apply
        to it, any weight which is not symmpetric gets
        a positive integer, a weight which should be a positive symmetry of any other weight (a weight which should be
        exactly like it) gets the ither weight's integer
        a weight which is negatively symmetric gets minus the integer
        """
        assert len(shape_v)>=2 ,"shape_v is incorrect size"
        assert all(x>=1 for x in shape_v), "cant have less then one sized layers"
        self._shape_v=shape_v

        if weights is not None:
            for i,l in enumerate(shape_v[:-1]):
                assert weights[i].shape==(shape_v[i+1], shape_v[i]+1), f"mismatch in weight and shape dimension" \
                    f" in matrix {i} of weights"
            self._weights=weights
        else:
            self._init_random_network(intensity_if_new)

        self._init_neurons()

        self._symmetry_mat = symmetry_mat
        if symmetry_mat is not None:
            assert symmetry_mat.shape == weights[0].shape, "mismatch in symmetry and weights[0] dimensions"
            self._weights[0]=self._apply_symetry(self._symmetry_mat,self._weights[0])
            self._mutables=self._mutable_weights(self._symmetry_mat)

        self._generate_id()
        self._name=f"NN{str(self._id).zfill(3)}"

        with np.printoptions(precision=3,suppress=True):
            self._weights_str=str(self.weights)

    def __repr__(self):
        return self._name+" -\n"+self._weights_str

    def _init_random_network(self,intensity):
        self._weights=[]
        for i, l in enumerate(self._shape_v[:-1]):
            layer_weights_shape=(self._shape_v[i+1], self._shape_v[i]+1)
            self._weights.append(intensity*np.random.random(size=layer_weights_shape)-(intensity/2))

    def _init_neurons(self):
        self._neuron_layers=[]
        for layer_size in self._shape_v:
            layer=np.zeros(shape=layer_size+1,dtype=np.float)
            layer[0]=1  # bias term
            self._neuron_layers.append(layer)
        #self._neuron_layers.append(np.zeros(shape=self._shape_v[-1], dtype=np.float))  # final output layer

    @staticmethod
    def _apply_symetry(symmetry_mat, weights_mat):
        for i in np.unique(symmetry_mat[symmetry_mat>0]):
            original = weights_mat[symmetry_mat == i]
            if not original.size:
                continue
            original_value = original[0]
            weights_mat[symmetry_mat == -i] = -original_value
            weights_mat[symmetry_mat == i] = original_value
        return weights_mat

    @staticmethod
    def _mutable_weights(symmetry_mat):
        mutables=np.zeros(symmetry_mat.shape, dtype=np.bool)
        for i in np.unique(symmetry_mat[symmetry_mat > 0]):
            first=np.where(symmetry_mat==i)[0]
            mutables[first]=True
        mutables[symmetry_mat == 0]=True
        return mutables

    def compute(self, input):
        assert input.shape == (self._shape_v[0],), "wrong input dimension"
        self._neuron_layers[0][1:]=input
        for i in range(len(self._neuron_layers) - 1):
            self._neuron_layers[i + 1][1:]=np.matmul(self._weights[i], self._neuron_layers[i])
            np.tanh(self._neuron_layers[i + 1])

        return self._neuron_layers[-1][1:]

    def _generate_id(self):
        d=3 #number of digits in name
        m=10**d
        s=sum(abs(x).sum() for x in self._weights)
        self._id= int(m-abs((s*1000) % (2*m) - m))

    @property
    def id(self):
        return self._id

    @property
    def weights(self):
        return self._weights.copy()

    @property
    def symmetry_mat(self):
        return self._symmetry_mat

    @property
    def shape_v(self):
        return self._shape_v.copy()


