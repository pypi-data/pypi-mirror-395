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

from shapeio.shape import Point, Vector, Matrix 
from shapeedit.math.coordinates import remap_point, remap_normal


def make_identity_matrix(name: str):
    """Identity matrix."""
    matrix = np.eye(4, dtype=np.float32)
    return from_np4x4_to_matrix(name, matrix)


def make_translation_matrix(name: str, translate_x: float, translate_y: float, translate_z: float):
    """Translation matrix."""
    matrix = np.eye(4, dtype=np.float32)
    matrix[0, 3] = translate_x
    matrix[1, 3] = translate_y
    matrix[2, 3] = translate_z
    return from_np4x4_to_matrix(name, matrix)


def make_scale_matrix(name: str, scale_x: float, scale_y: float, scale_z: float):
    """Non-uniform scale matrix."""
    matrix = np.eye(4, dtype=np.float32)
    matrix[0, 0] = scale_x
    matrix[1, 1] = scale_y
    matrix[2, 2] = scale_z
    return from_np4x4_to_matrix(name, matrix)


def make_rotation_z_matrix(name: str, theta: float):
    """Rotation matrix around the Z-axis."""
    c, s = np.cos(theta), np.sin(theta)
    matrix = np.eye(4, dtype=np.float32)
    matrix[0, 0] = c
    matrix[0, 1] = -s
    matrix[1, 0] = s
    matrix[1, 1] = c
    return from_np4x4_to_matrix(name, matrix)


def from_np4x4_to_matrix(name: str, mat4x4: np.ndarray) -> Matrix:
    if mat4x4.shape != (4, 4):
        raise ValueError("Parameter 'mat4x4' must be a np.ndarray with shape (4, 4)")

    arr4x3 = np.zeros((4, 3), dtype=np.float32)
    arr4x3[0, :] = mat4x4[0, 0:3]
    arr4x3[1, :] = mat4x4[1, 0:3]
    arr4x3[2, :] = mat4x4[2, 0:3]
    arr4x3[3, :] = mat4x4[0:3, 3]
    return Matrix.from_numpy(name, arr4x3)


class TestRemapPoint:
    def test_identity_remap_point(self):
        point = Point(1.0, 2.0, 3.0)
        from_matrix = make_identity_matrix("from")
        to_matrix = make_identity_matrix("to")

        result = remap_point(point, from_matrix, to_matrix)

        assert np.allclose(result.to_numpy(), point.to_numpy())

    def test_translation_remap_point(self):
        point = Point(1.0, 2.0, 3.0)
        from_matrix = make_identity_matrix("from")
        to_matrix = make_translation_matrix("to", 1, 1, 1)

        result = remap_point(point, from_matrix, to_matrix)

        # Point should be moved by -1 in each coordinate
        expected = np.array([0.0, 1.0, 2.0])
        assert np.allclose(result.to_numpy(), expected)

    def test_rotation_remap_point(self):
        point = Point(1.0, 0.0, 0.0)
        theta = np.deg2rad(90)
        from_matrix = make_identity_matrix("from")
        to_matrix = make_rotation_z_matrix("to", theta)

        result = remap_point(point, from_matrix, to_matrix)
        
        # Point should effectively rotate +90° in new space = (0, -1, 0)
        expected = np.array([0.0, 1.0, 0.0])
        assert np.allclose(result.to_numpy(), expected, atol=1e-6)


class TestRemapNormal:
    def test_identity_remap_normal(self):
        normal = Vector(0.0, 0.0, 1.0)
        from_matrix = make_identity_matrix("from")
        to_matrix = make_identity_matrix("to")

        result = remap_normal(normal, from_matrix, to_matrix)

        assert np.allclose(result.to_numpy(), normal.to_numpy())

    def test_nonuniform_scale_remap_normal(self):
        normal = Vector(0.0, 0.0, 1.0)
        from_matrix = make_identity_matrix("from")
        to_matrix = make_scale_matrix("to", 2.0, 1.0, 0.5)

        result = remap_normal(normal, from_matrix, to_matrix)

        # Vector should still be normalized
        assert np.isclose(np.linalg.norm(result.to_numpy()), 1.0)
        # Direction should still mostly align with Z axis
        assert result.z > 0.5

    def test_rotation_remap_normal(self):
        normal = Vector(1.0, 0.0, 0.0)
        theta = np.deg2rad(90)
        from_matrix = make_identity_matrix("from")
        to_matrix = make_rotation_z_matrix("to", theta)

        result = remap_normal(normal, from_matrix, to_matrix)

        # Vector should effectively rotate +90° in new space
        expected = np.array([0.0, 1.0, 0.0])
        assert np.allclose(result.to_numpy(), expected, atol=1e-6)

