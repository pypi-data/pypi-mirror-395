class KplerException(Exception):
    """All errors related to making an API request extend this."""

    pass


class HttpError(KplerException):
    """Errors produced at the HTTP layer."""

    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def __repr__(self):
        return f"<HttpError, status code={self.status_code}, message={self.body}>"


class AuthenticationError(HttpError):
    """Errors due to invalid authentication credentials."""

    def __init__(self, body):
        self.status_code = 401
        self.body = body

    def __repr__(self):
        return f"<AuthenticationError, message={self.body}>"


class RequestTimeoutError(HttpError):
    """Errors due to request timeout set in configuration"""

    def __init__(self, body):
        self.status_code = 408
        self.body = body

    def __repr__(self):
        return f"<TimeoutError, message={self.body}>"


class AuthenticationClassError(KplerException):
    """Errors due to not authenticated user."""

    def __repr__(self):
        return "<HttpError, you are not authenticated>"


class RestrictedPlatformException(KplerException):
    """Errors due to not available platform chosen."""

    def __init__(self, available_platforms):
        self.available_platforms = available_platforms

    def __str__(self):
        return repr(
            f"<RestrictedPlatformException, the platform which you have specified is not available for this client."
            f" Please choose from the following ones: {self.available_platforms}>"
        )


class MaximumDaysPeriodExceededException(KplerException):
    """Errors due to maximum days period exceeded."""

    def __str__(self):
        return repr(
            "<<MaximumDaysPeriodExceededException, period between start and end dates should be less then 31>"
        )


class WithProductEstimationPlatformException(KplerException):
    """Error due to inappropriate platform was chosen."""

    def __str__(self):
        return repr(
            "<<WithProductEstimationPlatformException, product estimation feature is for CPP trades only>"
        )
