class ApiError(Exception):
    """Exception raised for errors in API call.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="API error occurred"):
        super().__init__(message)


class FetchError(Exception):
    """Exception raised for errors during data fetching.

    Attributes:
        message -- explanation of the error
        status_code -- HTTP status code related to the error, if applicable
    """

    def __init__(self, message="Fetch error occurred", status_code=None):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"{self.__class__.__name__}: {self.args[0]} (Status Code: {self.status_code})"
