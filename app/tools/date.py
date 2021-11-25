"""Dates related tools."""
from datetime import date, timedelta
from typing import Generator, Optional


def working_days_percent(
    start: Optional[date] = None, end: Optional[date] = None
) -> float:
    """Count percent of worked days for the current month.

    :param start: start of work, start of the month by default
    :param end: end of work, today by default
    :returns: percent of work days
    """
    end = end if end is not None else date.today()
    start = start if start is not None else first_day_of_month(end)
    start = max(start, first_day_of_month(end))
    work_days = workdays(start, end)
    total_work_days = workdays(first_day_of_month(end), last_day_of_month(end))
    return round(100.0 * work_days / total_work_days, 2)


def daterange(start: date, end: date) -> Generator[date, None, None]:
    """Create a generator of dates between 2 dates included.

    :param start: start date
    :param end: end date
    :returns: date generator
    """
    for i in range(int((end - start).days) + 1):
        yield start + timedelta(i)


def workdays(start: date, end: date) -> int:
    """Count work days between 2 dates.

    :param start: start date
    :param end: end date
    :returns: number of work days
    """
    work_days = 0
    for day in daterange(start, end):
        if day.weekday() <= 4:
            work_days += 1
    return work_days


def last_day_of_month(day: date) -> date:
    """Find last day of month for the date.

    :param day: current day
    :returns: last day of current month"""
    year = day.year
    month = day.month
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)


def first_day_of_month(day: date) -> date:
    """Find first day of month for the date.

    :param day: current day
    :returns: first day of current month"""
    year = day.year
    month = day.month
    return date(year, month, 1)
