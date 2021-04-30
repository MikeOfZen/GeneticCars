from unittest import TestCase

import math
import numpy as np
import MathHelper as m
import cProfile
import timeit

class TestFind_distance_to_polygon(TestCase):
    def test_orthogonal_hit(self):
        sq = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1]], dtype=np.float)
        line = np.array([[3, 0], [0, 0]], dtype=np.float)
        dist=m.find_distance_to_polygon(sq, line)

        self.assertAlmostEqual(dist,2,3)


    def test_orthogonal_no_hit(self):
        sq = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1]], dtype=np.float)
        line = np.array([[3, 0], [2, 0]], dtype=np.float)
        dist=m.find_distance_to_polygon(sq, line)

        self.assertIsNone(dist)

    def test_orthogonal_edge(self):
        sq = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1]], dtype=np.float)
        line = np.array([[-3, -3], [0.5, 0.5]], dtype=np.float)
        dist=m.find_distance_to_polygon(sq, line)

        self.assertAlmostEqual(dist,math.sqrt(8),3)

    def test_two_intersections(self):
        sq = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1]], dtype=np.float)
        line = np.array([[0.5, 2], [-0.5, -2]], dtype=np.float)
        dist=m.find_distance_to_polygon(sq, line)

        self.assertAlmostEqual(dist,np.linalg.norm(np.array([0.25,1]),2))

    def test_line_intersection_time(self):
        setup=("""import MathHelper as m\n"""+
        """import numpy as np\n"""+
        """sq = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1]], dtype=np.float)\n"""+
        """line = np.array([[0.5, 2], [-0.5, -2]], dtype=np.float)""")
        code='dist=m.find_distance_to_polygon(sq, line)'
        print(timeit.timeit(code,setup,number=1000))
        self.assertTrue(True)

    def test_line_intersection_time(self):
        setup='import MathHelper as m\n' \
              'import numpy as np\n' \
              'l1s = np.array([-100, -100], dtype=np.float)\n' \
              'l1e = np.array([100, 100], dtype=np.float)\n' \
              'l2s = np.array([100, 20], dtype=np.float)\n' \
              'l2e = np.array([-100, 20], dtype=np.float)\n'
        code='dist=m.line_intersect(l1s,l1e,l2s,l2e)'
        print(timeit.timeit(code,setup,number=1000))
        self.assertTrue(True)

    def test_profile(self):
        setup="""import MathHelper as m\n"""+\
        """import numpy as np\n"""+\
        """sq = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1]], dtype=np.float)\n"""+\
        """line = np.array([[0.5, 2], [-0.5, -2]], dtype=np.float)\n"""
        code='for _ in range(1000):' \
             'dist=m.find_distance_to_polygon(sq, line)'
        cProfile.run(setup+code)
        self.assertTrue(True)
