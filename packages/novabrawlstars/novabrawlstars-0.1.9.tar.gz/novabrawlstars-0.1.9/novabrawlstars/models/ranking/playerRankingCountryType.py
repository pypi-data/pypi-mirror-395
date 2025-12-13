from .playerRankingType import PlayerRankingListType
from ..paging.pagingType import PagingType

class PlayerRankingCountryType:
    """
    Represents player rankings specific to a country.
    """

    def __init__(self, data: dict):
        """
        Initialize the PlayerRankingCountryType object.

        Args:
            data (dict): Dictionary containing country player ranking info from the API.
        """

        if data is None:
            data = {}

        self.items: PlayerRankingListType = PlayerRankingListType(data.get("items", []))
        """A list of PlayerRankingType objects representing the player rankings in the country."""

        self.paging: PagingType = PagingType(data.get("paging", {}))
        """Paging information for the player rankings."""