from ..paging.pagingType import PagingType
from .brawlerRankingType import BrawlerRankingListType

class BrawlerRankingCountryType:
    """
    Represents a country's brawler ranking information.
    """

    def __init__(self, data: dict):
        """
        Initialize the BrawlerRankingCountryType object.

        Args:
            data (dict): Dictionary containing country brawler ranking info from the API.
        """

        if data is None:
            data = {}

        self.items: BrawlerRankingListType = BrawlerRankingListType(data.get("items", []))
        """A list of BrawlerRankingType objects representing the brawler rankings in the country."""

        self.paging: PagingType = PagingType(data.get("paging", {}))
        """Paging information for the brawler rankings."""