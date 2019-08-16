from builtins import super

import math
import math_helpers.MathHelperC as m
import numpy as np

import config


class Car:
    """Car implements the physical calculations, draws itself, checks conditions"""
    def __init__(self,x,y,dir,name,track):
        super(Car, self).__init__()
        #starting coord
        self.x=x
        self.y = y
        self.dir=dir #angle
        self.name = name

        self.track = track
        #simulation vars
        self.v=0
        self.step_count=0

        self._init_sensors()

        self.set_controls(0,0)
        self.dead=False
        

    def _init_sensors(self):
        self.sensors = [Sensor(self, angle) for angle in config.sensor_angles]
        self.last_sensors_values = np.array([config.sensor_dist for v in self.sensors],dtype=np.float)

    def move(self):

        self.x += self.v * config.time_step * math.cos(self.dir)
        self.y += self.v * config.time_step * math.sin(self.dir)
        self.v += self.acceleration * config.time_step
        self._limit_v()
        self.dir += self.turn_rate * config.time_step

    def _limit_v(self):
        if self.v >= config.max_velocity:
            self.v=config.max_velocity
        if self.v <= -config.max_velocity:
            self.v = -config.max_velocity

    def _read_sensors(self):
        local_borders = self.track.get_borders_around_pt((self.x, self.y))
        self.last_sensors_values = np.array([v.get_reading(local_borders) for v in self.sensors], dtype=np.float)


    def _check_collisions(self):
        #not a real collision check, this depends on the assumption of only moving forward and at least 3 forward and side facing sensors
        for s in self.last_sensors_values:
            if s <= config.collision_distance:
                return True
        return False

    def get_sensor_values(self):
        return self.last_sensors_values

    def set_controls(self,acceleration, turn_rate):
        self.acceleration=acceleration
        self.turn_rate = turn_rate

    def step(self):
        if not self.dead:
            self.move()
            self._read_sensors()
            self.dead=self._check_collisions()
            self.step_count +=1
            return True
        return False

class ScoringCar(Car):
    def __init__(self,*args,**kwargs):
        super(ScoringCar, self).__init__(*args, **kwargs)
        self.fitness=0
        self._gate_idx=0
        self._steps_left=config.initial_steps_per_Gate
        self._final_fitness_flag=False
        self._set_gate()

    def _set_gate(self):
        self.score_sensors = [Sensor(self, angle) for angle in config.sensor_angles]

    def _read_sensors(self):
        super(ScoringCar, self)._read_sensors()
        gate = self.track.gates[self._gate_idx:self._gate_idx + 1]
        self.last_score_sensors_values = np.array([v.get_reading(gate) for v in self.score_sensors], dtype=np.float)

    def _check_score_collisions(self):
        for s in self.last_score_sensors_values:
            if s <= config.collision_distance:
                if self._gate_idx<len(self.track.gates):
                    self._gate_idx+=1
                    self._set_gate()
                    self.fitness =self._gate_idx
                    self._steps_left=config.steps_per_gate
                    self._check_finish()

    def _check_finish(self):
        if self._gate_idx==len(self.track.gates):
            self.finished=True
            self.dead=True

    def _add_final_fitness(self):
        self.fitness += 1/self.step_count
        self._final_fitness_flag=True

    def _decrement_step_and_die(self):
        self._steps_left -=1
        if self._steps_left <=0:
            self.dead=True

    def step(self):
        r=super(ScoringCar, self).step()
        if r:
            self._check_score_collisions()
            self._decrement_step_and_die()
        elif not self._final_fitness_flag:
            self._add_final_fitness()
        return r

class Sensor:
    def __init__(self, car, angle):
        self.car=car
        self.angle=angle

    def get_reading(self, borders):
        end_point_x= self.car.x + math.cos(self.car.dir+self.angle) * config.sensor_dist
        end_point_y = self.car.y + math.sin(self.car.dir + self.angle) * config.sensor_dist

        sensor_line_pts=np.array(((self.car.x,self.car.y),(end_point_x,end_point_y)),dtype=np.float)
        sensor_dist = m.find_distance_to_line_set(borders, sensor_line_pts)

        if sensor_dist is None:
            sensor_dist=config.sensor_dist
        return sensor_dist


class CarController:
    def __init__(self,car,brain):
        self.car=car
        self.brain=brain

    def step(self):
        if not self.car.dead:
            #get values
            feedback=self.car.get_sensor_values()

            #give to brain
            #take brain outputs
            controls=self.brain.compute(feedback)

            #give to car and step car
            self.car.set_controls(acceleration=controls[0], turn_rate=controls[1])
            self.car.step()

