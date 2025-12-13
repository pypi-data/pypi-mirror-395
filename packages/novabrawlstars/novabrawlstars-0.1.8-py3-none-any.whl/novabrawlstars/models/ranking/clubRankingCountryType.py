from .clubRankingType import ClubRankingListType
from ..paging.pagingType import PagingType

class ClubRankingCountryType:
    """
    Represents a country's club ranking information.
    """

    def __init__(self, data: dict):
        """
        Initialize the ClubRankingCountryType object.

        Args:
            data (dict): Dictionary containing country club ranking info from the API.
        """

        if data is None:
            data = {}
        
        self.items: ClubRankingListType = ClubRankingListType(data.get("items", []))
        """A list of ClubRankingType objects representing the club rankings in the country."""
        
        self.paging: PagingType = PagingType(data.get("paging", {}))
        """Paging information for the club rankings."""