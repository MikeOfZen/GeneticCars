import datetime
import os
import random

import numpy as np

import config as c
import experiment
from population import Population


class Evolution:
    """sets up a series of experiments, applying evolution between each one"""
    def __init__(self,population,track,generations_to_run,genetics):
        self.track=track
        self.population = population
        self.population_size=len(population)
        #self.net_shape=self.population[0].net.weights.shape

        self.genetics=genetics
        self.generations_to_run=generations_to_run
        self._max_score= len(self.track.gates)


    def run(self):
        self.generation = 0
        self._test()
        self._display_test_results()
        for i in range(1,self.generations_to_run):
            self.generation=i
            self.population=Population()
            self._select()
            self._display_selected()
            self._carry_over()
            self._adapt_mutation_rate()
            self._cross_breed()
            print("\n"*2+"-"*50+"\n Running test")
            self._test()
            self._display_test_results()
            self._save()
            if self._exit_condition():
                print("TARGET REACHED")
                break
        return self.population

    def _exit_condition(self):
        return self._last_top_score >= self._max_score

    def _save(self):
        if not self.generation % c.save_every_generation:
            filename = f"gen-{self.generation}-{datetime.datetime.now().strftime('%d%H%M%S')}-{self._last_top_score}"
            path = os.path.join(c.default_populations_dir,c.default_autosave_dir, filename)
            try:
                with open(path, "w+") as f:
                    f.write(self.population.save())
                    print("Saved!")
            except Exception as e:
                print(f"Could not save file {e}")
                self.population.save()

    def _test(self):
        self._experiment = self._setup_test()
        self._run_test()
        self._last_results=self._experiment.experiment_results()

    def _display_selected(self):
        print(f"Selected nets are: {[str(x) for x in self._last_selected]}")
        if c.verbose:
            print("Weights:\n"+"\n".join([repr(x) for x in self._last_selected]))

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
        self._last_top_score=max(self._last_scores)
        remaining_top_score=self._last_top_score
        while len(selected) < c.retain_percent * self.population_size:
            for i,t in enumerate(self._last_results):
                if t[1] >=remaining_top_score:
                    select_brain=self._last_results.pop(i)[0]
                    selected.append(select_brain)
                    break

            scores = [t[1] for t in self._last_results]
            remaining_top_score = max(scores)
        self._last_selected=selected

    def _carry_over(self):
        self.population+=self._last_selected

    def _cross_breed(self):

        for i in range(self.population_size-len(self.population)): #add variations of the previously selected to the existing population
            #selected_brain=self._last_selected[i%len(self._last_selected)]   #take a different brain from the self._last_selected each time

            brain_a=np.random.choice(self._last_selected)
            brain_b = np.random.choice(self._last_selected)
            if c.verbose:
                print(f"\nCrossbreeding {brain_a} and {brain_b}")
            offspring_net=self.genetics.cross_breed(brain_a.net,brain_b.net)
            if c.verbose:
                print(f"\nOffspring net - {repr(offspring_net)}")
            mutated_offspring_net=self.genetics.mutate(offspring_net,self.mutation_rate,mutate_all=c.mutate_all)
            if c.verbose:
                print(f"\nMutated Offspring net - {repr(mutated_offspring_net)}")
            new_brain=brain_a.__class__(mutated_offspring_net)
            self.population.append(new_brain)

    def _adapt_mutation_rate(self):
        # decrease mutation as advances in solving the track are made
        progress=self._last_top_score/self._max_score
        self.mutation_rate = (c.start_mutation_Rate)-progress*(c.start_mutation_Rate-c.end_mutation_rate)


class DrawnEvolution(Evolution):
    def __init__(self,population,track,generations_to_run,window,genetics):
        super(DrawnEvolution, self).__init__(population, track, generations_to_run,genetics)
        self.window=window

    def _setup_test(self):
        return experiment.DrawnExperiment(window=self.window, batch=self.window.new_activity_batch(), track=self.track,
                                          brain_pop=self.population)
    def _run_test(self):
        self.window.activity = self._experiment.step
        self.window.start()

