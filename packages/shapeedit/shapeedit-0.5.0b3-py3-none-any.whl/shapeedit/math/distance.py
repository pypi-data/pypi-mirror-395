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
from shapeio import shape


def signed_distance_between(
    point1: shape.Point,
    point2: shape.Point,
    plane: str = "xz"
) -> float:
    """
    Calculates the signed distance between two 3D points, projected onto a specified plane.

    The direction of the sign is determined based on a reference vector (perpendicular 
    to the projection plane). This allows distinguishing "in front" vs "behind" relationships or left/right side 
    relative to the reference direction.

    Supported planes:
        - "x", "y", "z": Distance along a single axis.
        - "xy", "xz", "zy": 2D plane projections.
        - "xyz": Full 3D Euclidean distance (always positive, not signed).

    Args:
        point1 (shape.Point): The first point (reference/origin).
        point2 (shape.Point): The second point (target).
        plane (str): The projection plane to consider ("x", "y", "z", "xy", "xz", "zy", "xyz").

    Returns:
        float: The signed distance between the projected points. Positive or negative
               depending on relative orientation. If plane is "xyz", returns Euclidean distance.
    
    Raises:
        ValueError: If the provided plane is not supported.
    """
    point1 = point1.to_numpy()
    point2 = point2.to_numpy()

    if plane == "x":
        point1_proj = np.array([point1[0], 0, 0])
        point2_proj = np.array([point2[0], 0, 0])
        reference_vector = np.array([0, 1, 0])
    elif plane == "y":
        point1_proj = np.array([0, point1[1], 0])
        point2_proj = np.array([0, point2[1], 0])
        reference_vector = np.array([1, 0, 0])
    elif plane == "z":
        point1_proj = np.array([0, 0, point1[2]])
        point2_proj = np.array([0, 0, point2[2]])
        reference_vector = np.array([1, 0, 0])
    elif plane == "xy":
        point1_proj = np.array([point1[0], point1[1], 0])
        point2_proj = np.array([point2[0], point2[1], 0])
        reference_vector = np.array([1, 0, 0])
    elif plane == "xz":
        point1_proj = np.array([point1[0], 0, point1[2]])
        point2_proj = np.array([point2[0], 0, point2[2]])
        reference_vector = np.array([0, 1, 0])
    elif plane == "zy":
        point1_proj = np.array([0, point1[1], point1[2]])
        point2_proj = np.array([0, point2[1], point2[2]])
        reference_vector = np.array([1, 0, 0])
    elif plane == "xyz": # Euclidean distance, never signed.
        point1_proj = np.array([point1[0], point1[1], point1[2]])
        point2_proj = np.array([point2[0], point2[1], point2[2]])
        vector_to_point = point2_proj - point1_proj
        distance = np.linalg.norm(vector_to_point)
        return distance
    else:
        raise ValueError("Invalid plane. Choose 'x', 'y', 'z', 'xy', 'xz', 'zy', or 'xyz'.")

    vector_to_point = point1_proj - point2_proj
    cross = np.cross(reference_vector, vector_to_point)
    signed_distance = np.linalg.norm(vector_to_point[:2]) * np.sign(cross[-1])

    return signed_distance


def distance_between(
    point1: shape.Point,
    point2: shape.Point,
    plane: str = "xz"
) -> float:
    """
    Calculates the absolute (unsigned) distance between two 3D points, 
    projected onto a specified plane.

    Internally uses `signed_distance_between` and returns the absolute value.
    Useful when directionality doesn't matter but dimensional filtering does.

    Args:
        point1 (shape.Point): The first point.
        point2 (shape.Point): The second point.
        plane (str): The projection plane to consider ("x", "y", "z", "xy", "xz", "zy", "xyz").

    Returns:
        float: The absolute distance between the projected points.
    
    Raises:
        ValueError: If the provided plane is not supported.
    """
    signed_distance = signed_distance_between(point1, point2, plane=plane)
    
    distance = abs(signed_distance)

    return distance

