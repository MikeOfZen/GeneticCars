import random

import numpy as np
from pyglet.window import key

import config
import neural


class Brain:
    def __init__(self):
        self._name=""

    def __str__(self):
        return self._name
    
    @staticmethod
    def scale_input(inputs):
        """scales the sensor output between 0..1"""
        return inputs/config.sensor_dist

    @staticmethod
    def scale_controls(controls):
        """scales the controls from 0..1 for acceleration and -1..1 for turn rate to values defined in the config"""
        np.putmask(controls,controls >=1,1)
        np.putmask(controls, controls <= -1, -1)
        controls=controls*config.control_scalar_max
        return controls

class ConstantBrain(Brain):
    def __init__(self,const_acceleration,const_turn_rate):
        super(ConstantBrain, self).__init__()
        self.turn_rate=const_acceleration
        self.acceleration = const_turn_rate

    def compute(self,input):
        return (self.acceleration,self.turn_rate)


class RandomBrain(Brain):
    def __init__(self):
        super(RandomBrain, self).__init__()
        self.acceleration=random.random()
        self.turn_rate = (random.random()-0.5)*0.4

    def compute(self,input):
        return (self.acceleration,self.turn_rate)


class UserBrain(Brain):
    def __init__(self,keys):
        super(UserBrain, self).__init__()
        self.keys =keys

        self.acceleration = 0
        self.turn_rate =0

        self._name="User"

    def __str__(self):
        return self._name


    def _check_keys(self):
        if self.keys[key.UP]:
            self.acceleration=config.max_user_acceleration
        elif self.keys[key.DOWN]:
            self.acceleration = -config.max_user_acceleration
        else:
            self.acceleration=0

        if self.keys[key.LEFT]:
            self.turn_rate=config.max_user_turnrate
        elif self.keys[key.RIGHT]:
            self.turn_rate = -config.max_user_turnrate
        else:
            self.turn_rate=0

    def compute(self, _):
        self._check_keys()
        return (self.acceleration,self.turn_rate)


class NeuralBrain(Brain):
    def __init__(self,weights):
        super(NeuralBrain, self).__init__()

        #create random neural network with 5 inputs and 2 outpus so 6x2
        if weights is None:
            weights=2*(np.random.random([2,6])-0.5)
        with np.printoptions(precision=3,suppress=True):
            self.weights_str=str(weights) #for jsonpickle human readable form
        self.net=neural.OneLayerNeuralNetwork(weights)

        d=3 #number of digits in name
        m=10**d
        self._id=int(m-abs((abs(weights).sum()*1000) % (2*m) - m))

        self._name=f"N{str(self._id).zfill(d)}"

    def compute(self, input):
        scaled_input=self.scale_input(input)
        controls=self.net.compute(scaled_input)
        scaled_controls=self.scale_controls(controls)

        return (scaled_controls[0],scaled_controls[1])

    def __repr__(self):
        return self._name+" -\n"+self.weights_str


    def mutate(self,mutation_factor):
