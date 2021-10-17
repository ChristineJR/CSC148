"""Assignment 1 - Compare all algorithms on a single problem (No tasks)

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

This module reads from a json file (whose name is hard-coded in the
compare_algorithms block) to determine the parcel, truck and map files to use.
It then constructs all nine possible algorithm configurations, and runs each
on this same data.  Results are printed to a csv file called 'results.csv'.

You have no tasks associated with this module.  It is provided to you so that
you can compare the performance of the algorithms and notice any patterns or
conclusions you might draw.  You may also find that reviewing the comparison
reveals bugs in your code.
"""
from typing import TextIO, Dict, Union
import json
from experiment import SchedulingExperiment


def print_table_title(file: TextIO) -> None:
    """Print the title row of a results table in csv format to <file>.
    """
    file.write('Algorithm,Parcel Priority,Parcel Order  ,Truck Order   ,'
               + 'Unused Trucks,Unused Space,Avg dist,Avg fullness,'
               + 'Unsched Parcels\n')


def print_table_row(config: Dict[str, Union[str, bool]],
                    stats: Dict[str, Union[int, float]], file: TextIO) -> None:
    """Print one row of a results table, in csv format.

    <config> is the configuration that was used.
    <stats> is the stats that resulted.
    <file> is the file to write to.
    """
    file.write(f'{config["algorithm"]:<9},'
               f'{config["parcel_priority"]:<15},'
               f'{config["parcel_order"]:<14},'
               f'{config["truck_order"]:<14},'
               f'{stats["unused_trucks"]:<13},'
               f'{stats["unused_space"]:<12},'
               f'{stats["avg_distance"]:<8.2f},'
               f'{stats["avg_fullness"]:<12.2f},'
               f'{stats["unscheduled"]}\n')


def compare_algorithms(config_file: str) -> None:
    """Compare all algorithms on a single problem.

    Run the random algorithm and every configuration of the greedy
    algorithm on the scheduling problem defined in <config_file>.

    Precondition: <config_file> a path to a json file with keys and values
    as in the dictionary format defined in Assignment 1.
    """
    with open(config_file, 'r') as file:
        basic_config = json.load(file)

    # We will use the keys 'parcel_file', 'fleet_file' and 'map_file' from
    # the dict <basic_config>.
    # If it has any other keys, we will ignore them.  Instead of taking the
    # algorithm configuration from a file, we try all possible configurations.

    # List of possible configurations for the scheduling algorithm.
    algorithm_configurations = [
        # --- Random
        {'algorithm': 'random',
         'parcel_priority': 'NA',
         'parcel_order': 'NA',
         'truck_order': 'NA'},
        # --- Greedy by volume, with 4 sub-configurations
        {'algorithm': 'greedy',
         'parcel_priority': 'volume',
         'parcel_order': 'non-decreasing',
         'truck_order': 'non-decreasing'},
        {'algorithm': 'greedy',
         'parcel_priority': 'volume',
         'parcel_order': 'non-decreasing',
         'truck_order': 'non-increasing'},
        {'algorithm': 'greedy',
         'parcel_priority': 'volume',
         'parcel_order': 'non-increasing',
         'truck_order': 'non-decreasing'},
        {'algorithm': 'greedy',
         'parcel_priority': 'volume',
         'parcel_order': 'non-increasing',
         'truck_order': 'non-increasing'},
        # --- Greedy by destination, with 4 sub-configurations
        {'algorithm': 'greedy',
         'parcel_priority': 'destination',
         'parcel_order': 'non-decreasing',
         'truck_order': 'non-decreasing'},
        {'algorithm': 'greedy',
         'parcel_priority': 'destination',
         'parcel_order': 'non-decreasing',
         'truck_order': 'non-increasing'},
        {'algorithm': 'greedy',
         'parcel_priority': 'destination',
         'parcel_order': 'non-increasing',
         'truck_order': 'non-decreasing'},
        {'algorithm': 'greedy',
         'parcel_priority': 'destination',
         'parcel_order': 'non-increasing',
         'truck_order': 'non-increasing'}
    ]

    with open('data/results.csv', 'w') as file:
        print_table_title(file)
        for item in algorithm_configurations:
            # Start with the basic configuration <config>, and add the
            # algorithm details from this item in our list of configurations.
            config = basic_config.copy()
            config.update(item)
            # Run an experiment on this configuration and print the results
            # to our csv file.
            expt = SchedulingExperiment(config)
            results = expt.run(report=False)
            print_table_row(config, results, file)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'json', 'experiment'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    # ------------------------------------------------------------------------
    # The following code can be used to explore how the different scheduling
    # algorithms compare on one example configuration.  It creates a report
    # in file 'data/results.csv'.
    # ------------------------------------------------------------------------
    compare_algorithms('data/demo.json')
