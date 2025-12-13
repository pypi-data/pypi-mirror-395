class PagingType:
    """
    Represents paging information for paginated API responses.
    """
    def __init__(self, data: dict):
        """
        Initialize the PagingType object.

        Args:
            data (dict): Dictionary containing paging info from the API.
        """

        if data is None:
            data = {}

        self.cursors: CursorsType = CursorsType(data.get("cursors", {}))
        """An object representing the cursors for pagination."""

class CursorsType:
    """
    Represents cursor information for pagination.
    """

    def __init__(self, data: dict):
        """
        Initialize the CursorsType object.

        args:
            data (dict): Dictionary containing cursor info from the API.
        """

        if data is None:
            data = {}

        self.after: str = data.get("after", "")
        """The cursor to get the next page of results."""
        
        self.before: str = data.get("before", "")
        """The cursor to get the previous page of results."""