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
from shapeedit.editors.primitive_editor import _PrimitiveEditor
from shapeedit.editors.vertex_editor import _VertexEditor


def test_subobject_editor_primitives(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    primitives = sub_object.primitives()
    assert len(primitives) == 22


def test_subobject_editor_primitives_filtered_by_primstateindex(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    primitives = sub_object.primitives(prim_state_index=0)
    assert len(primitives) == 2
    assert all([p._primitive.prim_state_index == 0 for p in primitives])


def test_subobject_editor_primitives_filtered_by_primstatename(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    primitives = sub_object.primitives(prim_state_name="Rails")
    assert len(primitives) == 6
    assert all([shape.prim_states[p._primitive.prim_state_index].name == "Rails" for p in primitives])


@pytest.mark.parametrize("bad_type", [
    "not an int", 0.1, []
])
def test_subobject_editor_primitives_filtered_by_primstateindex_raises(global_storage, bad_type):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    sub_object = ShapeEditor(shape).lod_control(0).distance_level(200).sub_object(0)

    with pytest.raises(TypeError):
        sub_object.primitives(prim_state_index=bad_type)


@pytest.mark.parametrize("bad_type", [
    1, 0.1, []
])
def test_subobject_editor_primitives_filtered_by_primstatename_raises(global_storage, bad_type):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    sub_object = ShapeEditor(shape).lod_control(0).distance_level(200).sub_object(0)

    with pytest.raises(TypeError):
        sub_object.primitives(prim_state_name=bad_type)


def test_subobject_editor_primitive_by_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    primitive = sub_object.primitive(0)
    assert isinstance(primitive, _PrimitiveEditor)


def test_subobject_editor_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    assert sub_object.index == 0


@pytest.mark.parametrize("bad_index", [
    22, -1, 300, 1337
])
def test_subobject_editor_primitive_by_index_raises(global_storage, bad_index):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    sub_object = ShapeEditor(shape).lod_control(0).distance_level(200).sub_object(0)

    with pytest.raises(IndexError):
        sub_object.primitive(bad_index)


def test_subobject_editor_vertices(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    vertices = sub_object.vertices()
    assert len(vertices) == 7427


def test_subobject_editor_vertex_by_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    vertex = sub_object.vertex(0)
    assert isinstance(vertex, _VertexEditor)


@pytest.mark.parametrize("bad_index", [
    7427, -1, 13337
])
def test_subobject_editor_vertex_by_index_raises(global_storage, bad_index):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    sub_object = ShapeEditor(shape).lod_control(0).distance_level(200).sub_object(0)

    with pytest.raises(IndexError):
        sub_object.vertex(bad_index)