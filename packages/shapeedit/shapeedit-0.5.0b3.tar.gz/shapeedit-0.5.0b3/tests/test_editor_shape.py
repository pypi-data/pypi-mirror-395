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
from shapeio.shape import Point

from shapeedit import ShapeEditor
from shapeedit.editors.lodcontrol_editor import _LodControlEditor


def test_shape_editor_replace_texture_image_matches(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    result = editor.replace_texture_image("DB_Rails10w.ACE", "V4_Rails1.ace")
    expected = "V4_Rails1.ace"
    assert result is True
    assert shape.images[0] != expected
    assert shape.images[1] != expected
    assert shape.images[2] == expected
    assert shape.images[4] == expected
    assert shape.images[5] == expected
    assert shape.images[10] == expected


def test_shape_editor_replace_texture_image_no_match(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    result = editor.replace_texture_image("NotInTheList.ace", "V4_Rails1.ace")
    expected = "DB_Rails10w.ACE"
    assert result is False
    assert shape.images[2] == expected
    assert shape.images[4] == expected
    assert shape.images[5] == expected
    assert shape.images[10] == expected


@pytest.mark.parametrize("ignore_case", [
    True, False
])
def test_shape_editor_replace_texture_image_ignore_case(global_storage, ignore_case):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    result = editor.replace_texture_image("DB_Rails10w.ace", "V4_Rails1.ace", ignore_case=ignore_case)
    
    if ignore_case:
        expected = "V4_Rails1.ace"
        assert result is True
    else:
        expected = "DB_Rails10w.ACE"
        assert result is False
    assert shape.images[0] != expected
    assert shape.images[1] != expected
    assert shape.images[2] == expected
    assert shape.images[4] == expected
    assert shape.images[5] == expected
    assert shape.images[10] == expected


@pytest.mark.parametrize("bad_input", [
    None, 1, Point(1, 2, 3), True
])
def test_shape_editor_replace_texture_image_bad_match_input_raises(global_storage, bad_input):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    with pytest.raises(TypeError):
        editor.replace_texture_image(bad_input, "V4_Rails1.ace")


@pytest.mark.parametrize("bad_input", [
    None, 1, Point(1, 2, 3), True
])
def test_shape_editor_replace_texture_image_bad_replace_input_raises(global_storage, bad_input):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    with pytest.raises(TypeError):
        editor.replace_texture_image("DB_Rails10w.ace", bad_input)


@pytest.mark.parametrize("bad_input", [
    None, 1, Point(1, 2, 3), "thisisastring"
])
def test_shape_editor_replace_texture_image_bad_case_input_raises(global_storage, bad_input):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    with pytest.raises(TypeError):
        editor.replace_texture_image("DB_Rails10w.ace", "V4_Rails1.ace", ignore_case=bad_input)


def test_shape_editor_lod_controls(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    lod_controls = editor.lod_controls()
    assert len(lod_controls) == 1


def test_shape_editor_lod_control_by_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    lod_control = editor.lod_control(0)
    assert isinstance(lod_control, _LodControlEditor)


@pytest.mark.parametrize("bad_index", [
    1, -1, 100
])
def test_shape_editor_lod_control_by_index_raises(global_storage, bad_index):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    with pytest.raises(IndexError):
        editor.lod_control(bad_index)


@pytest.mark.parametrize("bad_input", [
    None, 1, Point(1, 2, 3)
])
def test_shape_editor_bad_input_raises(global_storage, bad_input):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]

    with pytest.raises(TypeError):
        ShapeEditor(bad_input)


@pytest.mark.parametrize("bad_input", [
    None, Point(1, 2, 3)
])
def test_shape_editor_lod_control_bad_input_raises(global_storage, bad_input):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    with pytest.raises(TypeError):
        editor.lod_control(bad_input)
