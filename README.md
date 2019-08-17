# GeneticCars

This is an Experiment/Game in machine learning.
The objective was to create a driving algorithm, to drive around a simulated 2D track.
The Car has 2 controls (acceleration - gas, and turn rate - wheel) and 5 (or more) distance sensors to 'see' the track

the control is done with a neural network (of varying topology) which gets evolved by a genetic algorithm over a series of generetions.
the fitness of each network is the distance driven on the track (measured by gates in the track).

for each round of evolution the whole population is tested.
the best 20% (by distance) is selected. for the next population, the best 20% is kept as is (elitism)
the rest 80% is created by randomly crossing 2 members of the selected and mutating the result.
*the percentages, mutation levels and crossing algorithms are tunable in the config.

the simulation can run in 2 modes, with or without graphical output. 
it is faster to run the evolution over many generations without graphics, but viewing the actaul behaviour is only with graphics

the app allows to save and load various populations with various models.
and a number of tracks of various diffculties have been created and are possible to use.

finally it is possible to 'race' as a user against the evolved population.
