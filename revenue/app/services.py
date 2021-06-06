import datetime

from sqlalchemy import func, sql, types

from revenue.app.models import Receipt
from revenue.app import db, date_utils


def get_daily_breakdown_for(start: datetime, end: datetime, branch_id: str):
    """
    Fetch and compute the daily breakdown for the given range

    :param start: the start date for which we do the breakdown
    :param end: the end date for which we do the breakdown
    :param branch_id: to which we total
    :return: dictionary in the format of
    """
    s = start.replace(hour=0, minute=0, second=0, microsecond=0)
    e = end.replace(day=end.day+1, hour=0, minute=0, second=0)
    values = {"{}/{}/{}".format(d.day, d.month, d.year): 0.0 for d in date_utils.get_day_range(s, e)}

    # sqlite does not support concat func, so use + instead
    q = db.session.query(
        (
                sql.expression.cast(Receipt.day_num, types.Unicode)
                +
                "/"
                +
                sql.expression.cast(Receipt.month_num, types.Unicode)
                +
                "/{}".format(start.year)
        ).label("key"),
        func.sum(Receipt.value),
    )
    q = q.filter(Receipt.branch_id == branch_id)
    q = q.filter(Receipt.full_date.between(s, e))
    q = q.group_by("key")
    res = q.all()

    values.update({k: v for k, v in res})

    return values


def get_hourly_breakdown_for(start: datetime, branch_id: str):
    """
    Fetch and compute the hours breakdown for the given date

    :param start: the start date for which we do the breakdown
    :param branch_id: to which we total
    :return: dictionary in the format of {0: 0.0, ...,  22: 101.40, 23: 0.0}
    """
    s = start.replace(hour=0, minute=0, second=0, microsecond=0)
    e = start.replace(hour=23, minute=59, second=59)
    values = {i: 0.0 for i in range(0, 24)}

    q = db.session.query(
        Receipt.hour_num,
        func.sum(Receipt.value).label('hour_tots')
    )
    q = q.filter(Receipt.branch_id == branch_id)
    q = q.filter(Receipt.full_date.between(s, e))
    q = q.group_by(Receipt.hour_num)
    res = q.all()

    # result set is a list of tuples in the format [(17, 90.86222314867058)]
    # So fill the values map
    values.update(
        {hour_num: value for hour_num, value in res}
    )

    return values
