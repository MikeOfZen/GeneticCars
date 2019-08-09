from unittest import TestCase
import track,experiment,population,load
import cProfile

class TestFortime(TestCase):
    def setUp(self) -> None:
        pass

    def test_single_experiment_sim(self):
        setup=(
        'import main,load\n'
        'm=main.App()\n'
        'm.track_json=load.tracks[1]\n'
        'm.evolution_sim()'        )

        cProfile.run(setup)
        self.assertTrue(True)
