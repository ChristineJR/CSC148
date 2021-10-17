"""CSC148 Prep 7:

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

=== Module description ===
Complete the TODO in this file.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here
"""
from prep7 import contains_non_satisfier


def _p(n: int) -> bool:
    """A helper function that return True if <n> is smaller than 10, and
    return False if <n> is larger than or equal to 10"""
    return n < 10


def test_contains_non_satisfier_int() -> None:
    """Test contains_non_satisfier on an int."""
    assert not contains_non_satisfier(5, _p)
    assert contains_non_satisfier(17, _p)


def test_contains_non_satisfier_empty_list() -> None:
    """Test contains_non_satisfier on an empty list."""
    assert not contains_non_satisfier([], _p)


def test_contains_non_satisfier_list_of_integers1() -> None:
    """Test contains_non_satisfier on a nested list containing only integers
    satisfied the function _p."""
    assert not contains_non_satisfier([0, 1, 2], _p)


def test_contains_non_satisfier_list_of_integers2() -> None:
    """Test contains_non_satisfier on a nested list containing only integers
    not satisfied the function _p."""
    assert contains_non_satisfier([11, 12, 13], _p)


def test_contains_non_satisfier_list_of_integers3() -> None:
    """Test contains_non_satisfier on a nested list containing only integers,
    some of them satisfied the function _p and some did not."""
    assert contains_non_satisfier([0, 1, 2, 11], _p)
    assert contains_non_satisfier([0, 1, 11, 2], _p)
    assert contains_non_satisfier([0, 11, 1, 2], _p)
    assert contains_non_satisfier([11, 0, 1, 2], _p)


def test_contains_non_satisfier_list() -> None:
    """Test contains_non_satisfier on a nested list containing both of integers
    and nested lists."""
    assert not contains_non_satisfier([0, 1, 2, []], _p)
    assert not contains_non_satisfier([0, 1, 2, [3, 4]], _p)
    assert contains_non_satisfier([0, 1, 2, [11, 3]], _p)
# While we have provided you a doctest in prep7.py, we will not be
# providing sample test cases this time. The tests you write should help you
# test your own code as well!


if __name__ == '__main__':
    import pytest
    pytest.main(['prep7_starter_tests.py'])
