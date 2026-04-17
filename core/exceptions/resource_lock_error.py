from core.exceptions import ErrorCodeEnum


class ResourceLockException(Exception):
    """
        Exception raised for when there are locking errors
        Attributes:
            message -- explanation of the error
    """

    error_code = ErrorCodeEnum.RESOURCE_LOCKED_ERROR

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} (Error Code: {self.error_code}'