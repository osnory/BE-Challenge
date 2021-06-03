import random
from datetime import datetime
from functools import wraps

from flask import jsonify, request

from revenue.app import app, date_utils, db
from revenue.app.models import Receipt
from revenue.app import services


def parameters_check(f):
    @wraps(f)
    def endpoint(*args, **kwargs):
        args = request.args
        required_args = "start", "end", "branch_id"
        existing_args = {k: args.get(k) for k in required_args if k in args}
        if len(existing_args) < len(required_args):
            missing_args = set(required_args) - existing_args.keys()
            error_msg = "missing_required args {}".format(",".join(list(missing_args)))
            return jsonify(error=error_msg), 400

        try:
            start = date_utils.from_string(existing_args["start"])
            end = date_utils.from_string(existing_args["end"])
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

    hours_breakdown = services.get_hourly_breakdown_for(start, branch_id)
    body = {
        "branch_id": branch_id,
        "start": start,
        "hours_breakdown": hours_breakdown,
        "total": sum(hours_breakdown.values()),
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
    from datetime import datetime
    now = datetime.now()
    r = Receipt(
        external_id="???-{}".format(now.timestamp()),
        branch_id="???",
        full_date=now,
        epoch_date=now.timestamp(),
        value=random.random() * 100
    )
    db.session.add(r)
    db.session.commit()

    return jsonify(msg=r.as_dict())


