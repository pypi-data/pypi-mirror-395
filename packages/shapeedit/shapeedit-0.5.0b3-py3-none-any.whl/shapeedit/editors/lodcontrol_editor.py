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
from shapeio.shape import LodControl

from .distancelevel_editor import _DistanceLevelEditor

if TYPE_CHECKING:
    from .shape_editor import ShapeEditor


class _LodControlEditor:
    """
    Internal editor for a single `LodControl` within a `Shape`.

    This class is part of the internal shape-editing API and **should not**
    be instantiated directly. Instances are created and returned by
    `ShapeEditor.lod_control()` or `ShapeEditor.lod_controls()`.

    It provides safe access and editing of a single LOD control's distance
    levels, ensuring that changes keep the `Shape` data structure consistent
    and valid for MSTS/Open Rails.
    """

    def __init__(self, lod_control: LodControl, _parent: "ShapeEditor" = None):
        """
        Initializes a `_LodControlEditor` instance.

        Do not call this constructor directly. Use `ShapeEditor.lod_control()`
        or `ShapeEditor.lod_controls()` to obtain an instance.

        Args:
            lod_control (LodControl): The LOD control to wrap.
            _parent (ShapeEditor): The parent `ShapeEditor` instance.

        Raises:
            TypeError: If `_parent` is None, or if `lod_control` is not
                a `LodControl`, or if `_parent` is not a `ShapeEditor`.
        """
        from .shape_editor import ShapeEditor

        if _parent is None:
            raise TypeError("Parameter '_parent' must be a ShapeEditor, not None")

        if not isinstance(lod_control, LodControl):
            raise TypeError(f"Parameter 'lod_control' must be of type shape.LodControl, but got {type(lod_control).__name__}")
        
        if not isinstance(_parent, ShapeEditor):
            raise TypeError(f"Parameter '_parent' must be of type ShapeEditor, but got {type(_parent).__name__}")

        self._lod_control = lod_control
        self._parent = _parent
    
    def __repr__(self):
        """
        Return a string representation of the _LodControlEditor object.

        Returns:
            str: A string representation of the _LodControlEditor instance.
        """
        return f"_LodControlEditor({self._lod_control})"

    @property
    def index(self) -> int:
        """
        Index of this `LodControl` in the parent shape's `lod_controls` list.

        Returns:
            int: The index of this LOD control within the parent shape.

        Raises:
            IndexError: If the underlying `LodControl` is not found in the
                parent's `lod_controls` list.
        """
        try:
            return self._parent._shape.lod_controls.index(self._lod_control)
        except ValueError:
            raise IndexError("LodControl not found in parent's lod_controls list")
    
    def distance_level(self, dlevel_selection: int) -> _DistanceLevelEditor:
        """
        Returns an editor for a specific distance level in this LOD control.

        Args:
            dlevel_selection (int): The `dlevel_selection` identifier of
                the distance level to edit.

        Returns:
            _DistanceLevelEditor: An editor instance for the matching
            distance level.

        Raises:
            TypeError: If `dlevel_selection` is not an integer.
            ValueError: If no matching distance level is found.
        """
        if not isinstance(dlevel_selection, int):
            raise TypeError(f"Parameter 'dlevel_selection' must be of type int, but got {type(dlevel_selection).__name__}")

        for distance_level in self._lod_control.distance_levels:
            if distance_level.distance_level_header.dlevel_selection == dlevel_selection:
                return _DistanceLevelEditor(distance_level, _parent=self)

        raise ValueError(f"No DistanceLevel with dlevel_selection {dlevel_selection} found in this LodControl")
    
    def distance_levels(self) -> List[_DistanceLevelEditor]:
        """
        Returns editors for all distance levels in this LOD control.

        Each editor allows safe modifications to its respective distance level.

        Returns:
            List[_DistanceLevelEditor]: A list of editors for all distance levels.
        """
        return [
            _DistanceLevelEditor(distance_level, _parent=self)
            for distance_level in self._lod_control.distance_levels
        ]