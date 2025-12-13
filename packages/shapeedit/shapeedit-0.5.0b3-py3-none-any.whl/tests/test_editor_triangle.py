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

from shapeio.shape import Vector
from shapeedit import ShapeEditor


def test_primitive_editor_vertices(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    vertices = sub_object.primitive(0).triangle(0).vertices()
    assert len(vertices) == 3


def test_triangle_editor_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    triangle = sub_object.primitive(0).triangle(0)
    assert triangle.index == 0


def test_triangle_editor_facenormal_getter(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    triangle = sub_object.primitive(0).triangle(0)
    normal = triangle.face_normal
    assert isinstance(normal, Vector)


def test_triangle_editor_facenormal_getter_raises(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    triangle = sub_object.primitive(0).triangle(0)
    triangle._normal_idx.index = 10000000000

    with pytest.raises(IndexError):
        triangle.face_normal


def test_triangle_editor_facenormal_setter_adds_new_vector(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)
    new_normal = Vector(0.0, 0.0, 0.0)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    triangle = sub_object.primitive(0).triangle(0)
    triangle.face_normal = new_normal

    assert new_normal in shape.normals
    assert shape.normals[triangle._normal_idx.index] == new_normal


def test_triangle_editor_facenormal_setter_uses_existing_vector(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)
    existing_normal = shape.normals[0]

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    triangle = sub_object.primitive(0).triangle(0)
    triangle.face_normal = existing_normal

    assert shape.normals.count(existing_normal) == 1
    assert shape.normals[triangle._normal_idx.index] == existing_normal


@pytest.mark.parametrize("bad_value", [
    42, "not a vector", None, [1, 2, 3]
])
def test_triangle_editor_facenormal_setter_raises(global_storage, bad_value):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    sub_object = editor.lod_control(0).distance_level(200).sub_object(0)
    triangle = sub_object.primitive(0).triangle(0)
    
    with pytest.raises(TypeError):
        triangle.face_normal = bad_value
