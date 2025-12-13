from typing import List
from ..player.playerIconType import PlayerIconType

class PlayerRankingClubType:
    """
    Represents a player's club information in brawler rankings.
    """

    def __init__(self, data: dict):
        """
        Initialize the BrawlerPlayerClubType object.

        Args:
            data (dict): Dictionary containing player's club info from the API.
        """

        if data is None:
            data = {}

        self.name: str = data.get("name", "")
        """The name of the club."""

class BrawlerRankingType:
    """
    Represents a single brawler's ranking information.
    """

    def __init__(self, data: dict):
        """
        Initialize the BrawlerRankingType object.

        Args:
            data (dict): Dictionary containing brawler ranking info from the API.
        """

        if data is None:
            data = {}

        self.tag: str = data.get("tag", "")
        """The unique player tag of the member (e.g., '#P8G9')."""
        self.name: str = data.get("name", "")
        """The display name of the member."""
        self.nameColor: str = data.get("nameColor", "")
        """The color code of the member's name."""
        self.icon: PlayerIconType = PlayerIconType(data.get("icon", {}))
        """The player's icon information."""
        self.trophies: int = data.get("trophies", 0)
        """The current number of trophies held by the member."""
        self.rank: int = data.get("rank", 0)
        """The current rank of the brawler in the ranking list."""
        self.club: PlayerRankingClubType = PlayerRankingClubType(data.get("club", {}))
        """The player's club information."""

class BrawlerRankingListType:
    """
    Represents a list of brawler rankings.
    """

    def __init__(self, data: List[dict]):
        """
        Initialize the BrawlerRankingListType object.

        Args:
            data (List[dict]): List of dictionaries containing raw brawler ranking info from the API.
        """

        if data is None:
            data = []

        self.brawlerRankingList: List[BrawlerRankingType] = [BrawlerRankingType(b) for b in data if b]
        """A list of BrawlerRankingType objects representing the brawler rankings."""