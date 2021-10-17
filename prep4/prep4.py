"""Prep 4 Synthesize

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains four functions for you to implement, where each
operates on either a stack or a queue.

We've provided deliberately confusing implementations of these ADTs in
adts.py. This is because we don't want you to care at all about the
implementations of these classes, but instead ONLY use the public methods
defined in by the Stack or Queue ADTs. These are the following:
    Stack
        - is_empty()
        - push()
        - pop()
    Queue
        - is_empty()
        - enqueue()
        - dequeue()

In particular, this means that you shouldn't try to access any attributes
of either class, since the ADT descriptions only define what *operations*
(methods) can be used for the ADTs.

GENERAL HINT: save values in local variables! Even if you pop an item off of
a stack, it's not "gone forever" if you assign it to a variable.
"""
from typing import Any, Optional
from adts import Stack, Queue


################################################################################
# Part 1
# In this part of the prep, you will various Stack and Queue functions.
#
# You must NOT access any attributes of the Stack/Queues passed into each
# function.
#
# You may ONLY use the is_empty(), push(), and pop() methods of Stack, and
# the is_empty(), enqueue(), and dequeue() methods of Queue.
################################################################################
def peek(stack: Stack) -> Optional[Any]:
    """Return the top item on the given stack.

    If the stack is empty, return None.

    Unlike Stack.pop, this function should leave the stack unchanged when the
    function ends. You can (and should) still call pop and push, just make
    sure that if you take any items off the stack, you put them back on!

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> peek(stack)
    2
    >>> stack.pop()
    2
    """
    if stack.is_empty():
        return None
    else:
        a = stack.pop()
        stack.push(a)
        return a


def reverse_top_two(stack: Stack) -> None:
    """Reverse the top two elements on <stack>.

    Precondition: <stack> has at least two items.

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> reverse_top_two(stack)
    >>> stack.pop()
    1
    >>> stack.pop()
    2
    >>> stack.is_empty()
    True
    """
    a = stack.pop()
    b = stack.pop()
    stack.push(a)
    stack.push(b)


def remove_all(queue: Queue) -> None:
    """Remove all items from the given queue.

    >>> queue = Queue()
    >>> queue.enqueue(1)
    >>> queue.enqueue(2)
    >>> queue.enqueue(3)
    >>> remove_all(queue)
    >>> queue.is_empty()
    True
    """
    while not queue.is_empty():
        queue.dequeue()


def remove_all_but_one(queue: Queue) -> None:
    """Remove all items from the given queue except the last one.

    Precondition: <queue> contains at least one item.
                  or: not queue.is_empty()

    >>> queue = Queue()
    >>> queue.enqueue(1)
    >>> queue.enqueue(2)
    >>> queue.enqueue(3)
    >>> remove_all_but_one(queue)
    >>> queue.is_empty()
    False
    >>> queue.dequeue()
    3
    >>> queue.is_empty()
    True
    """
    lst = []
    while not queue.is_empty():
        lst.append(queue.dequeue())
    queue.enqueue(lst[-1])


################################################################################
# Part 2
# In Part 2 of the prep, we have given you the buggy function add_in_order().
# While the documentation of this function is correct, the implementation is
# not.
#
# In prep4_starter_tests.py, you must write a test case that will fail this
# buggy implementation, but pass on a working version of add_in_order().
#
# You are not required to fix the bug, although you may do so if you'd like.
################################################################################
def add_in_order(stack: Stack, lst: list) -> None:
    """
    Add all items in <lst> to <stack>, so that when items are removed from
    <stack>, they are returned in <lst> order.

    Precondition: stack.is_empty() is True

    >>> stack = Stack()
    >>> lst = [1, 1]
    >>> add_in_order(stack, lst)
    >>> results = []
    >>> results.append(stack.pop())
    >>> results.append(stack.pop())
    >>> lst == results
    True
    >>> stack.is_empty()
    True
    """
    for item in lst[::-1]:
        stack.push(item)


if __name__ == '__main__':
    # Uncomment the lines below to run the doctests in this file.
    # import doctest
    # doctest.testmod()

    # Remember, to get this to work you need to Run this file, not just the
    # doctests in this file!
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['adts'],
        'disable': ['E1136']
    })
