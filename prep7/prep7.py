"""Prep 7 Synthesize

=== CSC148 Winter 2021 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Sophia Huynh

=== Module Description ===
Your task in this prep is to implement a recursive function on nested lists,
using the following steps for *Recursive Function Design*:

1.  Identify the recursive structure of the input (in this case, always a nested
    list), and write down the code template for nested lists:

    def f(obj: Union[int, List]) -> ...:
        if isinstance(obj, int):
            ...
        else:
            ...
            for sublist in obj:
                ... f(sublist) ...
            ...

2.  Implement the base case(s) directly (in this case, a single integer).
3.  Write down a concrete example with a somewhat complex argument, (in this
    case, a nested list with sub-nested-lists), and then write down
    the relevant recursive calls and what they should return.
4.  Determine how to combine the recursive calls to compute the correct output.
    Make sure you can express this in English first, and then implement your
    idea.

HINT: The implementations here should be similar to ones you've seen
before in the readings or comprehension questions.
"""
from typing import Union, Callable


# Note: The type annotation for predicate (Callable[[int], bool]) means that
#       predicate is a function that takes an int and returns a bool.
def contains_non_satisfier(obj: Union[int, list],
                           predicate: Callable[[int], bool]) -> bool:
    """Return whether obj contains at least one element that does *not*
    satisfy predicate.

    If obj is an int, returns True if obj does *not* satisfy predicate
    (i.e. predicate(obj) is False)

    >>> def p(n: int) -> bool:
    ...     return n < 10
    >>> contains_non_satisfier(5, p)
    False
    >>> contains_non_satisfier(15, p)
    True
    >>> contains_non_satisfier([5, 2, [15, 7], 9], p)
    True
    """
    if isinstance(obj, int):
        return not predicate(obj)
    else:
        for i in obj:
            if contains_non_satisfier(i, predicate):
                return True
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={'disable': ['E1136']})
