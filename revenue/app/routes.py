from datetime import datetime
from functools import wraps

from flask import jsonify, request

from revenue.app import app, db
from revenue.app.models import Receipt


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

        date_format = "%d/%m/%Y"
        try:
            start = datetime.strptime(existing_args["start"], date_format)
            end = datetime.strptime(existing_args["end"], date_format)
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
def hourly(start: datetime, end: datetime, branch_id: str):
    # TODO
    return jsonify(msg="implement me")


@app.route("/daily")
def daily():
    # TODO
    return jsonify(msg="implement me")


@app.route("/ingest")
def ingest():
    from datetime import datetime
    now = datetime.now()
    r = Receipt(
        external_id="???-{}".format(now.timestamp()),
        brand_id="???".format(now),
        full_date=now,
        epoch_date=now.timestamp(),
    )
    db.session.add(r)
    db.session.commit()

    return jsonify(msg=r.as_dict())


@app.route("/add")
def add():
    r = request.args
    return jsonify(msg=r)

