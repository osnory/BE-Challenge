import logging

from functools import wraps

from flask import jsonify, request

from revenue.api import app, errors, services, validations

logger = logging.getLogger(__name__)


def error_handler(f):
    """
    Wraps function f with HTTP error handling codes and messages
    :param f: end point function
    :return: f` with error handling functionality added to f
    """
    @wraps(f)
    def endpoint(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except errors.HttpError as he:
            return jsonify(error=str(he)), he.error_code
        except Exception as e:
            logger.error(str(e))
            msg = "Unexpected error occurred. See logs for detail"
            return jsonify(error=msg), 500

    return endpoint


@app.route("/")
def index():
    return jsonify(
        hello="Hello!"
              "Please Use the Daily and Hourly end points to see some data"
    )


@app.route("/hourly")
@error_handler
def hourly():
    """

    :return: hourly breakdown for the given date and branch id
    """
    hourly_params = validations.validate_request_params_hourly(request.args)
    branch_id_exists_or_404(hourly_params.branch_id)
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
    """

    :return: daily breakdown for the given date range (incl, incl).
    """
    daily_params = validations.validate_request_params_daily(request.args)
    branch_id_exists_or_404(daily_params.branch_id)
    daily_breakdown = services.get_daily_breakdown_for(daily_params)
    body = {
        "branch_id": daily_params.branch_id,
        "start": daily_params.start,
        "end": daily_params.end,
        "daily_breakdown": daily_breakdown,
        "total": sum(daily_breakdown.values()),

    }

    return jsonify(data=body)


def branch_id_exists_or_404(branch_id: str):
    if services.brand_id_exists(branch_id):
        return branch_id

    # Oh No
    raise errors.NotFound(
        "branch id '{}' is unknown. Use any of {}".format(
            branch_id,
            services.get_all_brand_ids(),
        )
    )
