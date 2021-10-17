"""Assignment 1 - Tests

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

This module contains sample test cases that you can use to test your code.
These are a very incomplete set of test cases! We will be testing your code on
a much more thorough set of tests.

The self-test on MarkUs runs all of the tests below, along with a few others.
Make sure you run the self-test on MarkUs after submitting your code!

Once you have the entire program completed, that is, after Task 5, your
code should pass all of the tests we've provided.  As you develop your code,
test cases for parts that you haven't written yet will fail, of course.

But as you work through the earlier phases of the assignment, you can run the
individual tests below for each method as you complete it. We encourage you to
add further test cases in this file to improve your confidence in your code.

Tip: if you put your mouse inside a pytest function and right click, the "run"
menu will give you the option of running just that test function.
"""
import pytest
from typing import Dict
from distance_map import DistanceMap
from domain import Truck, Parcel, Fleet
from scheduler import GreedyScheduler
from container import PriorityQueue, _shorter
from experiment import SchedulingExperiment

# This variable is used in the special pytest test case defined by function
# test_experiment below.  The variable defines a single scheduling experiment
# test case to be run. It gives a unique identifier for the test case, and
# specifies both the configuration to use and the correct statistics to expect.
test_arguments = [
    ('1-small',
     {
         'depot_location': 'Toronto',
         'parcel_file': 'data/parcel-data-small.txt',
         'truck_file': 'data/truck-data-small.txt',
         'map_file': 'data/map-data.txt',
         'algorithm': 'greedy',
         'parcel_priority': 'volume',
         'parcel_order': 'non-decreasing',
         'truck_order': 'non-decreasing',
         'verbose': 'false'
     },
     {
         'fleet': 3,
         'unused_trucks': 0,
         'unused_space': 0,
         'avg_distance': 192.7,
         'avg_fullness': 100,
         'unscheduled': 0
     }),
    # You can add additional test cases here!
    # Write these in the format:
    # (<test_id>, <config dictionary>, <expected_stats dictionary>)
    # If you're adding multiple tests: remember to add a comma (,) after the
    # tuple!
]


def test_distance_map_basic() -> None:
    """Test DistanceMap when a single distance is provided."""
    m = DistanceMap()
    assert m.distance('Montreal', 'Toronto') == -1
    m.add_distance('Montreal', 'Toronto', 4)
    assert m.distance('Montreal', 'Toronto') == 4


def test_distance_map_repeated_adding() -> None:
    """Test that when DistanceMap.add_distance is called twice and the
    first two parameters are the same, the second time calling has no effect."""
    m_1 = DistanceMap()
    m_1.add_distance('Montreal', 'Toronto', 4)
    m_1.add_distance('Montreal', 'Toronto', 5)
    m_1.add_distance('Toronto', 'Montreal', 6, 7)
    assert m_1.distance('Montreal', 'Toronto') == 4
    assert m_1.distance('Toronto', 'Montreal') == 4


def test_add_distance_doctest() -> None:
    """Test the doctest provided for DistanceMap.add_distance"""
    m = DistanceMap()
    m.add_distance('Toronto', 'Hamilton', 9)
    assert m.distance('Toronto', 'Hamilton') == 9
    assert m.distance('Hamilton', 'Toronto') == 9

    m.add_distance('Toronto', 'York', 5, 6)
    assert m.distance('Toronto', 'York') == 5
    assert m.distance('York', 'Toronto') == 6


def test_num_trucks_doctest() -> None:
    """Test the doctest provided for Fleet.num_trucks"""
    f = Fleet()
    t1 = Truck(1423, 10, 'Toronto')
    f.add_truck(t1)
    assert f.num_trucks() == 1


