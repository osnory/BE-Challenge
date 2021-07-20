import collections

from sqlalchemy import func, sql, types

from revenue.api.models import BrandMapping, DailyParams, HourlyParams, Receipt
from revenue.api import db
from revenue.utils.date_utils import date_to_key, get_day_range


def predict():
    pass


def get_all_brand_ids():
    """

    :return: All supported brand ids
    """
    res = BrandMapping.query.all()
    return set([r.id for r in res])


def get_brand_id(brand_name: str):
    """

    :param brand_name: as appears on the csv data dump
    :return: brand id as it would appear in the DB
    """
    q = db.session.query(BrandMapping.id)
    q = q.filter(BrandMapping.name == brand_name)
    res = q.all()
    return res[0] if res else None


def brand_id_exists(brand_id: str):
    """

    :param brand_id: on DB
    :return: True if brand if exists on DB, false otherwise
    """
    q = db.session.query(BrandMapping)
    q = q.filter(BrandMapping.id == brand_id)
    res = q.all()
    return bool(res)

