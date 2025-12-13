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
from shapeedit.editors.subobject_editor import _SubObjectEditor


def test_distancelevel_editor_sub_objects(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_objects = editor.lod_control(0).distance_level(200).sub_objects()
    assert len(sub_objects) == 5


def test_distancelevel_editor_sub_object_by_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    assert isinstance(sub_object, _SubObjectEditor)


def test_distancelevel_editor_dlevelselection(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    distance_levels = editor.lod_control(0).distance_levels()
    assert distance_levels[0].dlevel_selection == 200
    assert distance_levels[1].dlevel_selection == 500
    assert distance_levels[2].dlevel_selection == 800
    assert distance_levels[3].dlevel_selection == 2000


def test_lodcontrol_editor_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    distance_level = editor.lod_control(0).distance_level(800)
    assert distance_level.index == 2


@pytest.mark.parametrize("bad_index", [
    5, -1, 30
])
def test_distancelevel_editor_sub_object_by_index_raises(global_storage, bad_index):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    distance_level = ShapeEditor(shape).lod_control(0).distance_level(200)

    with pytest.raises(IndexError):
        distance_level.sub_object(bad_index)