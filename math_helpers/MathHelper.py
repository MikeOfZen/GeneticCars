import numpy as np

def line_intersect(line1_start, line1_end, line2_start, line2_end):
    r = (line1_end - line1_start)
    s = (line2_end - line2_start)
    cross = r[0] * s[1] - r[1] * s[0]
    if not cross:
        return None
    u = ((line2_start[0] - line1_start[0]) * r[1] - (line2_start[1] - line1_start[1]) * r[0]) / cross
    t = ((line2_start[0] - line1_start[0]) * s[1] - (line2_start[1] - line1_start[1]) * s[0]) / cross
    if not (0 <= u <= 1 and 0 <= t <= 1):
        return None
    return line1_start + t * r


def line_polygon_intersects(convex_poly_pts,line_pts):
    candidates=[]
    num_of_pts=convex_poly_pts.shape[0]
    for i in range(num_of_pts):
        candidate=line_intersect(convex_poly_pts[i],convex_poly_pts[(i+1)%num_of_pts],
                       line_pts[0],line_pts[1])
        if candidate is not None:
            candidates.append(candidate)
    return candidates

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