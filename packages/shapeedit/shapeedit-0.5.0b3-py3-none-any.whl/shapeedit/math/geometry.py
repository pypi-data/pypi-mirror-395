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
from typing import List
from shapeio import shape


def calculate_point_centroid(
    points: List[shape.Point]
) -> shape.Point:
    """
    Calculates the centroid (geometric center) of a list of 3D points.

    The centroid is the arithmetic mean of all point positions.

    Args:
        points (List[shape.Point]): A list of points.

    Returns:
        shape.Point: The centroid of the input points.
    """
    positions = [p.to_numpy() for p in points]

    centroid = np.mean(positions, axis=0)

    return shape.Point.from_numpy(centroid)


def calculate_point_midpoint(
    point1: shape.Point,
    point2: shape.Point
) -> shape.Point:
    """
    Calculates the midpoint between two 3D points.

    The midpoint lies halfway between the two input points in 3D space.

    Args:
        point1 (shape.Point): The first point.
        point2 (shape.Point): The second point.

    Returns:
        shape.Point: The midpoint between the two points.
    """
    midpoint = (point1.to_numpy() + point2.to_numpy()) / 2

    return shape.Point.from_numpy(midpoint)


def calculate_uvpoint_midpoint(
    uv_point1: shape.UVPoint,
    uv_point2: shape.UVPoint
) -> shape.UVPoint:
    """
    Calculates the midpoint between two 2D UV points.

    This is a simple average of their (u, v) coordinates.

    Args:
        uv_point1 (shape.UVPoint): The first UV point.
        uv_point2 (shape.UVPoint): The second UV point.

    Returns:
        shape.UVPoint: The midpoint between the two UV points.
    """
    midpoint = (uv_point1.to_numpy() + uv_point2.to_numpy()) / 2

    return shape.UVPoint.from_numpy(midpoint)


def calculate_face_normal(
    point1: shape.Point,
    point2: shape.Point,
    point3: shape.Point,
    normalize: bool = True
) -> shape.Vector:
    """
    Calculates the normal vector of a face (triangle) defined by three 3D points.

    The normal is computed using the cross product of two edges of the triangle.
    If `normalize` is True, the resulting vector is normalized to unit length.

    Args:
        point1 (shape.Point): First vertex of the triangle.
        point2 (shape.Point): Second vertex of the triangle.
        point3 (shape.Point): Third vertex of the triangle.
        normalize (bool): Whether to normalize the result to unit length.

    Returns:
        shape.Vector: The face normal vector. Zero vector if the triangle is degenerate.
    """
    edge1 = point2.to_numpy().astype(np.float64) - point1.to_numpy().astype(np.float64)
    edge2 = point3.to_numpy().astype(np.float64) - point1.to_numpy().astype(np.float64)

    normal = np.cross(edge1, edge2).astype(np.float64)

    norm = np.linalg.norm(normal)
    if normalize:
        if norm > 1e-10:
            normal /= norm
        else:
            normal = np.zeros_like(normal)

    normal = np.round(normal, 4)

    return shape.Vector.from_numpy(normal)


def calculate_vertex_normal(
    point: shape.Point,
    connected_points: List[shape.Point],
    normalize: bool = False
) -> shape.Vector:
    """
    Estimates a vertex normal by averaging the normals of adjacent faces 
    formed by the vertex and its connected points.

    The function loops over consecutive pairs of connected points to form 
    triangles with the input point, calculates each face normal, and sums them.
    The result is optionally normalized.

    Args:
        point (shape.Point): The central vertex.
        connected_points (List[shape.Point]): Points connected to the vertex, in winding order.
        normalize (bool): Whether to normalize the resulting normal vector.

    Returns:
        shape.Vector: The summed (or normalized) vertex normal. Zero vector if fewer than two connections.
    """
    vertex_normal_sum = np.zeros(3, dtype=float)

    if len(connected_points) < 2:
        return shape.Vector(0, 0, 0)

    for i in range(len(connected_points) - 1):
        edge1 = connected_points[i].to_numpy().astype(np.float64) - point.to_numpy().astype(np.float64)
        edge2 = connected_points[i + 1].to_numpy().astype(np.float64) - point.to_numpy().astype(np.float64)

        normal = np.cross(edge1, edge2)

        if np.linalg.norm(normal) > 1e-10:
            normal /= np.linalg.norm(normal)
        else:
            normal = np.zeros_like(normal)

        normal = np.round(normal, 4)
        vertex_normal_sum += normal

    if normalize:
        norm = np.linalg.norm(vertex_normal_sum)
        if norm > 1e-10:
            vertex_normal_sum /= norm
        else:
            vertex_normal_sum = np.zeros_like(vertex_normal_sum)

    return shape.Vector.from_numpy(vertex_normal_sum)
