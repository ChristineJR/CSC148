"""
Assignment 0 - Sample tests

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.
"""
import pytest
from datetime import date
from weather import DailyWeather, HistoricalWeather, Country, load_data, \
                    load_country


################################################################################
# Sample test cases below
#
# Use the test cases below as an example for writing your own test cases,
# and as a start to testing your A0 code. Most of these test functions create
# objects "by hand" that are used for testing methods.  Once you implement
# function load_data, you will be able to create an HistoricalWeather object
# by calling load_data, or a Country object by calling load_country. You may
# find this makes testing easier.
#
# The self-test on MarkUs runs the tests below, along with a few others.
# Make sure you run the self-test on MarkUs after submitting your code!
#
# You do not have to submit this file for A0. This is for your own use.
#
# WARNING: THIS IS CURRENTLY AN EXTREMELY INCOMPLETE SET OF TESTS!
# We will test your code on a much more thorough set of tests!
################################################################################
def test_daily_weather_init():
    """Test that we initialize the day's weather correctly."""
    weather = DailyWeather((13.1, 9.2, 20.3), (5, 0, 1))

    assert weather.avg_temp == 13.1
    assert weather.low_temp == 9.2
    assert weather.high_temp == 20.3
    assert weather.precipitation == 5
    assert weather.rainfall == 0
    assert weather.snowfall == 1


def test_historical_weather_init():
    """Test that we initialize the historical weather correctly."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    assert historical.name == 'City Name'
    assert historical.coordinates == (-1.234, 4.567)


def test_add_weather_repeated_date():
    """Test that if a record for date d already exists, the information that
    is already recorded won't be changed."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    daily1 = DailyWeather((1, 2, 3), (4, 2, 2))
    daily2 = DailyWeather((3, 2, 1), (2, 2, 4))
    record_date = date(2020, 1, 12)
    historical.add_weather(record_date, daily1)
    historical.add_weather(record_date, daily2)

    assert historical.retrieve_weather(record_date) == daily1
    assert historical.retrieve_weather(record_date) != daily2


def test_retrieve_weather_none():
    """Test that it will return None if we retrieve a single weather
    record that is not in HistoricalWeather."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    daily = DailyWeather((1, 2, 3), (4, 2, 2))
    record_date1 = date(2020, 1, 12)
    record_date2 = date(2020, 1, 13)

    assert historical.retrieve_weather(record_date1) is None
    assert historical.retrieve_weather(record_date2) is None

    historical.add_weather(record_date1, daily)

    assert historical.retrieve_weather(record_date2) is None


def test_add_and_retrieve_weather():
    """Test that we can add and retrieve a single weather record from
    HistoricalWeather."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    daily = DailyWeather((1, 2, 3), (4, 2, 2))
    record_date = date(2020, 1, 12)
    historical.add_weather(record_date, daily)

    assert historical.retrieve_weather(record_date) is daily, \
        "Calling retrieve_weather() on a date should return the " + \
        "DailyWeather object that was added to that date."


