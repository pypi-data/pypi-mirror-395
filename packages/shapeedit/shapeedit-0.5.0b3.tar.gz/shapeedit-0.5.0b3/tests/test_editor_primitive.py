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
from shapeedit.editors.vertex_editor import _VertexEditor
from shapeedit.editors.triangle_editor import _TriangleEditor


def test_primitive_editor_vertices(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    vertices = sub_object.primitive(0).vertices()
    assert len(vertices) == 2353


def test_primitive_editor_connected_vertices(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    vertex = sub_object.vertex(1792)
    connected_vertices = sub_object.primitive(0).connected_vertices(vertex)
    assert len(connected_vertices) == 4


@pytest.mark.parametrize("bad_type", [
    1337, "not a _VertexEditor"
])
def test_primitive_editor_connected_vertices_raises(global_storage, bad_type):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)

    with pytest.raises(TypeError):
        sub_object.primitive(0).connected_vertices(bad_type)


def test_primitive_editor_triangles(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    triangles = sub_object.primitive(0).triangles()
    assert len(triangles) == 1667


def test_primitive_editor_triangle(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    triangle = sub_object.primitive(0).triangle(0)
    assert isinstance(triangle, _TriangleEditor)


@pytest.mark.parametrize("bad_index", [
    1667, -1, 30000, 13337
])
def test_subobject_editor_primitive_by_index_raises(global_storage, bad_index):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    sub_object = ShapeEditor(shape).lod_control(0).distance_level(200).sub_object(0)

    with pytest.raises(IndexError):
        sub_object.primitive(0).triangle(bad_index)


def test_primitive_editor_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    primitive = sub_object.primitive(0)
    assert primitive.index == 0


def test_primitive_editor_matrix_getter(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    primitive = sub_object.primitive(0)
    matrix = primitive.matrix
    assert matrix.name == "PNT5D_L01"
