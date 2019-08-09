#max car controls
max_velocity=100
max_acceleration=30
max_turnrate=1

#user control
max_user_acceleration=max_acceleration
max_user_turnrate=max_turnrate

sensor_dist=150
collision_distance=20 #this must be larger then one timestep * maxV to guerentee collision detection
border_detection_radius=300 #this is an optimization, where only borders close to the car are evaluated for distance


#population
default_population_size=20
default_filename="population.json"
default_populations_dir="populations"

#display
width=1000
height=800
fps=60

border_thickness=6
border_color=(255,255,255)
gate_thickness=1
gate_color=(255,0,0)

time_step=1/fps

#experiment settings
max_experiment_steps=20e3 #

#mutation settings
mutation_Rate = 0.025
retain_percent = 0.2

import brains
default_brain=brains.NeuralBrain
default_brain_argumetns=[None]

#converting here for apropriate types fro convinence
import math
sensor_angles=[0,45,-45,90,-90]
sensor_angles=[math.radians(x) for x in sensor_angles]

import numpy as np
control_scalar_max=np.array([max_acceleration,max_turnrate],dtype=np.float)
control_scalar_min=-control_scalar_max

mutation_multiplier = 10
faster_mutation_threshold = 0.25