def test_record_high():
    """Test record_high on a HistoricalWeather with two points of data, where
    the record high is at the earlier year."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(date(2012, 6, 4),
                           DailyWeather((0, 0, 20), (0, 0, 0)))

    historical.add_weather(date(2010, 6, 4),
                           DailyWeather((0, 0, 30), (0, 0, 0)))

    assert historical.record_high(6, 4) == 30


def test_record_high_different_days_and_months():
    """Test record_high on several HistoricalWeather with two points of data
    each, where the records in the same HistoricalWeather are with different
    days or months or both."""
    historical1 = HistoricalWeather("City Name", (-1.234, 4.567))
    historical1.add_weather(date(2012, 6, 4),
                            DailyWeather((0, 0, 20), (0, 0, 0)))
    historical1.add_weather(date(2012, 6, 5),
                            DailyWeather((0, 0, 30), (0, 0, 0)))

    assert historical1.record_high(6, 4) == 20
    assert historical1.record_high(6, 5) == 30

    historical2 = HistoricalWeather("City Name", (-1.234, 4.567))
    historical2.add_weather(date(2012, 6, 4),
                            DailyWeather((0, 0, 10), (0, 0, 0)))
    historical2.add_weather(date(2012, 7, 4),
                            DailyWeather((0, 0, 15), (0, 0, 0)))

    assert historical2.record_high(6, 4) == 10
    assert historical2.record_high(7, 4) == 15

    historical3 = HistoricalWeather("City Name", (-1.234, 4.567))
    historical3.add_weather(date(2012, 6, 4),
                            DailyWeather((0, 0, 0), (0, 0, 0)))
    historical3.add_weather(date(2012, 7, 5),
                            DailyWeather((0, 0, 1), (0, 0, 0)))

    assert historical3.record_high(6, 4) == 0
    assert historical3.record_high(7, 5) == 1


def test_monthly_average():
    """Test monthly_average on a HistoricalWeather that has one point of data
    per month, all within a single year."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(date(2012, 1, 8),
                           DailyWeather((-0.25, -1.75, 0.25), (0, 0, 0)))

    historical.add_weather(date(2012, 2, 9),
                           DailyWeather((0.0, -3.0, 1.0), (0, 0, 0)))

    historical.add_weather(date(2012, 3, 10),
                           DailyWeather((0.75, -3.75, 2.25), (0, 0, 0)))

    historical.add_weather(date(2012, 4, 11),
                           DailyWeather((2.0, -4.0, 4.0), (0, 0, 0)))

    historical.add_weather(date(2012, 5, 12),
                           DailyWeather((3.75, -3.75, 6.25), (0, 0, 0)))

    historical.add_weather(date(2012, 6, 13),
                           DailyWeather((6.0, -3.0, 9.0), (0, 0, 0)))

    historical.add_weather(date(2012, 7, 14),
                           DailyWeather((8.75, -1.75, 12.25), (0, 0, 0)))

    historical.add_weather(date(2012, 8, 15),
                           DailyWeather((12.0, 0.0, 16.0), (0, 0, 0)))

    historical.add_weather(date(2012, 9, 16),
                           DailyWeather((15.75, 2.25, 20.25), (0, 0, 0)))

    historical.add_weather(date(2012, 10, 17),
                           DailyWeather((20.0, 5.0, 25.0), (0, 0, 0)))

    historical.add_weather(date(2012, 11, 18),
                           DailyWeather((24.75, 8.25, 30.25), (0, 0, 0)))

    historical.add_weather(date(2012, 12, 19),
                           DailyWeather((30.0, 12.0, 36.0), (0, 0, 0)))

    assert historical.monthly_average() == {'Jan': -1.75, 'Feb': -3.0,
                                            'Mar': -3.75, 'Apr': -4.0,
                                            'May': -3.75, 'Jun': -3.0,
                                            'Jul': -1.75, 'Aug': 0.0,
                                            'Sep': 2.25, 'Oct': 5.0,
                                            'Nov': 8.25, 'Dec': 12.0
                                            }


def test_monthly_average_none():
    """Test monthly_average on a HistoricalWeather with no data record
    will create a dictionary mapping all month name to None."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    assert historical.monthly_average() == {'Jan': None, 'Feb': None,
                                            'Mar': None, 'Apr': None,
                                            'May': None, 'Jun': None,
                                            'Jul': None, 'Aug': None,
                                            'Sep': None, 'Oct': None,
                                            'Nov': None, 'Dec': None}


def test_monthly_average_more_data():
    """Test monthly_average on a HistoricalWeather that has more than one
    point of data in some months, maybe within different years.
    In addition, adding a record for date already exists will not affect
    the result."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    historical.add_weather(date(2012, 1, 8),
                           DailyWeather((-0.25, -1.75, 0.25), (0, 0, 0)))
    historical.add_weather(date(2012, 1, 8),
                           DailyWeather((0.0, -3.0, 1.0), (0, 0, 0)))
    historical.add_weather(date(2012, 1, 9),
                           DailyWeather((0.75, -3.75, 2.25), (0, 0, 0)))
    historical.add_weather(date(2013, 1, 9),
                           DailyWeather((2.0, -4.75, 4.0), (0, 0, 0)))
    historical.add_weather(date(2013, 1, 10),
                           DailyWeather((3.75, -3.75, 6.25), (0, 0, 0)))
    historical.add_weather(date(2012, 2, 8),
                           DailyWeather((6.0, -3.25, 9.0), (0, 0, 0)))
    historical.add_weather(date(2012, 12, 1),
                           DailyWeather((12.0, 0.0, 16.0), (0, 0, 0)))
    historical.add_weather(date(2012, 2, 11),
                           DailyWeather((8.75, -1.75, 12.25), (0, 0, 0)))
    historical.add_weather(date(2012, 12, 31),
                           DailyWeather((30.0, 12.0, 36.0), (0, 0, 0)))
    assert historical.monthly_average() == {'Jan': -3.5, 'Feb': -2.5,
                                            'Mar': None, 'Apr': None,
                                            'May': None, 'Jun': None,
                                            'Jul': None, 'Aug': None,
                                            'Sep': None, 'Oct': None,
                                            'Nov': None, 'Dec': 6.0}