def test_num_nonempty_trucks_doctest() -> None:
    """Test the doctest provided for Fleet.num_nonempty_trucks"""
    f = Fleet()

    t1 = Truck(1423, 10, 'Toronto')
    f.add_truck(t1)
    p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
    assert t1.pack(p1) is True

    p2 = Parcel(2, 4, 'Toronto', 'Montreal')
    assert t1.pack(p2) is True
    assert t1.fullness() == 90.0

    t2 = Truck(5912, 20, 'Toronto')
    f.add_truck(t2)
    p3 = Parcel(3, 2, 'New York', 'Windsor')
    assert t2.pack(p3) is True
    assert t2.fullness() == 10.0

    t3 = Truck(1111, 50, 'Toronto')
    f.add_truck(t3)
    assert f.num_nonempty_trucks() == 2


def test_parcel_allocations_doctest() -> None:
    """Test the doctest provided for Fleet.parcel_allocations"""
    f = Fleet()
    t1 = Truck(1423, 10, 'Toronto')
    p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
    p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
    assert t1.pack(p1) is True
    assert t1.pack(p2) is True
    t2 = Truck(1333, 10, 'Toronto')
    p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
    assert t2.pack(p3) is True
    f.add_truck(t1)
    f.add_truck(t2)
    assert f.parcel_allocations() == {1423: [27, 12], 1333: [28]}


def test_total_unused_space_doctest() -> None:
    """Test the doctest provided for Fleet.total_unused_space"""
    f = Fleet()
    assert f.total_unused_space() == 0

    t = Truck(1423, 1000, 'Toronto')
    p = Parcel(1, 5, 'Buffalo', 'Hamilton')
    assert t.pack(p) is True

    f.add_truck(t)
    assert f.total_unused_space() == 995


def test_average_fullness_doctest() -> None:
    """Test the doctest provided for Fleet.average_fullness"""
    f = Fleet()
    t = Truck(1423, 10, 'Toronto')
    p = Parcel(1, 5, 'Buffalo', 'Hamilton')
    assert t.pack(p) is True

    f.add_truck(t)
    assert f.average_fullness() == 50.0


def test_total_distance_travelled_doctest() -> None:
    """Test the doctest provided for Fleet.total_distance_travelled"""
    f = Fleet()
    t1 = Truck(1423, 10, 'Toronto')
    p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
    assert t1.pack(p1) is True

    t2 = Truck(1333, 10, 'Toronto')
    p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
    assert t2.pack(p2) is True

    m = DistanceMap()
    m.add_distance('Toronto', 'Hamilton', 9)
    f.add_truck(t1)
    f.add_truck(t2)
    assert f.total_distance_travelled(m) == 36


def test_average_distance_travelled_doctest() -> None:
    """Test the doctest provided for Fleet.average_distance_travelled"""
    f = Fleet()
    t1 = Truck(1423, 10, 'Toronto')
    p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
    assert t1.pack(p1) is True

    t2 = Truck(1333, 10, 'Toronto')
    p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
    assert t2.pack(p2) is True

    m = DistanceMap()
    m.add_distance('Toronto', 'Hamilton', 9)
    f.add_truck(t1)
    f.add_truck(t2)
    assert f.average_distance_travelled(m) == 18.0


def test_priority_queue_is_empty_doctest() -> None:
    """Test the doctest provided for PriorityQueue.is_empty"""
    pq = PriorityQueue(str.__lt__)
    assert pq.is_empty() is True

    pq.add('fred')
    assert pq.is_empty() is False


def test_priority_queue_add_remove_doctest() -> None:
    """Test the doctest provided for PriorityQueue.add and
    PriorityQueue.remove"""
    pq = PriorityQueue(_shorter)
    pq.add('fred')
    pq.add('arju')
    pq.add('monalisa')
    pq.add('hat')
    assert pq.remove() == 'hat'
    assert pq.remove() == 'fred'
    assert pq.remove() == 'arju'
    assert pq.remove() == 'monalisa'


