from math import atan2, degrees

def angle_vector2(x: float, y: float) -> float:
    return degrees(atan2(y, x))


def angle_line(p1: tuple, p2: tuple) -> float:
    return angle_vector2(p2[0] - p1[0], p2[1] - p1[1])