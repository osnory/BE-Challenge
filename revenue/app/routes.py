from datetime import datetime
from functools import wraps

from flask import jsonify, request

from revenue.app import app, date_utils, db, errors, loader, models, validations
from revenue.app import services


def error_handler(f):
    @wraps(f)
    def endpoint(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except errors.HttpError as he:
            return jsonify(error=he.msg), he.error_code
    return endpoint


@app.route("/")
def index():
    return jsonify(hello="Hello")


@app.route("/hourly")
@error_handler
def hourly():
    hourly_params = validations.validate_request_params_hourly(request.args)
    hourly_breakdown = services.get_hourly_breakdown_for(hourly_params)

    body = {
        "branch_id": hourly_params.branch_id,
        "start": hourly_params.start,
        "hourly_breakdown": hourly_breakdown,
        "total": sum(hourly_breakdown.values()),
    }

    return jsonify(data=body)


@app.route("/daily")
@error_handler
def daily():
    daily_params = validations.validate_request_params_daily(request.args)
    daily_breakdown = services.get_daily_breakdown_for(daily_params)
    body = {
        "branch_id": daily_params.branch_id,
        "start": daily_params.start,
        "end": daily_params.end,
        "daily_breakdown": daily_breakdown,
        "total": sum(daily_breakdown.values()),

    }

    return jsonify(data=body)


@app.route("/ingest")
def ingest():
    db.drop_all()
    db.create_all()
    item_stream = loader.get_csv_stream(loader.DATA_FILE)
    receipt_stream = loader.get_receipt_stream(item_stream)
    loader.load_receipts(db, receipt_stream, 1000)

    records = db.session.query(models.Receipt).count()
    return jsonify(records=records)


