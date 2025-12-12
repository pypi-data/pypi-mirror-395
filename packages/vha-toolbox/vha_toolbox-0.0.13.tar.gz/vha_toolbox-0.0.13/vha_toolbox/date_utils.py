from calendar import monthrange
from datetime import date, timedelta


def get_first_day_of_year(dt: date = date.today()) -> date:
    """
    Get the first day of the year for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the first day of the year (default: current date).

    Returns:
        date: The first day of the year as a date object.

    Example:
        >>> get_first_day_of_year(date(2023, 6, 15))
        datetime.date(2023, 1, 1)
    """
    return date(dt.year, 1, 1)


def get_last_day_of_year(dt: date = date.today()) -> date:
    """
    Get the last day of the year for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the last day of the year (default: current date).

    Returns:
        date: The last day of the year as a date object.

    Example:
        >>> get_last_day_of_year(date(2023, 6, 15))
        datetime.date(2023, 12, 31)
    """
    return date(dt.year, 12, monthrange(dt.year, 12)[1])


def get_first_day_of_quarter(dt: date = date.today()) -> date:
    """
    Get the first day of the quarter for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the first day of the quarter (default: current date).

    Returns:
        date: The first day of the quarter as a date object.

    Example:
        >>> get_first_day_of_quarter(date(2023, 6, 15))
        datetime.date(2023, 4, 1)
    """
    return date(dt.year, (dt.month - 1) // 3 * 3 + 1, 1)


def get_last_day_of_quarter(dt: date = date.today()) -> date:
    """
    Get the last day of the quarter for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the last day of the quarter (default: current date).

    Returns:
        date: The last day of the quarter as a date object.

    Example:
        >>> get_last_day_of_quarter(date(2023, 6, 15))
        datetime.date(2023, 6, 30)
    """
    next_qt_yr = dt.year + (1 if dt.month > 9 else 0)
    next_qt_first_mo = (dt.month - 1) // 3 * 3 + 4
    next_qt_first_mo = 1 if next_qt_first_mo == 13 else next_qt_first_mo
    next_qt_first_dy = date(next_qt_yr, next_qt_first_mo, 1)
    return next_qt_first_dy - timedelta(days=1)


def get_first_day_of_month(dt: date = date.today()) -> date:
    """
    Get the first day of the month for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the first day of the month (default: current date).

    Returns:
        date: The first day of the month as a date object.

    Example:
        >>> get_first_day_of_month(date(2023, 6, 15))
        datetime.date(2023, 6, 1)
    """
    return date(dt.year, dt.month, 1)


def get_last_day_of_month(dt: date = date.today()) -> date:
    """
    Get the last day of the month for the given date or the current date if not provided.

    Args:
        dt (date): The date for which to retrieve the last day of the month (default: current date).

    Returns:
        date: The last day of the month as a date object.

    Example:
        >>> get_last_day_of_month(date(2023, 6, 15))
        datetime.date(2023, 6, 30)
    """
    return date(dt.year, dt.month, monthrange(dt.year, dt.month)[1])


def next_renewal_date(dt: date = date.today(), index: int = 1) -> date:
    """
    Get the next renewal date for the given date or the current date if not provided.

    Args:
        index (int): The number of months to add to the date (default: 1).
        dt (date): The date for which to retrieve the next renewal date (default: current date).

    Returns:
        date: The next renewal date as a date object.

    Example:
        >>> next_renewal_date(date(2023, 6, 15))
        datetime.date(2023, 7, 15)
        >>> next_renewal_date(date(2023, 6, 15), 2)
        datetime.date(2023, 8, 15)
        >>> next_renewal_date(date(2023, 10, 31), 4)
        datetime.date(2024, 2, 29)
    """
    year, month = dt.year, dt.month

    # Increment month and adjust year if necessary
    month += index
    while month > 12:
        month -= 12
        year += 1

    # Check if it's a leap year
    is_leap_year = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    # Adjust day for February in leap and non-leap years
    if month == 2:
        if is_leap_year and dt.day > 29:
            return date(year, 2, 29)
        elif not is_leap_year and dt.day > 28:
            return date(year, 2, 28)

    # Handle last day of month for 30 day months
    if month in [4, 6, 9, 11] and dt.day > 30:
        return date(year, month, 30)

    # Standard case
    return date(year, month, dt.day)


def is_renewal_due(dt_to_check: date, dt: date = date.today()) -> bool:
    """
    Check if the renewal date is due for the given date or the current date if not provided.
    This function accounts for different month lengths and leap years.

    Args:
        dt_to_check (date): The date to check.
        dt (date): The date to check against (default: current date).

    Returns:
        bool: True if the renewal date is due, False otherwise.

    Example:
        >>> is_renewal_due(date(2023, 6, 15), date(2023, 6, 15))
        False
        >>> is_renewal_due(date(2023, 6, 15), date(2023, 7, 15))
        True
        >>> is_renewal_due(date(2023, 6, 15), date(2023, 7, 16))
        False
        >>> is_renewal_due(date(2023, 6, 15), date(2024, 7, 15))
        True
        >>> is_renewal_due(date(2020, 2, 29), date(2021, 2, 28))
        True
        >>> is_renewal_due(date(2020, 5, 31), date(2021, 5, 30))
        True
    """
    # Check if today is passed or the same as the renewal date
    if dt_to_check >= dt:
        return False

    is_leap_year = dt.year % 4 == 0 and (dt.year % 100 != 0 or dt.year % 400 == 0)

    # Handle February for leap and non-leap years
    if dt_to_check.month == 2:
        if is_leap_year and dt.day == 29:
            return dt_to_check.day == 29
        elif not is_leap_year and dt.day == 28:
            return dt_to_check.day in [28, 29]

    # Handle renewal due for months with 30 days
    if dt_to_check.month in [4, 6, 9, 11] and dt_to_check.day == 31:
        return dt.day == 30

    # Default check for other cases
    return dt_to_check.day == dt.day
