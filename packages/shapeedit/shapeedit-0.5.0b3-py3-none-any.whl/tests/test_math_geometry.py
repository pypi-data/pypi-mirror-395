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

import numpy as np
import pytest

from shapeio.shape import Point, UVPoint
from shapeedit.math.geometry import (
    calculate_point_centroid,
    calculate_point_midpoint,
    calculate_uvpoint_midpoint,
    calculate_face_normal,
    calculate_vertex_normal
)


def test_calculate_point_centroid():
    points = [
        Point(0, 0, 0),
        Point(2, 0, 0),
        Point(0, 2, 0),
        Point(0, 0, 2)
    ]

    centroid = calculate_point_centroid(points)

    expected = np.array([0.5, 0.5, 0.5])
    assert np.allclose(centroid.to_numpy(), expected)


def test_calculate_point_midpoint():
    point1 = Point(0, 0, 0)
    point2 = Point(2, 2, 2)

    midpoint = calculate_point_midpoint(point1, point2)

    expected = np.array([1, 1, 1])
    assert np.allclose(midpoint.to_numpy(), expected)


def test_calculate_uvpoint_midpoint():
    uvpoint1 = UVPoint(0, 0)
    uvpoint2 = UVPoint(1, 1)

    midpoint = calculate_uvpoint_midpoint(uvpoint1, uvpoint2)

    expected = np.array([0.5, 0.5])
    assert np.allclose(midpoint.to_numpy(), expected)


def test_calculate_face_normal_xy_plane():
    point1 = Point(0, 0, 0)
    point2 = Point(1, 0, 0)
    point3 = Point(0, 1, 0)

    normal = calculate_face_normal(point1, point2, point3)

    expected = np.array([0, 0, 1])
    assert np.allclose(normal.to_numpy(), expected)


def test_calculate_face_normal_degenerate():
    point1 = Point(0, 0, 0)
    point2 = Point(1, 0, 0)
    point3 = Point(2, 0, 0)

    normal = calculate_face_normal(point1, point2, point3)

    expected = np.array([0, 0, 0])
    assert np.allclose(normal.to_numpy(), expected)


def test_calculate_vertex_normal_square_normalized():
    point = Point(0, 0, 0)
    connected = [
        Point(1, 0, 0),
        Point(0, 1, 0),
        Point(-1, 0, 0),
        Point(0, -1, 0)
    ]

    normal = calculate_vertex_normal(point, connected, normalize=True)

    expected = np.array([0, 0, 1])
    assert np.allclose(normal.to_numpy(), expected, atol=1e-4)


def test_calculate_vertex_normal_fewer_than_two_connections():
    point = Point(0, 0, 0)

    normal = calculate_vertex_normal(point, [Point(1, 0, 0)])

    expected = np.array([0, 0, 0])
    assert np.allclose(normal.to_numpy(), expected)

