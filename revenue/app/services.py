import collections
import datetime

from sqlalchemy import func, sql, types

from revenue.app.models import Receipt, DailyParams, HourlyParams
from revenue.app import db
from revenue.app.date_utils import date_to_key, get_day_range


def get_daily_breakdown_for(params: DailyParams):
    """
    Fetch and compute the daily breakdown for the given range

    :param params: DailyParams from models
    :return: dictionary in the format of
    """
    s = params.start.replace(hour=0, minute=0, second=0, microsecond=0)
    e = params.end.replace(day=params.end.day, hour=23, minute=59, second=59)
    values = collections.OrderedDict(
        {date_to_key(d): 0.0 for d in get_day_range(s, e)}
    )

    # sqlite does not support concat func, so use + instead
    q = db.session.query(
        (
                sql.expression.cast(Receipt.day_num, types.Unicode)
                +
                "/"
                +
                sql.expression.cast(Receipt.month_num, types.Unicode)
                +
                "/"
                +
                sql.expression.cast(Receipt.year_num, types.Unicode)
        ).label("key"),
        func.sum(Receipt.value),
    )
    q = q.filter(Receipt.branch_id == params.branch_id)
    q = q.filter(Receipt.full_date.between(s, e))
    q = q.group_by("key")
    res = q.all()

    values.update({k: v for k, v in res})

    return values


def get_hourly_breakdown_for(params: HourlyParams):
    """
    Fetch and compute the hours breakdown for the given date

    :param params: verified params from models
    :return: dictionary in the format of {0: 0.0, ...,  22: 101.40, 23: 0.0}
    """
    s = params.start.replace(hour=0, minute=0, second=0, microsecond=0)
    e = params.start.replace(hour=23, minute=59, second=59)
    values = {i: 0.0 for i in range(0, 24)}

    q = db.session.query(
        Receipt.hour_num,
        func.sum(Receipt.value).label('hour_tots')
    )
    q = q.filter(Receipt.branch_id == params.branch_id)
    q = q.filter(Receipt.full_date.between(s, e))
    q = q.group_by(Receipt.hour_num)
    res = q.all()

    # result set is a list of tuples in the format [(17, 90.86222314867058)]
    # So fill the values map
    values.update(
        {hour_num: value for hour_num, value in res}
    )

    return values
