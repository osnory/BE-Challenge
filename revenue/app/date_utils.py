from datetime import datetime


DATE_FORMAT = "%d/%m/%Y"


def from_string(date: str):
    """

    :param date: in DATE_FORMAT format, such as 03/06/2020
    :return: datetime object.
    """
    return datetime.strptime(date, DATE_FORMAT)


def to_string(date: datetime):
    """
    converts date to string

    :param date: to conver
    :return: into DATE_FORMAT format, such as 03/06/2020
    """
    return date.strftime(DATE_FORMAT)
