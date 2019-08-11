import random

import numpy as np

import config as c
import experiment
from population import Population


class Evolution:
    """sets up a series of experiments, applying evolution between each one"""
    def __init__(self,population,track,generations_to_run):
        self.track=track
        self.population = population
        self.population_size=len(population)
        #self.net_shape=self.population[0].net.weights.shape

        self.generations_to_run=generations_to_run


    def run(self):
        self.generation = 0
        self._test()
        self._display_test_results()
        for i in range(1,self.generations_to_run):
            self.generation=i
            self._select()
            self.population=Population()
            self._carry_over()
            self._adapt_mutation_rate()
            self._mutate()
            self._test()
            self._display_test_results()
        return self.population

    def _test(self):
        self._experiment = self._setup_test()
        self._run_test()
        self._last_results=self._experiment.experiment_results()

    def _display_test_results(self):
        print(f"Generation - {self.generation} results \n")
        print("\n".join([f"{x[0]} - {x[1]}" for x in self._last_results]))

    def _run_test(self):
        self._experiment.run()

    def _setup_test(self):
        return experiment.Experiment(track=self.track,brain_pop=self.population)

    def _select(self):
        random.shuffle(self._last_results)
        self._last_scores=[t[1] for t in self._last_results]

        selected=[]
        top_score=max(self._last_scores)
        while len(selected) < c.retain_percent * self.population_size:
            for i,t in enumerate(self._last_results):
                if t[1] >=top_score:
                    select_brain=self._last_results.pop(i)[0]
                    selected.append(select_brain)
                    break

            scores = [t[1] for t in self._last_results]
            top_score = max(scores)
        self._last_selected=selected

    def _carry_over(self):
        self.population+=self._last_selected

    def _mutate(self):

        for i in range(self.population_size-len(self.population)): #add variations of the previously selected to the existing population
            selected_brain=self._last_selected[i%len(self._last_selected)]   #take a different brain from the self._last_selected each time

            new_net=selected_brain.net.weights.copy()
            random_factor= (2*(np.random.random(new_net.shape)-0.5)) * self.mutation_rate
            new_net=new_net+random_factor
            new_brain=selected_brain.__class__(new_net)
            self.population.append(new_brain)

    def _adapt_mutation_rate(self):
        # increase mutation if variance in scores is low
        if np.array(self._last_scores).std() > c.faster_mutation_threshold:
            self.mutation_rate = c.mutation_Rate * c.mutation_multiplier
        else:
            self.mutation_rate = c.mutation_Rate


class DrawnEvolution(Evolution):
    def __init__(self,population,track,generations_to_run,window):
        super(DrawnEvolution, self).__init__(population, track, generations_to_run)
        self.window=window

    def _setup_test(self):
        return experiment.DrawnExperiment(window=self.window, batch=self.window.new_activity_batch(), track=self.track,
                                          brain_pop=self.population)
    def _run_test(self):
        self.window.activity = self._experiment.step
        self.window.start()