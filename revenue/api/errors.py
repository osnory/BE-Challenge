class HttpError(Exception):
    """

    Main Error Class for Http Related Errors

    An HTTP error always has an Http status code associated with it


    """

    def __init__(self, msg, error_code):
        super().__init__(msg)
        self.msg = msg
        self.error_code = error_code


class BadRequest(HttpError):
    def __init__(self, msg):
        super().__init__(msg, 400)


class NotFound(HttpError):
    def __init__(self, msg):
        super().__init__(msg, 404)
