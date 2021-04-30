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
    def __init__(self,net=None):
        super(NeuralBrain, self).__init__()
        if net is None:
            self.net=neural.NeuralNetwork(config.default_neural_shape,None,config.default_symmetry_mat)
        else:
            self.net=net

 #for jsonpickle human readable form

        self._id=self.net.id
        self._name="BN"+str(self._id).zfill(3)

    def compute(self, input):
        scaled_input=self.scale_input(input)
        controls=self.net.compute(scaled_input)
        scaled_controls=self.scale_controls(controls)

        return (scaled_controls[0],scaled_controls[1])

    def __repr__(self):
        return self._name+"\n"+ repr(self.net)


