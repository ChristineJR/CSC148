"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict, Tuple


class DistanceMap:
    """ A distance map that can be used to store or look up the distance
    between any two cities.

    === Private Attributes ===
    _map:
      A dictionary of distance. <_map>'s value is undefined until
      <self>.add_distance is called. It contains keys that each of
      them is a distinct tuple containing the names of two cities, and
      its corresponding value is the distance between these two cities.
    """
    _map: Dict[Tuple[str, str], int]

    def __init__(self) -> None:
        """Create a DistanceMap with no distance.
        >>> m = DistanceMap()
        >>> m.distance('Toronto', 'York')
        -1
        """
        self._map = {}

    def add_distance(self, a: str, b: str, d_1: int, d_2: int = -1) -> None:
        """Add the distance between <a> and <b> into this DistanceMap.
        The distance from <a> to <b> is <d_1>.
        The distance from <b> to <a> is <d_2> if <d_2> is provided, or is
        <d_1> too if not.

        If the distance between <a> and <b> has already contained in this
        DistanceMap, nothing changes.

        Precondition: No two cities have negative distance, therefore,
        d_1 >= 0 and d_2 >= 0.

        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> m.distance('Toronto', 'Hamilton')
        9
        >>> m.distance('Hamilton', 'Toronto')
        9

        >>> m.add_distance('Toronto', 'York', 5, 6)
        >>> m.distance('Toronto', 'York')
        5
        >>> m.distance('York', 'Toronto')
        6
        """
        if (a, b) not in self._map:
            self._map[(a, b)] = d_1
            if d_2 == -1:
                self._map[(b, a)] = d_1
            else:
                self._map[(b, a)] = d_2

    def distance(self, a: str, b: str) -> int:
        """Return the distance from <a> to <b>, or return -1 if this
        distance is not stored in this DistanceMap.

        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> m.distance('Toronto', 'Hamilton')
        9
        >>> m.distance('Toronto', 'York')
        -1
        """
        if (a, b) in self._map:
            return self._map[(a, b)]
        return -1


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest

    doctest.testmod()
