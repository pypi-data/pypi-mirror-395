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

import shapeio


def _fast_clone(obj):
    """
    Recursively clone Python base types and custom classes.
    Avoids deepcopy overhead before each test.
    """
    # Base immutable types - just return
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj

    # Lists / tuples / sets - clone elements
    elif isinstance(obj, list):
        return [_fast_clone(x) for x in obj]
    elif isinstance(obj, tuple):
        return tuple(_fast_clone(x) for x in obj)
    elif isinstance(obj, set):
        return {_fast_clone(x) for x in obj}

    # Dicts - clone keys/values
    elif isinstance(obj, dict):
        return {_fast_clone(k): _fast_clone(v) for k, v in obj.items()}

    # Custom class with __dict__
    elif hasattr(obj, "__dict__"):
        clone = obj.__class__.__new__(obj.__class__)  # avoid __init__
        for k, v in obj.__dict__.items():
            setattr(clone, k, _fast_clone(v))
        return clone

    # Fallback: return object as-is
    else:
        return obj


@pytest.fixture(scope="session")
def _loaded_shape():
    return shapeio.load("./tests/data/DK10f_A1tPnt5dLft.s")


@pytest.fixture(scope="function")
def global_storage(_loaded_shape):
    shape_copy = _fast_clone(_loaded_shape) # Each test gets a fresh copy
    return {"shape_DK10f_A1tPnt5dLft": shape_copy}
