from collections import namedtuple
from itertools import combinations
import math

Point = namedtuple("Point", ["x", "y"])


def distance(p1, p2):
    """ Euclidean distance between two points."""
    return math.sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2))


def minimal_distance_naive(points):
    """ Brute force algorithm to find the minimal distance in a set of points."""
    min_dis = float("inf")
    for ii in range(len(points) - 1):
        for jj in range(ii + 1, len(points)):
            min_dis = min(min_dis, distance(points[ii], points[jj]))

    return min_dis


def minimal_distance_split(points):
    """ Finds the minimal distance in a set of points by splitting the set of
        points into two sets."""

    points = sorted(points)
    midline = len(points) // 2

    min_dis = float("inf")
    for ii in range(midline):
        for jj in range(ii + 1, midline + 1):
            min_dis = min(distance(points[ii], points[jj]), min_dis)
        
    for ii in range(midline, len(points) - 1):
        for jj in range(ii + 1, len(points)):
            min_dis = min(distance(points[ii], points[jj]), min_dis)
    
    points_filtered = []
    for point in points:
        if abs(midline - point.x) < min_dis:
            points_filtered.append(point)
    
    # points_filtered = sorted(points_filtered, key=lambda p: p.y)
    for ii in range(len(points_filtered)):
        for jj in range(ii + 1, len(points_filtered) - 1):
            min_dis = min(min_dis, distance(points_filtered[ii], points_filtered[jj]))

    return min_dis


def minimal_distance_recursive(points, left, right):
    """ Finds the minimal distance in a set of points by recursively splitting the set of points."""

    if right - left <= 4:
        min_distance = float("inf")
        for p1, p2 in combinations(points[left:right + 1], 2):
            min_distance = min(min_distance, distance(p1, p2))

        return min_distance
    
    # Split points into halves and find the minimal distance in each half
    midline = (left + right) // 2 
    mid_x = points[midline].x
    distance_left = minimal_distance_recursive(points, left, midline)
    distance_right = minimal_distance_recursive(points, midline, right)
    min_distance = min(distance_left, distance_right)

    # Check if there is a smaller distance between pairs of points of each half
    strip = [p for p in points[left:right + 1] if abs(mid_x - p.x) < min_distance]

    for p1, p2 in combinations(strip, 2):
        min_distance = min(min_distance, distance(p1, p2))

    return min_distance


def minimal_distance(points):

    points = sorted(points)
    return minimal_distance_recursive(points, 0, len(points))


def main():
    x = [4, -2, -3, -1, 2, -4, 1, -1,  3, -4, -2]
    y = [4, -2, -4,  3, 3,  0, 1, -1, -1,  2,  4]

    assert len(x) == len(y)

    points = []
    for ii in range(len(x)):
        points.append(Point(x[ii], y[ii]))

    print(minimal_distance_naive(points))
    print(minimal_distance_split(points))
    print(minimal_distance(points))


if __name__=="__main__":
    main()