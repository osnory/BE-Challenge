from datetime import datetime
from functools import wraps

from flask import jsonify, request

from revenue.app import app, date_utils, db, loader, models
from revenue.app import services


def parameters_check(f):
    @wraps(f)
    def endpoint():
        args = request.args
        required_args = "start", "end", "branch_id"
        existing_args = {k: args.get(k) for k in required_args if k in args}
        if len(existing_args) < len(required_args):
            missing_args = set(required_args) - existing_args.keys()
            error_msg = "missing_required args {}".format(",".join(list(missing_args)))
            return jsonify(error=error_msg), 400

        try:
            start = date_utils.from_api_string(existing_args["start"])
            end = date_utils.from_api_string(existing_args["end"])
            if start > end:
                raise ValueError("start date must be lower than end date")
            branch_id = existing_args["branch_id"]
            if not branch_id:
                raise ValueError("branch id cannot be empty")
        except ValueError as e:
            return jsonify(error=str(e)), 400
        else:
            return f(start=start, end=end, branch_id=branch_id)
    return endpoint


@app.route("/")
def index():
    return jsonify(hello="Hello")


@app.route("/hourly")
@parameters_check
def hourly(start: datetime, branch_id: str, **kwargs):

    hourly_breakdown = services.get_hourly_breakdown_for(start, branch_id)
    body = {
        "branch_id": branch_id,
        "start": start,
        "hourly_breakdown": hourly_breakdown,
        "total": sum(hourly_breakdown.values()),
    }

    return jsonify(data=body)


@app.route("/daily")
@parameters_check
def daily(start: datetime, end: datetime, branch_id: str):
    daily_breakdown = services.get_daily_breakdown_for(start, end, branch_id)
    body = {
        "branch_id": branch_id,
        "start": start,
        "end": end,
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


