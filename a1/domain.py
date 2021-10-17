"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """ A parcel that will be delivered.

    ===== Public Attributes =====
    p_id:
        An integer which is the unique ID for this parcel.
    volume:
        A positive integer, which is the volume of this parcel, measured in
        units of cubic centimetres (cc).
    source:
        A string which is the name of the city the parcel came from.
    destination:
        A string which is the name of the city where it must be delivered to.

    === Representation Invariants ===
    - volume is a positive integer

    === Sample Usage ===
    >>> p = Parcel(2, 3, 'Toronto', 'London')
    >>> p.p_id
    2
    >>> p.volume
    3
    >>> p.source
    'Toronto'
    >>> p.destination
    'London'
    """
    p_id: int
    volume: int
    source: str
    destination: str

    def __init__(self, id1: int, vol: int,
                 source: str, destination: str) -> None:
        """ Initialize the parcel with its ID number, volume, source, and
        destination.

        Precondition: vol > 0

        >>> p = Parcel(33, 50, 'Toronto', 'London')
        >>> p.volume
        50
        >>> p.destination
        'London'
        """
        self.p_id = id1
        self.volume = vol
        self.source = source
        self.destination = destination

    def __str__(self) -> str:
        """Return a string representing this Parcel.

        >>> p = Parcel(2, 3, 'Toronto', 'London')
        >>> print(p)
        Parcel 2: Volume: 3, Source: Toronto, Destination: London
        """
        return "Parcel {}: Volume: {}, " \
               "Source: {}, Destination: {}".format(self.p_id,
                                                    self.volume,
                                                    self.source,
                                                    self.destination)


class Truck:
    """ A truck that will be used in delivering.

    ===== Public Attributes =====
    lst_parcel:
        A list of Parcels that are contained in this truck.
    route:
        A list of strings which are names of all places that this truck
        need to travel through, starting with its depot and ending with
        its depot.
    vol_capacity:
        A positive integer, which is the volume capacity of this truck,
        measured in units of cubic centimetres (cc).
    ava_space:
        A positive integer, which is the available space of this truck,
        measured in units of cubic centimetres (cc).
    t_id:
        An integer which is the unique ID for this truck.

    === Representation Invariants ===
    - route[0] is the depot city of the truck, and it is not the same as
    the parcel's destination
    - vol_capacity > 0
    - ava_space > 0

     === Sample Usage ===
     >>> t = Truck(2, 50, 'Toronto')
     >>> p = Parcel(44, 20, 'Toronto', 'London')
     >>> t.pack(p)
     True
     >>> t.fullness()
     40.0
    """
    lst_parcel: List[Parcel]
    route: List[str]
    vol_capacity: int
    ava_space: int
    t_id: int

    def __init__(self, id1: int, vol: int, depot: str) -> None:
        """Initialize the truck with its ID number, capacity, and depot city.

        Precondition: vol > 0

        >>> t = Truck(2, 50, 'Toronto')
        >>> t.vol_capacity
        50
        >>> t.t_id
        2
        """
        self.t_id = id1
        self.vol_capacity = vol
        self.ava_space = vol
        self.lst_parcel = []
        self.route = [depot]

    def __str__(self) -> str:
        """Return a string representing this Truck.

        >>> t = Truck(2, 50, 'Toronto')
        >>> p = Parcel(44, 23, 'Toronto', 'London')
        >>> t.pack(p)
        True
        >>> print(t)
        Truck 2:
        Total capacity: 50 Available space: 27
        Route: Toronto -> London -> Toronto
        Containing:
        Parcel 44: Volume: 23, Source: Toronto, Destination: London
        """
        result1 = ''
        result2 = ''
        for location in self.route:
            result1 += location + ' -> '
        result1 = result1[0:-4]

        if not self.lst_parcel:
            result2 = 'N/A'
        else:
            n = 0
            for item in self.lst_parcel:
                result2 += f'{item}'
                n += 1
                if n < len(self.lst_parcel):
                    result2 += '\n'

        return f'Truck {self.t_id}:\nTotal capacity: {self.vol_capacity} ' \
               f'Available space: {self.ava_space}\nRoute: {result1}\n' \
               f'Containing:\n{result2}'

    def pack(self, item: Parcel) -> bool:
        """Place <item> on this Truck. Return True if there is enough volume
        capacity, or return False if this action fails.

        Precondition: No parcel with the same ID as <item> has already been
        added to this Truck.

        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 10, 'Buffalo', 'Hamilton')
        >>> t1.pack(p2)
        False
        """
        if self.ava_space - item.volume < 0:
            return False
        if not self.lst_parcel:
            self.route.append(self.route[0])
        self.lst_parcel.append(item)
        if item.destination != self.route[-2]:
            self.route.insert(-1, item.destination)
        self.ava_space -= item.volume
        return True

    def fullness(self) -> float:
        """Return the fullness of this Truck. The fullness of a truck is the
        percentage of its volume that is taken by parcels.

        >>> t = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t.pack(p2)
        True
        >>> t.fullness()
        90.0
        """
        return (self.vol_capacity - self.ava_space) / self.vol_capacity * 100

    def route_distance(self, dmap: DistanceMap) -> int:
        """Return the total distance of the route for this Truck, computed
        with the distance recorded in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      distance of the route.

        >>> t = Truck(123, 30, 'Toronto')
        >>> p = Parcel(2, 2, 'Toronto', 'London')
        >>> d = DistanceMap()
        >>> d.add_distance('Toronto', 'London', 3)
        >>> t.route_distance(d)
        0
        >>> t.pack(p)
        True
        >>> t.route_distance(d)
        6
        """
        n = 0
        if len(self.route) > 2:
            count = 0
            while count < len(self.route) - 1:
                n += dmap.distance(self.route[count], self.route[count + 1])
                count += 1
        return n


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet

        >>> f = Fleet()
        >>> t1 = Truck(2, 50, 'Toronto')
        >>> p1 = Parcel(44, 23, 'Toronto', 'London')
        >>> t1.pack(p1)
        True
        >>> f.add_truck(t1)
        >>> print(f)
        The fleet contains the following trucks:
        Truck 2:
        Total capacity: 50 Available space: 27
        Route: Toronto -> London -> Toronto
        Containing:
        Parcel 44: Volume: 23, Source: Toronto, Destination: London
        """
        result = ''
        n = 0
        for t in self.trucks:
            result += f'{t}'
            n += 1
            if n < len(self.trucks):
                result += '\n'
        if n == 0:
            result = 'The fleet contains no trucks.'
        else:
            result = 'The fleet contains the following trucks:\n' + result
        return result

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        lst = self._used_trucks()
        return len(lst)

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        result = {}
        for i in self.trucks:
            t_id = i.t_id
            pid = []
            for x in i.lst_parcel:
                pid.append(x.p_id)
            result[t_id] = pid
        return result

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        n = 0
        lst = self._used_trucks()
        for i in lst:
            n += i.ava_space
        return n

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        n = 0
        lst = self._used_trucks()
        for i in lst:
            n += i.fullness()
        return n

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        return self._total_fullness() / len(self._used_trucks())

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        lst1 = self._used_trucks()
        lst2 = []
        for i in lst1:
            if i.route_distance(dmap) != 0:
                lst2.append(i.route_distance(dmap))
        return sum(lst2)

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        lst1 = self._used_trucks()
        lst2 = []
        for i in lst1:
            if i.route_distance(dmap) != 0:
                lst2.append(i.route_distance(dmap))
        return sum(lst2) / len(lst2)

    def _used_trucks(self) -> List[Truck]:
        """Return a list of Trucks that are non-empty in this Fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> result = f._used_trucks()
        >>> result[0].t_id
        1423
        """
        lst = []
        for t in self.trucks:
            if t.ava_space != t.vol_capacity:
                lst.append(t)
        return lst


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
