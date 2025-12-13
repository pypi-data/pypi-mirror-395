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

from typing import Optional
from shapeio.shape import SubObject, Primitive


class _SubObjectHelper:
    """
    Internal helper class for a `SubObject`.

    This class is used internally within `_SubObjectEditor` to manage
    low-level SubObject data, such as geometry info and vertex sets.
    It **should not be instantiated or used directly** by
    external code.

    Args:
        sub_object (SubObject): The SubObject to wrap.

    Raises:
        TypeError: If `sub_object` is not a `SubObject`.
    """

    def __init__(self, sub_object: SubObject):
        """
        Initializes the internal `_SubObjectHelper`.

        Do not instantiate this class directly; it is intended for internal use
        within `_SubObjectEditor` and its children editors.

        Args:
            sub_object (SubObject): The SubObject to wrap and manage.

        Raises:
            TypeError: If `sub_object` is not a `SubObject` instance.
        """
        if not isinstance(sub_object, SubObject):
            raise TypeError(f"""Parameter 'sub_object' must be of type shape.SubObject,
                but got {type(sub_object).__name__}""")
        
        self._sub_object = sub_object

    def update_geometry_info(self):
        """
        Recalculates and updates geometry information for the SubObject.

        Updates `geometry_info` and `cullable_prims` based on the
        current primitives and triangle lists, including:
            - Total number of face normals
            - Total number of trilist indices
            - Primitive-level counts in geometry nodes
        """
        geometry_info = self._sub_object.sub_object_header.geometry_info

        # Gather vertex and face counts based on trilist data
        vertex_idxs_counts = []
        normal_idxs_counts = []

        for primitive in self._sub_object.primitives:
            indexed_trilist = primitive.indexed_trilist
            triangle_count = len(indexed_trilist.vertex_idxs)
            vertex_idxs_counts.append(triangle_count * 3)
            normal_idxs_counts.append(triangle_count)

        # Update values within geometry_info
        geometry_info.face_normals = sum(normal_idxs_counts)
        geometry_info.trilist_indices = sum(vertex_idxs_counts)

        # Update values within cullable_prims
        current_prim_idx = 0

        for geometry_node in geometry_info.geometry_nodes:
            num_primitives = geometry_node.cullable_prims.num_prims
            from_idx = current_prim_idx
            to_idx = current_prim_idx + num_primitives

            geometry_node.cullable_prims.num_flat_sections = sum(normal_idxs_counts[from_idx:to_idx])
            geometry_node.cullable_prims.num_prim_indices = sum(vertex_idxs_counts[from_idx:to_idx])

            current_prim_idx += num_primitives

    def find_vertexset_index(self, primitive: Primitive) -> Optional[int]:
        """
        Finds the vertex set index that contains vertices associated with the given primitive.

        Args:
            primitive (Primitive): The primitive for which to find the vertex set index.

        Returns:
            Optional[int]: The index of the vertex set that contains vertices associated with
            the primitive, or `None` if the primitive index is out of range.
        """
        geometry_info = self._sub_object.sub_object_header.geometry_info
        total_prims = 0

        for idx, node in enumerate(geometry_info.geometry_nodes):
            total_prims += node.cullable_prims.num_prims
            if total_prims > self._sub_object.primitives.index(primitive):
                return idx
        
        return None

    def expand_vertexset(self, primitive: Primitive) -> Optional[int]:
        """
        Expands the vertex set counts to make way for
        adding a new vertex to the specified primitive.

        Finds the vertex state index corresponding to the primitive,
        increments the vertex count, and adjusts start indices in
        the vertex sets.

        Args:
            primitive (Primitive): The primitive whose vertex set should be expanded.

        Returns:
            Optional[int]: The new vertex index in the expanded vertex set,
            or `None` if no update was performed.
        """
        vtx_state_idx_to_update = self.find_vertexset_index(primitive)
        if vtx_state_idx_to_update is None:
            return None

        # Update the vertex count and adjust start indices
        total_vertex_count = 0
        new_vertex_idx = None
        update_next_sets = False

        for vertex_set in self._sub_object.vertex_sets:
            if vertex_set.vtx_state == vtx_state_idx_to_update:
                new_vertex_idx = vertex_set.vtx_start_index + vertex_set.vtx_count
                vertex_set.vtx_count += 1
                update_next_sets = True

            elif update_next_sets:
                vertex_set.vtx_start_index = total_vertex_count

            total_vertex_count = vertex_set.vtx_start_index + vertex_set.vtx_count

        return new_vertex_idx