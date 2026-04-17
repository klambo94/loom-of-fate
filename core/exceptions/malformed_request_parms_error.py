from core.exceptions import ErrorCodeEnum


class MalformedRequestParmsException(Exception):
    """
        Exception raised for errors in the input.
        Attributes:
            message -- explanation of the error
    """

    error_code = ErrorCodeEnum.MALFORMED_REQUEST

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} (Error Code: {self.error_code}'