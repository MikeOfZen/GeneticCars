#max car controls
max_velocity=100
max_acceleration=30
max_turnrate=1

#user control
max_user_acceleration=max_acceleration
max_user_turnrate=max_turnrate

sensor_dist=150
collision_distance=10 #this must be larger then one timestep * maxV to guerentee collision detection
border_detection_radius=300 #this is an optimization, where only borders close to the car are evaluated for distance


#population
default_population_size=50
default_filename="population.json"
default_populations_dir="populations"

#display
width=1000
height=800
fps=60

border_thickness=3
border_color=(255,255,255)
gate_thickness=1
gate_color=(255,0,0)

time_step=1/fps

#experiment settings
max_experiment_steps = 1e5  #

#mutation settings
mutation_Rate = 2
retain_percent = 0.2
throttle_mutation_by_std=False

import brains
default_brain=brains.NeuralBrain
default_brain_argumetns=[None]



default_neural_shape=[5,5,2]
default_initial_network_intensity=0.1
default_symmetry_mat=None


#converting here for apropriate types fro convinence
import math
sensor_angles=[0,45,-45,90,-90]
sensor_angles=[math.radians(x) for x in sensor_angles]

import numpy as np
control_scalar_max=np.array([max_acceleration,max_turnrate],dtype=np.float)
control_scalar_min=-control_scalar_max

mutation_multiplier = 5
faster_mutation_threshold = 1.0 #must be float


verbose=True