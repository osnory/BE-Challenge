from collections import namedtuple
from datetime import datetime

from revenue.app import db


class Receipt(db.Model):
    """
        An Entry has the external receipt id for reference
        and the full date for querying and flexibility to support other use cases if required
        It also has brand_id which is used for querying
        It has 3 fields that we use for grouping, namely month, day, hour
    """

    __tablename__ = 'receipts'

    @classmethod
    def create(cls, external_id: str, branch_id: str, full_date: datetime, value: float):
        return cls(
            external_id="{}-{}".format(branch_id, external_id),
            branch_id=branch_id,
            full_date=full_date,
            value=value,
            year_num=full_date.year,
            month_num=full_date.month,
            day_num=full_date.day,
            hour_num=full_date.hour,
        )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    external_id = db.Column(db.String(64), unique=True, nullable=False)
    branch_id = db.Column(db.String(64), index=True, nullable=False)
    full_date = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)

    # These are derived values and used to aggregate on the DB level
    year_num = db.Column(db.Integer, index=True)
    month_num = db.Column(db.Integer, index=True)
    day_num = db.Column(db.Integer, index=True)
    hour_num = db.Column(db.Integer, index=True)

    def _fields(self):
        return [(c.name, getattr(self, c.name)) for c in self.__table__.columns]

    def __repr__(self):
        fields = ["{}={}".format(k, v) for k, v in self._fields()]
        return "<Receipt : {}>".format(",".join(fields))

    def as_dict(self):
        return dict(self._fields())


class BrandMapping(db.Model):
    """
    Holds all brand names to ids mappings
    """

    @classmethod
    def from_id_to_name(cls, _id, _name):
        return cls(id=_id, name=_name)

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)




"""
Models to hold validated request parameters.
"""
HourlyParams = namedtuple("HourlyParams", "start, branch_id")
DailyParams = namedtuple("DailyParams", "start, end, branch_id")