def test_greedy_scheduler_example() -> None:
    """Test GreedyScheduler on the example provided."""
    p17 = Parcel(17, 25, 'York', 'Toronto')
    p21 = Parcel(21, 10, 'York', 'London')
    p13 = Parcel(13, 8, 'York', 'London')
    p42 = Parcel(42, 20, 'York', 'Toronto')
    p25 = Parcel(25, 15, 'York', 'Toronto')
    p61 = Parcel(61, 15, 'York', 'Hamilton')
    p76 = Parcel(76, 20, 'York', 'London')

    t1 = Truck(1, 40, 'York')
    t2 = Truck(2, 40, 'York')
    t3 = Truck(3, 25, 'York')

    f = Fleet()
    f.add_truck(t1)
    f.add_truck(t2)
    f.add_truck(t3)

    # We've left parcel_file, truck_file, and map_file empty in the config
    # dictionary below because you should *not* use these in your
    # GreedyScheduler. It is not responsible for reading data from these files.
    config = {'depot_location': 'York',
              'parcel_file': '',
              'truck_file': '',
              'map_file': '',
              'algorithm': 'greedy',
              'parcel_priority': 'destination',
              'parcel_order': 'non-increasing',
              'truck_order': 'non-increasing',
              'verbose': 'false'}

    scheduler = GreedyScheduler(config)
    unscheduled = scheduler.schedule([p17, p21, p13, p42, p25, p61, p76],
                                     [t1, t2, t3])

    assert unscheduled == [p76]

    truck_parcels = f.parcel_allocations()
    assert truck_parcels[1] == [17, 61]
    assert truck_parcels[2] == [42, 25]
    assert truck_parcels[3] == [21, 13]


################################################################################
# The test below uses pytest.mark.parametrize.
#
# This provides a way of running the same test code with different parameters
# without having to repeat the body multiple times.
#
# The line above the test_experiment method works as follows:
# @pytest.mark.parametrize('test_id, config, expected_stats', test_arguments)
#                           ^                                 ^
#                    These are the parameters        This is a list where each
#                    of test_experiment that         element is a tuple
#                    we're filling.                  containing values for those
#                                                    parameters.
#
# test_arguments is the variable defined near the top of this module.
#
# We have included one item in test_arguments for you. This is a tuple
# representing the following parameter configurations:
#     test_id        = '1-small'
#     config         = {'depot_location': 'Toronto', ...}
#     expected_stats = {'fleet': 3, ...}
#
# If you want to add additional test cases, you create a tuple with the same
# format and add it to the list.
#
# For more details, see:
# https://docs.pytest.org/en/stable/parametrize.html
#
# NOTE: if you get a "FileNotFoundError", try replacing the filename
# with the full path to the file (e.g., "C:\\Users\\David\\Documents\\...")
################################################################################
@pytest.mark.parametrize('stat', [
    'fleet', 'unused_trucks', 'unused_space', 'avg_distance', 'avg_fullness',
    'unscheduled'])
class TestExperiment:
    """
    Tests for SchedulingExperiment.run
    """
    @pytest.mark.parametrize('test_id, config, expected_stats', test_arguments)
    def test_experiment(self, test_id: str, config: Dict[str, str],
                        expected_stats: Dict[str, str], stat: str) -> None:
        """Run the SchedulingExperiment on the given config and expected_stats.
        Assert that the stat returned from the experiment matches
        expected_stats[stat].
        """
        experiment = SchedulingExperiment(config)
        results = experiment.run()

        # pytest.approx lets us use approximate values so we can avoid
        # failing a test case over very small differences in floating point
        # values. These can arise simply from doing mathematical operations in
        # a different order. [If you find this intriguing, take csc336!]

        # In this case, we're making sure our actual value is in the range
        # (expected - 1e-1, expected + 1e-1)
        expected = expected_stats[stat]
        actual = results[stat]
        assert actual == pytest.approx(expected, abs=1e-1)


if __name__ == '__main__':
    pytest.main(['a1_starter_tests.py'])
