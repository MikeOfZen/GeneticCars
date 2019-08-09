import numpy as np
import json
import config

class Track:

    def __init__(self, track):

        self.track_json=track
        self.name=self.track_json["name"]
        self._numpyfy()
        self._transform()

    def _numpyfy(self):
        self.borders=np.array(self.track_json["borders"],dtype=np.float)
        self.gates = np.array(self.track_json["gates"], dtype=np.float)
        self.start=np.array(self.track_json["start"],dtype=np.float)

    def _transform(self):
        self._transformation=np.array(self.track_json["transform"],dtype=np.float)
        self.borders+=self._transformation
        self.gates += self._transformation
        self.start[:-1] += self._transformation

    def get_borders_around_pt(self,pt):
        """return the borders whose at least one endpoint lies inside a circle of size config.border_detection_radius (for exmaple 300)"""
        # to evaluate for coliisions, this necessitates not having any border longer then about 2*sqrt(border_detection_radius**2+detection_distance**2)

        distance_vectors=self.borders-pt
        distances=np.linalg.norm(distance_vectors, axis=2)
        found=distances < config.border_detection_radius
        select=found.any(axis=1)
        return self.borders[select]