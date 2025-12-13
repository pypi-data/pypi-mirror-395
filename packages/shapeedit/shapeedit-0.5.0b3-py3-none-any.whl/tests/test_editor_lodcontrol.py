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

import pytest

from shapeedit import ShapeEditor
from shapeedit.editors.distancelevel_editor import _DistanceLevelEditor
from shapeedit.editors.lodcontrol_editor import _LodControlEditor


def test_lodcontrol_editor_distance_levels(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    distance_levels = editor.lod_control(0).distance_levels()
    assert len(distance_levels) == 4


def test_lodcontrol_editor_distance_level_by_distance(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    distance_level = editor.lod_control(0).distance_level(200)
    assert isinstance(distance_level, _DistanceLevelEditor)


def test_lodcontrol_editor_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    lod_control = editor.lod_control(0)
    assert lod_control.index == 0


@pytest.mark.parametrize("bad_value", [
    1, -1, 300, 1337
])
def test_lodcontrol_editor_distance_level_by_distance_raises(global_storage, bad_value):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    lod_control = ShapeEditor(shape).lod_control(0)

    with pytest.raises(ValueError):
        lod_control.distance_level(bad_value)