def test_contiguous_precipitation():
    """Test contiguous_precipitation on a HistoricalWeather that has alternating
    snow and rain."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(date(2012, 6, 4),
                           DailyWeather((0, 0, 0), (3, 3, 0)))

    historical.add_weather(date(2012, 6, 5),
                           DailyWeather((0, 0, 0), (2, 0, 2)))

    historical.add_weather(date(2012, 6, 6),
                           DailyWeather((0, 0, 0), (4, 4, 0)))

    historical.add_weather(date(2012, 6, 8),
                           DailyWeather((0, 0, 0), (5, 5, 0)))

    historical.add_weather(date(2012, 6, 7),
                           DailyWeather((0, 0, 0), (1, 0, 1)))

    assert historical.contiguous_precipitation() == (date(2012, 6, 4), 5)


def test_contiguous_precipitation_tie():
    """Test that contiguous_precipitation on a HistoricalWeather in the case
    of a tie for the longest sequence, and it returns any one of the tied
    start dates."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    historical.add_weather(date(2012, 6, 4),
                           DailyWeather((0, 0, 0), (3, 3, 0)))
    historical.add_weather(date(2012, 6, 5),
                           DailyWeather((0, 0, 0), (0, 0, 2)))
    historical.add_weather(date(2012, 6, 6),
                           DailyWeather((0, 0, 0), (4, 4, 0)))
    historical.add_weather(date(2012, 6, 7),
                           DailyWeather((0, 0, 0), (0, 0, 1)))

    assert historical.contiguous_precipitation() == (date(2012, 6, 4), 1) or \
           historical.contiguous_precipitation() == (date(2012, 6, 6), 1)

    historical.add_weather(date(2012, 6, 8),
                           DailyWeather((0, 0, 0), (5, 5, 0)))

    assert historical.contiguous_precipitation() == (date(2012, 6, 4), 1) or \
           historical.contiguous_precipitation() == (date(2012, 6, 6), 1) or \
           historical.contiguous_precipitation() == (date(2012, 6, 8), 1)


