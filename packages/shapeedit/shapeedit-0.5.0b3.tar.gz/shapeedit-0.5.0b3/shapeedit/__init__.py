"""
ShapeEdit

This module provides operations for safely modifying existing MSTS/ORTS shape files.

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

__version__ = '0.5.0b3'
__all__ = [
    'math', 'utils',
    'ShapeEditor',
]

__author__ = 'Peter Grønbæk Andersen <peter@grnbk.io>'

from . import math
from . import utils
from .editors.shape_editor import ShapeEditor
