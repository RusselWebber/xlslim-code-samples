# Various functions to calculate areas
import math


def area_circle(r: float) -> float:
    """Calculates the area of a circle as pi x r x r"""
    return math.pi * r ** 2


def area_square(l: float) -> float:
    """Calculates the area of a square as l x l"""
    return l * l


def area_rectangle(l: float, w: float) -> float:
    """Calculates the area of a rectangle as l x w"""
    return l * w
