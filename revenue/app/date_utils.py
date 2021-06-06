import datetime
from datetime import datetime as dt


DATE_FORMAT = "%d/%m/%Y"


def from_string(date: str):
    """

    :param date: in DATE_FORMAT format, such as 03/06/2020
    :return: datetime object.
    """
    return dt.strptime(date, DATE_FORMAT)


def to_string(date: dt):
    """
    converts date to string

    :param date: to conver
    :return: into DATE_FORMAT format, such as 03/06/2020
    """
    return date.strftime(DATE_FORMAT)


def get_day_range(start: dt, end: dt):
    """
    Helper function to return all dates in between two dates
    :param start: day to start from (incl)
    :param end: day to end on (incl)
    :return: inclusive dates for the range between start and end
    """
    return [start + datetime.timedelta(days=i) for i in range((end - start).days + 1)]
