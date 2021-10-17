"""Assignment 1 - Parcel and Truck data generator (No tasks)

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

This module generates random parcel and truck data and writes each to a file.
Values defined in the module control the amount of data, the range of possible
values, etc.

You have no tasks associated with this module.  It is provided to you to assist
in testing.  However, your best test cases will likely be very small ones that
you hand-craft to force important conditions to arise.
"""

from random import randint, choice


def generate(parcel_filename: str = 'data/demo-parcel-data.txt',
             truck_filename: str = 'data/demo-truck-data.txt') -> None:
    """Generate random truck and parcel data, and save to the files
    <parcel_filename> and <truck_filename> respectively. File format is as
    defined in Assignment 1.
    """
    # Set constants controlling parcel data
    num_ids_to_pick_from = 20
    num_ids = 15
    cities = ['Belleville', 'Guelph', 'Hamilton', 'Toronto', 'London', 'Ottawa']
    min_volume = 5
    max_volume = 25

    depot = 'Toronto'

    # Generate some random parcels
    ids = list(range(num_ids_to_pick_from))
    with open(parcel_filename, 'w') as file:
        for dummy in range(num_ids):
            # Pick a random id from among those left and remove it so we
            # don't pick it again.
            id_ = choice(ids)
            ids.remove(id_)
            source = choice(cities)
            temp = cities.copy()
            temp.remove(source)
            if source != depot:
                temp.remove(depot)
            destination = choice(temp)
            volume = randint(min_volume, max_volume)
            file.write(f'{id_}, {source}, {destination}, {volume}\n')

    # Set constants controlling truck data
    num_ids_to_pick_from = 10
    num_ids = 5
    min_volume = 20
    max_volume = 50

    # Generate some random trucks
    ids = list(range(num_ids_to_pick_from))
    with open(truck_filename, 'w') as file:
        for dummy in range(num_ids):
            # Pick a random id from among those left and remove it so we
            # don't pick it again.
            id_ = choice(ids)
            ids.remove(id_)
            volume = randint(min_volume, max_volume)
            file.write(f'{id_}, {volume}\n')


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='.pylintrc')
    generate()
