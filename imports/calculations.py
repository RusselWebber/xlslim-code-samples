from area_calculators.circle import area as circle_area
from area_calculators.square import area as square_area
from area_calculators.rectangle import area as rectangle_area


def complex_area(l: float, w: float, r: float) -> float:
    """Return the area of a complex shape with the area of a square with sides l, a rectangle
    with sides l and w, and a circle with radius r."""
    return circle_area(r) + square_area(l) + rectangle_area(l, w)


def another_complex_area(l: float, w: float, r: float) -> float:
    """Return the area of a complex shape with the area of two squares with sides l, a rectangle
    with sides l and w, and a circle with radius r."""
    return circle_area(r) + 2 * square_area(l) + rectangle_area(l, w)


def yet_another_complex_area(l: float, w: float, r: float) -> float:
    """Return the area of a complex shape with the area of two squares with sides l, two rectangles
    with sides l and w, and a circle with radius r."""
    return circle_area(r) + 2 * square_area(l) + rectangle_area(l, w)


if __name__ == "__main__":
    print(complex_area(3, 4, 5))
