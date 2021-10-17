"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Dict, Union, Callable
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """A scheduler that go through the parcels and trucks in random order.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks> in random order.
        That is, for each parcel, it will schedule it onto a randomly chosen
        truck (from among those trucks that have capacity to add that parcel).
        >>> s = RandomScheduler()
        >>> p1 = Parcel(1, 10, 'York', 'Toronto')
        >>> p2 = Parcel(2, 20, 'York', 'London')
        >>> p3 = Parcel(3, 10, 'York', 'London')
        >>> p4 = Parcel(4, 50, 'York', 'Toronto')
        >>> p5 = Parcel(5, 50, 'York', 'Toronto')
        >>> p6 = Parcel(6, 50, 'York', 'Hamilton')
        >>> p7 = Parcel(7, 50, 'York', 'London')
        >>> p_lst = [p1, p2, p3, p4, p5, p6, p7]
        >>> t = Truck(1, 40, 'York')
        >>> t_lst = [t]
        >>> result = s.schedule(p_lst, t_lst)
        >>> len(result)
        4
        """
        lst1 = []
        lst1 += parcels
        lst2 = []
        lst2 += parcels
        shuffle(lst1)
        sentence = ''
        for _ in range(0, len(lst1)):
            valid_space = []
            package = choice(lst1)
            for i in trucks:
                if package.volume <= i.ava_space:
                    valid_space.append(i)
            shuffle(valid_space)
            if valid_space:
                go = choice(valid_space)
                go.pack(package)
                sentence += f'Parcel {package.p_id} is placed on ' \
                            f'Truck {go.t_id}.\n'
                lst2.remove(package)
            else:
                sentence += f'Parcel {package.p_id} cannot be placed on any ' \
                            f'truck.\n'
            lst1.remove(package)
        if verbose:
            print(sentence)
        return lst2


class GreedyScheduler(Scheduler):
    """ A scheduler that processes parcels one at a time,
    picking a truck for each, but it tries to pick the “best” truck
    it can for each parcel.

    ===== Private Attributes =====
    _higher_priority: A function that determines the priority for parcels when
    processing it.
    _truck_priority: A function that determines the priority for trucks when
    choosing it.
    """
    _higher_priority: Callable[[Union[Parcel, Truck], Union[Parcel, Truck]],
                               bool]
    _truck_priority: Callable[[Parcel, Parcel], bool]

    def __init__(self, config: Dict[str, str]) -> None:
        """ Initialize the GreedyScheduler with the priority, parcel order,
        and truck order.
        """
        priority = config['parcel_priority']
        p_order = config['parcel_order']
        t_order = config['truck_order']
        if priority == 'volume':
            if p_order == 'non-increasing':
                self._higher_priority = _non_increasing
            else:
                self._higher_priority = _non_decreasing
        else:
            if p_order == 'non-increasing':
                self._higher_priority = _destination_non_increasing
            else:
                self._higher_priority = _destination_non_decreasing
        if t_order == 'non-increasing':
            self._truck_priority = _non_increasing
        else:
            self._truck_priority = _non_decreasing

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.
        """
        result = []
        word = ''
        pq = PriorityQueue(self._higher_priority)
        for p in parcels:
            pq.add(p)
        while not pq.is_empty():
            item = pq.remove()
            lst = []
            for t in trucks:
                if t.ava_space >= item.volume:
                    lst.append(t)
            if not lst:
                result.append(item)
                word += f'Parcel {item.p_id} cannot be placed on any truck.\n'
            else:
                lst = _choose_same_destination(lst, item)
                t_pq = PriorityQueue(self._truck_priority)
                for k in lst:
                    t_pq.add(k)
                truck = t_pq.remove()
                truck.pack(item)
                word += f'Parcel {item.p_id} is placed on truck {truck.t_id}.\n'
        if verbose:
            print(word)
        return result


def _non_increasing(a: Union[Parcel, Truck], b: Union[Parcel, Truck]) -> bool:
    """Return True if <a> has larger volume than what <b> has.

    Precondition: <a> and <b> are of the same type.

    >>> p1 = Parcel(27, 10, 'Toronto', 'Hamilton')
    >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
    >>> _non_increasing(p1, p2)
    True
    >>> t1 = Truck(1423, 10, 'Toronto')
    >>> t2 = Truck(5912, 20, 'Toronto')
    >>> _non_increasing(t1, t2)
    False
    """
    try:
        return a.volume > b.volume
    except AttributeError:
        return a.ava_space > b.ava_space


def _non_decreasing(a: Union[Parcel, Truck], b: Union[Parcel, Truck]) -> bool:
    """Return True if <a> has larger volume than what <b> has.

    Precondition: <a> and <b> are of the same type.

    >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
    >>> p2 = Parcel(12, 10, 'Toronto', 'Hamilton')
    >>> _non_decreasing(p1, p2)
    True
    >>> t1 = Truck(1423, 20, 'Toronto')
    >>> t2 = Truck(5912, 10, 'Toronto')
    >>> _non_decreasing(t1, t2)
    False
    """
    try:
        return a.volume < b.volume
    except AttributeError:
        return a.ava_space < b.ava_space


def _destination_non_increasing(a: Parcel, b: Parcel) -> bool:
    """Return True if a is bigger than b

    >>> p1 = Parcel(2, 3, 'York', 'London')
    >>> p2 = Parcel(44, 3, 'London', 'Toronto')
    >>> _destination_non_increasing(p2, p1)
    True
    """
    return a.destination > b.destination


def _destination_non_decreasing(a: Parcel, b: Parcel) -> bool:
    """Return True if a is smaller than b

    >>> p1 = Parcel(2, 3, 'York', 'London')
    >>> p2 = Parcel(44, 3, 'London', 'Toronto')
    >>> _destination_non_decreasing(p1, p2)
    True
    """
    return a.destination < b.destination


def _choose_same_destination(lst: List[Truck], p: Parcel) -> List[Truck]:
    """Given a list of Trucks <lst> and a Parcel <p>. Among these trucks,
    if there are any that already have the parcel’s destination at the end
    of their route, only those trucks are considered. Otherwise, all trucks
    that have enough unused volume are considered.

    Return a list of Trucks that are considered.

    >>> t1 = Truck(111, 30, 'Toronto')
    >>> t2 = Truck(321, 20, 'Toronto')
    >>> t3 = Truck(4, 78, 'York')
    >>> lst1 = [t1, t2, t3]
    >>> p1 = Parcel(23, 2, 'Toronto', 'London')
    >>> p2 = Parcel(34, 8, 'Toronto', 'London')
    >>> result1 = _choose_same_destination(lst1, p1)
    >>> len(result1)
    3
    >>> t1.pack(p1)
    True
    >>> result2 = _choose_same_destination(lst1, p2)
    >>> len(result2)
    1
    """
    result = []
    for i in lst:
        if len(i.route) != 1 and i.route[-2] == p.destination:
            result.append(i)
    if not result:
        result = lst
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
