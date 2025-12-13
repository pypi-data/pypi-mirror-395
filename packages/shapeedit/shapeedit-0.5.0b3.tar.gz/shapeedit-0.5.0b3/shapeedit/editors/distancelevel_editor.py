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

from typing import TYPE_CHECKING, List
from shapeio.shape import DistanceLevel

from .subobject_editor import _SubObjectEditor

if TYPE_CHECKING:
    from .lodcontrol_editor import _LodControlEditor


class _DistanceLevelEditor:
    """
    Internal editor for a single `DistanceLevel` within a `LodControl`.

    This class is internal to the shape editing API and **should not**
    be instantiated directly. Instances are created and returned by
    `_LodControlEditor.distance_level()` or `_LodControlEditor.distance_levels()`.
    """

    def __init__(self, distance_level: DistanceLevel, _parent: "_LodControlEditor" = None):
        """
        Initializes a `_DistanceLevelEditor`.

        Do not call this constructor directly. Use `_LodControlEditor.distance_level()`
        or `_LodControlEditor.distance_levels()` to obtain an instance.

        Args:
            distance_level (DistanceLevel): The distance level to wrap.
            _parent (_LodControlEditor): The parent `_LodControlEditor` instance.

        Raises:
            TypeError: If `_parent` is None, or if `distance_level` is not
                a `DistanceLevel`, or if `_parent` is not a `_LodControlEditor`.
        """
        from .lodcontrol_editor import _LodControlEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a _LodControlEditor, not None")

        if not isinstance(distance_level, DistanceLevel):
            raise TypeError(f"Parameter 'distance_level' must be of type shape.DistanceLevel, but got {type(distance_level).__name__}")
        
        if not isinstance(_parent, _LodControlEditor):
            raise TypeError(f"Parameter '_parent' must be of type _LodControlEditor, but got {type(_parent).__name__}")

        self._distance_level = distance_level
        self._parent = _parent
    
    def __repr__(self):
        """
        Return a string representation of the _DistanceLevelEditor object.

        Returns:
            str: A string representation of the _DistanceLevelEditor instance.
        """
        return f"_DistanceLevelEditor({self._distance_level})"

    @property
    def index(self) -> int:
        """
        Index of this `DistanceLevel` in the parent LOD control's list.

        Returns:
            int: The index of this distance level within the parent's
            `distance_levels` list.

        Raises:
            IndexError: If the underlying `DistanceLevel` is not found in the
                parent's `distance_levels` list.
        """
        try:
            return self._parent._lod_control.distance_levels.index(self._distance_level)
        except ValueError:
            raise IndexError("DistanceLevel not found in parent's distance_levels list")
    
    @property
    def dlevel_selection(self) -> int:
        """
        The `dlevel_selection` identifier of this distance level.

        Returns:
            int: The `dlevel_selection` value from the distance level header.
        """
        return self._distance_level.distance_level_header.dlevel_selection

    def sub_object(self, sub_object_index: int) -> _SubObjectEditor:
        """
        Returns an editor for a specific SubObject at this distance level.

        Args:
            sub_object_index (int): Index of the SubObject to edit.

        Returns:
            _SubObjectEditor: An editor for the specified SubObject.

        Raises:
            TypeError: If `sub_object_index` is not an integer.
            IndexError: If `sub_object_index` is out of the valid range.
        """
        if not isinstance(sub_object_index, int):
            raise TypeError(f"Parameter 'sub_object_index' must be of type int, but got {type(sub_object_index).__name__}")
        
        if not (0 <= sub_object_index < len(self._distance_level.sub_objects)):
            raise IndexError(
                f"sub_object_index {sub_object_index} out of range "
                f"(valid range: 0 to {len(self._distance_level.sub_objects) - 1})"
            )

        sub_object = self._distance_level.sub_objects[sub_object_index]
        return _SubObjectEditor(sub_object, _parent=self)
    
    def sub_objects(self) -> List[_SubObjectEditor]:
        """
        Returns editors for all SubObject in this distance level.

        Returns:
            List[_SubObjectEditor]: A list of editors for all SubObject.
        """
        return [
            _SubObjectEditor(sub_object, _parent=self)
            for sub_object in self._distance_level.sub_objects
        ]
