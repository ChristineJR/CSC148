"""Prep 8 Synthesize

=== CSC148 Winter 2021 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu and Diane Horton

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 David Liu and Diane Horton

=== Module Description ===
Your task in this prep is to implement each of the unimplemented Tree methods
in this file.

The starter code has a recursive template that treats both the "empty tree"
and the "size-one" tree ("leaf") as base cases.  You may not need both of these
base cases -- it depends on the method you are writing.  If you can, collapse
down to just one base case.
"""
from __future__ import annotations
from typing import Any, List, Optional


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[Any]
    # The list of all subtrees of this tree.
    _subtrees: List[Tree]

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty Tree.
    #
    #   Note: self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node (a 'leaf')

    def __init__(self, root: Any, subtrees: List[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return True if this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also do len(subtree) here
            return size

    def num_negatives(self) -> int:
        """Return the number of negative integers in this tree.

        Precondition: all items in this tree are integers.

        Remember, 0 is *not* negative.

        >>> t1 = Tree(17, [])
        >>> t1.num_negatives()
        0
        >>> t2 = Tree(-10, [])
        >>> t2.num_negatives()
        1
        >>> t3 = Tree(-11, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t3.num_negatives()
        3
        """
        if self.is_empty():
            return 0
        else:
            n = 0
            if self._root < 0:
                n += 1
            for subtree in self._subtrees:
                n += subtree.num_negatives()
            return n

    def maximum(self: Tree) -> int:
        """Return the maximum item stored in this tree.

        Return 0 if this tree is empty.

        Precondition: all values in this tree are positive integers.

        >>> t1 = Tree(17, [])
        >>> t1.maximum()
        17
        >>> t3 = Tree(1, [Tree(22, []), Tree(100, []), Tree(30, [])])
        >>> t3.maximum()
        100
        """
        if self.is_empty():
            return 0
        else:
            m = self._root
            for subtree in self._subtrees:
                n = subtree.maximum()
                if n > m:
                    m = n
            return m

    def height(self: Tree) -> int:
        """Return the height of this tree.

        Please refer to the prep readings for the definition of tree height.

        >>> t1 = Tree(17, [])
        >>> t1.height()
        1
        >>> t2 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t2.height()
        2
        """
        if self.is_empty():
            return 0
        elif not self._subtrees:
            return 1
        else:
            n = 1
            lst = []
            for subtree in self._subtrees:
                lst.append(subtree.height())
            n += max(lst)
            return n

    def __contains__(self, item: Any) -> bool:
        """Return whether this tree contains <item>.

        >>> t = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t.__contains__(-30)  # Could also write -30 in t.
        True
        >>> t.__contains__(148)
        False
        """
        if self.is_empty():
            return False
        else:
            n = False
            if self._root == item:
                n = True
            for subtree in self._subtrees:
                if subtree.__contains__(item) is True:
                    n = True
            return n


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={'disable': ['E1136']})
