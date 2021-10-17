"""Assignment 1 - Container and priority queue (Task 3)

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

This module contains the Container and PriorityQueue classes.
"""

from typing import Any, List, Callable


class Container:
    """A container that holds Objects.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def add(self, item: Any) -> None:
        """Add <item> to this Container.
        """
        raise NotImplementedError

    def remove(self) -> Any:
        """Remove and return a single item from this Container.
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        """Return True iff this Container is empty.
        """
        raise NotImplementedError


# Used in the doctest examples for PriorityQueue
def _shorter(a: str, b: str) -> bool:
    """
    Return True if <a> is shorter than <b>.
    """
    return len(a) < len(b)


class PriorityQueue(Container):
    """A queue of items that operates in FIFO-priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first.  Ties are resolved in first-in-first-out
    (FIFO) order, meaning the item which was inserted *earlier* is the first one
    to be removed.

    Priority is defined by the <higher_priority> function that is provided at
    time of initialization.

    All objects in the container must be of the same type.

    === Private Attributes ===
    _queue:
      The end of the list represents the *front* of the queue, that is,
      the next item to be removed.
    _higher_priority:
      A function that compares two items by their priority.
      If <_higher_priority>(x, y) is true, then x has higher priority than y
      and should be removed from the queue before y.

    === Representation Invariants ===
    - all elements of <_queue> are of the same type.
    - the elements of <_queue> are appropriate arguments for the
      function <_higher_priority>.
    - the elements of <_queue> are in order according to the
      function <_higher_priority>.
    """
    _queue: List[Any]
    _higher_priority: Callable[[Any, Any], bool]

    def __init__(self, higher_priority: Callable[[Any, Any], bool]) -> None:
        """Initialize this to an empty PriorityQueue. For any two elements x
        and y of the queue, if <higher_priority>(x, y) is true, then x has
        higher priority than y.

        >>> pq = PriorityQueue(str.__lt__)
        >>> pq.is_empty()
        True
        """
        self._queue = []
        self._higher_priority = higher_priority

    def add(self, item: Any) -> None:
        """Add <item> to this PriorityQueue.

        >>> # Define a PriorityQueue with priority on shorter strings.
        >>> # I.e., when we remove, we get the shortest remaining string.
        >>> pq = PriorityQueue(_shorter)
        >>> pq.add('fred')
        >>> pq.add('arju')
        >>> pq.add('monalisa')
        >>> pq.add('hat')
        >>> # 'arju' and fred have the same priority, but 'arju' is behind
        >>> # 'fred' in the queue because it was added later.
        >>> pq._queue
        ['monalisa', 'arju', 'fred', 'hat']
        >>> pq.remove()
        'hat'
        >>> pq._queue
        ['monalisa', 'arju', 'fred']
        """
        index = 0
        valid = True
        if len(self._queue) == 0:
            self._queue.append(item)
        else:
            while valid and index < len(self._queue):
                if self._higher_priority(item, self._queue[index]):
                    index += 1
                else:
                    valid = False

            if valid:
                self._queue.append(item)
            else:
                self._queue.insert(index, item)

    def remove(self) -> Any:
        """Remove and return the next item from this PriorityQueue.

        Precondition: this priority queue is non-empty.

        >>> # When we hit the tie, the one that was added first will be
        >>> # removed first.
        >>> pq = PriorityQueue(_shorter)
        >>> pq.add('fred')
        >>> pq.add('arju')
        >>> pq.add('monalisa')
        >>> pq.add('hat')
        >>> pq.remove()
        'hat'
        >>> pq.remove()
        'fred'
        >>> pq.remove()
        'arju'
        >>> pq.remove()
        'monalisa'
        """
        return self._queue.pop()

    def is_empty(self) -> bool:
        """Return True iff this PriorityQueue is empty.

        >>> pq = PriorityQueue(str.__lt__)
        >>> pq.is_empty()
        True
        >>> pq.add('fred')
        >>> pq.is_empty()
        False
        """
        return not self._queue


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
