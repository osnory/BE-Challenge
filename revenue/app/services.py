
from datetime import datetime

from revenue.app.models import Receipt
from revenue.app import date_utils


def get_daily_breakdown_for(start: datetime, end: datetime, branch_id: str):
    """
    Fetch and compute the daily breakdown for the given range

    :param start: the start date for which we do the breakdown
    :param end: the end date for which we do the breakdown
    :param branch_id: to which we total
    :return: dictionary in the format of
    """
    s = start.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    e = end.replace(day=end.day+1, hour=0, minute=0, second=0).timestamp()

    rs = get_receipts_for_range(s, e, branch_id)

    values = {d: 0.0 for d in range(start.day, end.day+1)}

    for date, value in rs:
        values[date.day] += value

    values = {date_utils.to_string(start.replace(day=k)): v for k, v in values.items()}

    return values


def get_hourly_breakdown_for(start: datetime, branch_id: str):
    """
    Fetch and compute the hours breakdown for the given date

    :param start: the start date for which we do the breakdown
    :param branch_id: to which we total
    :return: dictionary in the format of {0: 0.0, ...,  22: 101.40, 23: 0.0}
    """
    s = start.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    e = start.replace(hour=23, minute=59, second=59).timestamp()

    rs = get_receipts_for_range(s, e, branch_id)

    values = {i: 0.0 for i in range(0, 24)}

    for date, value in rs:
        values[date.hour] += value

    return values


def get_receipts_for_range(start: float, end: float, branch_id: str):
    """
    Getting the receipts for the given range from the DB.

    :param start: the start epoch time
    :param end: the end epoch time
    :param branch_id: the branch id
    :return: list of tuples where each tuple is (date : datetime, value: float)
    """

    q = Receipt.query
    q = q.filter(Receipt.branch_id == branch_id)
    q = q.filter(Receipt.epoch_date.between(start, end))
    q = q.with_entities(Receipt.full_date, Receipt.value)

    return q.all()
