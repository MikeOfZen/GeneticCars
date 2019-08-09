from unittest import TestCase

import config
import gui
import track
import brains
import experiment
import load
import pyglet


class TestExperiment(TestCase):

    def setUp(self) -> None:
        self.brain_pop = [brains.NeuralBrain() for _ in range(10)]
        self.t=track.Track(load.rectangular_track)

    def test_execution(self):
        e=experiment.Experiment(track=self.t,brain_pop=self.brain_pop)
        e.run()
        results=e.experiment_results()
        print("\n".join([f"{x[0]} - {x[1]}" for x in results]))

class TestDrawnExperiment(TestCase):

    def setUp(self) -> None:
        self.brain_pop = [brains.NeuralBrain() for _ in range(10)]

        self.window = gui.GameWindow(width=config.width, height=config.height)
        self.t = gui.DrawingTrack(window=self.window, batch=self.window.fixed_batch, track_json=load.rectangular_track)

    def test_execution(self):
        e=experiment.DrawnExperiment(window=self.window, batch=self.window.fixed_batch, track=self.t, brain_pop=self.brain_pop)

        self.window.activity=e.step
        self.window.start()

        results=e.experiment_results()
        print("\n".join([f"{x[0]} - {x[1]}" for x in results]))

class TestUserExperiment(TestCase):

    def setUp(self) -> None:
        self.brain_pop = [brains.NeuralBrain(None) for _ in range(10)]

        self.window = gui.GameWindow(width=config.width, height=config.height)
        self.t = gui.DrawingTrack(window=self.window, batch=self.window.fixed_batch, track_json=load.tracks[0])

    def test_execution(self):
        e=experiment.UserExperiment(window=self.window, batch=self.window.fixed_batch, track=self.t, brain_pop=self.brain_pop)

        self.window.activity=e.step
        self.window.start()
        results=e.experiment_results()
        print("\n".join([f"{x[0]} - {x[1]}" for x in results]))