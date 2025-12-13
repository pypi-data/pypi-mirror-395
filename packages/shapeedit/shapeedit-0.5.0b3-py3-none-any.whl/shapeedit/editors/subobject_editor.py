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

from typing import TYPE_CHECKING, List, Optional
from shapeio.shape import SubObject, Vertex

from .primitive_editor import _PrimitiveEditor
from .vertex_editor import _VertexEditor
from ..helpers.subobject_helper import _SubObjectHelper

if TYPE_CHECKING:
    from .distancelevel_editor import _DistanceLevelEditor


class _SubObjectEditor:
    """
    Internal editor for a single `SubObject` within a `DistanceLevel`.

    This class is part of the internal shape-editing API and **should not**
    be instantiated directly. Instances are created and returned by
    `_DistanceLevelEditor.sub_object()` or `_DistanceLevelEditor.sub_objects()`.

    It provides safe access and editing of a SubObject's primitives and
    vertices, preserving the consistency of the underlying `Shape` data
    structure used in MSTS/Open Rails.
    """

    def __init__(self, sub_object: SubObject, _parent: "_DistanceLevelEditor" = None):
        """
        Initializes a `_SubObjectEditor` instance.

        Do not call this constructor directly. Use `_DistanceLevelEditor.sub_object()`
        or `_DistanceLevelEditor.sub_objects()` to obtain an instance.

        Args:
            sub_object (SubObject): The SubObject to wrap.
            _parent (_DistanceLevelEditor): The parent distance level editor.

        Raises:
            TypeError: If `_parent` is None, or if `sub_object` is not
                a `SubObject`, or if `_parent` is not a `_DistanceLevelEditor`.
        """
        from .distancelevel_editor import _DistanceLevelEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a _DistanceLevelEditor, not None")

        if not isinstance(sub_object, SubObject):
            raise TypeError(f"Parameter 'sub_object' must be of type shape.SubObject, but got {type(sub_object).__name__}")
        
        if not isinstance(_parent, _DistanceLevelEditor):
            raise TypeError(f"Parameter '_parent' must be of type _DistanceLevelEditor, but got {type(_parent).__name__}")

        self._sub_object = sub_object
        self._parent = _parent
        self._sub_object_helper = _SubObjectHelper(sub_object)
    
    def __repr__(self):
        """
        Return a string representation of the _SubObjectEditor object.

        Returns:
            str: A string representation of the _SubObjectEditor instance.
        """
        return f"_SubObjectEditor({self._sub_object})"
    
    @property
    def index(self) -> int:
        """
        Index of this `SubObject` in the parent DistanceLevel's list.

        Returns:
            int: The index of this SubObject within the parent's `sub_objects` list.

        Raises:
            IndexError: If the underlying `SubObject` is not found in the parent's list.
        """
        try:
            return self._parent._distance_level.sub_objects.index(self._sub_object)
        except ValueError:
            raise IndexError("SubObject not found in parent's sub_objects list")

    def primitive(self, primitive_index: int) -> _PrimitiveEditor:
        """
        Returns an editor for a specific Primitive in this SubObject.

        Args:
            primitive_index (int): Index of the Primitive to edit.

        Returns:
            _PrimitiveEditor: An editor for the specified Primitive.

        Raises:
            TypeError: If `primitive_index` is not an integer.
            IndexError: If `primitive_index` is out of the valid range.
        """
        if not isinstance(primitive_index, int):
            raise TypeError(f"Parameter 'primitive_index' must be of type int, but got {type(primitive_index).__name__}")
        
        if not (0 <= primitive_index < len(self._sub_object.primitives)):
            raise IndexError(
                f"primitive_index {primitive_index} out of range "
                f"(valid range: 0 to {len(self._sub_object.primitives) - 1})"
            )

        primitive = self._sub_object.primitives[primitive_index]
        return _PrimitiveEditor(primitive, _parent=self)
    
    def primitives(self,
        prim_state_index: Optional[int] = None,
        prim_state_name: Optional[str] = None
    ) -> List[_PrimitiveEditor]:
        """
        Returns editors for primitives in this SubObject, optionally filtered by prim_state.

        Args:
            prim_state_index (int, optional): Only include primitives with this prim_state index.
            prim_state_name (str, optional): Only include primitives with this prim_state name.

        Returns:
            List[_PrimitiveEditor]: A list of primitive editors matching the filters.

        Raises:
            TypeError: If `prim_state_index` is not an integer or
                       `prim_state_name` is not a string.
        """
        if prim_state_index is not None and not isinstance(prim_state_index, int):
            raise TypeError(f"Parameter 'prim_state_index' must be of type int, but got {type(prim_state_index).__name__}")
        
        if prim_state_name is not None and not isinstance(prim_state_name, str):
            raise TypeError(f"Parameter 'prim_state_name' must be of type str, but got {type(prim_state_name).__name__}")
        
        shape = self._parent._parent._parent._shape
        primitives = []

        for primitive in self._sub_object.primitives:
            if prim_state_index is not None and primitive.prim_state_index != prim_state_index:
                continue

            if prim_state_name is not None:
                state_name = shape.prim_states[primitive.prim_state_index].name
                if state_name != prim_state_name:
                    continue

            primitives.append(_PrimitiveEditor(primitive, _parent=self))

        return primitives
    
    def vertex(self, vertex_index: int) -> _VertexEditor:
        """
        Returns an editor for a specific vertex in this SubObject.

        Args:
            vertex_index (int): Index of the vertex to edit.

        Returns:
            _VertexEditor: An editor for the specified vertex.

        Raises:
            TypeError: If `vertex_index` is not an integer.
            IndexError: If `vertex_index` is out of the valid range.
        """
        if not isinstance(vertex_index, int):
            raise TypeError(f"Parameter 'vertex_index' must be of type int, but got {type(vertex_index).__name__}")

        if not (0 <= vertex_index < len(self._sub_object.vertices)):
            raise IndexError(
                f"vertex_index {vertex_index} out of range "
                f"(valid range: 0 to {len(self._sub_object.vertices) - 1})"
            )

        vertex = self._sub_object.vertices[vertex_index]
        return _VertexEditor(vertex, _parent=self)
    
    def vertices(self) -> List[_VertexEditor]:
        """
        Returns editors for all vertices in this SubObject.

        Returns:
            List[_VertexEditor]: A list of vertex editors.
        """
        return [
            _VertexEditor(vertex, _parent=self)
            for vertex in self._sub_object.vertices
        ]