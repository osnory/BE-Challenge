from revenue.app import errors, date_utils, models

BRANCH_NAMES_TO_IDS = {
    "Nory Sushi": "352h67i328fh",
    "Nory Pizza": "345hngydkgs",
    "Nory Taco": "2hg8j32gw8g"
}

BRANCH_IDS = set(BRANCH_NAMES_TO_IDS.values())


def get_brand_id(brand_name: str):
    """
    Idealy this would come from the DB

    :param brand_name: as appears on the csv data dump
    :return: brand id as it would appear in the DB
    """
    return BRANCH_NAMES_TO_IDS.get(brand_name)


def validate_request_params_hourly(params: dict):
    start_str, branch_id = validate_params_exist(params, ("start", "branch_id"))
    start = validate_date(start_str)
    branch_id = validate_branch_id(branch_id)
    return models.HourlyParams(start=start, branch_id=branch_id)


def validate_request_params_daily(params: dict):
    start_str, end_str, branch_id = validate_params_exist(params, ("start", "end", "branch_id"))
    start, end = validate_start_and_end_dates(start_str, end_str)
    branch_id = validate_branch_id(branch_id)
    return models.DailyParams(start=start, end=end, branch_id=branch_id)


def validate_params_exist(params, required_args):
    existing_args = [params.get(k) for k in required_args if k in params]
    if len(existing_args) < len(required_args):
        missing_args = set(required_args) - set(existing_args)
        error_msg = "missing_required args {}".format(",".join(list(missing_args)))
        raise errors.BadRequest(error_msg)
    return existing_args


def validate_date(date_str: str):
    try:
        return date_utils.from_api_string(date_str)
    except ValueError as ve:
        raise errors.BadRequest("bad date format: {}".format(ve))


def validate_branch_id(branch_id: str):
    if branch_id not in BRANCH_IDS:
        raise errors.NotFound("branch id {} unknown. Use any of {}".format(branch_id, BRANCH_IDS))
    return branch_id


def validate_start_and_end_dates(start_str, end_str):
    start = validate_date(start_str)
    end = validate_date(end_str)
    if start > end:
        msg = "start date {} cannot be after end date {}"
        raise errors.BadRequest(msg.format(start, end))
    return start, end
