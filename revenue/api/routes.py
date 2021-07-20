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


@app.route("/sales/daily")
@error_handler
def predict():
    """
    Prediction Endpoint
    """

    parameters = request.args

    # Here is where you should call your prediction service
    predictions = services.predict()

    # Define and fill up your paylaod here
    body = {}
    return jsonify(data=body)
