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

from shapeedit.utils.grouping import group_items_by


def test_group_items():
    items = [1, 2, 4, 5, 7]

    result = group_items_by(items, lambda a, b: abs(a - b) == 1)

    expected = [[1, 2], [4, 5], [7]]
    assert result == expected


def test_group_items_by_empty_list():
    items = []

    result = group_items_by(items, lambda a, b: a == b)

    expected = []
    assert result == expected


def test_group_items_by_all_same():
    items = [5, 5, 5, 5]

    result = group_items_by(items, lambda a, b: a == b)

    expected = [[5, 5, 5, 5]]
    assert result == expected


def test_group_items_by_no_matches():
    items = [1, 2, 3]

    result = group_items_by(items, lambda a, b: False)

    expected = [[1], [2], [3]]
    assert result == expected


def test_group_items_by_custom_condition():
    items = [2, 4, 1, 3, 6, 8]

    result = group_items_by(items, lambda a, b: (a % 2) == (b % 2))

    expected = [[2, 4, 6, 8], [1, 3]]
    assert result == expected


def test_group_items_by_string_equality():
    items = ["apple", "apricot", "banana", "blueberry", "avocado"]

    result = group_items_by(items, lambda a, b: a[0] == b[0])

    expected = [["apple", "apricot", "avocado"], ["banana", "blueberry"]]
    assert result == expected
