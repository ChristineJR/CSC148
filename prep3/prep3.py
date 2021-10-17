"""Prep 3 Synthesize

=== CSC148 Winter 2021 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 David Liu

=== Module Description ===
This module contains an illustration of *inheritance* through an abstract
Employee class that defines a common interface for all of its subclasses.

As usual, delete the TODO comments after you've completed each part.

There is also a task inside prep3_starter_tests.py.
Make sure to look at that file and complete the TODO there as well.
"""
from datetime import date
from typing import List


################################################################################
# Part 1
# In this part of the prep, you will implement the total_pay method of the
# Employee class.
#
# You may add new PRIVATE instance attributes to the class if needed.
#
# Private instance attributes are attributes whose names start with _ and
# should not be accessed by code outside of the class.
#
# Document any new attributes in your class docstring, include type
# annotations for them, and make sure you initialize them properly.
#
# Do NOT modify the method headers.
#
# You may assume as a precondition that the pay method is not called on the
# same employee twice in the same month.
#
# Remember: 'precondition' here means that your implementation can assume this
# is true, and you do not need to check for it!
################################################################################
class Employee:
    """An employee of a company.

    This is an abstract class. Only child classes should be instantiated.

    === Public attributes ===
    id_: This employee's ID number.
    name: This employee's name.

    === Private attributes ===
    _accumulation: The total amount of pay this Employee has received.
    """
    id_: int
    name: str
    _accumulation: float

    def __init__(self, id_: int, name: str) -> None:
        """Initialize this employee.

        Note: This initializer is meant for internal use only;
        Employee is an abstract class and should not be instantiated directly.
        """
        self.id_ = id_
        self.name = name
        self._accumulation = 0.0

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.
        """
        raise NotImplementedError

    def pay(self, pay_date: date) -> None:
        """Pay this Employee on the given date and record the payment.

        (Assume this is called once per month.)
        """
        payment = self.get_monthly_payment()
        self._accumulation += payment
        print(f'An employee was paid {payment} on {pay_date}.')

    def total_pay(self) -> float:
        """Return the total amount of pay this Employee has received.

        >>> e = SalariedEmployee(14, 'Gilbert the cat', 1200.0)
        >>> e.pay(date(2018, 6, 28))
        An employee was paid 100.0 on 2018-06-28.
        >>> e.pay(date(2018, 7, 28))
        An employee was paid 100.0 on 2018-07-28.
        >>> e.pay(date(2018, 8, 28))
        An employee was paid 100.0 on 2018-08-28.
        >>> e.total_pay()
        300.0
        """
        return self._accumulation


class SalariedEmployee(Employee):
    """An employee whose pay is computed based on an annual salary.

    === Public attributes ===
    salary: This employee's annual salary

    === Representation invariants ===
    - salary >= 0
    """
    id_: int
    name: str
    salary: float

    def __init__(self, id_: int, name: str, salary: float) -> None:
        """Initialize this salaried Employee.

        Precondition: salary >= 0

        >>> e = SalariedEmployee(14, 'Fred Flintstone', 5200.0)
        >>> e.salary
        5200.0
        """
        # Note that to call the superclass' initializer, we need to use the
        # full name '__init__'. This is the only time we write '__init__'
        # explicitly.
        Employee.__init__(self, id_, name)
        self.salary = salary

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.

        >>> e = SalariedEmployee(99, 'Mr Slate', 120000.0)
        >>> e.get_monthly_payment()
        10000.0
        """
        return round(self.salary / 12, 2)


class HourlyEmployee(Employee):
    """An employee whose pay is computed based on an hourly rate.

    === Public attributes ===
    hourly_wage:
        This employee's hourly rate of pay.
    hours_per_month:
        The number of hours this employee works each month.

    === Representation invariants ===
    - hourly_wage >= 0
    - hours_per_month >= 0
    """
    id_: int
    name: str
    hourly_wage: float
    hours_per_month: float

    def __init__(self, id_: int, name: str, hourly_wage: float,
                 hours_per_month: float) -> None:
        """Initialize this HourlyEmployee.

        Precondition: hourly_wage >= 0 and hours_per_month >= 0
        >>> barney = HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0)
        >>> barney.hourly_wage
        1.25
        >>> barney.hours_per_month
        50.0
        """
        Employee.__init__(self, id_, name)
        self.hourly_wage = hourly_wage
        self.hours_per_month = hours_per_month

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.

        >>> e = HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0)
        >>> e.get_monthly_payment()
        62.5
        """
        return round(self.hours_per_month * self.hourly_wage, 2)


################################################################################
# Part 2
# In this part of the prep, you will be implementing the total_payroll method
# of the Company class.
#
# You should not need to add any additional attributes to the class in order
# to be able to write this method.
################################################################################
class Company:
    """A company with employees.

    We use this class mainly as a client for the various Employee classes
    we defined in employee.

    === Attributes ===
    employees: the employees in the company.
    """
    employees: List[Employee]

    def __init__(self, employees: List[Employee]) -> None:
        self.employees = employees

    def pay_all(self, pay_date: date) -> None:
        """Pay all employees at this company."""
        for employee in self.employees:
            employee.pay(pay_date)

    def total_payroll(self) -> float:
        """Return the total of all payments ever made to all employees.

        >>> my_corp = Company([\
        SalariedEmployee(24, 'Gilbert the cat', 1200.0), \
        HourlyEmployee(25, 'Chairman Meow', 500.25, 1.0)])
        >>> my_corp.pay_all(date(2018, 6, 28))
        An employee was paid 100.0 on 2018-06-28.
        An employee was paid 500.25 on 2018-06-28.
        >>> my_corp.total_payroll()
        600.25
        """
        total = 0
        for employee in self.employees:
            total += employee.total_pay()
        return total


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Remember: you'll need to *run this file* to actually get the lines below
    # to run. This is different than just running doctests.
    # To run this file in PyCharm, right-click in the file and select
    # "Run...", and then select "prep3" from the menu that appears.
    # DON'T select "Doctests in prep3", as that command will not actually
    # run this file, but instead only run its doctests.
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['datetime'],
        'allowed-io': ['pay']
    })
