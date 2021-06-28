class HttpError(Exception):
    """

    Main Error Class for Http Related Errors

    An HTTP error always has an Http status code associated with it


    """
    error_code = 500


class BadRequest(HttpError):
    error_code = 400


class NotFound(HttpError):
    error_code = 404
