from unittest import TestCase
import load,track
import numpy as np
class TestTrack(TestCase):

    def setUp(self) -> None:
        self.t=track.Track(load.tracks[2])

    def test_get_borders_around_pt(self):
        local_borders=self.t.get_borders_around_pt(np.array([-525,0]))
        print(local_borders)
        self.assertTrue(len(local_borders)==3)
        local_borders=self.t.get_borders_around_pt(np.array([0,0]))
        print(local_borders)
        self.assertTrue(len(local_borders)==4)
        local_borders = self.t.get_borders_around_pt(np.array([1000, 0]))
        print(local_borders)
        self.assertTrue(len(local_borders) == 0)
