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

from typing import List, Callable, TypeVar

T = TypeVar('T')


def group_items_by(
    items: List[T],
    group_func: Callable[[T, T], bool]
) -> List[List[T]]:
    """
    Groups items into consecutive sublists based on a pairwise grouping condition.

    Iterates through the list of items and assigns each item to the first group
    where the provided `group_func` returns True when comparing the last item in
    that group with the current item. If no existing group matches, a new group is created.

    This method groups items sequentially, relying on the relationship between the
    current item and the last item in each group. It does not merge groups based on
    transitive relations between non-consecutive items.

    Args:
        items (List[T]): The list of items to be grouped.
        group_func (Callable[[T, T], bool]): A binary predicate function that takes two items
            (the last item in an existing group and a new candidate item) and returns True
            if the new item should be grouped with the existing group.

    Returns:
        List[List[T]]: A list of groups (sublists), where each group contains items that
            satisfy the grouping condition in sequence.

    Example:
        >>> group_items_by([1, 2, 4, 5, 7], lambda a, b: abs(a - b) == 1)
        [[1, 2], [4, 5], [7]]
    """
    if not items:
        return []

    groups: List[List[T]] = []

    for item in items:
        added_to_group = False

        for group in groups:
            if group_func(group[-1], item):
                group.append(item)
                added_to_group = True
                break

        if not added_to_group:
            groups.append([item])

    return groups

