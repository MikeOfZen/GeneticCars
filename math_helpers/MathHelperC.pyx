#cython: boundscheck = False
#cython: wraparound = False
#cython: cdivision=True

cimport numpy as np
import numpy as np

ctypedef np.float_t DTYPE_t

cpdef line_intersect(np.ndarray[DTYPE_t, ndim=1] line1_start,np.ndarray[DTYPE_t, ndim=1] line1_end,np.ndarray[DTYPE_t, ndim=1] line2_start,np.ndarray[DTYPE_t, ndim=1] line2_end):
    cdef float[2] r,s,intersection

    cdef float cross,u,t
    r[0] =line1_end[0] - line1_start[0]
    r[1] =line1_end[1] - line1_start[1]

    s[0] =line2_end[0] - line2_start[0]
    s[1] =line2_end[1] - line2_start[1]


    cross = r[0] * s[1] - r[1] * s[0]
    if cross == 0:
        return None

    u = ((line2_start[0] - line1_start[0]) * r[1] - (line2_start[1] - line1_start[1]) * r[0]) / cross
    t = ((line2_start[0] - line1_start[0]) * s[1] - (line2_start[1] - line1_start[1]) * s[0]) / cross
    if not (0 <= u <= 1 and 0 <= t <= 1):
        return None
    intersection[0]=line1_start[0] + t * r[0]
    intersection[1]=line1_start[1] + t * r[1]
    return intersection


def line_polygon_intersects(convex_poly_pts,line_pts):
    hits=[]
    num_of_pts=convex_poly_pts.shape[0]
    for i in range(num_of_pts):
        candidate=line_intersect(convex_poly_pts[i],convex_poly_pts[(i+1)%num_of_pts],
                       line_pts[0],line_pts[1])
        if candidate is not None:
            hits.append(candidate)
    return hits

def find_shortest_distance(origin,candidates):
    smallest=None
    for candidate in candidates:
        dist=np.linalg.norm(origin-candidate)
        if not smallest or dist < smallest:
            smallest=dist
    return smallest

def find_distance_to_polygon(convex_poly_pts,line_pts):
    hits=line_polygon_intersects(convex_poly_pts,line_pts)
    if hits:
        return find_shortest_distance(line_pts[0],hits)
    return None

def find_distance_to_line_set(line_set,test_line_pts):
    """return intersection point of test line with any other line in line set to any line in the line set by"""
    hits=[]
    for l in line_set:
        candidate=line_intersect(l[0],l[1],
                       test_line_pts[0],test_line_pts[1])
        if candidate is not None:
            hits.append(candidate)

    if hits:
        return find_shortest_distance(test_line_pts[0],hits)
    return None