import brains
import car
import gui
import load


class TestSubject:
    def __init__(self,controller,brain,car):
        self.controller=controller
        self.brain=brain
        self.car=car


class Experiment:
    """sets up and runs the experiment
    gets a population of Brains"""
    def __init__(self, track, brain_pop):
        super(Experiment, self).__init__()
        self.brain_pop=brain_pop
        self.track = track
        self.steps=0
        self.subjects=[]

        self._init_experiment()

    def _init_experiment(self):
        for brain in self.brain_pop:

            c = self._init_car(str(brain))
            controller=car.CarController(c,brain)
            self.subjects.append(TestSubject(controller, brain, c))

    def _init_car(self, name):
        return car.ScoringCar(x=self.track.start[0],
                              y=self.track.start[1],
                              dir=self.track.start[2],
                              name=name,
                              track=self.track)

    def run(self):
        while self.step():
            pass

    def experiment_results(self):
        results=[]
        for subject in self.subjects:
            fitness=subject.car.fitness
            results.append((subject.brain,fitness))
        return results

    def experiment_over(self):
        return self._all_dead()

    def _all_dead(self):
        return all(subject.car.dead for subject in self.subjects)

    def step(self):
        if not self.experiment_over():
            for subject in self.subjects:
                self.steps+=1
                subject.controller.step()
            return True
        return False

class DrawnExperiment(Experiment):
    """responsible for drawing the experiment"""
    def __init__(self,window,batch,track,brain_pop):
        self.window=window
        self.batch=batch
        super(DrawnExperiment, self).__init__(track,brain_pop)

    def _init_car(self, name):
        return gui.DrawingCar(window=self.window,
                              batch=self.batch,
                              x=self.track.start[0],
                              y=self.track.start[1],
                              dir=self.track.start[2],
                              name=name,
                              track=self.track)

class UserExperiment(DrawnExperiment):
    """an experiment which includes a user"""
    def __init__(self,window,batch,track,brain_pop):
        super(UserExperiment, self).__init__(window,batch,track,brain_pop)
        c=self._init_car("U")
        c.sprite.image=load.user_img
        user_brain=brains.UserBrain(self.window.keys)
        controller=car.CarController(c,user_brain)

        self.subjects.append(TestSubject(controller,user_brain,c))

    def experiment_over(self):
        return self._all_dead()


#todo make an experiment able to save and load itself