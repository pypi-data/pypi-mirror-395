class ApiError(Exception):
    """
    Generic error returned by the Brawl Stars API.

    Args:
        message (str): A description of the error.
        code (int | None, optional): The HTTP status code returned by the API. Defaults to None.
    """
    def __init__(self, message: str, code: int | None=None):
        super().__init__(f"API Error [{code}] {message}" if code else message)
        self.code = code

class InvalidTokenError(Exception):
    """
    Raised when the provided API token is invalid or missing.

    Args:
        message (str): A description of the authentication error.
        code (int | None, optional): The HTTP status code (usually 403). Defaults to None.
    """
    def __init__(self, message: str, code: int | None=None):
        super().__init__(f"Invalid Token [{code}] {message}" if code else message)
        self.code = code

class NotFoundError(Exception):
    """
    Raised when a requested resource (player, brawler, club, etc.) is not found.

    Args:
        message (str): A description indicating which resource was not found.
        code (int | None, optional): The HTTP status code (usually 404). Defaults to None.
    """
    def __init__(self, message: str, code: int | None=None):
        super().__init__(f"Not Found [{code}] {message}" if code else message)
        self.code = code
    
class RateLimitError(Exception):
    """
    Raised when the API rate limit has been exceeded.

    Args:
        message (str): A description of the rate limit error.
        code (int | None, optional): The HTTP status code (usually 429). Defaults to None.
    """
    def __init__(self, message: str, code: int | None=None):
        super().__init__(f"Rate Limit [{code}] {message}" if code else message)
        self.code = code

class UnexpectedError(Exception):
    """
    Raised when an unexpected error occurs during the API request.

    Args:
        message (str): A description of the unexpected error.
        code (int | None, optional): The HTTP status code associated with the error. Defaults to None.
    """
    def __init__(self, message: str, code: int | None=None):
        super().__init__(f"Unexpected Error [{code}] {message}" if code else message)
        self.code = code

class ServiceErrorMaintenance(Exception):
    """
    Raised when the service is under maintenance.

    Args:
        message (str): A description of the maintenance status.
        code (int | None, optional): The HTTP status code (usually 503). Defaults to None.
    """
    def __init__(self, message: str, code: int | None=None):
        super().__init__(f"Service Maintenance [{code}] {message}" if code else message)
        self.code = code