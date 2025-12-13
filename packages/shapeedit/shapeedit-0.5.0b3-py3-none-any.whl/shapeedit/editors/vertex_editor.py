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

from typing import TYPE_CHECKING
from shapeio.shape import Vertex, Point, UVPoint, Vector

if TYPE_CHECKING:
    from .subobject_editor import _SubObjectEditor


class _VertexEditor:
    """
    Internal editor for a single `Vertex` within a `SubObject`.

    This class is part of the internal shape-editing API and **should not**
    be instantiated directly. Instances are created and returned by
    `_SubObjectEditor.vertex()` or `_SubObjectEditor.vertices()`.

    It provides safe access and modification of the vertex's point, UV point,
    and normal, preserving the consistency of the underlying `Shape` data
    structure used in MSTS/Open Rails.
    """

    def __init__(self, vertex: Vertex, _parent: "_SubObjectEditor" = None):
        """
        Initializes a `_VertexEditor` instance.

        Do not call this constructor directly. Use `_SubObjectEditor.vertex()`
        or `_SubObjectEditor.vertices()` to obtain an instance.

        Args:
            vertex (Vertex): The vertex to wrap.
            _parent (_SubObjectEditor): The parent SubObject editor.

        Raises:
            TypeError: If `_parent` is None, or if `vertex` is not a `Vertex`,
                or if `_parent` is not a `_SubObjectEditor`.
        """
        from .subobject_editor import _SubObjectEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a _SubObjectEditor, not None")

        if not isinstance(vertex, Vertex):
            raise TypeError(f"Parameter 'vertex' must be of type shape.Vertex, but got {type(vertex).__name__}")
        
        if not isinstance(_parent, _SubObjectEditor):
            raise TypeError(f"Parameter '_parent' must be of type _SubObjectEditor, but got {type(_parent).__name__}")

        self._vertex = vertex
        self._parent = _parent
    
    def __repr__(self):
        """
        Return a string representation of the _VertexEditor object.

        Returns:
            str: A string representation of the _VertexEditor instance.
        """
        return f"_VertexEditor({self._vertex})"
    
    @property
    def index(self) -> int:
        """
        Index of this `Vertex` in the parent SubObject's vertices list.

        Returns:
            int: The index of this vertex within the parent SubObject.

        Raises:
            IndexError: If the vertex is not found in the parent's list.
        """
        try:
            return self._parent._sub_object.vertices.index(self._vertex)
        except ValueError:
            raise IndexError("Vertex not found in parent's vertices list")

    @property
    def point(self) -> Point:
        """
        The `Point` associated with this vertex.

        Returns:
            Point: The point object referenced by this vertex.

        Raises:
            IndexError: If the Vertex's point index is not found in the shape's points list.
        """
        shape = self._parent._parent._parent._parent._shape
        point_idx = self._vertex.point_index

        if not (point_idx < len(shape.points)):
            raise IndexError(f"Point index {point_idx} not found in shape's points list")
        
        return shape.points[point_idx]
    
    @point.setter
    def point(self, point: Point):
        """
        Sets the `Point` for this vertex.

        If the point does not exist in the shape's points list, it is appended.

        Args:
            point (Point): The new point to assign.

        Raises:
            TypeError: If `point` is not a `Point` instance.
        """
        shape = self._parent._parent._parent._parent._shape

        if not isinstance(point, Point):
            raise TypeError(f"Parameter 'point' must be of type shape.Point, but got {type(point).__name__}")

        if point in shape.points:
            point_idx = shape.points.index(point)
        else:
            shape.points.append(point)
            point_idx = len(shape.points) - 1

        self._vertex.point_index = point_idx

    @property
    def uv_point(self) -> UVPoint:
        """
        The `UVPoint` associated with this vertex.

        Returns:
            UVPoint: The UV point object referenced by this vertex.

        Raises:
            IndexError: If the UV point index is not found in the shape's uv_points list.
        """
        shape = self._parent._parent._parent._parent._shape
        uv_point_idx = self._vertex.vertex_uvs[0]

        if not (uv_point_idx < len(shape.uv_points)):
            raise IndexError(f"UVPoint index {uv_point_idx} not found in shape's uv_points list")
        
        return shape.uv_points[uv_point_idx]

    @uv_point.setter
    def uv_point(self, uv_point: UVPoint):
        """
        Sets the `UVPoint` for this vertex.

        If the UV point does not exist in the shape's uv_points list, it is appended.

        Args:
            uv_point (UVPoint): The new UV point to assign.

        Raises:
            TypeError: If `uv_point` is not a `UVPoint` instance.
        """
        shape = self._parent._parent._parent._parent._shape

        if not isinstance(uv_point, UVPoint):
            raise TypeError(f"Parameter 'uv_point' must be of type shape.UVPoint, but got {type(uv_point).__name__}")

        if uv_point in shape.uv_points:
            uv_point_idx = shape.uv_points.index(uv_point)
        else:
            shape.uv_points.append(uv_point)
            uv_point_idx = len(shape.uv_points) - 1

        self._vertex.vertex_uvs[0] = uv_point_idx

    @property
    def normal(self) -> Vector:
        """
        The `Vector` normal associated with this vertex.

        Returns:
            Vector: The normal vector referenced by this vertex.

        Raises:
            IndexError: If the normal index is not found in the shape's normals list.
        """
        shape = self._parent._parent._parent._parent._shape
        normal_idx = self._vertex.normal_index

        if not (normal_idx < len(shape.normals)):
            raise IndexError(f"Normal index {normal_idx} not found in shape's normals list")
        
        return shape.normals[normal_idx]

    @normal.setter
    def normal(self, normal: Vector):
        """
        Sets the `Vector` normal for this vertex.

        If the normal vector does not exist in the shape's normals list, it is appended.

        Args:
            normal (Vector): The new normal vector to assign.

        Raises:
            TypeError: If `normal` is not a `Vector` instance.
        """
        shape = self._parent._parent._parent._parent._shape

        if not isinstance(normal, Vector):
            raise TypeError(f"Parameter 'normal' must be of type shape.Vector, but got {type(normal).__name__}")

        if normal in shape.normals:
            normal_idx = shape.normals.index(normal)
        else:
            shape.normals.append(normal)
            normal_idx = len(shape.normals) - 1

        self._vertex.normal_index = normal_idx