def test_contiguous_precipitation_not_consecutive():
    """Test that contiguous_precipitation on a HistoricalWeather with data
    for a sequence of days which are not consecutive."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    historical.add_weather(date(2012, 6, 4),
                           DailyWeather((0, 0, 0), (3, 3, 0)))
    historical.add_weather(date(2013, 6, 5),
                           DailyWeather((0, 0, 0), (2, 0, 2)))
    historical.add_weather(date(2014, 6, 6),
                           DailyWeather((0, 0, 0), (4, 4, 0)))
    historical.add_weather(date(2012, 6, 9),
                           DailyWeather((0, 0, 0), (1, 0, 1)))
    historical.add_weather(date(2012, 6, 2),
                           DailyWeather((0, 0, 0), (5, 5, 0)))
    result = historical.contiguous_precipitation()

    assert isinstance(result[0], date)
    assert result[1] == 1


def test_contiguous_precipitation_in_the_middle():
    """Test that contiguous_precipitation on a HistoricalWeather with data
    containing a sequence of consecutive days with precipitation in the
    middle.
    In addition, adding a record for date already exists will not affect
    the result."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    historical.add_weather(date(2012, 6, 4),
                           DailyWeather((0, 0, 0), (3, 3, 0)))
    historical.add_weather(date(2012, 6, 5),
                           DailyWeather((0, 0, 0), (2, 0, 2)))
    historical.add_weather(date(2012, 6, 6),
                           DailyWeather((0, 0, 0), (0, 4, 0)))
    historical.add_weather(date(2012, 6, 6),
                           DailyWeather((0, 0, 0), (1, 4, 0)))
    historical.add_weather(date(2012, 6, 7),
                           DailyWeather((0, 0, 0), (-1, 0, 1)))
    historical.add_weather(date(2012, 6, 8),
                           DailyWeather((0, 0, 0), (1, 3, 0)))
    historical.add_weather(date(2012, 6, 9),
                           DailyWeather((0, 0, 0), (3, 3, 0)))
    historical.add_weather(date(2012, 6, 10),
                           DailyWeather((0, 0, 0), (3, 0, 2)))
    historical.add_weather(date(2012, 6, 11),
                           DailyWeather((0, 0, 0), (0, 4, 0)))

    assert historical.contiguous_precipitation() == (date(2012, 6, 7), 4)

    historical.add_weather(date(2012, 6, 12),
                           DailyWeather((0, 0, 0), (1, 0, 1)))

    assert historical.contiguous_precipitation() == (date(2012, 6, 7), 4)


def test_contiguous_precipitation_at_the_end():
    """Test that contiguous_precipitation on a HistoricalWeather with data
    containing a sequence of consecutive days with precipitation at the end.
    In addition, adding a record for date already exists will not affect
    the result."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    historical.add_weather(date(2012, 6, 4),
                           DailyWeather((0, 0, 0), (3, 3, 0)))
    historical.add_weather(date(2012, 6, 5),
                           DailyWeather((0, 0, 0), (2, 0, 2)))
    historical.add_weather(date(2012, 6, 6),
                           DailyWeather((0, 0, 0), (0, 4, 0)))
    historical.add_weather(date(2012, 6, 6),
                           DailyWeather((0, 0, 0), (1, 4, 0)))
    historical.add_weather(date(2012, 6, 7),
                           DailyWeather((0, 0, 0), (-1, 0, 1)))
    historical.add_weather(date(2012, 6, 8),
                           DailyWeather((0, 0, 0), (1, 3, 0)))
    historical.add_weather(date(2012, 6, 9),
                           DailyWeather((0, 0, 0), (0, 3, 0)))
    historical.add_weather(date(2012, 6, 10),
                           DailyWeather((0, 0, 0), (3, 0, 2)))
    historical.add_weather(date(2012, 6, 11),
                           DailyWeather((0, 0, 0), (3, 4, 0)))
    historical.add_weather(date(2012, 6, 12),
                           DailyWeather((0, 0, 0), (1, 0, 1)))

    assert historical.contiguous_precipitation() == (date(2012, 6, 10), 3)


def test_percentage_snowfall():
    """Test percentage_snowfall on a HistoricalWeather that has a single day
    with both snow and rain"""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))

    historical.add_weather(date(2012, 11, 21),
                           DailyWeather((0, 0, 0), (7, 3, 2)))

    assert historical.percentage_snowfall() == 0.4


def test_percentage_snowfall_trace():
    """Test percentage_snowfall on a HistoricalWeather that has several data,
    including data with trace amount of rainfall or snowfall.
    In addition, adding a record for date already exists will not affect
    the result."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    historical.add_weather(date(2012, 11, 21),
                           DailyWeather((0, 0, 0), (7, 3, 2)))
    historical.add_weather(date(2012, 11, 21),
                           DailyWeather((0, 0, 0), (7, 3, 1)))
    historical.add_weather(date(2012, 11, 22),
                           DailyWeather((0, 0, 0), (7, -1, 3)))
    historical.add_weather(date(2012, 11, 23),
                           DailyWeather((0, 0, 0), (7, 6, -1)))
    historical.add_weather(date(2016, 11, 25),
                           DailyWeather((0, 0, 0), (7, 5, 1)))
    assert historical.percentage_snowfall() == 0.3


