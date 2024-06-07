import requests
import pandas as pd
import numpy as np



def get_holidays(start_year=2010, end_year=2030):
    """
    Get US holidays between two years
    Based on the Nager.Date API

    Args:
    start_year (int): the start year
    end_year (int): the end year

    Example:
    get_holidays(2010, 2030)

    Returns:
    pandas.DataFrame: a dataframe of US holidays between the two years
    """

    years = [i for i in range(start_year, end_year)]

    dates = []
    for year in years:
        print(year)
        r = requests.get(f'https://date.nager.at/api/v3/PublicHolidays/{year}/US')

        data = pd.json_normalize(r.json())
        dates.append(data)


    df = pd.concat(dates)
    return df

df = get_holidays()

def get_business_days(start_date, end_date, holidays):
    """
    Get business days between two dates

    Args:
    start_date (str): the start date
    end_date (str): the end date
    holidays (list): list of holidays

    Example:
    get_business_days('2021-01-01', '2021-12-31', df['date'])

    Returns:
    list: list of business days between the two dates
    """

    bdates = pd.bdate_range(start_date, end_date, freq='C', weekmask='Mon Tue Wed Thu Fri', holidays=holidays)
    return bdates


bdates = get_business_days('2021-01-01', '2021-12-31', df['date'])

def business_hours(start_date: str, end_date :str, holidays, hours=8):
    """
    Calculate the number of business hours between two dates
    
    Args:
    start_date (str): the start date
    end_date (str): the end date
    holidays (list): list of holidays
    hours (int): number of hours per day

    Example:
    business_hours('2021-01-01', '2021-12-31', df['date'], 8)

    Returns:
    int: the number of business hours between the two dates
    """
    bdates = get_business_days(start_date, end_date, holidays)
    hours = len(bdates) * hours
    return hours


def get_busday_count_hours(start_date, business_hours=8):
    """
    Get the end date based on the start date and the number of business hours

    Args:
    start_date (str): the start date
    business_hours (int): the number of business hours

    Example:
    get_busday_count_hours('2021-01-01', 8)

    Returns:
    str: the end date
    """

    end_date = pd.Timestamp(start_date) + pd.offsets.BDay(business_hours/8)
    return end_date
