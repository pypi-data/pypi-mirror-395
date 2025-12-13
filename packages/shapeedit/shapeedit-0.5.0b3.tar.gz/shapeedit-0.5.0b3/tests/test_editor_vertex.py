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

from shapeio.shape import Point, UVPoint, Vector
from shapeedit import ShapeEditor


def test_vertex_editor_index(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    assert vertex.index == 0


def test_vertex_editor_point_getter(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    point = vertex.point
    assert isinstance(point, Point)


def test_vertex_editor_point_getter_raises(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    vertex._vertex.point_index = 10000000000

    with pytest.raises(IndexError):
        vertex.point


def test_vertex_editor_point_setter_adds_new_point(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)
    new_point = Point(0.0, 0.0, 0.0)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    vertex.point = new_point

    assert new_point in shape.points
    assert shape.points[vertex._vertex.point_index] == new_point


def test_vertex_editor_point_setter_uses_existing_point(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)
    existing_point = shape.points[0]

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    vertex.point = existing_point

    assert shape.points.count(existing_point) == 1
    assert shape.points[vertex._vertex.point_index] == existing_point


@pytest.mark.parametrize("bad_value", [
    42, "not a point", None, [1, 2, 3]
])
def test_vertex_editor_point_setter_raises(global_storage, bad_value):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    
    with pytest.raises(TypeError):
        vertex.point = bad_value


def test_vertex_editor_uvpoint_getter(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    uv_point = vertex.uv_point
    assert isinstance(uv_point, UVPoint)


def test_vertex_editor_uvpoint_getter_raises(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    vertex._vertex.vertex_uvs[0] = 10000000000

    with pytest.raises(IndexError):
        vertex.uv_point


def test_vertex_editor_uvpoint_setter_adds_new_point(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)
    new_uv_point = UVPoint(0.0, 0.0)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    vertex.uv_point = new_uv_point

    assert new_uv_point in shape.uv_points
    assert shape.uv_points[vertex._vertex.vertex_uvs[0]] == new_uv_point


def test_vertex_editor_uvpoint_setter_uses_existing_point(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)
    existing_uv_point = shape.uv_points[0]

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    vertex.uv_point = existing_uv_point

    assert shape.uv_points.count(existing_uv_point) == 1
    assert shape.uv_points[vertex._vertex.vertex_uvs[0]] == existing_uv_point


@pytest.mark.parametrize("bad_value", [
    42, "not a point", None, [1, 2, 3]
])
def test_vertex_editor_uvpoint_setter_raises(global_storage, bad_value):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    
    with pytest.raises(TypeError):
        vertex.uv_point = bad_value


def test_vertex_editor_normal_getter(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    normal = vertex.normal
    assert isinstance(normal, Vector)


def test_vertex_editor_normal_getter_raises(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    vertex._vertex.normal_index = 10000000000

    with pytest.raises(IndexError):
        vertex.normal


def test_vertex_editor_normal_setter_adds_new_vector(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)
    new_normal = Vector(0.0, 0.0, 0.0)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    vertex.normal = new_normal

    assert new_normal in shape.normals
    assert shape.normals[vertex._vertex.normal_index] == new_normal


def test_vertex_editor_normal_setter_uses_existing_vector(global_storage):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)
    existing_normal = shape.normals[0]

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    vertex.normal = existing_normal

    assert shape.normals.count(existing_normal) == 1
    assert shape.normals[vertex._vertex.normal_index] == existing_normal


@pytest.mark.parametrize("bad_value", [
    42, "not a vector", None, [1, 2, 3]
])
def test_vertex_editor_normal_setter_raises(global_storage, bad_value):
    shape = global_storage["shape_DK10f_A1tPnt5dLft"]
    editor = ShapeEditor(shape)

    vertex = editor.lod_control(0).distance_level(200).sub_object(0).vertex(0)
    
    with pytest.raises(TypeError):
        vertex.normal = bad_value