def test_country_init():
    """Test that we initialize Country correctly."""
    country = Country("Country Name")

    assert country.name == 'Country Name'


def test_add_and_retrieve_history():
    """Test that we can add and retrieve a single weather record from
    a Country."""
    historical = HistoricalWeather("City Name", (-1.234, 4.567))
    country = Country("Country Name")
    country.add_history(historical)

    assert country.retrieve_history("City Name") is historical, \
        "Calling retrieve_history() on a location should return the " + \
        "HistoricalWeather object that was added to that location."


def test_add_repeated_history():
    """Test that if a location is already recorded in this Country, then
    nothing will change."""
    historical1 = HistoricalWeather("City Name", (-1.234, 4.567))
    historical2 = HistoricalWeather("City Name", (-5.678, 1.234))
    country = Country("Country Name")
    country.add_history(historical1)
    country.add_history(historical2)
    location = country.retrieve_history("City Name")

    assert location == historical1


def test_snowiest_location():
    """Test that snowiest_location with two locations returns the one with a
    higher percentage snowfall."""
    country = Country('Country Name')

    # Create one HistoricalWeather record
    historical = HistoricalWeather('City Name', (-1.234, 4.567))

    historical.add_weather(date(2012, 11, 21),
                           DailyWeather((-5, -10, 15), (7, 3, 2)))

    historical.add_weather(date(2012, 10, 21),
                           DailyWeather((-7, -20, 15), (0, 0, 0)))

    historical.add_weather(date(2011, 11, 21),
                           DailyWeather((-8, -15, 15), (0, 0, 0)))

    country.add_history(historical)

    # Create another HistoricalWeather record
    historical2 = HistoricalWeather("Another City", (0.123, -3.4567))

    historical2.add_weather(date(2012, 11, 21),
                            DailyWeather((-5, -10, 15), (9, 5, 4)))

    historical2.add_weather(date(2012, 10, 21),
                            DailyWeather((-7, -20, 15), (20, 15, 5)))

    country.add_history(historical2)

    assert country.snowiest_location() == ('City Name', 0.4)


def test_snowiest_location_none():
    """Test that if there are no locations in this Country,
    snowiest_location returns (None, None)."""
    country = Country('Country Name')
    assert country.snowiest_location() == (None, None)


def test_snowiest_location_tie():
    """Test that snowiest_location with two locations with the same percentage
    snowfall will return one of the locations."""
    country = Country('Country Name')
    # Create one HistoricalWeather record
    historical = HistoricalWeather('City Name', (-1.234, 4.567))
    historical.add_weather(date(2012, 11, 21),
                           DailyWeather((-5, -10, 15), (7, 3, 2)))
    historical.add_weather(date(2012, 10, 21),
                           DailyWeather((-7, -20, 15), (0, 0, -1)))
    historical.add_weather(date(2011, 11, 21),
                           DailyWeather((-8, -15, 15), (0, 0, 0)))
    country.add_history(historical)
    # Create another HistoricalWeather record
    historical2 = HistoricalWeather("Another City", (0.123, -3.4567))
    historical2.add_weather(date(2012, 11, 21),
                            DailyWeather((-5, -10, 15), (9, 3, 0)))
    historical2.add_weather(date(2012, 10, 21),
                            DailyWeather((-7, -20, 15), (20, 0, 2)))
    country.add_history(historical2)

    assert country.snowiest_location() == ('City Name', 0.4) or \
           country.snowiest_location() == ('Another City', 0.4)


def test_load_data():
    """Test load_data on small_sample_data.csv"""
    with open('student_data/small_sample_data.csv') as source:
        historical_weather = load_data(source)

    assert historical_weather is not None, \
        "HistoricalWeather should have been returned when calling load_data " \
        "on small_sample_data.csv but got None."

    assert historical_weather.name == 'THUNDER BAY'
    assert historical_weather.coordinates == (48.3809, 89.2477)
    # Note: You may want to check more properties below!
    #       The current test just reads the HistoricalWeather object from
    #       student_data/small_sample_data.csv
    #       and checks that the name attribute is properly set.


if __name__ == '__main__':
    pytest.main(['a0_starter_tests.py'])
