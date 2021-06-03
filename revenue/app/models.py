from revenue.app import db


class Receipt(db.Model):

    __tablename__ = 'receipts'

    """
    An Entry has the external receipt id for reference
    and the full date for flexibility to support other use cases if required
    It also has brand_id which is used for querying 
    and the epoch date so a range selection can be used
    """
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(64), unique=True, nullable=False)
    brand_id = db.Column(db.String(64), index=True, nullable=False)
    full_date = db.Column(db.DateTime, nullable=False)
    epoch_date = db.Column(db.BigInteger, index=True, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
