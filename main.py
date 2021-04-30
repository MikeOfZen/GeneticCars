import os

import config
import consolemenu as cm
import consolemenu.items as cmi
import evolution
import experiment
import genetics
import gui
import load
import track
from population import Population


# todo menu options
# set experiment settings, such as number of generations, mutation settings, drawing or not, save progress or not
# (weights,fitness,experiment etc)
# , which model size to train (network size)

# save as - population -V
# load (filename) -V
# play as user agaisnt top -V
# set track to use -V
# stop experiment (must save global population ) - V
# run experiment, with population
# display population (make each brain display itself) -v

class App:
    def __init__(self):
        self.population=Population()
        self.population.create_random_pop(config.default_brain,config.default_brain_argumetns)

        self.track_json=load.tracks[0]

        self.menu = cm.ConsoleMenu("Genetic Cars",show_exit_option=True)
        self.menu.append_item( cmi.FunctionItem("Load population from file", self.load, []))
        self.menu.append_item( cmi.FunctionItem("Save population to file", self.save, []))
        self.menu.append_item( cmi.FunctionItem("Display population", self.population.display, []))
        self.menu.append_item(cmi.FunctionItem("change population size", self.change_pop_size, []))
        self.menu.append_item(cmi.FunctionItem("Randmoize population", self.population.create_random_pop, [config.default_brain,config.default_brain_argumetns]))

        track_selection_menu = cm.ConsoleMenu("Select a track")
        track_selection_item = cmi.SubmenuItem("Track selection",track_selection_menu,self.menu)

        for t in load.tracks:
            track_selection_menu.append_item(cmi.FunctionItem(t["name"],self._set_track, [t]))

        self.menu.append_item(track_selection_item)

        self.menu.append_item(cmi.FunctionItem("Play against population", self.user_experiment, []))
        self.menu.append_item(cmi.FunctionItem("Run single experiment (Drawn)", self.single_experiment_drawn, []))
        self.menu.append_item(cmi.FunctionItem("Run single experiment (Simulate)", self.single_experiment_sim, []))

        self.menu.append_item(cmi.FunctionItem("Run evolution (Drawn)", self.evolution_drawn, []))
        self.menu.append_item(cmi.FunctionItem("Run evolution (Simulate)", self.evolution_sim, []))

        self.genetics=genetics.default_genetics

    def change_pop_size(self):
        config.population_size= input_with_conditions("Please input population size [1-500]", int,
                                                   [lambda x: x > 0, lambda x: x < 500])
        print("population size will change after 1 round of evolution and selection")

    def _set_track(self, track_json):
        self.track_json=track_json

    def show(self):
        self.menu.show()

    def load(self):
        filename=input("Please input desired filename to load (or leave empty for default -"+config.default_filename)
        if filename =='':
            filename=config.default_filename
        path = os.path.join(config.default_populations_dir, filename)
        try:
            with open(path,"r") as f:
                self.population.load(f.read())
                print("Loaded - "+path)
        except Exception as e:
            print("Could not load file - "+e)

    def save(self):
        filename=input("\nPlease input desired filename to save (or leave empty for default -"+config.default_filename)
        if filename =='':
            filename=config.default_filename
        path=os.path.join(config.default_populations_dir,filename)
        try:
            with open(path,"w+") as f:
                f.write(self.population.save())
                print("Saved!")
        except Exception as e:
            print("Could not save file "+e)


    def user_experiment(self):
        window = gui.GameWindow(width=config.width, height=config.height)
        t = gui.DrawingTrack(window=window, batch=window.fixed_batch, track=self.track_json)
        e = experiment.UserExperiment(window=window, batch=window.new_activity_batch(), track=t,
                                      brain_pop=self.population)
        window.activity = e.step
        window.start()
        del window
        results = e.experiment_results()
        print("Fitness results"+"\n".join([x[0] +"-"+ x[1] for x in results]))

    def single_experiment_drawn(self):
        window = gui.GameWindow(width=config.width, height=config.height)
        t = gui.DrawingTrack(window=window, batch=window.fixed_batch, track=self.track_json)
        e = experiment.DrawnExperiment(window=window, batch=window.new_activity_batch(), track=t,
                                       brain_pop=self.population)
        window.activity = e.step
        window.start()
        del window
        results = e.experiment_results()
        print("Fitness results"+"\n".join([{x[0]} +"-"+ {x[1]} for x in results]))

    def single_experiment_sim(self):
        t = track.Track( track=self.track_json)
        e=experiment.Experiment(track=t,brain_pop=self.population)
        e.run()
        results=e.experiment_results()
        print("Fitness results"+"\n".join([x[0] + x[1] for x in results]))

    def evolution_sim(self):
        generations_to_run=input_with_conditions("Please input number of generations to evolve [1-500]",int,[lambda x:x>0,lambda x:x<500])
        t = track.Track(track=self.track_json)
        ev= evolution.Evolution(self.population,t,generations_to_run,self.genetics)
        temp_population=ev.run()

        save = input_with_conditions("Accept evolution results (y/n)", str,[lambda x: x in ["y","n"]])
        save= True if save=="y" else False
        if save:
            self.population.clear()
            self.population.extend(temp_population)

    def evolution_drawn(self):
        generations_to_run=input_with_conditions("Please input number of generations to evolve [1-500]",int,[lambda x:x>0,lambda x:x<500])
        window = gui.GameWindow(width=config.width, height=config.height,close_on_finish=False)
        t = gui.DrawingTrack(window=window, batch=window.fixed_batch, track=self.track_json)

        ev= evolution.DrawnEvolution(self.population,t,generations_to_run,window,genetics=self.genetics)
        temp_population=ev.run()

        save = input_with_conditions("Accept evolution results (y/n)", str,[lambda x: x in ["y","n"]])
        save= True if save=="y" else False
        if save:
            self.population.clear()
            self.population.extend(temp_population)

def input_with_conditions(prompt,type,conditions):
        while True:
            inpu=input(prompt)
            try:
                typed_input=type(inpu)
            except Exception as e:
                print("Incorrect type, please try again")
                continue
            if all(c(typed_input) for c in conditions):
                return typed_input
            else:
                print("Input conditions not met, please try again")
                continue


if __name__=="__main__":
    m=App()
    m.show()