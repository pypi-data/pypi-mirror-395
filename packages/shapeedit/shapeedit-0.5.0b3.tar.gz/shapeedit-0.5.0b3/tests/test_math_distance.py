"""
This file is part of ShapeEdit.

Copyright (C) 2025 Peter Grønbæk Andersen <peter@grnbk.io>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import pytest
import math

from shapeio.shape import Point
from shapeedit.math.distance import distance_between, signed_distance_between


@pytest.mark.parametrize("plane", ["x", "y", "z", "xy", "xz", "zy", "xyz"])
def test_signed_distance_between_returns_float(plane):
    point1 = Point(0, 0, 0)
    point2 = Point(1, 1, 1)
    distance = signed_distance_between(point1, point2, plane=plane)
    assert isinstance(distance, float)


def test_signed_distance_between_xyz_is_always_positive():
    point1 = Point(0, 0, 0)
    point2 = Point(3, 4, 0)
    distance = signed_distance_between(point1, point2, plane="xyz")
    assert math.isclose(distance, 5.0)


def test_signed_distance_between_invalid_plane_raises():
    with pytest.raises(ValueError):
        signed_distance_between(Point(0, 0, 0), Point(1, 0, 0), plane="bad")


def test_distance_between_matches_absolute_signed_distance():
    point1 = Point(0, 0, 0)
    point2 = Point(1, 0, 0)
    signed_distance = signed_distance_between(point1, point2, "xz")
    absolute_distance = distance_between(point1, point2, "xz")
    assert absolute_distance == abs(signed_distance)

