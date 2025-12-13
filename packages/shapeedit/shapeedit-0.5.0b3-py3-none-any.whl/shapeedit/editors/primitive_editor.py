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

import copy
from typing import TYPE_CHECKING, List
from shapeio.shape import Primitive, Vertex, Point, UVPoint, Vector
from shapeio.shape import Matrix, VertexIdx, NormalIdx

from .triangle_editor import _TriangleEditor
from .vertex_editor import _VertexEditor
from ..math.geometry import calculate_face_normal

if TYPE_CHECKING:
    from .subobject_editor import _SubObjectEditor


class _PrimitiveEditor:
    """
    Internal editor for a single `Primitive` within a `SubObject`.

    This class is part of the internal shape-editing API and **should not**
    be instantiated directly. Instances are created and returned by
    `_SubObjectEditor.primitive()` or `_SubObjectEditor.primitives()`.

    It provides safe access to the primitive's vertices, triangles, and
    transformation matrix, preserving the consistency of the underlying
    `Shape` data structure used in MSTS/Open Rails.
    """

    def __init__(self, primitive: Primitive, _parent: "_SubObjectEditor" = None):
        """
        Initializes a `_PrimitiveEditor` instance.

        Do not call this constructor directly. Use `_SubObjectEditor.primitive()`
        or `_SubObjectEditor.primitives()` to obtain an instance.

        Args:
            primitive (Primitive): The primitive to wrap.
            _parent (_SubObjectEditor): The parent SubObject editor.

        Raises:
            TypeError: If `_parent` is None, or if `primitive` is not a `Primitive`,
                       or if `_parent` is not a `_SubObjectEditor`.
        """
        from .subobject_editor import _SubObjectEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a _SubObjectEditor, not None")

        if not isinstance(primitive, Primitive):
            raise TypeError(f"Parameter 'primitive' must be of type shape.Primitive, but got {type(primitive).__name__}")
        
        if not isinstance(_parent, _SubObjectEditor):
            raise TypeError(f"Parameter '_parent' must be of type _SubObjectEditor, but got {type(_parent).__name__}")

        self._primitive = primitive
        self._parent = _parent
    
    def __repr__(self):
        """
        Return a string representation of the _PrimitiveEditor object.

        Returns:
            str: A string representation of the _PrimitiveEditor instance.
        """
        return f"_PrimitiveEditor({self._primitive})"
    
    @property
    def index(self) -> int:
        """
        Index of this `Primitive` in the parent SubObject's primitives list.

        Returns:
            int: The index of this primitive within the parent SubObject.

        Raises:
            IndexError: If the primitive is not found in the parent's list.
        """
        try:
            return self._parent._sub_object.primitives.index(self._primitive)
        except ValueError:
            raise IndexError("Primitive not found in parent's primitives list")

    @property
    def matrix(self) -> Matrix:
        """
        Returns the transformation matrix associated with this primitive.

        Returns:
            Matrix: The matrix object referenced by this primitive.
        """
        shape = self._parent._parent._parent._parent._shape
        prim_state_idx = self._primitive.prim_state_index
        vtx_state_idx = shape.prim_states[prim_state_idx].vtx_state_index
        matrix_idx = shape.vtx_states[vtx_state_idx].matrix_index
        return shape.matrices[matrix_idx]

    def vertices(self) -> List[_VertexEditor]:
        """
        Returns editors for all vertices used by this primitive.

        The vertices are returned in the order they first appear in the
        primitive's indexed triangle list. Each vertex only appear once in the returned list.

        Returns:
            List[_VertexEditor]: A list of vertex editors.
        """
        parent_vertices = self._parent._sub_object.vertices
        seen = set()
        unique_ordered_indices = []

        for vertex_idx in self._primitive.indexed_trilist.vertex_idxs:
            for idx in (vertex_idx.vertex1_index, vertex_idx.vertex2_index, vertex_idx.vertex3_index):
                if idx not in seen:
                    seen.add(idx)
                    unique_ordered_indices.append(idx)

        return [_VertexEditor(parent_vertices[idx], _parent=self._parent) for idx in unique_ordered_indices]

    def connected_vertices(self, vertex: _VertexEditor) -> List[_VertexEditor]:
        """
        Returns editors for vertices connected to the given vertex.

        The vertices are returned in the order they first appear in the
        primitive's indexed triangle list. Each connected vertex only appears once.

        Args:
            vertex (_VertexEditor): The vertex to find connections for.

        Returns:
            List[_VertexEditor]: A list of vertex editors connected to the given vertex.
        
        Raises:
            TypeError: If `vertex` is not a `_VertexEditor`.
        """
        if not isinstance(vertex, _VertexEditor):
            raise TypeError(f"Parameter 'vertex' must be of type _VertexEditor, but got {type(vertex).__name__}")

        parent_vertices = self._parent._sub_object.vertices
        seen = set()
        connected_indices = []

        target_idx = vertex.index

        for vertex_idx in self._primitive.indexed_trilist.vertex_idxs:
            indices = (vertex_idx.vertex1_index, vertex_idx.vertex2_index, vertex_idx.vertex3_index)
            if target_idx in indices:
                for idx in indices:
                    if idx != target_idx and idx not in seen:
                        seen.add(idx)
                        connected_indices.append(idx)

        return [_VertexEditor(parent_vertices[idx], _parent=self._parent) for idx in connected_indices]

    def triangle(self, triangle_index: int) -> _TriangleEditor:
        """
        Returns an editor for a specific triangle in this primitive.

        Args:
            triangle_index (int): Index of the triangle to edit.

        Returns:
            _TriangleEditor: An editor for the specified triangle.

        Raises:
            TypeError: If `triangle_index` is not an integer.
            IndexError: If `triangle_index` is out of range of the primitive's
                        vertex or normal index lists.
        """
        if not isinstance(triangle_index, int):
            raise TypeError(f"Parameter 'triangle_index' must be of type int, but got {type(triangle_index).__name__}")

        indexed_trilist = self._primitive.indexed_trilist

        if not (0 <= triangle_index < len(indexed_trilist.vertex_idxs)):
            raise IndexError(
                f"triangle_index {triangle_index} out of range "
                f"(valid range: 0 to {len(indexed_trilist.vertex_idxs) - 1})"
            )
        
        if not (0 <= triangle_index < len(indexed_trilist.normal_idxs)):
            raise IndexError(
                f"triangle_index {triangle_index} out of range "
                f"(valid range: 0 to {len(indexed_trilist.normal_idxs) - 1})"
            )

        vertex_idx = indexed_trilist.vertex_idxs[triangle_index]
        normal_idx = indexed_trilist.normal_idxs[triangle_index]
        return _TriangleEditor(vertex_idx, normal_idx, _parent=self)
    
    def triangles(self) -> List[_TriangleEditor]:
        """
        Returns editors for all triangles in this primitive.

        Returns:
            List[_TriangleEditor]: A list of triangle editors, in order of the
            primitive's indexed triangle list.
        """
        indexed_trilist = self._primitive.indexed_trilist
        return [
            _TriangleEditor(vertex_idx, normal_idx, _parent=self)
            for vertex_idx, normal_idx in zip(indexed_trilist.vertex_idxs, indexed_trilist.normal_idxs)
        ]

    def add_vertex(self, new_point: Point, new_uv_point: UVPoint, new_normal: Vector) -> _VertexEditor:
        """
        Adds a new vertex to the this primitive's parent SubObject.

        This method inserts a new vertex into the parent SubObject at the
        correct position, updates all necessary indices in existing primitives
        to make room for the new vertex, and then assigns the specified point,
        UV point, and normal to the new vertex.

        Args:
            new_point (Point): The point (position) to assign to the new vertex.
            new_uv_point (UVPoint): The UV point (texture coordinates) to assign.
            new_normal (Vector): The normal vector to assign.

        Returns:
            _VertexEditor: An editor for the newly created vertex.

        Raises:
            TypeError: If any of the arguments are not of the expected types.
            IndexError: If index adjustments fail due to inconsistent geometry data.
        """
        if not isinstance(new_point, Point):
            raise TypeError(f"Parameter 'new_point' must be of type shape.Point, but got {type(new_point).__name__}")

        if not isinstance(new_uv_point, UVPoint):
            raise TypeError(f"Parameter 'new_uv_point' must be of type shape.UVPoint, but got {type(new_uv_point).__name__}")

        if not isinstance(new_normal, Vector):
            raise TypeError(f"Parameter 'new_normal' must be of type shape.Vector, but got {type(new_normal).__name__}")

        sub_object = self._parent
        sub_object_helper = sub_object._sub_object_helper

        # Make way for the new vertex, and get the index to insert it into.
        new_vertex_idx = sub_object_helper.expand_vertexset(self._primitive)

        # Increment vertex indexes where necessary in the parent sub_object primitives.
        for primitive in sub_object.primitives():
            for triangle in primitive.triangles():
                tri_idxs = triangle._vertex_idx
                vertex_idxs = [tri_idxs.vertex1_index, tri_idxs.vertex2_index, tri_idxs.vertex3_index]

                for idx, vertex_idx in enumerate(vertex_idxs):
                    if vertex_idx >= new_vertex_idx:
                        vertex_idxs[idx] = vertex_idx + 1

                tri_idxs.vertex1_index, tri_idxs.vertex2_index, tri_idxs.vertex3_index = vertex_idxs
        
        # Create the new vertex and its corresponding _VertexEditor.
        new_vertex = Vertex(
            flags="00000000",
            point_index=0, # Updated by the new editor later
            normal_index=0, # Updated by the new editor later
            colour1="ff969696",
            colour2="ff808080",
            vertex_uvs=[0] # Updated by the new editor later
        )
        new_vertex_editor = _VertexEditor(new_vertex, sub_object)

        # Update point, uv_point and normal data for the new vertex.
        new_vertex_editor.point = copy.deepcopy(new_point)
        new_vertex_editor.uv_point = copy.deepcopy(new_uv_point)
        new_vertex_editor.normal = copy.deepcopy(new_normal)

        # Add new vertex to the sub_object at the correct position.
        sub_object._sub_object.vertices[new_vertex_idx:new_vertex_idx] = [new_vertex]

        return new_vertex_editor
    
    def insert_triangle(self, vertex1: _VertexEditor, vertex2: _VertexEditor, vertex3: _VertexEditor) -> _TriangleEditor:
        """
        Inserts a new triangle into this primitive's indexed trilist.

        Validates that the vertices belong to the same SubObject and vertex set,
        calculates the triangle's face normal, creates the corresponding VertexIdx
        and NormalIdx objects, and appends them to the indexed trilist.

        Args:
            vertex1 (_VertexEditor): The first vertex of the triangle.
            vertex2 (_VertexEditor): The second vertex of the triangle.
            vertex3 (_VertexEditor): The third vertex of the triangle.

        Returns:
            _TriangleEditor: An editor for the newly created triangle.

        Raises:
            TypeError: If any vertex argument is not of type _VertexEditor.
            ValueError: If any vertex does not belong to the same SubObject or vertex set as this primitive.
        """
        sub_object = self._parent
        sub_object_helper = sub_object._sub_object_helper
        indexed_trilist = self._primitive.indexed_trilist

        parameters = [("vertex1", vertex1), ("vertex2", vertex2), ("vertex3", vertex3)]

        for name, vertex in parameters:
            if not isinstance(vertex, _VertexEditor):
                raise TypeError(f"Parameter '{name}' must be of type _VertexEditor, but got {type(vertex).__name__}")

        for name, vertex in parameters:
            if vertex._parent._sub_object is not self._parent._sub_object:
                raise ValueError(f"Parameter '{name}' is not from the same SubObject as this primitive")

        # Calculate face normal of the new triangle.
        face_normal = calculate_face_normal(vertex1.point, vertex2.point, vertex3.point)

        # Create the new VertexIdx, NormalIdx and their corresponding _TriangleEditor.
        new_vertex_idx = VertexIdx(
            vertex1_index=vertex1.index,
            vertex2_index=vertex2.index, 
            vertex3_index=vertex3.index,
        )
        new_normal_idx = NormalIdx(
            index=0, # Updated by the new editor later
            unknown2=3
        )
        new_triangle_editor = _TriangleEditor(new_vertex_idx, new_normal_idx, self)

        # Update face normal for the new triangle.
        new_triangle_editor.face_normal = copy.deepcopy(face_normal)

        # Add new triangle to the indexed_trilist.
        indexed_trilist.vertex_idxs.append(new_vertex_idx)
        indexed_trilist.normal_idxs.append(new_normal_idx)
        indexed_trilist.flags.append("00000000")

        # Update geometry_info in the parent sub_object.
        sub_object_helper.update_geometry_info()

        return new_triangle_editor

    def remove_triangle(self, vertex1: _VertexEditor, vertex2: _VertexEditor, vertex3: _VertexEditor):
        """
        Removes a triangle from this primitive that matches the specified vertices.

        Validates that the vertices belong to the same SubObject and vertex set,
        then searches the primitive's indexed trilist for a triangle containing
        exactly these vertices and removes it. Updates the parent SubObject's
        geometry information afterward.

        Args:
            vertex1 (_VertexEditor): The first vertex of the triangle to remove.
            vertex2 (_VertexEditor): The second vertex of the triangle to remove.
            vertex3 (_VertexEditor): The third vertex of the triangle to remove.

        Raises:
            TypeError: If any vertex argument is not of type _VertexEditor.
            ValueError: If any vertex does not belong to the same SubObject or vertex set as this primitive.
        """
        sub_object = self._parent
        sub_object_helper = sub_object._sub_object_helper
        indexed_trilist = self._primitive.indexed_trilist

        parameters = [("vertex1", vertex1), ("vertex2", vertex2), ("vertex3", vertex3)]

        for name, vertex in parameters:
            if not isinstance(vertex, _VertexEditor):
                raise TypeError(f"Parameter '{name}' must be of type _VertexEditor, but got {type(vertex).__name__}")

        for name, vertex in parameters:
            if vertex._parent._sub_object is not self._parent._sub_object:
                raise ValueError(f"Parameter '{name}' is not from the same SubObject as this primitive")

        # Remove the triangle from the indexed trilist.
        for triangle in reversed(self.triangles()):
            tri_vertex_idxs = [v.index for v in triangle.vertices()]

            should_remove = all([
                vertex1.index in tri_vertex_idxs,
                vertex2.index in tri_vertex_idxs,
                vertex3.index in tri_vertex_idxs
            ])

            if should_remove:
                tri_idx = triangle.index
                del indexed_trilist.vertex_idxs[tri_idx]
                del indexed_trilist.normal_idxs[tri_idx]
                del indexed_trilist.flags[tri_idx]

        # Update geometry_info in the parent sub_object.
        sub_object_helper.update_geometry_info()

    def remove_triangles_connected_to(self, vertex: _VertexEditor):
        """
        Removes all triangles in this primitive that include the specified vertex.

        Validates that the vertex belongs to the same SubObject and vertex set,
        then iterates over the primitive's indexed trilist and deletes all triangles
        containing the vertex. Updates the parent SubObject's geometry information.

        Args:
            vertex (_VertexEditor): The vertex whose connected triangles should be removed.

        Raises:
            TypeError: If the vertex is not of type _VertexEditor.
            ValueError: If the vertex does not belong to the same SubObject or vertex set as this primitive.
        """
        sub_object = self._parent
        sub_object_helper = sub_object._sub_object_helper
        indexed_trilist = self._primitive.indexed_trilist

        if not isinstance(vertex, _VertexEditor):
            raise TypeError(f"Parameter 'vertex' must be of type _VertexEditor, but got {type(vertex).__name__}")

        if not self._parent._sub_object is vertex._parent._sub_object:
            raise ValueError("Parameter 'vertex' is not from the same SubObject as this primitive")
        
        # Remove connected triangles from the indexed trilist.
        for triangle in reversed(self.triangles()):
            tri_vertex_idxs = [v.index for v in triangle.vertices()]
            
            should_remove = vertex.index in tri_vertex_idxs

            if should_remove:
                tri_idx = triangle.index
                del indexed_trilist.vertex_idxs[tri_idx]
                del indexed_trilist.normal_idxs[tri_idx]
                del indexed_trilist.flags[tri_idx]

        # Update geometry_info in the parent sub_object.
        sub_object_helper.update_geometry_info()