# GeneticCars

This is an Experiment/Game in machine learning.
The objective was to create a driving algorithm, to drive around a simulated 2D track, without crashing in the walls.
The Car has 2 controls (acceleration - gas, and turn rate - wheel) and 5 (or more) distance sensors to 'see' the track

The control is done with a neural network (of varying topology) which gets evolved by a genetic algorithm over a series of generetions.
With the fitness of each network being the distance driven on the track (measured by gates in the track).

![Alt text](/doc/After100generations.PNG?raw=true "The population solving the track after 100 generations")
-The population solving the track after 100 generations

# Model
For the duration of the simulation, the car drives along the track updating its physical model
with inputs from the 'brain' ie, neural network. in each step the car scans its enviorment (the sourrounding walls) with its sensors (ray casting) and updates the brain with these outputs. if the car drives into one of the wall (marked in white), it dies (turns red). if the car doesnt make enough progress for some time it can also die (effective for eliminating non-moving/very slow networks). 
Each time the car passes a gate (marked in red) it's score (fitness) is incremented. at the end of the simulation, the last gate the car has passed determines it's simulation score.
if any car reaches the final gate, the experiment is over. 

# Evolution
For each round of evolution, the whole population is tested, and the best 20% is selected.
For the next population, the best 20% is kept as is (elitism)
the rest 80% is created by randomly crossing 2 members of the selected and mutating the result.
*the percentages, mutation levels and crossing algorithms are tunable in the config.

# Interface
the simulation can run in 2 modes, with or without graphical output. 
it is faster to run the evolution over many generations without graphics, but viewing the actaul behaviour is only with graphics

the app allows to save and load various populations with various models.
and a number of tracks of various diffculties have been created and are possible to use.

finally it is possible to 'race' as a user against the evolved population.

# Required
Libraries used: Numpy, Pyglet, Consolemenu, PILlow
