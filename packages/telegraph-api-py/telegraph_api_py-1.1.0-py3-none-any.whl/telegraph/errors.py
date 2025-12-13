"""
Telegraph API Error Classes
"""


class TelegraphError(Exception):
    """
    Base exception class for Telegraph API errors.

    Attributes:
        message: Error message describing what went wrong
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"TelegraphError: {self.message}"


class TelegraphAPIError(TelegraphError):
    """
    Exception raised when the Telegraph API returns an error response.

    Attributes:
        message: Error message from the API
        error_code: Optional error code if provided by the API
    """

    def __init__(self, message: str, error_code: str = None) -> None:
        self.error_code = error_code
        super().__init__(message)

    def __str__(self) -> str:
        if self.error_code:
            return f"TelegraphAPIError [{self.error_code}]: {self.message}"
        return f"TelegraphAPIError: {self.message}"


class TelegraphHTTPError(TelegraphError):
    """
    Exception raised when an HTTP error occurs during API request.

    Attributes:
        message: Error message
        status_code: HTTP status code
        response_text: Response body text
    """

    def __init__(self, message: str, status_code: int = None, response_text: str = None) -> None:
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message)

    def __str__(self) -> str:
        if self.status_code:
            return f"TelegraphHTTPError [{self.status_code}]: {self.message}"
        return f"TelegraphHTTPError: {self.message}"


class TelegraphConnectionError(TelegraphError):
    """
    Exception raised when a connection error occurs.

    Attributes:
        message: Error message
    """

    def __str__(self) -> str:
        return f"TelegraphConnectionError: {self.message}"


class TelegraphValidationError(TelegraphError):
    """
    Exception raised when input validation fails.

    Attributes:
        message: Error message describing the validation failure
        field: Optional field name that failed validation
    """

    def __init__(self, message: str, field: str = None) -> None:
        self.field = field
        super().__init__(message)

    def __str__(self) -> str:
        if self.field:
            return f"TelegraphValidationError [{self.field}]: {self.message}"
        return f"TelegraphValidationError: {self.message}"
